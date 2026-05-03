process BUILD_PEPTIDE_TXT {

    tag "$sample_id"

    input:
    tuple val(sample_id), path(peptides_csv)

    output:
    tuple val(sample_id), path("${sample_id}_peptides.txt")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.peptide_txt_cli \
        --input_file ${peptides_csv} \
        --output_file ${sample_id}_peptides.txt
    """
}
