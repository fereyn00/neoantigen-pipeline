process NETCHOP {

    tag "$enst"
    container 'netchop_image:latest'

    input:
    tuple val(sample), val(type), val(enst), path(fasta)

    output:
    path "netchop.txt"

    publishDir {
        "data/netchop_output/${sample}/${type}/${enst}"
    }, mode: 'copy', overwrite: true

    script:
    """
    export TMPDIR=/tmp

    netChop ${fasta} -t 0.5 -v 0 > netchop.txt
    """
}
