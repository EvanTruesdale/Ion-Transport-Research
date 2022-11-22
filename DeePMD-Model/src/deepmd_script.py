import json
import os
import time
import argparse
import subprocess
from subprocess import DEVNULL
from azureml.core import Run
import numpy as np

print('Starting script')

# Set up defaults for hyperparameters
parser = argparse.ArgumentParser()
parser.add_argument("--data_directory", type=str)
args = parser.parse_args()
data_directory = args.data_directory

# Writes the input.json for DeePMD with the given hyperparameters
data = {
    "model": {
        "type_map": ["Al", "La", "Li", "O", "Zr"],
        "descriptor": {
            "type":           "se_e2_a",
            "sel":            [2, 20, 50, 70, 20],
            "rcut":           7.00,
            "rcut_smth":      0.50,
            "neuron":         [25, 50, 100],
            "resnet_dt":      False,
            "axis_neuron":    16,
            "seed":           1
        },
        "fitting_net": {
            "neuron":         [240, 240, 240],
            "resnet_dt":      True,
            "seed":           1
        },
    },

    "learning_rate": {
        "type":           "exp",
        "start_lr":       0.001,
        "stop_lr":        3.51e-8,
        "decay_steps":    5000
    },

    "loss": {
        "type":           "ener",
        "start_pref_e":   0.02,
        "limit_pref_e":   1,
        "start_pref_f":   1000,
        "limit_pref_f":   1,
        "start_pref_v":   0.3,
        "limit_pref_v":   0.3
    },

    "training": {
        "training_data": {
            "systems":    [os.path.join(data_directory, "npy_LLZO_Ia3d_Al20_training")],
            "batch_size": "auto"
        },
        "validation_data": {
            "systems":    [os.path.join(data_directory, "npy_LLZO_Ia3d_Al20_validation")],
            "batch_size": "auto"
        },
        "numb_steps":     1000000,
        "seed":           1,
        "disp_file":      "lcurve.out",
        "disp_freq":      100,
        "save_freq":      1000
    }
}

# Saves input.json
with open('input.json', 'w') as f:
    json.dump(data, f)
    print('input.json written successfully')

# Runs DeePMD as a subprocess
# Not normally required, but necessary for DeePMD since we don't have direct
# access to the output files using Docker
# This allows the model to train while the rest of the script keeps running
try:
    process = subprocess.Popen('dp train input.json', shell=True, stdout=DEVNULL)
    print("deepmd running")
except:
    print("error with running process")

run = Run.get_context()
run_id = run.id

# outputs/ and logs/ need to be made manually
# these directories will appear in the Outputs/Logs tab in Azure ML Studio
os.makedirs('outputs', exist_ok=True)
os.system('cp input.json outputs/input.json')
os.makedirs('logs', exist_ok=True)

# This loop tracks whether lcurve.out has been updated or not
# On an update, the various errors are logged to Azure AND the lcurve file
# is copied to logs/ so that it can be viewed in real time
# The loop exits when the DeePMD subprocess finishes
last_step = 0
while process.poll() == None:
    time.sleep(1)
    try:
        data = np.genfromtxt("lcurve.out", names=True)
        if last_step < data['step'][-1]:
            last_step = data['step'][-1]
            os.system('cp lcurve.out logs/lcurve.out')
            for name in data.dtype.names[1:-1]:
                run.log(name, data[name][-1])
    except (IndexError, OSError) as e:
        continue

# Freeze model into graph.pb
try:
    os.system('dp freeze -o graph.pb')
    print("froze model")
except:
    print("error freezing model")

# Move model and final lcurve to the outputs and logs folders for later access
try:
    os.system('mv graph.pb outputs/graph.pb')
    os.system('mv lcurve.out logs/lcurve.out')
    print("model moved")
except:
    print("error moving model")
