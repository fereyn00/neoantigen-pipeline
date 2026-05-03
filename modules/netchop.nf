process NETCHOP {

    tag "${sample}:${fasta.simpleName}"

    container 'netchop_image:latest'
    containerOptions '--platform=linux/amd64'

    input:
    tuple val(sample), path(fasta)

    output:
    tuple val(sample), path("${fasta.simpleName}/netchop.txt")

    publishDir "data/netchop_output/${sample}",
        mode: 'copy',
        overwrite: true,
        pattern: "**/*"

    script:
    """
    export TMPDIR=/tmp
    mkdir -p ${fasta.simpleName}
    netChop ${fasta} -t 0.5 -v 0 > ${fasta.simpleName}/netchop.txt
    """
}

process MAKE_FASTA {

    publishDir "data/netchop_input", mode: "copy"

    input:
    tuple val(sample_id), path(transcript_csv)

    output:
    tuple val(sample_id), path("${sample_id}/*_tumor.fasta")

    script:
    """
    export PYTHONPATH=${projectDir}/scr

    python3 ${projectDir}/scr/pipeline/fasta_from_transcripts.py \
        --input ${transcript_csv} \
        --output_dir ${sample_id}
    """
}
