
process TRIMGALORE {
    tag "$sample"
    publishDir "${params.outdir}/${sample}/trim_galore_outs", mode: 'copy', overwrite: true
   
    input:
      tuple val(sample), path(read1), path(read2), val(condition)
 
    output:
      tuple val(sample),
            path("${sample}_1_val_1.*"),
            path("${sample}_2_val_2.*"),
            val(condition)
 
    script:
      """
      trim_galore --quality 20 --length 20 --paired --output_dir ./ "$read1" "$read2"
      """
}