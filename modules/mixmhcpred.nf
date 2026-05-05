process BUILD_MIXMHCPRED_ALLELES {

    tag "$sample_id"

    input:
    tuple val(sample_id), path(hla_file)

    output:
    tuple val(sample_id), path("${sample_id}_mixmhcpred_alleles.txt")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.mixmhcpred_alleles_cli \
        --hla_file ${hla_file} \
        > ${sample_id}_mixmhcpred_alleles.txt
    """
}

process MIXMHCPRED {

    tag "$sample_id"

    container 'mixmhcpred_image:latest'
    containerOptions '--platform=linux/amd64'

    input:
    tuple val(sample_id), path(pep_file), path(allele_file)

    output:
    tuple val(sample_id), path("${sample_id}_mixmhcpred.txt")

    script:
    """
    alleles=\$(cat ${allele_file})

    MixMHCpred \
        -i ${pep_file} \
        -o ${sample_id}_mixmhcpred.txt \
        -a "\${alleles}"
    """
}
