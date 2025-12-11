#!/bin/bash
#SBATCH --job-name=mmseqs_ecoli
#SBATCH --output=logs/mmseqs_ecoli_%j.out
#SBATCH --error=logs/mmseqs_ecoli_%j.err
#SBATCH --cpus-per-task=32
#SBATCH --mem=8G
#SBATCH --time=00:30:00

# Input and output paths
PROTEIN_FAA="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_bakta_out/assembly.faa"
OUTDIR="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_mmseqs_out"
PREFIX="ecoli_prot90"
TMPDIR="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_mmseqs_tmp"

# Create output directories
mkdir -p $OUTDIR
mkdir -p $TMPDIR

# Container path
CONTAINER="/farmshare/user_data/isagolda/containers/bioinformatics_latest.sif"

# Load Apptainer
module load apptainer

# Run MMseqs2
apptainer exec \
  -B /farmshare/home/classes/bios/270 \
  -B /home/users/isagolda/repos/BIOS270-AU25/Project1 \
  $CONTAINER \
  mmseqs easy-cluster \
    $PROTEIN_FAA \
    $OUTDIR/$PREFIX \
    $TMPDIR \
    --min-seq-id 0.9 \
    -c 0.8 \
    --cov-mode 1 \
    -s 7 \
    --threads 32

echo "MMseqs2 clustering completed!"
echo "Cluster results: $OUTDIR/${PREFIX}_cluster.tsv"

# Clean up tmp directory
rm -rf $TMPDIR
