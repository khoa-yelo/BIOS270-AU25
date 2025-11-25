// RNA-seq QC → Trim Galore → Salmon + DESeq2 (from CSV samplesheet)
// Expect a CSV with columns: sample,read1,read2,condition
// No intermediate samples.csv is generated; DESeq2 infers quant.sf paths
// from --outdir/<sample>/salmon_outs/quant.sf
nextflow.enable.dsl=2

include { FASTQC } from './modules/qc/fastqc.nf'
include { TRIMGALORE } from './modules/qc/trimgalore.nf'
include { SALMON_INDEX } from './modules/pseudoalign/salmon_index.nf'
include { SALMON } from './modules/pseudoalign/salmon.nf'
include { DESEQ2 } from './modules/diffexp/deseq2.nf'

// -------------------- Channels --------------------
def samplesheet_ch = Channel
  .fromPath(params.samplesheet)
  .ifEmpty { error "Missing --samplesheet file: ${params.samplesheet}" }

samples_ch = samplesheet_ch.splitCsv(header:true).map { row ->
    tuple(row.sample.trim(), file(row.read1.trim(), absolute: true), file(row.read2.trim(), absolute:true), row.condition.trim())
}

// ------------------ Index Logic -------------------
if (params.index) {
    log.info "Using provided Salmon index: ${params.index}"
    index_ch = Channel.value(file(params.index))
} else if (params.transcriptome) {
    log.info "Building Salmon index from transcriptome: ${params.transcriptome}"
    transcriptome_ch = Channel.value(file(params.transcriptome))
    index_ch = SALMON_INDEX(transcriptome_ch)
} else {
    error """
    ERROR: Must provide either 'index' or 'transcriptome' parameter in params.yaml

    Options:
    1. Provide pre-built index:
       index: '/path/to/existing/salmon_index'

    2. Provide transcriptome to build index:
       transcriptome: '/path/to/transcriptome.fasta'

    Example transcriptome path:
       transcriptome: '/farmshare/home/classes/bios/270/data/ecoli_ref/GCF_000401755.1_Escherichia_coli_ATCC_25922_cds_from_genomic.fna'
    """
}

// -------------------- Workflow --------------------

workflow {
    FASTQC(samples_ch)
    trimmed_ch = TRIMGALORE(samples_ch)
    quant_ch   = SALMON(trimmed_ch, params.index)

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