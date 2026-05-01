process BUILD_TRANSCRIPTS {

    publishDir "data/processed", mode: 'copy'

    input:
    tuple val(sample_id), path(maf_file)

    output:
    tuple val(sample_id), path("${sample_id}_transcripts.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.cli \
        --sample_id ${sample_id} \
        --maf ${maf_file} \
        --output ${sample_id}_transcripts.csv
    """
}
