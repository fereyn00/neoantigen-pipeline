#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { MAKE_FASTA; NETCHOP } from './modules/netchop.nf'
include { NETMHCPAN } from './modules/netmhcpan.nf'

workflow {

    fasta_files = Channel.fromPath("data/netchop_input/*.fasta")

    transcripts = fasta_files.flatMap { file ->

        def results = []
        def sample = file.baseName
        def type = sample.contains("tumor") ? "tumor" : "germline"

        def enst = null
        def seq = ""

        file.withReader { r ->
            r.eachLine { line ->

                if (line.startsWith(">")) {

                    if (enst != null) {
                        results << tuple(sample, type, enst, seq)
                    }

                    def parts = line.split("\\|")
                    enst = parts[2]
                    seq = ""

                } else {
                    seq += line.trim()
                }
            }

            if (enst != null) {
                results << tuple(sample, type, enst, seq)
            }
        }

        results
    }

    fasta_ch = transcripts | MAKE_FASTA
    netchop_out = fasta_ch | NETCHOP


    peptides = Channel.fromPath("data/netmhcpan_input/*_peptides.txt")

    netmhcpan_out = peptides
        .map { pep ->
            def id = pep.baseName.replace("_peptides","")
            def hla = file("data/netmhcpan_input/${id}_hla.txt")
            tuple(id, pep, hla)
        }
        | NETMHCPAN
}
