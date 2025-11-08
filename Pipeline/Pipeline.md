# Code

Today, we’ll learn how to build pipeline with Slurm and Nextflow

>*"I’ll just run these steps manually this one time..." - last words before three weeks of debugging filenames.*

## Resource 

[nextflow](https://training.nextflow.io/latest/hello_nextflow/)


## Slurm pipeline

How could one add a differential expression analysis step in  `rnaseq_pipeline_array_depend.sh` such that the step is executed after all `salmon` runs completed? (explain conceptually, no code is needed for this question)

## Nextflow

In the current `rnaseq_nf` pipeline, we assume transcriptome index was created with `salmon`. This may not be the case in practice.

For this exercise, add a `SALMON_INDEX` process input path to a reference transcriptome and output index folder, which subsequently used as input for `SALMON` process 

To index reference transcriptome with salmon

```bash
# add
```

Write your pipeline such that when `index` is provided, use that, if not, use `transcriptome` param, if both is not provided, return error msg