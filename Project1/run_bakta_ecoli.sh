#!/bin/bash
#SBATCH --job-name=bakta_ecoli
#SBATCH --output=logs/bakta_ecoli_%j.out
#SBATCH --error=logs/bakta_ecoli_%j.err
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=02:00:00

# Input and output paths
ASSEMBLY="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_flye_out/assembly.fasta"
OUTDIR="/home/users/isagolda/repos/BIOS270-AU25/Project1/ecoli_bakta_out"
BAKTA_DB="/farmshare/home/classes/bios/270/data/archive/bakta_db/db"

# Container path 
CONTAINER="/farmshare/home/classes/bios/270/envs/bakta_1.8.2--pyhdfd78af_0.sif"

# Load Apptainer
module load apptainer

# Run Bakta
apptainer exec \
  -B /farmshare/home/classes/bios/270 \
  -B /home/users/isagolda/repos/BIOS270-AU25/Project1 \
  $CONTAINER \
  bakta --db $BAKTA_DB \
        --output $OUTDIR \
        --force \
        --threads 16 \
        $ASSEMBLY

echo "Bakta annotation completed!"
echo "Protein sequences: $OUTDIR/assembly.faa"

