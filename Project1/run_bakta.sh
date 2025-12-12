#!/bin/bash
#SBATCH --job-name=bakta_annotation
#SBATCH --partition=normal
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=2:00:00
#SBATCH --output=bakta_%j.log
#SBATCH --error=bakta_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lchan8@stanford.edu

module load apptainer

CONTAINER=/farmshare/home/classes/bios/270/envs/bakta_1.8.2--pyhdfd78af_0.sif
BAKTA_DB=/farmshare/home/classes/bios/270/data/archive/bakta_db
WORK_DIR=$(pwd)

# Annotate E. coli
singularity exec -B $WORK_DIR -B $BAKTA_DB $CONTAINER bakta \
    --db $BAKTA_DB/db \
    --output $WORK_DIR/ecoli_bakta_out \
    $WORK_DIR/ecoli_flye_out/assembly.fasta \
    --force \
    --threads 16

# Annotate K. pneumoniae
singularity exec -B $WORK_DIR -B $BAKTA_DB $CONTAINER bakta \
    --db $BAKTA_DB/db \
    --output $WORK_DIR/kpneumo_bakta_out \
    $WORK_DIR/kpneumo_flye_out/assembly.fasta \
    --force \
    --threads 16
