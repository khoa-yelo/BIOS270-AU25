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