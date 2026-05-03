process ADD_NETCHOP_SCORE {

    tag "$sample_id"

    publishDir "data/processed_with_netchop", mode: 'copy'

    input:
    tuple val(sample_id), path(peptides_csv), path(netchop_dirs)

    output:
    tuple val(sample_id), path("${sample_id}_peptides_with_netchop.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.add_netchop_scores \
        --input_file ${peptides_csv} \
        --netchop_dir "\$PWD" \
        --output_file ${sample_id}_peptides_with_netchop.csv
    """
}

process ADD_IC50 {

    tag "$sample_id"

    publishDir "data/processed_with_ic50", mode: 'copy'

    input:
    tuple val(sample_id), path(peptides_csv), path(netmhcpan_file)

    output:
    tuple val(sample_id), path("${sample_id}_peptides_with_ic50.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.add_ic50 \
        --input_file ${peptides_csv} \
        --netmhcpan_file ${netmhcpan_file} \
        --output_file ${sample_id}_peptides_with_ic50.csv
    """
}

process ADD_EXPRESSION {

    tag "$sample_id"

    publishDir "data/processed_with_expressions", mode: 'copy'

    input:
    tuple val(sample_id), path(peptides_csv), path(expression_file)

    output:
    tuple val(sample_id), path("${sample_id}_peptides_with_expressions.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.add_expression \
        --input_file ${peptides_csv} \
        --expression_file ${expression_file} \
        --output_file ${sample_id}_peptides_with_expressions.csv
    """
}

process ADD_PEPTIDE_SCORE {

    tag "$sample_id"

    publishDir "data/processed_with_peptide_score", mode: 'copy'

    input:
    tuple val(sample_id), path(peptides_csv)

    output:
    tuple val(sample_id), path("${sample_id}_peptides_with_peptide_score.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.add_peptide_score \
        --input_file ${peptides_csv} \
        --output_file ${sample_id}_peptides_with_peptide_score.csv
    """
}
