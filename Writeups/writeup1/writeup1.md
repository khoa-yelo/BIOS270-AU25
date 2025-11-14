# Write-up 1: Bash & SLURM

**Name:** Troy Helenihi  
**Student ID:** troy430  
**Date:** 11/12/2025

---

## Overview

This document contains the answers to the questions at the end of `Setup.md` and `Environment.md`.

---

## Content

`Setup.md` questions:

**1. How many slurm jobs will be submitted?**
> Three SLURM jobs will be submitted because the directive `#SBATCH --array=0-2` creates jobs with indices 0, 1, and 2.

**2. What is the purpose of the `if` statement?**
> The purpose of the `if` statement is to evenly split the work across the three SLURM jobs by having each one process only the lines of `data.txt` whose line numbers **match** its array index (based on the modulo result).

**3. What is the expected output in each `*.out` file?**

*Each job’s output file contains the line numbers and values from `data.txt` that correspond to its array index:*

- **Job 0 (`SLURM_ARRAY_TASK_ID=0`)**
```bash
0: 12
3: 8
```
- **Job 1 (`SLURM_ARRAY_TASK_ID=1`)**
```bash
1: 7
4: 27
```
- **Job 2 (`SLURM_ARRAY_TASK_ID=2`)**
```bash
2: 91
5: 30
```
Each file is saved as `logs/warmup_<jobID>_<arrayIndex>.out`.

`Environment.md` questions:



## Acknowledgement
Collaborator: Eliel Akinbami - helped clarify instructions for customizing my Bash profile.