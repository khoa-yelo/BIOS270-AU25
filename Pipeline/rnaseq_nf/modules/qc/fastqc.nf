
process FASTQC {
   
    tag "$sample"
    publishDir "${params.outdir}/${sample}/fastqc_outs", mode: 'copy', overwrite: true
   
    input:
      tuple val(sample), path(read1), path(read2), val(condition)
   
    output:
      path "*.html"
      path "*.zip"
  
    script:
      """
      fastqc -o . "$read1" "$read2"
      """
}
