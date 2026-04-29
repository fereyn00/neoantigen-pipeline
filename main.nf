#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { NETMHCPAN } from './modules/netmhcpan.nf'

workflow {

    peptides = Channel.fromPath("data/netmhcpan_input/*_peptides.txt")

    peptides
        .map { pep ->
            def id = pep.baseName.replace("_peptides","")
            def hla = file("data/netmhcpan_input/${id}_hla.txt")
            tuple(id, pep, hla)
        }
        | NETMHCPAN
}
