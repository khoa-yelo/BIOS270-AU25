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

Your lab is sequencing several new bacterial strains and wants to
understand their genomes, focusing specifically on protein‑coding genes
that appear in multiple copies (paralogs). You have extracted genomic
DNA and sequenced it using the Oxford Nanopore platform, obtaining long‑read FASTQ
files.

For this project, you are provided with two raw fastq outputs:

-   **E. coli**:
    `/farmshare/home/classes/bios/270/data/project1/SRR33251869.fastq`
-   **K. pneumoniae**:
    `/farmshare/home/classes/bios/270/data/project1/SRR33251867.fastq`

The expected inputs and outputs are:
#### **Input**

-   Raw long‑read Nanopore FASTQ files

#### **Output**

For each input fastq files, output:
- A **TSV file** listing all proteins that occur more than once (paralogs), with three columns:  
  **`protein_id`**, **`protein_name`**, **`copy_number`**
- **Visualizations**, including bar plots showing top 10 most frequent paralogs

------------------------------------------------------------------------

## Step 1:  Genome Assembly with Flye

Since you do not have good reference genomes and are focusing on novel
paralogs, you will assemble each genome de novo using **Flye**.

Flye is available inside this container:

    /farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif

Example command (E. coli):

    flye --nano-raw SRR33251869.fastq --out-dir ecoli_flye_out --threads 32

The key output is the assembled genome:

    /farmshare/home/classes/bios/270/data/project1/ecoli_flye_out/assembly.fasta

------------------------------------------------------------------------

## Step 2: Genome Annotation with Bakta

Use **Bakta** to predict and annotate genes.\
Container:

    /farmshare/home/classes/bios/270/envs/bakta_1.8.2--pyhdfd78af_0.sif

Example command:

    bakta --db /farmshare/home/classes/bios/270/data/archive/bakta_db/db --output ecoli_bakta_out/ ecoli/assembly.fasta --force

The file you care about is the predicted protein FASTA (`.faa`), e.g.:

    /farmshare/home/classes/bios/270/data/project1/ecoli_bakta_out/assembly.faa

------------------------------------------------------------------------

## Step 3: Protein Clustering with MMseqs2

Cluster proteins to detect duplicated genes (paralogs).\
Example command:

    mmseqs easy-cluster ecoli_bakta_out/assembly.faa ecoli_prot90 tmp --min-seq-id 0.9 -c 0.8 --cov-mode 1 -s 7 --threads 32

Clustering output:

    /farmshare/home/classes/bios/270/data/project1/ecoli_mmseqs_out/ecoli_prot90_cluster.tsv

This file contains two columns:

- **Column 1** – `cluster_id` (the representative protein ID for the cluster)  
- **Column 2** – `protein_id`
------------------------------------------------------------------------

## Step 4: Summarize and Visualize the result

In this step, you will write a custom Python or R script that:

- Takes as input:
  - the protein FASTA file `assembly.faa` generated in **Step 2**, and  
  - the clustering result `clusters.tsv` generated in **Step 3**
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

------------------------------------------------------------------------