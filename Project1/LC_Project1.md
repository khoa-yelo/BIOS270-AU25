# Project 1: Genomics Pipeline 

In this project, you will build an end‑to‑end genomics pipeline to
identify paralogous protein‑coding genes starting directly from raw
Nanopore FASTQ files.

> *Finally, we are here.*

------------------------------------------------------------------------

## Resources

- [**Flye**](https://github.com/mikolmogorov/Flye)
- [**Bakta**](https://github.com/oschwengers/bakta)
- [**MMSeqs2**](https://github.com/soedinglab/MMseqs2)

------------------------------------------------------------------------

## Overview

Your lab wants to investigate the genomes of several new bacterial strains, focusing specifically on 
protein‑coding genes that appear in multiple copies (paralogs). You have extracted genomic
DNA and sequenced it using the Oxford Nanopore platform, obtaining long‑read FASTQ files.

For this project, you are provided with two raw fastq files:

-   **E. coli**:
    `/farmshare/home/classes/bios/270/data/project1/SRR33251869.fastq`
-   **K. pneumoniae**:
    `/farmshare/home/classes/bios/270/data/project1/SRR33251867.fastq`

The expected inputs and outputs of your pipeline are:
#### **Input**

-   Raw long‑read Nanopore FASTQ files

#### **Output**

For each input fastq file, output:
- A **TSV file** listing all proteins that occur more than once (paralogs), with three columns:  
  **`protein_id`**, **`protein_name`**, **`copy_number`**
- **Visualizations**: minimally, a **PNG** image with bar plot showing top 10 most frequent paralogs

------------------------------------------------------------------------

## Step 1:  Genome Assembly with Flye

Let say you do not have good reference genomes for these strains and also want to potentially discover novel
paralogs. Therefore, you will assemble their genomes de novo using **Flye**.

Container:

    /farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif

Example command:

    flye --nano-raw SRR33251869.fastq --out-dir ecoli_flye_out --threads 32

The key output of this step is the assembled genome `assembly.fasta`, e.g.:

    /farmshare/home/classes/bios/270/data/project1/ecoli_flye_out/assembly.fasta
 
Slurm script to run Flye assembly

```bash
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
```

------------------------------------------------------------------------

## Step 2: Genome Annotation with Bakta

Use **Bakta** to predict and annotate genes.\
Container:

    /farmshare/home/classes/bios/270/envs/bakta_1.8.2--pyhdfd78af_0.sif

Example command:

    bakta --db /farmshare/home/classes/bios/270/data/archive/bakta_db/db --output ecoli_bakta_out/ ecoli_flye_out/assembly.fasta --force

The file you care about is the predicted protein FASTA (`.faa`), e.g.:

    /farmshare/home/classes/bios/270/data/project1/ecoli_bakta_out/assembly.faa

Slurm script to run Bakta annotation

```bash
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
```

------------------------------------------------------------------------

## Step 3: Protein Clustering with MMseqs2

Cluster proteins to detect duplicated genes (paralogs).\
Example command:

    mmseqs easy-cluster ecoli_bakta_out/assembly.faa ecoli_prot90 tmp --min-seq-id 0.9 -c 0.8 --cov-mode 1 -s 7 --threads 32

Clustering output e.g. :

    /farmshare/home/classes/bios/270/data/project1/ecoli_mmseqs_out/ecoli_prot90_cluster.tsv

This file contains two columns:

- **Column 1** – `cluster_id` (the representative protein ID for the cluster)  
- **Column 2** – `protein_id`

Slurm script to run MMseq2

```bash
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
```

------------------------------------------------------------------------

## Step 4: Summarize and Visualize the result

In this step, you will write a custom Python or R script that:

- Takes as input:
  - the protein FASTA file `assembly.faa` generated in **Step 2**, and  
  - the clustering result `*_cluster.tsv` generated in **Step 3**
- Parses the protein headers in `assembly.faa` to extract the **protein name** for each `protein_id`
- Uses `clusters.tsv` to:
  - identify clusters containing more than one protein (paralogs)  
  - compute the **copy number** for each protein (number of occurrences per cluster)
- Produces:
  - a **TSV summary file** with columns: `protein_id`, `protein_name`, `copy_number`  
  - one or more **visualizations** (e.g. bar plots) showing the most frequent paralogs and their copy numbers across the genome.

## Estimated Runtime and Resource (per FASTQ)

| Step | Tool        | Threads  | RAM (GB) | Wall Time (typical) |
|------|-------------|-------------------|----------|----------------------|
| 1    | Flye        | 16–32             | 32–64    | 1–2 hours      | 
| 2    | Bakta       | 8–16              | 8–16     | 20–40 minutes    | 
| 3    | MMseqs2     | 8–32              | 1–4     | < 5 minutes     | 
| 4    | Custom Script (Python/R) | 1–4 | 1–4 | < 5 minutes |

##  Reference Outputs

To assist with your project, expected outputs for each step are already
available:

    /farmshare/home/classes/bios/270/data/project1/

Example:

    /farmshare/home/classes/bios/270/data/project1/ecoli_flye_out
    
Slurm script to run data summarization and visualization

```bash
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
```
Python script to run data summarization and visualization

```python
#!/usr/bin/env python3
"""
Summarize and visualize protein paralogs from MMseqs2 clustering results.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def parse_faa_headers(faa_file):
    """Extract protein_id -> protein_name mapping from FASTA headers."""
    protein_names = {}
    with open(faa_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                parts = line[1:].strip().split(' ', 1)
                protein_id = parts[0]
                protein_name = parts[1] if len(parts) > 1 else "Unknown"
                protein_names[protein_id] = protein_name
    return protein_names


def parse_clusters(cluster_file):
    """Parse MMseqs2 cluster TSV file."""
    clusters = defaultdict(list)
    with open(cluster_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                cluster_id, protein_id = parts[0], parts[1]
                clusters[cluster_id].append(protein_id)
    return clusters


def find_paralogs(clusters, protein_names):
    """Identify clusters with >1 member (paralogs) and get their info."""
    paralogs = []
    for cluster_id, members in clusters.items():
        copy_number = len(members)
        if copy_number > 1:
            protein_name = protein_names.get(cluster_id, "Unknown")
            paralogs.append({
                'protein_id': cluster_id,
                'protein_name': protein_name,
                'copy_number': copy_number
            })
    return pd.DataFrame(paralogs)


def create_visualization(df, output_prefix, sample_name):
    """Create bar plot of top 10 most frequent paralogs."""
    top_paralogs = df.nlargest(10, 'copy_number')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(range(len(top_paralogs)), top_paralogs['copy_number'], color='steelblue')
    
    labels = [name[:40] + '...' if len(name) > 40 else name
              for name in top_paralogs['protein_name']]
    
    ax.set_yticks(range(len(top_paralogs)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('Copy Number')
    ax.set_title(f'Top 10 Most Frequent Paralogs - {sample_name}')
    
    for i, (bar, val) in enumerate(zip(bars, top_paralogs['copy_number'])):
        ax.text(val + 0.1, i, str(val), va='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_top10_paralogs.png', dpi=150)
    plt.close()
    print(f"Saved visualization: {output_prefix}_top10_paralogs.png")


def main():
    parser = argparse.ArgumentParser(description='Summarize protein paralogs')
    parser.add_argument('--faa', required=True, help='Protein FASTA file (.faa)')
    parser.add_argument('--clusters', required=True, help='MMseqs2 cluster TSV file')
    parser.add_argument('--output', required=True, help='Output prefix')
    parser.add_argument('--sample', default='Sample', help='Sample name for plot title')
    args = parser.parse_args()
    
    print(f"Parsing protein sequences from {args.faa}...")
    protein_names = parse_faa_headers(args.faa)
    print(f"  Found {len(protein_names)} proteins")
    
    print(f"Parsing clusters from {args.clusters}...")
    clusters = parse_clusters(args.clusters)
    print(f"  Found {len(clusters)} clusters")
    
    print("Identifying paralogs (clusters with >1 member)...")
    df = find_paralogs(clusters, protein_names)
    df = df.sort_values('copy_number', ascending=False)
    print(f"  Found {len(df)} paralog families")
    
    tsv_file = f'{args.output}_paralogs.tsv'
    df.to_csv(tsv_file, sep='\t', index=False)
    print(f"Saved summary: {tsv_file}")
    
    if len(df) > 0:
        create_visualization(df, args.output, args.sample)
    else:
        print("No paralogs found - skipping visualization")
    
    print(f"\n=== Summary for {args.sample} ===")
    print(f"Total paralog families: {len(df)}")
    if len(df) > 0:
        print(f"Total duplicated proteins: {df['copy_number'].sum()}")
        print(f"Max copy number: {df['copy_number'].max()}")
        print(f"\nTop 5 paralogs:")
        for _, row in df.head().iterrows():
            print(f"  {row['protein_name'][:50]}: {row['copy_number']} copies")


if __name__ == '__main__':
    main()
```

**Visualization Outputs**
![Top 10 Most Frequent Paralogs in E. coli](/farmshare/user_data/lchan8/repos/BIOS270-AU25/Project1/ecoli_top10_paralogs.png)

![Top 10 Most Frequent Paralogs in K. pneumoniae](/farmshare/user_data/lchan8/repos/BIOS270-AU25/Project1/kpneumo_top10_paralogs.png)

**Screenshots of directory with all outputs**
![Screenshot of directory with all outputs #1](/farmshare/user_data/lchan8/repos/BIOS270-AU25/Project1/screenshots/Screenshot_directory_output_1.png)

![Screenshot of directory with all outputs #2](/farmshare/user_data/lchan8/repos/BIOS270-AU25/Project1/screenshots/Screenshot_directory_output_2.png)

![Screenshot of directory with all outputs #3](/farmshare/user_data/lchan8/repos/BIOS270-AU25/Project1/screenshots/Screenshot_directory_output_3.png)

![Screenshot of directory with all outputs #4](/farmshare/user_data/lchan8/repos/BIOS270-AU25/Project1/screenshots/Screenshot_directory_output_4.png)

------------------------------------------------------------------------
