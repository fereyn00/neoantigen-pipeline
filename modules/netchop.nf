process NETCHOP {

    container 'netchop_image:latest'
    containerOptions '--platform linux/amd64'

    input:
    tuple val(sample), path(fasta)

    output:
    tuple val(sample), path("netchop.txt")

    script:
    """
    export TMPDIR=/tmp
    /opt/netchop-3.1/bin/netChop ${fasta} -t 0.5 -v 0 > netchop.txt
    """
}

process MAKE_FASTA {

    input:
    tuple val(sample_id), path(transcript_csv)

    output:
    tuple val(sample_id), path("${sample_id}_tumor.fasta")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 ${projectDir}/scr/pipeline/fasta_from_transcripts.py \
        --input ${transcript_csv} \
        --output_dir .
    """
}
