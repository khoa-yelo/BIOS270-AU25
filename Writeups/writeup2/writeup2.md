# Write-up 2:

**Name:** Riley Juenemann       
**Student ID:** rjuene    
**Date:** 11/13/2025    

---

## Example outputs 
![Python example](../../Environment/scripts/python_example_plot.png)

![R example png](../../Environment/scripts/r_example_plot.png)

## Updated environment file

The new file lists changes in `rpy2` as a dependency, but there are no comments about dependency categories. Additionally, `defaults` is no longer listed as a channel.

```
name: bioinfo_example
channels:
  - bioconda
  - conda-forge
dependencies:
  - bioconductor-deseq2
  - biopython
  - matplotlib
  - numpy
  - pandas
  - pip
  - python=3.11
  - r-base=4.3
  - r-essentials
  - rpy2
  - seaborn

prefix: "/scratch/users/rjuene/envs/micromamba/envs/bioinfo_example"
```

## Micromamba questions
What micromamba command can you use to list all created environments?
`micromamba env list`

What micromamba command can you use to list all packages installed in a specific environment?
`micromamba list`

What micromamba command can you use to remove a package?
`micromamba uninstall <package name>`

What micromamba command can you use to install a package from a specific channel?
`micromamba install -c <channel name (eg conda-forge)> <package name>`

