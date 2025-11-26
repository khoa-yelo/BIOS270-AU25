# Write-up 4:

**Name:** Riley Juenemann       
**Student ID:** rjuene    
**Date:** 11/20/2025    

---

## 1. SLURM Pipeline

Similar to how the `salmon` job submission in `rnaseq_pipeline_array_depend.sh` 
depends on Trim Galore, we could add another step to the script for `DESeq2` 
job submission that depends on the `salmon` jobs using the flag 
`--dependency=afterok:$SALMON_QUANT` in the `sbatch`. This ensures that the `DESeq2` 
jobs will only be submitted after all the `salmon` jobs have completed.

## 2. Nextflow Pipeline

I believe the following would work, but I am having trouble running the original
`rnaseq.nf` pipeline.

```
process SALMON_INDEX {
    tag "salmon_index"
    
    input:
      path transcriptome
    
    output:
      path "salmon_index"
    
    publishDir "${params.outdir}/salmon_index_outs", mode: 'copy', overwrite: true
    
    script:
      """
      salmon index -t ${transcriptome} -i salmon_index
      """
}
```

```
// RNA-seq QC → Trim Galore → Salmon + DESeq2 (from CSV samplesheet)
// Expect a CSV with columns: sample,read1,read2,condition
// No intermediate samples.csv is generated; DESeq2 infers quant.sf paths
// from --outdir/<sample>/salmon_outs/quant.sf
nextflow.enable.dsl=2

include { FASTQC } from './modules/qc/fastqc.nf'
include { TRIMGALORE } from './modules/qc/trimgalore.nf'
include { SALMON } from './modules/pseudoalign/salmon.nf'
include { SALMON_INDEX } from './modules/pseudoalign/salmon_index.nf'
include { DESEQ2 } from './modules/diffexp/deseq2.nf'

// -------------------- Channels --------------------
def samplesheet_ch = Channel
  .fromPath(params.samplesheet)
  .ifEmpty { error "Missing --samplesheet file: ${params.samplesheet}" }

samples_ch = samplesheet_ch.splitCsv(header:true).map { row ->
    tuple(row.sample.trim(), file(row.read1.trim(), absolute: true), file(row.read2.trim(), absolute:true), row.condition.trim())
}


// -------------------- Workflow --------------------

workflow {
    
    FASTQC(samples_ch)
    trimmed_ch = TRIMGALORE(samples_ch)
    
    if( params.index ) {
        quant_ch   = SALMON(trimmed_ch, params.index)
    }
    else if( params.transcriptome ) {
        salmon_index_ch = SALMON_INDEX(file(params.transcriptome))
        quant_ch   = SALMON(trimmed_ch, salmon_index_ch)
    }
    else {
        error "Either index or transcriptome parameters must be provided for SALMON."
    }
    
    if( params.run_deseq ) {
        // Collect all Salmon outputs into a map {sample: quant_path}

        quant_paths_ch = quant_ch
            .map { sample, quant, cond -> "${sample},${quant}" }
            .collectFile(
                name: "quant_paths.csv", 
                newLine: true, 
                seed: "sample,quant_path"  // This adds the header as the first line
            )
        DESEQ2(quant_paths_ch, samplesheet_ch)
    }
}
workflow.onComplete {
    log.info "Pipeline finished. Results in: ${params.outdir}"
}
```


