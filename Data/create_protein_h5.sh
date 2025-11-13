#!/bin/bash
#SBATCH --job-name=createh5
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=12G
#SBATCH --time=48:00:00

$RUN python create_protein_h5.py  --output protein_embeddings.h5 --protein_ids all_protein_ids.txt