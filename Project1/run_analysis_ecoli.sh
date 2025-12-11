#!/bin/bash
#SBATCH --job-name=analyze_ecoli
#SBATCH --output=logs/analyze_ecoli_%j.out
#SBATCH --error=logs/analyze_ecoli_%j.err
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=00:15:00

# Input files
FAA="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_bakta_out/assembly.faa"
CLUSTER="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_mmseqs_out/ecoli_prot90_cluster.tsv"

# Output files
TSV="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_paralogs.tsv"
PNG="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_paralogs_top10.png"

# Container path
CONTAINER="/farmshare/user_data/isagolda/containers/bioinformatics_latest.sif"

# Load Apptainer
module load apptainer

# Run analysis (INSIDE CONTAINER via apptainer exec)
apptainer exec \
  -B /home/users/isagolda/repos/BIOS270-AU25/Project1 \
  $CONTAINER \
  python3 /home/users/isagolda/repos/BIOS270-AU25/Project1/analyze_paralogs.py \
    --faa $FAA \
    --cluster $CLUSTER \
    --output-tsv $TSV \
    --output-png $PNG \
    --top-n 10

echo "Analysis completed!"
echo "Results: $TSV"
echo "Plot: $PNG"
