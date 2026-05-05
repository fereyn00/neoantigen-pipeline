process BUILD_MHCFLURRY_INPUT {

    tag "$sample_id"

    input:
    tuple val(sample_id), path(peptides_csv)

    output:
    tuple val(sample_id), path("${sample_id}_mhcflurry_input.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.mhcflurry_input_cli \
        --input_file ${peptides_csv} \
        --output_file ${sample_id}_mhcflurry_input.csv
    """
}

process MHCFLURRY {

    tag "$sample_id"

    container 'mhcflurry_image:latest'
    containerOptions '--platform=linux/amd64'

    input:
    tuple val(sample_id), path(mhcflurry_input_csv)

    output:
    tuple val(sample_id), path("${sample_id}_mhcflurry.csv")

    script:
    """
    mhcflurry-predict \
        ${mhcflurry_input_csv} \
        --no-flanking \
        --no-throw \
        --prediction-column-prefix mhcflurry_ \
        --out ${sample_id}_mhcflurry.csv
    """
}
