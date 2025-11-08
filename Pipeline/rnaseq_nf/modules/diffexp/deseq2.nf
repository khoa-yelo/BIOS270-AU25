process DESEQ2 {
    tag 'DESeq2'
    publishDir "${params.outdir}/deseq2", mode: 'copy', overwrite: true

    input:
      path quant_csv  // quant_paths.csv
      path samplesheet

    output:
      path("results/*.csv")
      path("results/*.png")

    script:
      """
      deseq2.R --samplesheet ${samplesheet} --quant_paths ${quant_csv} --outdir results
      """
}
