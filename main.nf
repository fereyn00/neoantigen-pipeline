#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { BUILD_TRANSCRIPTS } from './modules/build_transcripts.nf'
include { GENERATE_PEPTIDES } from './modules/build_peptides.nf'
include { BUILD_PEPTIDE_TXT } from './modules/build_peptides_txt.nf'
include { MAKE_FASTA; NETCHOP } from './modules/netchop.nf'
include { NETMHCPAN } from './modules/netmhcpan.nf'
include { ENSURE_DOCKER_IMAGES } from './modules/docker_images.nf'


workflow {

    docker_images_ready = ENSURE_DOCKER_IMAGES()

    maf_files = Channel.fromPath("data/mafs/*.csv")
        .map { file -> tuple(file.baseName, file) }

    maf_files.view { println "MAF input: $it" }


    transcripts = maf_files | BUILD_TRANSCRIPTS


    peptides = transcripts | GENERATE_PEPTIDES


    peptides_txt = peptides | BUILD_PEPTIDE_TXT


    fasta_ch = (transcripts | MAKE_FASTA)
        .flatMap { sample_id, fasta_files ->
            def files = fasta_files instanceof Collection ? fasta_files : [fasta_files]
            files.collect { fasta -> tuple(sample_id, fasta) }
        }


    netchop_out = fasta_ch
        .combine(docker_images_ready)
        .map { sample_id, fasta, ready -> tuple(sample_id, fasta) }
        | NETCHOP


    netmhcpan_out = peptides_txt
        .combine(docker_images_ready)
        .map { sample_id, pep, ready ->
            def hla = file("data/netmhcpan_input/${sample_id}_hla.txt")
            tuple(sample_id, pep, hla)
        }
        | NETMHCPAN
}
