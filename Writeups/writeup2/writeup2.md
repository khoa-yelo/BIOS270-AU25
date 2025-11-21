# Write-up 1: setup

**Name:** Louise Lima  
**Student ID:** llima23  
**Date:** 11/13/2025  

---

## 1. Compare the new YAML file (bioinfo_example_latest.yaml) with the original one. What changes do you notice?
Simpler, cleaner, new dependencies
---
## 2. What micromamba command can you use to list all created environemnts?
micromamba env list

## 3. What micromamba command can you use to list all packages installed in a specific environment?
micromamba list

## 4. What micromamba command can you use to remove a package?
micromamba remove package_name

## 5. What micromamba command can you use to install a package from a specific channel?
micromamba install -c channel_name package_name

## 6. What micromamba command can you use to remove an environment?
micromamba env remove -n bioinfo_example

## 7. What are all the r-base and Bioconductor packages that were installed in the bioinfo_example environment? (Hint: You may want to use one of the commands from your answers to the above questions, and combine it with the grep command.)
r-base                             4.3.3         h2fbd60f_20          conda-forge
r-base64enc                        0.1_3         r43hb1dbf0f_1007     conda-forge
bioconductor-apeglm                1.24.0        r43hf17093f_1        bioconda   
bioconductor-biobase               2.62.0        r43ha9d7317_3        bioconda   
bioconductor-biocgenerics          0.48.1        r43hdfd78af_2        bioconda   
bioconductor-biocparallel          1.36.0        r43hf17093f_2        bioconda   
bioconductor-data-packages         20250625      hdfd78af_0           bioconda   
bioconductor-delayedarray          0.28.0        r43ha9d7317_2        bioconda   
bioconductor-deseq2                1.42.0        r43hf17093f_2        bioconda   
bioconductor-genomeinfodb          1.38.1        r43hdfd78af_1        bioconda   
bioconductor-genomeinfodbdata      1.2.11        r43hdfd78af_1        bioconda   
bioconductor-genomicranges         1.54.1        r43ha9d7317_2        bioconda   
bioconductor-iranges               2.36.0        r43ha9d7317_2        bioconda   
bioconductor-matrixgenerics        1.14.0        r43hdfd78af_3        bioconda   
bioconductor-s4arrays              1.2.0         r43ha9d7317_2        bioconda   
bioconductor-s4vectors             0.40.2        r43ha9d7317_2        bioconda   
bioconductor-sparsearray           1.2.2         r43ha9d7317_2        bioconda   
bioconductor-summarizedexperiment  1.32.0        r43hdfd78af_0        bioconda   
bioconductor-xvector               0.42.0        r43ha9d7317_2        bioconda   
bioconductor-zlibbioc              1.48.0        r43ha9d7317_2        bioconda   
