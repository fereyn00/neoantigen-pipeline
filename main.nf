#!/usr/bin/env nextflow
nextflow.enable.dsl=2

// -----------------------------
// Modules
// -----------------------------
include { BUILD_TRANSCRIPTS } from './modules/build_transcripts.nf'
include { GENERATE_PEPTIDES } from './modules/build_peptides.nf'
include { BUILD_PEPTIDE_TXT } from './modules/build_peptides_txt.nf'
include { MAKE_FASTA; NETCHOP } from './modules/netchop.nf'
include { NETMHCPAN } from './modules/netmhcpan.nf'


workflow {

    // -----------------------------
    // INPUT MAF
    // -----------------------------
    maf_files = Channel.fromPath("data/mafs/*.csv")
        .map { file -> tuple(file.baseName, file) }

    maf_files.view { println "MAF input: $it" }


    // -----------------------------
    // STEP 1: TRANSCRIPTS
    // -----------------------------
    transcripts = maf_files | BUILD_TRANSCRIPTS


    // -----------------------------
    // STEP 2: PEPTIDES
    // -----------------------------
    peptides = transcripts | GENERATE_PEPTIDES


    // -----------------------------
    // STEP 3: PEPTIDE TXT
    // -----------------------------
    peptides_txt = peptides | BUILD_PEPTIDE_TXT


    // -----------------------------
    // STEP 4: FASTA
    // -----------------------------
    fasta_ch = transcripts | MAKE_FASTA


    // -----------------------------
    // STEP 5: NETCHOP
    // -----------------------------
    netchop_out = fasta_ch | NETCHOP


    // -----------------------------
    // STEP 6: NETMHC
    // -----------------------------
    netmhcpan_out = peptides_txt
        .map { sample_id, pep ->
            def hla = file("data/netmhcpan_input/${sample_id}_hla.txt")
            tuple(sample_id, pep, hla)
        }
        | NETMHCPAN
}
