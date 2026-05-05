process ADD_FINAL_SCORE {

    tag "$sample_id"

    publishDir "output", mode: 'copy'

    input:
    tuple val(sample_id), path(peptides_csv), path(netchop_dirs), path(netmhcpan_files), path(mhcflurry_file), path(mixmhcpred_file), path(expression_file)

    output:
    tuple val(sample_id), path("${sample_id}_neoantigen_candidates.csv")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.add_final_scores \
        --input_file ${peptides_csv} \
        --netchop_dir "\$PWD" \
        --netmhcpan_files ${netmhcpan_files} \
        --mhcflurry_file ${mhcflurry_file} \
        --mixmhcpred_file ${mixmhcpred_file} \
        --expression_file ${expression_file} \
        --output_file ${sample_id}_neoantigen_candidates.csv
    """
}
