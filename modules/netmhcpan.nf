process SPLIT_NETMHCPAN_BATCHES {

    tag "$sample_id"

    input:
    tuple val(sample_id), path(pep_file), path(hla_file)

    output:
    tuple val(sample_id), path("${sample_id}_netmhcpan_batches/*.txt")

    script:
    """
    PYTHONPATH=${projectDir}/scr python3 -m pipeline.netmhcpan_batch_cli \
        --peptide_file ${pep_file} \
        --hla_file ${hla_file} \
        --output_dir ${sample_id}_netmhcpan_batches \
        --chunk_size ${params.netmhcpan_chunk_size}
    """
}

process NETMHCPAN {

    tag "${sample_id}:${hla}:${chunk_id}"

    container 'netmhcpan_image:latest'
    containerOptions '--platform=linux/arm64/v8'

    input:
    tuple val(sample_id), val(hla), val(chunk_id), path(pep_file)

    output:
    tuple val(sample_id),
          path("*.out")

    script:
    """
    netMHCpan \
        -p ${pep_file} \
        -BA \
        -a "${hla}" \
        > ${pep_file.simpleName}.out
    """
}
