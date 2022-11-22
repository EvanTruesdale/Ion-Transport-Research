#!/bin/bash

for T in 1500 1200 900; do
	atomsk.exe POSCAR-$T lammps structure-$T.lmp
	if [ ${?} -eq 0 ]
	then
		true
	else
		exit $?
	fi
done