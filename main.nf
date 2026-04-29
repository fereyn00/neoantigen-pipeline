#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { NETCHOP } from './modules/netchop.nf'
include { NETMHCPAN } from './modules/netmhcpan.nf'

THRESHOLD = 0.5

workflow {

    /*
     * =========================
     *  NETCHOP BRANCH
     * =========================
     */

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

        return results
    }

    fasta_ch = transcripts.map { sample, type, enst, seq ->
        def f = file("${sample}_${type}_${enst}.fasta")
        f.text = ">${enst}\n${seq}"
        tuple(sample, type, enst, f)
    }

    netchop_out = fasta_ch | NETCHOP


    /*
     * =========================
     *  NETMHCPAN BRANCH
     * =========================
     */

    peptides = Channel.fromPath("data/netmhcpan_input/*_peptides.txt")

    netmhcpan_out = peptides
        .map { pep ->
            def id = pep.baseName.replace("_peptides","")
            def hla = file("data/netmhcpan_input/${id}_hla.txt")
            tuple(id, pep, hla)
        }
        | NETMHCPAN


    /*
     * =========================
     *  OPTIONAL: join both streams (if needed later)
     * =========================
     */

}
