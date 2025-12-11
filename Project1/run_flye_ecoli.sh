#!/bin/bash
#SBATCH --job-name=flye_ecoli
#SBATCH --output=logs/flye_ecoli_%j.out
#SBATCH --error=logs/flye_ecoli_%j.err
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=04:00:00

# Input and output paths
FASTQ="/farmshare/home/classes/bios/270/data/project1/SRR33251869.fastq"
OUTDIR="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_flye_out"

# Load Apptainer
module load apptainer

# Run Flye
apptainer exec \
  -B /farmshare/home/classes/bios/270 \
  -B $SCRATCH \
  /farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif \
  flye --nano-raw $FASTQ \
       --out-dir $OUTDIR \
       --threads 32

echo "Flye assembly completed!"
echo "Assembly output: $OUTDIR/assembly.fasta"


