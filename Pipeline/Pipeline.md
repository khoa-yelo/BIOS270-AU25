# Pipeline

> *"I’ll just run these steps manually this one time..." — last words before three weeks of debugging filenames.*


Today, we’ll learn how to build and manage pipelines using **SLURM** and **Nextflow**

---

## Resource

🔗 [Nextflow](https://training.nextflow.io/latest/hello_nextflow/)

---

## SLURM Pipeline

How could you add a differential expression analysis (DESeq2) step to the `rnaseq_pipeline_array_depend.sh` script so that it runs only after all `salmon` jobs have finished?
*(No code required - describe conceptually)*

---

## Nextflow Pipeline

In the current `rnaseq_nf` pipeline, we assume the **transcriptome index** has already been created with `salmon`.  However, in practice, this may not always be the case.

Add a `SALMON_INDEX` process that:

- Takes a reference transcriptome FASTA file as input (`transcriptome` in `params.yaml` file)
- Outputs a Salmon index directory, used as input for the downstream `SALMON` process

Command for indexing a reference transcriptome:

```bash
salmon index -t <transcriptome.fa> -i <index_dir>
```

Modify your pipeline so that:

1. If the user provides `--index`, use that directly.  
2. If `--index` is **not provided**, but `--transcriptome` is, automatically run `SALMON_INDEX` to build one.  
3. If **neither** parameter is provided, exit with an informative error message.