# Project 2: Machine Learning

---

## Project Proposal

### 1. Project Overview
 
Breastmilk represents the most ancient and important food, providing nutrients, antibodies, microbiota, immune cells, and other bioactive molecules critical for healthy human development. As a result, the World Health Organization (WHO) recommends exclusive breastfeeding for the first six months of life. Despite the univerally recognized benefits of breastfeeding, breastfeeding mothers do not produce milk with the same composition. Recent studies have demonstrated that immune cells are transferred to offspring through breastfeeding, and these transferred immune cells shape the development of the offspring's immune system and affect disease susceptibility. However, it remains unknown what factors determine breastmilk immune cell composition and what are the functions of these immune cells in breastmilk production and offspring health. Building upon recent work on the entero-mammary axis, we will **identify how maternal gut microbiota and environmental factors affect breastmilk immune cell composition and breast-fed offspring health.** Completion of this work will reveal novel intervention strategies for enhancing offspring health by optimizing the composition of breastmilk immune cells received by offspring.

**Aim 1: Define how maternal gut microbiota shapes breastmilk immune cell composition.**
*Expected outcomes*: We will establish the first paired dataset of maternal gut microbiota and breastmilk immune cell composition. We will identify how differences in gut microbiota abundance correlate with differences in breastmilk immune cell composition (e.g., proportion and phenotype of breastmilk immune cells). The study will include mothers on antibiotics so that we know we will detect perturbations in gut microbiota.
*Potential challenges*: Given that milk and stool samples will not all be available for processing at the same time, we will correct for any batch effects in the flow cytometry and 16S sequencing datasets, as mentioned below in the **Data suitability** section. We will also cryopreserve breastmilk immune cells in case we want to perform sequencing to follow-up on our findings.
  
**Aim 2: Determine how maternal nutrition and clinical history correlate with gut microbiota and breastmilk immune cell composition**
*Expected outcomes*: We will identify how maternal diet, antibiotics status, vaccination status, infection/disease status, and other clinical history parameters correlate with breastmilk immune cell composition. We anticipate that vaccination status and infection/disease status will alter the breastmilk immune cell composition compared with the baseline.
*Potential challenges*: There are a lot of confounding variables and population heterogeneity that will make it difficult to identify true signals. I will include these cofounders as covariates in my analysis. I will also use dimensionality reduction to reduce the number of features being tested to the ones that contribute the most to variations. 
  
**Aim 3: Identify breastmilk immune cell composition correlates of breast-fed offspring health.**
*Expected outcomes*: We will identify how breastmilk immune cell composition correlates with longitudinal offspring's clinical history, including their infection/disease status.
*Potential challenges*: Similar to Aim 2.
  

### 2. Data

**Dataset description**
This data will be generated in the lab in collaboration with the Human Milk Research Biorepository. We will plan to enroll 75 breastfeeding mothers and collect fresh milk and stool samples, as well as obtain mothers' and offspring' clinical history records (.csv data files). With the fresh milk samples, we will perform high-dimensional flow cytometry with 30+ markers (.fcs/.csv data files). With the stool samples, we will perform 16S sequencing (.fastq data files). 

**Data suitability**
For the flow cytometry dataset, I will read the .fcs files into R and create an SQL file. For the 16S sequencing dataset, I will need to process the data for downstream analysis. First, I will run FastQC to perform quality check. Second, I will remove 16S primers using Cutadapt and perform quality filtering and trimming using DADA2. Afterwards, I will group similar sequences together using Amplicon Sequence Variant (ASV) inference and merge paired reads, which will enable me to remove artificial hybrid sequences. Each unique sequence will then be compared against a reference database, such as SILVA, for taxonomy assignment, and my output will be a feature table with identified taxa and their abundance in the samples. In addition, I will check for batch effects by visualizing the flow cytometry and 16S sequencing datasets by sample collection time point to determine if batch correction would be necessary to account for any batch effects introduced by sample processing on different days.

**Storage and data management**
All data will be stored on a secure HPC storage system and backed up on an external hard drive. To share the data will collaborators, I can use rclone to share across cloud storages.

### 3. Environment

**Coding environment**
I will be analyzing the data on an HPC and submit slurm jobs in the terminal.

**Dependencies**
*Clinical history data*
R: tidyverse, ggplot2, ggpubr, MaAsLin2, randomforest

*Flow cytometry data*
R: FlowSOM, CytoNorm, uwot
Tools: FlowJo

*16S sequencing data*
R: dada2, phyloseq, microbiome, vegan, ALDEx2, ComplexHeatmap
Tools: FastQC, cutadapt

**Reproducibility**
I will git commit my work to keep a record of what I do and maintain an up-to-date README.md that will be a centralized and concise record of my work. I will make changes to my environment using an environment.yml file that can be shared with collaborators. I will also upload my container with all the necessary packages/libraries/tools installed with the same versions I will use in my work.


### 4. Pipeline

1. From my 16S sequencing data processing output, I will filter low-prevalence taxa (e.g., present in less than 10% of samples). I will aggregate taxa to genus or family level to reduce sparsity.
2. For the flow cytometry data, I will perform unsupervised clustering of breastmilk immune cells based on the features measured. 
3. I will create a merged dataset with clinical covariates.
4. I will perform multivariate testing and adjust for confounders.
5. Data visualization with heatmaps, scatterplots for top correlates, PCA and UMAP plots, box plots, etc.

**Scalability and efficiency**  
I will use Nextflow for 16S sequencing data processing. I will also use parallelization with arrayed tasks whenever I can in Slurm jobs.


### 5. Machine Learning

**Task definition**
Can maternal gut microbiota predict breastmilk immune cell composition? (Supervised)

**Feature representation**  
I will convert the 16S data into transformed abundances at genus level. I will convert the flow cytometry data into proportions of immune cell subsets with different activation profiles/phenotypes.

**Model selection**  
I will use random forest because it provides feature importance and is robust to outliers, which can be present with a small sample size.

**Generalization strategy** (for supervised learning)  
I will perform leave-one-out-cross-validation to check that the model is not driven by any outliers.

**Evaluation metrics**  
I will use AUROC and AUPRC because my data may be imbalanced given the small sample size.