What micromamba command can you use to remove an environment?
`micromamba env remove -n <environment name>

What are all the r-base and Bioconductor packages that were installed in the bioinfo_example environment? (Hint: You may want to use one of the commands from your answers to the above questions, and combine it with the grep command.)


r-base packages were installed so that the R programming language will run. Bioconductor is a collection of R packages useful for analysis of common biological assays, such as sequencing, SNPs, and other genomic data.

r-base packages
```
  r-abind                            1.4_5         r43hc72bb7e_1006      conda-forge
  r-ashr                             2.2_63        r43h93ab643_2         conda-forge
  r-askpass                          1.2.1         r43h2b5f3a1_0         conda-forge
  r-assertthat                       0.2.1         r43hc72bb7e_5         conda-forge
  r-backports                        1.5.0         r43hb1dbf0f_1         conda-forge
  r-base                             4.3.3         h2fbd60f_20           conda-forge
  r-base64enc                        0.1_3         r43hb1dbf0f_1007      conda-forge
  r-bbmle                            1.0.25.1      r43hc72bb7e_1         conda-forge
  r-bdsmatrix                        1.3_7         r43h2b5f3a1_2         conda-forge
  r-bh                               1.87.0_1      r43hc72bb7e_0         conda-forge
  r-bit                              4.6.0         r43h2b5f3a1_0         conda-forge
  r-bit64                            4.6.0_1       r43h2b5f3a1_0         conda-forge
  r-bitops                           1.0_9         r43h2b5f3a1_0         conda-forge
  r-blob                             1.2.4         r43hc72bb7e_2         conda-forge
  r-boot                             1.3_32        r43hc72bb7e_0         conda-forge
  r-broom                            1.0.9         r43hc72bb7e_0         conda-forge
  r-bslib                            0.9.0         r43hc72bb7e_0         conda-forge
  r-cachem                           1.1.0         r43hb1dbf0f_1         conda-forge
  r-callr                            3.7.6         r43hc72bb7e_1         conda-forge
  r-caret                            6.0_94        r43hdb488b9_2         conda-forge
  r-cellranger                       1.1.0         r43hc72bb7e_1007      conda-forge
  r-class                            7.3_23        r43h2b5f3a1_0         conda-forge
  r-cli                              3.6.5         r43h93ab643_0         conda-forge
  r-clipr                            0.8.0         r43hc72bb7e_3         conda-forge
  r-clock                            0.7.3         r43h93ab643_0         conda-forge
  r-cluster                          2.1.8.1       r43hb67ce94_0         conda-forge
  r-coda                             0.19_4.1      r43hc72bb7e_1         conda-forge
  r-codetools                        0.2_20        r43hc72bb7e_1         conda-forge
  r-colorspace                       2.1_1         r43hdb488b9_0         conda-forge
  r-commonmark                       2.0.0         r43h2b5f3a1_0         conda-forge
  r-conflicted                       1.2.0         r43h785f33e_2         conda-forge
  r-cpp11                            0.5.2         r43h785f33e_1         conda-forge
  r-crayon                           1.5.3         r43hc72bb7e_1         conda-forge
  r-crul                             1.6.0         r43hc72bb7e_0         conda-forge
  r-curl                             7.0.0         r43h10955f1_0         conda-forge
  r-data.table                       1.17.8        r43h1c8cec4_0         conda-forge
  r-dbi                              1.2.3         r43hc72bb7e_1         conda-forge
  r-dbplyr                           2.5.1         r43hc72bb7e_0         conda-forge
  r-diagram                          1.6.5         r43ha770c72_3         conda-forge
  r-digest                           0.6.37        r43h0d4f4ea_0         conda-forge
  r-dplyr                            1.1.4         r43h0d4f4ea_1         conda-forge
  r-dtplyr                           1.3.2         r43hc72bb7e_0         conda-forge
  r-e1071                            1.7_16        r43h93ab643_0         conda-forge
  r-ellipsis                         0.3.2         r43hb1dbf0f_3         conda-forge
  r-emdbook                          1.3.14        r43hc72bb7e_0         conda-forge
  r-essentials                       4.3           r43hd8ed1ab_2005      conda-forge
  r-etrunct                          0.1           r43hc72bb7e_1006      conda-forge
  r-evaluate                         1.0.5         r43hc72bb7e_0         conda-forge
  r-fansi                            1.0.6         r43hb1dbf0f_1         conda-forge
  r-farver                           2.1.2         r43ha18555a_1         conda-forge
  r-fastmap                          1.2.0         r43ha18555a_1         conda-forge
  r-fontawesome                      0.5.3         r43hc72bb7e_0         conda-forge
  r-forcats                          1.0.0         r43hc72bb7e_2         conda-forge
  r-foreach                          1.5.2         r43hc72bb7e_3         conda-forge
  r-foreign                          0.8_90        r43h2b5f3a1_0         conda-forge
  r-formatr                          1.14          r43hc72bb7e_2         conda-forge
  r-fs                               1.6.6         r43h93ab643_0         conda-forge
  r-futile.logger                    1.4.3         r43hc72bb7e_1006      conda-forge
  r-futile.options                   1.0.1         r43hc72bb7e_1005      conda-forge
  r-future                           1.67.0        r43h785f33e_0         conda-forge
  r-future.apply                     1.20.0        r43hc72bb7e_0         conda-forge
  r-gargle                           1.6.0         r43h785f33e_0         conda-forge
  r-generics                         0.1.4         r43hc72bb7e_0         conda-forge
  r-ggplot2                          3.5.2         r43hc72bb7e_0         conda-forge
  r-gistr                            0.9.0         r43hc72bb7e_3         conda-forge
  r-glmnet                           4.1_10        r43ha36cffa_0         conda-forge
  r-globals                          0.18.0        r43hc72bb7e_0         conda-forge
  r-glue                             1.8.0         r43h2b5f3a1_0         conda-forge
  r-googledrive                      2.1.2         r43hc72bb7e_0         conda-forge
  r-googlesheets4                    1.1.2         r43h785f33e_0         conda-forge
  r-gower                            1.0.1         r43hb1dbf0f_2         conda-forge
  r-gtable                           0.3.6         r43hc72bb7e_0         conda-forge
  r-hardhat                          1.4.2         r43hc72bb7e_0         conda-forge
  r-haven                            2.5.5         r43h6d565e7_0         conda-forge
  r-hexbin                           1.28.5        r43hb67ce94_0         conda-forge
  r-highr                            0.11          r43hc72bb7e_1         conda-forge
  r-hms                              1.1.3         r43hc72bb7e_2         conda-forge
  r-htmltools                        0.5.8.1       r43ha18555a_1         conda-forge
  r-htmlwidgets                      1.6.4         r43h785f33e_3         conda-forge
  r-httpcode                         0.3.0         r43ha770c72_4         conda-forge
  r-httpuv                           1.6.16        r43h6d565e7_0         conda-forge
  r-httr                             1.4.7         r43hc72bb7e_1         conda-forge
  r-ids                              1.0.1         r43hc72bb7e_4         conda-forge
  r-invgamma                         1.2           r43hc72bb7e_0         conda-forge
  r-ipred                            0.9_15        r43hdb488b9_1         conda-forge
  r-irdisplay                        1.1           r43hd8ed1ab_3         conda-forge
  r-irkernel                         1.3.2         r43h785f33e_2         conda-forge
  r-irlba                            2.3.5.1       r43h0d28552_3         conda-forge
  r-isoband                          0.2.7         r43ha18555a_3         conda-forge
  r-iterators                        1.0.14        r43hc72bb7e_3         conda-forge
  r-jquerylib                        0.1.4         r43hc72bb7e_3         conda-forge
  r-jsonlite                         2.0.0         r43h2b5f3a1_0         conda-forge
  r-kernsmooth                       2.23_26       r43h8461fee_0         conda-forge
  r-knitr                            1.50          r43hc72bb7e_0         conda-forge
  r-labeling                         0.4.3         r43hc72bb7e_1         conda-forge
  r-lambda.r                         1.2.4         r43hc72bb7e_4         conda-forge
  r-later                            1.4.4         r43h3697838_0         conda-forge
  r-lattice                          0.22_7        r43h2b5f3a1_0         conda-forge
  r-lava                             1.8.1         r43hc72bb7e_0         conda-forge
  r-lazyeval                         0.2.2         r43hb1dbf0f_5         conda-forge
  r-lifecycle                        1.0.4         r43hc72bb7e_1         conda-forge
  r-listenv                          0.9.1         r43hc72bb7e_1         conda-forge
  r-lobstr                           1.1.2         r43ha18555a_4         conda-forge
  r-locfit                           1.5_9.12      r43h2b5f3a1_0         conda-forge
  r-lubridate                        1.9.4         r43h2b5f3a1_0         conda-forge
  r-magrittr                         2.0.3         r43hb1dbf0f_3         conda-forge
  r-maps                             3.4.3         r43h2b5f3a1_0         conda-forge
  r-mass                             7.3_60.0.1    r43hb1dbf0f_1         conda-forge
  r-matrix                           1.6_5         r43he966344_1         conda-forge
  r-matrixstats                      1.5.0         r43h2b5f3a1_0         conda-forge
  r-memoise                          2.0.1         r43hc72bb7e_3         conda-forge
  r-mgcv                             1.9_3         r43h2ae2be5_0         conda-forge
  r-mime                             0.13          r43h2b5f3a1_0         conda-forge
  r-mixsqp                           0.3_54        r43hb79369c_3         conda-forge
  r-modelmetrics                     1.2.2.2       r43h0d4f4ea_4         conda-forge
  r-modelr                           0.1.11        r43hc72bb7e_2         conda-forge
  r-munsell                          0.5.1         r43hc72bb7e_1         conda-forge
  r-mvtnorm                          1.3_3         r43h9ad1c49_0         conda-forge
  r-nlme                             3.1_168       r43hb67ce94_0         conda-forge
  r-nnet                             7.3_20        r43h2b5f3a1_0         conda-forge
  r-numderiv                         2016.8_1.1    r43hc72bb7e_6         conda-forge
  r-openssl                          2.3.3         r43he8289e2_0         conda-forge
  r-parallelly                       1.45.1        r43h54b55ab_0         conda-forge
  r-pbdzmq                           0.3_14        r43h549f438_0         conda-forge
  r-pillar                           1.11.0        r43hc72bb7e_0         conda-forge
  r-pkgconfig                        2.0.3         r43hc72bb7e_4         conda-forge
  r-plyr                             1.8.9         r43h3697838_2         conda-forge
  r-prettyunits                      1.2.0         r43hc72bb7e_1         conda-forge
  r-proc                             1.19.0.1      r43h3697838_0         conda-forge
  r-processx                         3.8.6         r43h2b5f3a1_0         conda-forge
  r-prodlim                          2025.04.28    r43h93ab643_0         conda-forge
  r-progress                         1.2.3         r43hc72bb7e_1         conda-forge
  r-progressr                        0.15.1        r43hc72bb7e_0         conda-forge
  r-promises                         1.3.3         r43h3697838_0         conda-forge
  r-proxy                            0.4_27        r43hb1dbf0f_3         conda-forge
  r-pryr                             0.1.6         r43h0d4f4ea_2         conda-forge
  r-ps                               1.9.1         r43h2b5f3a1_0         conda-forge
  r-purrr                            1.1.0         r43h54b55ab_0         conda-forge
  r-quantmod                         0.4.28        r43hc72bb7e_0         conda-forge
  r-r6                               2.6.1         r43hc72bb7e_0         conda-forge
  r-ragg                             1.5.0         r43h9f1dc4d_0         conda-forge
  r-randomforest                     4.7_1.2       r43hb67ce94_0         conda-forge
  r-rappdirs                         0.3.3         r43hb1dbf0f_3         conda-forge
  r-rbokeh                           0.5.2         r43hc72bb7e_4         conda-forge
  r-rcolorbrewer                     1.1_3         r43h785f33e_3         conda-forge
  r-rcpp                             1.1.0         r43h93ab643_0         conda-forge
  r-rcpparmadillo                    15.0.2_1      r43h3704496_0         conda-forge
  r-rcppeigen                        0.3.4.0.2     r43hb79369c_0         conda-forge
  r-rcppnumerical                    0.6_0         r43h0d4f4ea_1         conda-forge
  r-rcurl                            1.98_1.17     r43hb79926e_0         conda-forge
  r-readr                            2.1.5         r43h0d4f4ea_1         conda-forge
  r-readxl                           1.4.5         r43h328fee5_0         conda-forge
  r-recipes                          1.3.1         r43hc72bb7e_0         conda-forge
  r-recommended                      4.3           r43hd8ed1ab_1007      conda-forge
  r-rematch                          2.0.0         r43hc72bb7e_1         conda-forge
  r-rematch2                         2.1.2         r43hc72bb7e_4         conda-forge
  r-repr                             1.1.7         r43h785f33e_1         conda-forge
  r-reprex                           2.1.1         r43hc72bb7e_1         conda-forge
  r-reshape2                         1.4.4         r43h3697838_5         conda-forge
  r-rlang                            1.1.6         r43h93ab643_0         conda-forge
  r-rmarkdown                        2.29          r43hc72bb7e_0         conda-forge
  r-rpart                            4.1.24        r43h2b5f3a1_0         conda-forge
  r-rstudioapi                       0.17.1        r43hc72bb7e_0         conda-forge
  r-rvest                            1.0.5         r43hc72bb7e_0         conda-forge
  r-sass                             0.4.10        r43h93ab643_0         conda-forge
  r-scales                           1.4.0         r43hc72bb7e_0         conda-forge
  r-selectr                          0.4_2         r43hc72bb7e_4         conda-forge
  r-shape                            1.4.6.1       r43ha770c72_1         conda-forge
  r-shiny                            1.11.1        r43h785f33e_0         conda-forge
  r-snow                             0.4_4         r43hc72bb7e_3         conda-forge
  r-sourcetools                      0.1.7_1       r43ha18555a_2         conda-forge
  r-sparsevctrs                      0.3.4         r43h2b5f3a1_0         conda-forge
  r-spatial                          7.3_18        r43h2b5f3a1_0         conda-forge
  r-squarem                          2021.1        r43hc72bb7e_3         conda-forge
  r-stringi                          1.8.7         r43h3c328a7_0         conda-forge
  r-stringr                          1.5.2         r43h785f33e_0         conda-forge
  r-survival                         3.8_3         r43h2b5f3a1_0         conda-forge
  r-sys                              3.4.3         r43h2b5f3a1_0         conda-forge
  r-systemfonts                      1.2.3         r43h74f4acd_0         conda-forge
  r-textshaping                      1.0.3         r43h74f4acd_0         conda-forge
  r-tibble                           3.3.0         r43h2b5f3a1_0         conda-forge
  r-tidyr                            1.3.1         r43h0d4f4ea_1         conda-forge
  r-tidyselect                       1.2.1         r43hc72bb7e_1         conda-forge
  r-tidyverse                        2.0.0         r43h785f33e_2         conda-forge
  r-timechange                       0.3.0         r43ha18555a_1         conda-forge
  r-timedate                         4041.110      r43hc72bb7e_0         conda-forge
  r-tinytex                          0.57          r43hc72bb7e_0         conda-forge
  r-triebeard                        0.4.1         r43h3697838_3         conda-forge
  r-truncnorm                        1.0_9         r43h2b5f3a1_4         conda-forge
  r-ttr                              0.24.4        r43hdb488b9_1         conda-forge
  r-tzdb                             0.5.0         r43h3697838_1         conda-forge
  r-urltools                         1.7.3.1       r43h3697838_0         conda-forge
  r-utf8                             1.2.6         r43h2b5f3a1_0         conda-forge
  r-uuid                             1.2_1         r43hdb488b9_0         conda-forge
  r-vctrs                            0.6.5         r43h0d4f4ea_1         conda-forge
  r-viridislite                      0.4.2         r43hc72bb7e_2         conda-forge
  r-vroom                            1.6.5         r43h0d4f4ea_1         conda-forge
  r-withr                            3.0.2         r43hc72bb7e_0         conda-forge
  r-xfun                             0.53          r43h3697838_0         conda-forge
  r-xml2                             1.4.0         r43hc6fd541_0         conda-forge
  r-xtable                           1.8_4         r43hc72bb7e_6         conda-forge
  r-xts                              0.14.1        r43h2b5f3a1_0         conda-forge
  r-yaml                             2.3.10        r43hdb488b9_0         conda-forge
  r-zoo                              1.8_14        r43h2b5f3a1_0         conda-forge
```

Bioconductor packages
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
```

## Containers

`singularity run bioinfo_example_latest.sif python hello.py` does not run the new file to print Hello World! This is because containers are designed to be isolated environments and do not know the paths to files outside of them unless the -B flag is used to mount those paths to the container.

This is the correct command to run the new file:
```
singularity run \
  -B /farmshare/user_data/rjuene/repos/BIOS270-AU25/Writeups/writeup2 \
  bioinfo_example_latest.sif \
  python /farmshare/user_data/rjuene/repos/BIOS270-AU25/Writeups/writeup2/hello.py
``` 
## v2
![GitLab](GitLab.png)
![test_reseek](test_reseek.png)


## Screenshot of the running code-server and JupyterLab
![code_server](code_server.png)
![jupyter](jupyter.png)
