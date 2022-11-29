#!/bin/bash

for T in 1500 1200 900; do
	atomsk.exe POSCAR-$T-1 lammps structure-$T-1.lmp
	if [ ${?} -eq 0 ]
	then
		true
	else
		exit $?
	fi
done