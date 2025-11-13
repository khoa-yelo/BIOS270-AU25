# Write-up 0

**Name:** Yujin Moon  
**Student ID:** ymoon1  
**Date:** 11/11/2025  

---

## Content

For the Warm-up:SLURM exercise:
1. A single job will be submitted, but 3 array tasks will run.
2. The if statement assigns each line to one array task, using modulo arithmetic.
3. The expected output of each *.out file is like below:
   
   Task 0 (ID=0) → warmup_<jobID>_0.out
   0: 12
   3: 8

   Task 1 (ID=1) → warmup_<jobID>_1.out
   1: 7
   4: 27

   Task 2 (ID=2) → warmup_<jobID>_2.out
   2: 91
   5: 30



