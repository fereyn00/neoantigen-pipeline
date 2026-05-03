process NETMHCPAN {

    tag "${sample_id}"

    container 'netmhcpan_image:latest'
    containerOptions '--platform=linux/arm64/v8'

    publishDir "data/netmhcpan_output", mode: 'copy'

    input:
    tuple val(sample_id), path(pep_file), path(hla_file)

    output:
    tuple val(sample_id),
          path("${sample_id}.out")

    script:
    """
    HLA=\$(tr ',;[:space:]' '\\n' < ${hla_file} | tr -d '*' | awk 'NF' | sed 's/^HLA-//' | sed 's/^/HLA-/' | paste -sd, -)

    echo "HLA = \$HLA"

    netMHCpan \
        -p ${pep_file} \
        -BA \
        -a "\$HLA" \
        > ${sample_id}.out
    """
}
