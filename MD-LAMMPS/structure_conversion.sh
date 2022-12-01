#!/bin/bash

for c in "00" "05" "10" "15" "20" "25" "30" "35" "40" "45" "50" "55" "60" "65" "70" "75" "80"; do
	for i in 0 1 2; do
		atomsk.exe POSCAR-Al$c-$i lammps LAMMPS-structures/Al$c/structure-$i.lmp
		if [ ${?} -eq 0 ]
		then
			true
		else
			exit $?
		fi
	done
done
