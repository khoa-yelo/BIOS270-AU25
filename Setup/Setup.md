# Overview

This guide walks you through setting up a productive computing environment for your coursework and future research. This includes command-line shortcuts, environment management, data management, and pipeline development tools, and cloud or GPU resources for your machine learning projects.

---

## Resources

- [**tmux cheatsheet**](https://tmuxai.dev/tmux-cheat-sheet/)



> **Note:** Include **screenshots** and **code snippets** in your *Write-up 1* to document your work clearly.

---

## Set Up Your `~/.bashrc` (or `~/.bash_profile`)

To accelerate your work on the command line, customize your Bash profile with shortcuts and environment variables.  
Your Bash profile automatically runs every time you log in.

Below is an example setup, feel free to modify or add your favorite shortcuts.

```bash
# Example custom bash profile

# -----------------------------
# Functions
# -----------------------------
# Example: print numbers from 1 to N (default = 5)
count() {
  local limit=${1:-5}
  for ((i=1; i<=limit; i++)); do
    echo "Count is: $i"
    sleep 1
  done
}

# -----------------------------
# Environment variables
# -----------------------------
export CLASS="$SCRATCH/bios270"
export CLASS_REPO="$CLASS/repos/BIOS270-AU25"
export CLASS_DATA="$CLASS/data"
export CLASS_ENVS="$CLASS/envs"

# -----------------------------
# Basic shortcuts
# -----------------------------
alias reload="source ~/.bashrc"
alias l='ls -ltrh'
alias ..="cd .."

# -----------------------------
# Quick navigation
# -----------------------------
alias cdc="cd $CLASS"
alias cdcd="cd $CLASS_DATA"
alias cdcr="cd $CLASS_REPO"

# -----------------------------
# Git and file utilities
# -----------------------------
alias gs="git status"
alias usage='du -h -d1'
alias space='df -h'

# -----------------------------
# SLURM queue and job utilities
# -----------------------------
alias qu='squeue -u $USER'

checkstatus() {
   sacct -j "$1" --format=JobID,JobName,State,Elapsed,MaxRSS,MaxVMSize,CPUTime,NodeList%20
}

# -----------------------------
# Interactive job launchers
# -----------------------------
alias small='srun --pty -p normal --mem=12G --cpus-per-task=2 --time=2:00:00 bash'
alias med='srun --pty -p normal --mem=32G --cpus-per-task=4 --time=2:00:00 bash'
alias large='srun --pty -p normal --mem=64G --cpus-per-task=8 --time=4:00:00 bash'
alias gpu='srun --pty -p gpu --gres=gpu:1 --mem=32G --cpus-per-task=4 --time=2:00:00 bash'
```

---

## Tools for Setting Up Your Environment

### 1. Install **Micromamba**

Micromamba is a lightweight package manager compatible with Conda.  
When installing, choose a prefix location on a disk with plenty of storage (not `$HOME`), since this is where packages will be installed.

```bash
"${SHELL}" <(curl -L https://micro.mamba.pm/install.sh)
# Prefix location? [~/micromamba] $CLASS_ENVS/micromamba
source ~/.bashrc
# Test your installation
micromamba --version
```

---

### 2. Install **Docker Desktop**

Download [Docker Desktop](https://www.docker.com/products/docker-desktop/) for your operating system.  
We’ll use it to build and push container images in later exercises.

You’ll also need:
- [**Stanford GitLab**](https://gitlab.stanford.edu/): create a new project named `containers` and set up SSH keys.  
- [**Docker Hub**](https://hub.docker.com/signup): create an account.

---

## Tools for Managing Your Data

Set up **Google Cloud Platform (GCP)** using your **personal email** (Stanford email addresses cannot be used to create new projects).

- New users receive **$300 in free credits**.
- Otherwise, enter billing info — we’ll stay within the free tier.

You’ll use:
- [**Google Cloud Storage (GCS)**](https://cloud.google.com/storage) – for large data storage  
- [**Google BigQuery**](https://cloud.google.com/bigquery) – for SQL analytics  
- [**SQLiteStudio**](https://sqlitestudio.pl/) – for local SQL testing  
- [**Google Sheets**](https://sheets.google.com) – for data summaries and reports  

---

## Tools for Pipeline Development

- Install [**Nextflow**](https://www.nextflow.io/) for workflow management and pipeline automation.

---

## Tools for Machine Learning Projects

You’ll need access to **GPUs** for training your ML models.

### Option 1: Google Cloud Platform (Recommended)
- Use [**Vertex AI Workbench**](https://cloud.google.com/vertex-ai/docs/workbench) for Jupyter-based GPU training.  
- New accounts have **$300 credits**.  
- Request increased GPU quota under **`metrics:gpu_all_regions`** in GCP Console.  
- Create and test a new instance.

### Option 2: **Google Colab Pro**
Sign up with your Stanford email — it’s free for students.  
[Sign up here](https://colab.research.google.com/signup).  
Save Colab compute units for Project 2.

### Option 3: **Runpod Credits (if needed)**
If Colab or GCP are unavailable, fill out the provided Google Form to request **Runpod credits** and set up a [Runpod](https://www.runpod.io/) account.

---

### (Optional) **Weights & Biases**

Create a [Weights & Biases account](https://wandb.ai/site/) to track your ML training metrics and experiment logs.
