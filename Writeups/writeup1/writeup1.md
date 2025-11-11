# Write-up 1

**Name:** Tim Jing
**Student ID:** timjing
**Date:** 11/11/2025  

---

## Overview

This writeup covers setup.md and environment.md. 

---

## Content

#### Setup.md
1. Three jobs will be submitted. This is becuase the job indicates --array=0-2, and each index represents one SLURM job.

2. The if statement checks the line number of `data.txt` and ensures that each of the 3 SLURM jobs receives 1/3rd of the lines to process, based on whether the line number % 3 = the index of the job in the array.

3. Each .out file will contain "line_number: value_of_line" where the line_number % 3 = the index of the job.

#### Environment.md

1. You can use `micromamba env list` to list all created environments.

2. You can use `micromamba list -n <env_name>` to list all packages in an environment.

3. You can use `micromamba remove -n <env_name> <package_name>` to remove a package.

4. You can use `micromamba install -n <env_name> -c <channel_name> <package_name>` to install a package from a certain channel.

5. You can use `micromamba env remove -n <env_name>` to remove an environment.

6. I used `micromamba list -n bioinfo_example` to first list all installed packages and then `grep -E "r-base|bioconductor"` to filter al the lines. They were linked with the pipe operator. The results are below:

```
bioconductor-apeglm                1.24.0        r43hf17093f_1         bioconda   
  bioconductor-biobase               2.62.0        r43ha9d7317_3         bioconda   
  bioconductor-biocgenerics          0.48.1        r43hdfd78af_2         bioconda   
  bioconductor-biocparallel          1.36.0        r43hf17093f_2         bioconda   
  bioconductor-data-packages         20250625      hdfd78af_0            bioconda   
  bioconductor-delayedarray          0.28.0        r43ha9d7317_2         bioconda   
  bioconductor-deseq2                1.42.0        r43hf17093f_2         bioconda   
  bioconductor-genomeinfodb          1.38.1        r43hdfd78af_1         bioconda   
  bioconductor-genomeinfodbdata      1.2.11        r43hdfd78af_1         bioconda   
  bioconductor-genomicranges         1.54.1        r43ha9d7317_2         bioconda   
  bioconductor-iranges               2.36.0        r43ha9d7317_2         bioconda   
  bioconductor-matrixgenerics        1.14.0        r43hdfd78af_3         bioconda   
  bioconductor-s4arrays              1.2.0         r43ha9d7317_2         bioconda   
  bioconductor-s4vectors             0.40.2        r43ha9d7317_2         bioconda   
  bioconductor-sparsearray           1.2.2         r43ha9d7317_2         bioconda   
  bioconductor-summarizedexperiment  1.32.0        r43hdfd78af_0         bioconda   
  bioconductor-xvector               0.42.0        r43ha9d7317_2         bioconda   
  bioconductor-zlibbioc              1.48.0        r43ha9d7317_2         bioconda   
  r-base                             4.3.3         h2fbd60f_20           conda-forge
  r-base64enc                        0.1_3         r43hb1dbf0f_1007      conda-forge
```


## Acknowledgement
Collaborator: N/A
