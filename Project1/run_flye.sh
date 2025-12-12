#!/bin/bash
#SBATCH --job-name=flye_assembly
#SBATCH --partition=normal
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=3:00:00
#SBATCH --output=flye_%j.log
#SBATCH --error=flye_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lchan8@stanford.edu

module load apptainer

CONTAINER=/farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif
DATA_DIR=/farmshare/home/classes/bios/270/data/project1
WORK_DIR=$(pwd)

# Assemble E. coli
singularity exec -B $WORK_DIR -B $DATA_DIR $CONTAINER flye \
    --nano-raw $DATA_DIR/SRR33251869.fastq \
    --out-dir $WORK_DIR/ecoli_flye_out \
    --threads 32

# Assemble K. pneumoniae
singularity exec -B $WORK_DIR -B $DATA_DIR $CONTAINER flye \
    --nano-raw $DATA_DIR/SRR33251867.fastq \
    --out-dir $WORK_DIR/kpneumo_flye_out \
    --threads 32
