#!/bin/bash
#SBATCH --job-name=summarize
#SBATCH --partition=normal
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=30:00
#SBATCH --output=summarize_%j.log
#SBATCH --error=summarize_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lchan8@stanford.edu

module load apptainer

CONTAINER=/farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif
WORK_DIR=$(pwd)

# Run for E. coli
singularity exec -B $WORK_DIR $CONTAINER python3 $WORK_DIR/summarize_paralogs.py \
    --faa $WORK_DIR/ecoli_bakta_out/assembly.faa \
    --clusters $WORK_DIR/ecoli_mmseqs_out/ecoli_prot90_cluster.tsv \
    --output $WORK_DIR/ecoli \
    --sample "E. coli"

# Run for K. pneumoniae
singularity exec -B $WORK_DIR $CONTAINER python3 $WORK_DIR/summarize_paralogs.py \
    --faa $WORK_DIR/kpneumo_bakta_out/assembly.faa \
    --clusters $WORK_DIR/kpneumo_mmseqs_out/kpneumo_prot90_cluster.tsv \
    --output $WORK_DIR/kpneumo \
    --sample "K. pneumoniae"
