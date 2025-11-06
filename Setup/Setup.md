# Setup

This document helps you set up an efficient computing environment for this course, including command-line shortcuts and tools to manage your environment, data, and workflow.

>*“Yet another Duo push…” - when authentication takes longer than the job itself.*
---

## Resources

- [**tmux cheatsheet**](https://tmuxai.dev/tmux-cheat-sheet/)



> **Instruction:** Include **screenshots** and **code snippets** in your Write-up to document your work.

---

## Set Up Your `~/.bashrc` (or `~/.bash_profile`)

Customize your Bash profile with shortcuts and environment variables.  
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
export CLASS="/farmshare/home/classes/bios/270"

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

When installing, choose a prefix location on a disk with plenty of storage (i.e. usually not `$HOME`), since this is where packages will be installed.

```bash
"${SHELL}" <(curl -L https://micro.mamba.pm/install.sh)
# Prefix location? [~/micromamba] $SCRATCH/envs/micromamba
source ~/.bashrc
# Test your installation
micromamba --version
```

---

### 2. Install **Docker Desktop**

Download [Docker Desktop](https://www.docker.com/products/docker-desktop/) to your laptop.  We’ll use it to build and push container images in later exercises.

You’ll also need a place to store your container images. We'll practice pushing images to `Docker Hub` for public images and Stanford Gitlab Container Registry, where you can store your private images. Complete the following steps:   
- [**Stanford GitLab**](https://gitlab.stanford.edu/): sign-in and create a new project named `containers`.  
- [**Docker Hub**](https://hub.docker.com/signup): create an account.

---

## Tools for Managing Your Data

Set up [**Google Cloud Platform (GCP)**](https://cloud.google.com/) using your **personal email** (as Stanford requires approval to create new projects with Stanford email).

- New users receive $300 in free credits.
- You should have also received an email about redeeming a $50 credit coupon. Please use your Stanford email to redeem but apply the coupon to your **personal email account**
- Create a new project named `BIOS270`


---

## Tools for Pipeline Development

- Install [**Nextflow**](https://www.nextflow.io/) on Farmshare for pipeline developement.

```bash
curl -s https://get.nextflow.io | bash
# To confirm it's installed correctly
nextflow info
```
---

## Tools for Machine Learning Projects

You’ll need access to **GPUs** for training your ML models.

### Option 1: Google Cloud Platform (Recommended)
- Use [**Vertex AI Workbench**](https://cloud.google.com/vertex-ai/docs/workbench) for Jupyter-based GPU training.  
- Request increased GPU quota under **`metric: compute.googleapis.com/gpus_all_regions`** in `IAM & Admin` -> `Quotas & System limits`.  
- When approved, create and test a new gpu instance.

### Option 2: **Google Colab Pro**
Sign up with your Stanford email, it’s free for students. [Sign up here](https://colab.research.google.com/signup).  
Save Colab compute units for Project 2.

>For your future GPU usage after this course, Stanford offers 5,000 GPU hours for free on [Marlowe](https://datascience.stanford.edu/marlowe/marlowe-access), talk to your PI to apply! 

### (Optional) **Weights & Biases**

Create a [Weights & Biases account](https://wandb.ai/site/) to track your ML training metrics and experiment logs.

---
## Warm-up: SLURM exercise

Given a `data.txt` with the content below
```
12
7
91
8
27
30
```

Below is a common and useful logic one may use to submit a slurm array job

```bash
#SBATCH --job-name=warmup
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --array=0-2
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00

i=0
# loop through each line in data.txt, `value` store line content
while read -r value; do
    if (( i % SLURM_ARRAY_TASK_COUNT == SLURM_ARRAY_TASK_ID )); then
        echo "$i: $value"
    fi
    # increment
    ((i++))
done < data.txt
```

Answer the following questions in your `write-up`:
1. How many slurm job will be submitted?
2. What is the purpose of the `if` statement?
3. What is the expected output in each `*.out` file?
