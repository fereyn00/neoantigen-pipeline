#!/usr/bin/env nextflow
nextflow.enable.dsl=2


// =====================================================
// MODULES
// =====================================================
include { BUILD_TRANSCRIPTS } from './modules/build_transcripts.nf'
include { GENERATE_PEPTIDES } from './modules/build_peptides.nf'
include { BUILD_PEPTIDE_TXT } from './modules/build_peptide_txt.nf'

include { MAKE_FASTA; NETCHOP } from './modules/netchop.nf'
include { NETMHCPAN } from './modules/netmhcpan.nf'


workflow {

    // =====================================================
    // 🧬 INPUT MAF FILES
    // =====================================================
    maf_files = Channel.fromPath("data/mafs/*.csv")
        .map { f ->
            tuple(f.baseName, f)
        }

    transcripts = maf_files | BUILD_TRANSCRIPTS


    // =====================================================
    // 🧬 BRANCH 1: NETCHOP (FIXED)
    // =====================================================
    // transcripts MUST already contain:
    // sample, type, enst, sequence

    fasta_ch = transcripts | MAKE_FASTA
    netchop_out = fasta_ch | NETCHOP


    // =====================================================
    // 🧬 BRANCH 2: PEPTIDES
    // =====================================================
    peptides = transcripts | GENERATE_PEPTIDES
    peptide_txt = peptides | BUILD_PEPTIDE_TXT


    // =====================================================
    // 🧬 HLA FILES
    // =====================================================
    hla_files = Channel.fromPath("data/netmhcpan_input/*_hla.txt")
        .map { f ->
            tuple(f.baseName.replace("_hla",""), f)
        }


    // =====================================================
    // 🧬 PEPTIDE FILES
    // =====================================================
    peptide_ch = peptide_txt
        .map { pep ->
            def f = pep instanceof List ? pep[-1] : pep
            def id = f.baseName.replace("_peptides","")
            tuple(id, f)
        }


    // =====================================================
    // 🧬 JOIN PEPTIDES + HLA
    // =====================================================
    netmhcpan_in = peptide_ch.join(hla_files)


    // =====================================================
    // 🧬 NETMHCPAN
    // =====================================================
    netmhcpan_out = netmhcpan_in | NETMHCPAN
}
