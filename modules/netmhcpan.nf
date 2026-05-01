process NETMHCPAN {

    tag "${sample_id}"

    container 'netmhcpan_image:latest'
    containerOptions '--platform linux/amd64'

    publishDir "data/netmhcpan_output", mode: 'copy'

    input:
    tuple val(sample_id), path(pep_file), path(hla_file)

    output:
    tuple val(sample_id),
          path("${sample_id}.out"),
          path("${sample_id}.xls")

    script:
    """
    HLA=\$(cat ${hla_file} | tr ',' '\\n' | sed 's/^HLA-//' | sed 's/^/HLA-/' | paste -sd, -)

    echo "HLA = \$HLA"

    netMHCpan \
        -p ${pep_file} \
        -BA \
        -a "\$HLA" \
        -xls \
        -xlsfile ${sample_id}.xls \
        > ${sample_id}.out
    """
}
