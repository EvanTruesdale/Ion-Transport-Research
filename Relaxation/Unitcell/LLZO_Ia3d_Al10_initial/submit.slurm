#!/bin/bash

#SBATCH --job-name=relax
#SBATCH --account=cmt
#SBATCH --partition=compute

#SBATCH --nodes=4
#SBATCH --ntasks-per-node=40
#SBATCH --time=24:00:00
#SBATCH --mem=150G

#SBATCH --mail-type=ALL
#SBATCH --mail-user=evan@truecrew.net

#SBATCH --chdir=.
#SBATCH --export=all

module load intel/oneAPI/2021.1.1

## Usual calculations
for file in LLZO_Ia3d_Al10_partial/*
do
	if test -f "LLZO_Ia3d_Al10_partial_relaxed/"${file:23}; then
		echo "${file:23} already exists"
	else
		echo "${file:23} being generated"
		cp $file POSCAR
		mpirun -np 160 /gscratch/cmt/software/vasp_5.4.4/bin/vasp_gam > output_file
		mv CONTCAR "LLZO_Ia3d_Al10_partial_relaxed/"${file:23}
		mv output_file "LLZO_Ia3d_Al10_partial_relaxed/"${file:23}"_output"
		echo "${file:23} has been generated"
	fi
done	
