#!/bin/bash

username="etrues"
host_server="klone.hyak.uw.edu"
target_dir="/gscratch/cmt/etrues/superfast_ion/MD-LAMMPS-35/"
zip_file="data.tar.gz"

cp ../../DeePMD-Model/model/graph.pb graph.pb
tar -zcvf data.tar.gz structure*.lmp graph.pb submit-highT.slurm submit-lowT.slurm jobs_submit.sh
if [ ${?} -eq 0 ]
then
	true
else
	exit $?
fi
rm graph.pb

scp data.tar.gz "$username"@"$host_server":"$target_dir"
ssh etrues@klone.hyak.uw.edu "cd $target_dir; tar -zxvf $zip_file; bash jobs_submit.sh;"
rm data.tar.gz