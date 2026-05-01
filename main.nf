#!/usr/bin/env nextflow
nextflow.enable.dsl=2


// -----------------------------
// Neoantigen transcript builder
// -----------------------------
include { BUILD_TRANSCRIPTS } from './modules/build_transcripts.nf'
include { GENERATE_PEPTIDES } from './modules/build_peptides.nf'


// -----------------------------
// Existing modules
// -----------------------------
include { MAKE_FASTA; NETCHOP } from './modules/netchop.nf'
include { NETMHCPAN } from './modules/netmhcpan.nf'


workflow {

    // =====================================================
    // 🧬 MAF INPUT
    // =====================================================
    maf_files = Channel.fromPath("data/mafs/*.csv")
        .map { file ->
            tuple(file.baseName, file)
        }

    maf_files.view { println "MAF input: $it" }


    // =====================================================
    // 🧬 STEP 1: TRANSCRIPTS
    // =====================================================
    transcripts = maf_files | BUILD_TRANSCRIPTS


    // =====================================================
    // 🧬 STEP 2: PEPTIDES (FIXED — YOU MISSED THIS)
    // =====================================================
    peptides = transcripts | GENERATE_PEPTIDES


    // =====================================================
    // 🧬 EXISTING PIPELINE
    // =====================================================

    fasta_files = Channel.fromPath("data/netchop_input/*.fasta")

    transcripts_fasta = fasta_files.flatMap { file ->

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

    fasta_ch = transcripts_fasta | MAKE_FASTA
    netchop_out = fasta_ch | NETCHOP


    peptides_input = Channel.fromPath("data/netmhcpan_input/*_peptides.txt")

    netmhcpan_out = peptides_input
        .map { pep ->
            def id = pep.baseName.replace("_peptides", "")
            def hla = file("data/netmhcpan_input/${id}_hla.txt")
            tuple(id, pep, hla)
        }
        | NETMHCPAN

}
