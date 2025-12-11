cd ~/repos/BIOS270-AU25/Project1

cat > Project1_Writeup.md << 'EOF'
# Project 1: Genomics Pipeline - E. coli Paralog Analysis

**Student:** Isabel Goldaracena  
**Date:** December 2024  
**Course:** BIOS270-AU25

---

## Overview

This project implements an end-to-end genomics pipeline to identify paralogous protein-coding genes in *E. coli* starting from raw Nanopore FASTQ sequencing data.

**Pipeline Steps:**
1. Genome assembly with Flye
2. Genome annotation with Bakta
3. Protein clustering with MMseqs2
4. Paralog analysis and visualization

---

## Input Data

- **Organism:** *Escherichia coli*
- **Data:** Raw Nanopore long-read sequencing (FASTQ)
- **File:** `/farmshare/home/classes/bios/270/data/project1/SRR33251869.fastq`

---

## Step 1: Genome Assembly with Flye

### Script: `run_flye_ecoli.sh`
```bash
#!/bin/bash
#SBATCH --job-name=flye_ecoli
#SBATCH --output=logs/flye_ecoli_%j.out
#SBATCH --error=logs/flye_ecoli_%j.err
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=04:00:00

# Input and output paths
FASTQ="/farmshare/home/classes/bios/270/data/project1/SRR33251869.fastq"
OUTDIR="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_flye_out"

# Container path
CONTAINER="/farmshare/user_data/isagolda/containers/bioinformatics_latest.sif"

# Load Apptainer
module load apptainer

# Run Flye
apptainer exec \
  -B /farmshare/home/classes/bios/270 \
  -B /home/users/isagolda/repos/BIOS270-AU25/Project1 \
  $CONTAINER \
  flye --nano-raw $FASTQ \
       --out-dir $OUTDIR \
       --threads 32

echo "Flye assembly completed!"
echo "Assembly output: $OUTDIR/assembly.fasta"
```

### Assembly Results

- **Total length:** 5,072,098 bp
- **Number of contigs:** 12
- **Largest contig:** 4,733,170 bp
- **N50:** 4,733,170 bp
- **Mean coverage:** 72x

---

## Step 2: Genome Annotation with Bakta

### Script: `run_bakta_ecoli.sh`
```bash
#!/bin/bash
#SBATCH --job-name=bakta_ecoli
#SBATCH --output=logs/bakta_ecoli_%j.out
#SBATCH --error=logs/bakta_ecoli_%j.err
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=02:00:00

# Input and output paths
ASSEMBLY="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_flye_out/assembly.fasta"
OUTDIR="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_bakta_out"
BAKTA_DB="/farmshare/home/classes/bios/270/data/archive/bakta_db/db"

# Container path (Bakta uses a different container!)
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
```

### Annotation Results

- **Total proteins predicted:** [Number from your results]
- **Key output:** `assembly.faa` (protein sequences)

---

## Step 3: Protein Clustering with MMseqs2

### Script: `run_mmseqs_ecoli.sh`
```bash
#!/bin/bash
#SBATCH --job-name=mmseqs_ecoli
#SBATCH --output=logs/mmseqs_ecoli_%j.out
#SBATCH --error=logs/mmseqs_ecoli_%j.err
#SBATCH --cpus-per-task=32
#SBATCH --mem=8G
#SBATCH --time=00:30:00

# Input and output paths
PROTEIN_FAA="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_bakta_out/assembly.faa"
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
```

### Clustering Parameters

- **Minimum sequence identity:** 90%
- **Coverage:** 80%
- **Sensitivity:** 7

---

## Step 4: Paralog Analysis and Visualization

### Script: `run_analysis_ecoli.sh`
```bash
#!/bin/bash
#SBATCH --job-name=analyze_ecoli
#SBATCH --output=logs/analyze_ecoli_%j.out
#SBATCH --error=logs/analyze_ecoli_%j.err
#SBATCH --cpus-per-task=4
#SBATCH --mem=4G
#SBATCH --time=00:15:00

# Input files
FAA="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_bakta_out/assembly.faa"
CLUSTER="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_mmseqs_out/ecoli_prot90_cluster.tsv"

# Output files
TSV="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_paralogs.tsv"
PNG="/home/users/isagolda/repos/BIOS270-AU25/Project1/results/ecoli_paralogs_top10.png"

# Container path
CONTAINER="/farmshare/user_data/isagolda/containers/bioinformatics_latest.sif"

# Load Apptainer
module load apptainer

# Run analysis
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
```

---

## Results

### Summary Statistics

- **Total paralogous proteins:** [Your number]
- **Highest copy number:** [Your number]
- **Proteins with 2 copies:** [Your number]
- **Proteins with 3+ copies:** [Your number]

### Top 10 Most Frequent Paralogs

![Top 10 Paralogs](results/ecoli_paralogs_top10.png)

### Complete Paralog Table

See: [`results/ecoli_paralogs.tsv`](results/ecoli_paralogs.tsv)

---

## Biological Interpretation

[Add your interpretation here - what types of proteins are most commonly duplicated? Why might these be paralogs in E. coli?]

Common paralogous proteins in bacteria include:
- **Transposases** - Mobile genetic elements that can move around the genome
- **Integrases** - Enzymes that integrate foreign DNA
- **ABC transporters** - Membrane proteins for nutrient uptake
- **Phage proteins** - Remnants of viral infections

---

## Conclusion

[Add your conclusions here]

---

## Files Included
- `run_flye_ecoli.sh` - SLURM script for genome assembly
- `run_bakta_ecoli.sh` - SLURM script for genome annotation
- `run_mmseqs_ecoli.sh` - SLURM script for protein clustering
- `run_analysis_ecoli.sh` - SLURM script for paralog analysis
- `analyze_paralogs.py` - Python script for analysis and visualization-dw `results/ecoli_paralogs.tsv` - Complete paralog results
- `results/ecoli_paralogs_top10.png` - Visualization :1,$
1,$1,$d
1,$d
1,$d
d
