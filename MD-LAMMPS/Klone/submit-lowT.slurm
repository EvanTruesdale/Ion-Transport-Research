#!/bin/bash

#SBATCH --job-name=lammps
#SBATCH --account=cmt
#SBATCH --partition=compute

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --time=4-00:00:00
#SBATCH --mem=150G

#SBATCH --mail-type=ALL
#SBATCH --mail-user=evan@truecrew.net

#SBATCH --chdir=.
#SBATCH --export=all

source /gscratch/stf/etrues/miniconda3/etc/profile.d/conda.sh
conda activate deepmd-gpu

## Usual calculations

for i in {0..10}
do
	cat << EOF > calc-$T.in
clear
units metal
dimension 3
boundary p p p
atom_style atomic
neighbor 2.0 bin
neigh_modify every 10 delay 0 check no
read_data structure-$T.lmp
pair_style deepmd graph.pb
pair_coeff * *
reset_timestep 0
timestep 0.004
velocity all create $T $RANDOM
fix th all nvt temp $T $T 0.5
thermo 500
compute msd all msd com yes
compute mscd all msd com yes average yes
fix msdwrite all ave/time 1 9 10 c_msd file msd$i-$T.out mode vector
fix mscdwrite all ave/time 1 9 10 c_mscd file mscd$i-$T.out mode vector
run $t
print "All done"
EOF

mpirun -np 40 lmp -in calc-$T.in
done
