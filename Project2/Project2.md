# Project 2: Machine Learning

In this project, you will write a proposal for your bioinformatics/ML project

> *“Wow, my model has 97% accuracy!” - a happy moment just before realizing the test set had unintentionally leaked into the training data.*

---

## Project Proposal

Your proposal should include the following sections.

### 1. Project Overview

- **Overarching goal**  
  Clearly state the primary objective of the project.

- **Rationale**  
  Explain why the project is important or interesting.  
  What problem does it address, and why is it worth solving?

- **Specific aims** (at least two)  
  For each aim, provide:
  - A clear **aim statement**  
  - **Expected outcomes** - what you hope to demonstrate or achieve  
  - **Potential challenges** and how you plan to address them  


### 2. Data

Describe the dataset you will work with and how you plan to manage it.

- **Dataset description**
  - **Source** (e.g., public repository, lab-generated, simulated, etc.)
  - **Size** (number of samples, features, storage)
  - **Format** (CSV, FASTQ, images, JSON, Parquet, etc.)

- **Data suitability**
  - Is the current format optimal for downstream processing?
  - What transformations or preprocessing steps will be necessary?

- **Storage and data management**
  - Where will you store the dataset?
  - How will you back it up?
  - How will you share it with collaborators if needed?


### 3. Environment

Document how your computational environment will be set up.

- **Coding environment**
  - Local machine? HPC? Jupyter notebook? code-server?

- **Dependencies**
  - Key packages, libraries, or tools required for your analysis.

- **Reproducibility**
  - How will you ensure others can rerun your analysis?
    - Version control  
    - Requirements file / environment.yml  
    - Containerization  


### 4. Pipeline

Describe the sequence of steps your analysis will follow.

- **Algorithms and methods**  
  What models, algorithms, or computational steps do you plan to run? Are there steps that depends on output of other steps?

- **Scalability and efficiency**  
  How will you ensure your pipeline runs efficiently on your dataset size, format, number of samples?


### 5. Machine Learning

Brainstorm an ML task that can be performed on your data

- **Task definition**  
  What is the supervised or unsupervised learning problem that appropriate for your data?

- **Feature representation**  
  How will you convert raw data into numerical form suitable for modeling?

- **Model selection**  
  Which model(s) will you apply and why?

- **Generalization strategy** (for supervised learning)  
  How will you ensure your model performs well on unseen data?

- **Evaluation metrics**  
  What metrics will you track? Why are they appropriate for your task?
