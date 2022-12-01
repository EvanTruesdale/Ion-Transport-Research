#!/bin/bash
## [300]=500000 [600]=250000 [900]=100000 [1200]=50000 [1500]=25000

declare -A pairs=( [900]=100000 [1200]=50000 [1500]=25000 )
for T in "${!pairs[@]}"; do
	t=${pairs[$T]}
	sbatch --export=T=$T,t=$t submit-highT.slurm
done

declare -A pairs=( [300]=500000 [600]=250000 )
for T in "${!pairs[@]}"; do
	t=${pairs[$T]}
	sbatch --export=T=$T,t=$t submit-lowT.slurm
done
