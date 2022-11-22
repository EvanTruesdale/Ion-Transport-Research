#!/bin/bash

#SBATCH --job-name=sic
#SBATCH --account=cmt
#SBATCH --partition=compute

#SBATCH --nodes=8
#SBATCH --ntasks-per-node=40
#SBATCH --time=24:00:00
#SBATCH --mem=150G

#SBATCH --mail-type=ALL
#SBATCH --mail-user=evan@truecrew.net

#SBATCH --chdir=.
#SBATCH --export=all

module load intel/oneAPI/2021.1.1

## Usual calculations
for file in POSCAR-*
do
	if test -f "vasprun"${file:7}".xml"; then
		echo "${file:7} already exists"
	else
		echo "${file:7} being generated"
		cp $file POSCAR
		mpirun -np 320 /gscratch/cmt/software/vasp_5.4.4/bin/vasp_gam > output_file
		mv output_file "output_file${file:7}"
		mv vasprun.xml "./vasprun"${file:7}".xml"	
	fi
done 
