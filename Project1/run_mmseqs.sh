#!/bin/bash
#SBATCH --job-name=mmseqs_cluster
#SBATCH --partition=normal
#SBATCH --cpus-per-task=32
#SBATCH --mem=32G
#SBATCH --time=1:00:00
#SBATCH --output=mmseqs_%j.log
#SBATCH --error=mmseqs_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lchan8@stanford.edu

module load apptainer

CONTAINER=/farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif
WORK_DIR=$(pwd)

# Create output directories
mkdir -p $WORK_DIR/ecoli_mmseqs_out $WORK_DIR/kpneumo_mmseqs_out

# Cluster E. coli proteins
singularity exec -B $WORK_DIR $CONTAINER mmseqs easy-cluster \
    $WORK_DIR/ecoli_bakta_out/assembly.faa \
    $WORK_DIR/ecoli_mmseqs_out/ecoli_prot90 \
    $WORK_DIR/tmp_ecoli \
    --min-seq-id 0.9 \
    -c 0.8 \
    --cov-mode 1 \
    -s 7 \
    --threads 32

# Cluster K. pneumoniae proteins
singularity exec -B $WORK_DIR $CONTAINER mmseqs easy-cluster \
    $WORK_DIR/kpneumo_bakta_out/assembly.faa \
    $WORK_DIR/kpneumo_mmseqs_out/kpneumo_prot90 \
    $WORK_DIR/tmp_kpneumo \
    --min-seq-id 0.9 \
    -c 0.8 \
    --cov-mode 1 \
    -s 7 \
    --threads 32

# Cleanup temp directories
rm -rf $WORK_DIR/tmp_ecoli $WORK_DIR/tmp_kpneumo
