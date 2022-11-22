#!/bin/bash

#SBATCH --job-name=vasp
#SBATCH --account=cmt
#SBATCH --partition=compute

#SBATCH --nodes=4
#SBATCH --ntasks-per-node=40
#SBATCH --time=2-00:00:00
#SBATCH --mem=150G

#SBATCH --mail-type=ALL
#SBATCH --mail-user=evan@truecrew.net

#SBATCH --chdir=.
#SBATCH --export=all

module load intel/oneAPI/2021.1.1

## Usual calculations
mpirun -np 160 /gscratch/cmt/software/vasp_5.4.4/bin/vasp_gam > output_file 
