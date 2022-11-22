#!/bin/bash

username="etrues"
host_server="klone.hyak.uw.edu"
target_dir="/gscratch/cmt/etrues/superfast_ion/MD-VASP/"
zip_file="data.tar.gz"

tar -zcvf data.tar.gz submit.slurm POSCAR KPOINTS INCAR POTCAR
if [ ${?} -eq 0 ]
then
	true
else
	exit $?
fi

scp data.tar.gz "$username"@"$host_server":"$target_dir"
ssh etrues@klone.hyak.uw.edu "cd $target_dir; tar -zxvf $zip_file; sbatch submit.slurm;"
