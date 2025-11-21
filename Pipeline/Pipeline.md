# Pipeline

> *"I’ll just run these steps manually this one time..." — last words before three weeks of debugging filenames.*


Today, we’ll learn how to build and manage pipelines using **SLURM** and **Nextflow**

---

## Resource

🔗 [Nextflow](https://training.nextflow.io/latest/hello_nextflow/)

---

## SLURM Pipeline

How could one add a differential expression analysis (DESeq2) step to the `rnaseq_pipeline_array_depend.sh` script such that DESeq2 runs only after all `salmon` jobs for all samples have completed?
*(No code required - describe conceptually)*

---

## Nextflow Pipeline

In the current `rnaseq_nf` pipeline, we assume that the **transcriptome index** has already been created via `salmon index`.  However, this may not always be the case.

Add a `SALMON_INDEX` process that:

- Takes a reference transcriptome FASTA file as input (specify `transcriptome` in `params.yaml` file with `/farmshare/home/classes/bios/270/data/ecoli_ref/GCF_000401755.1_Escherichia_coli_ATCC_25922_cds_from_genomic.fna`)
- Outputs a Salmon index directory, used as input for the downstream `SALMON` process

Command for indexing a reference transcriptome:

```bash
salmon index -t <transcriptome.fa> -i <output_index_dir>
```

Modify your pipeline such that:

1. If the user provides `index` in `params.yaml`, use `index` directly as input for `SALMON` process, skip `SALMON_INDEX`.  
2. If `index` is **not provided**, but `transcriptome` is, run `SALMON_INDEX` to build index and used the output index directory as input to `SALMON`.  
3. If **neither** parameter is provided, exit with an informative error message.
