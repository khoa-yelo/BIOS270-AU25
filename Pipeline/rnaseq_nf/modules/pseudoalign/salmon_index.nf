process SALMON_INDEX {
    tag "salmon_index"
    publishDir "${params.outdir}/salmon_index", mode: 'copy'
    
    input:
    path transcriptome
    
    output:
    path "salmon_index", emit: index

    script:
    """
    salmon index \\
        -t ${transcriptome} \\
        -i salmon_index \\
        --threads ${task.cpus}
    """
}