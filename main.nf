#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { BUILD_TRANSCRIPTS } from './modules/build_transcripts.nf'
include { GENERATE_PEPTIDES } from './modules/build_peptides.nf'
include { BUILD_PEPTIDE_TXT } from './modules/build_peptides_txt.nf'
include { MAKE_FASTA; NETCHOP } from './modules/netchop.nf'
include { SPLIT_NETMHCPAN_BATCHES; NETMHCPAN } from './modules/netmhcpan.nf'
include { ENSURE_DOCKER_IMAGES } from './modules/docker_images.nf'
include { ADD_FINAL_SCORE } from './modules/add_scores.nf'


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


    netmhcpan_batches = peptides_txt
        .map { sample_id, pep ->
            def hla = file("data/netmhcpan_input/${sample_id}_hla.txt")
            tuple(sample_id, pep, hla)
        }
        | SPLIT_NETMHCPAN_BATCHES

    netmhcpan_batch_files = netmhcpan_batches
        .flatMap { sample_id, batch_files ->
            def files = batch_files instanceof Collection ? batch_files : [batch_files]
            files.collect { batch_file ->
                def match = batch_file.name =~ /^(HLA-[^_]+)__chunk_(\d+)\.txt$/
                if (!match) {
                    throw new IllegalArgumentException("Unexpected NetMHCpan batch file: ${batch_file.name}")
                }
                tuple(sample_id, match[0][1], match[0][2], batch_file)
            }
        }

    netmhcpan_out = netmhcpan_batch_files
        .combine(docker_images_ready)
        .map { sample_id, hla, chunk_id, pep, ready ->
            tuple(sample_id, hla, chunk_id, pep)
        }
        | NETMHCPAN

    final_scores = peptides
        .join(netchop_out.groupTuple())
        .join(netmhcpan_out.groupTuple())
        .map { sample_id, peptides_csv, netchop_dirs, netmhcpan_files ->
            def expression_file = file("data/expressions/${sample_id}_kallisto_expressions.csv")
            tuple(sample_id, peptides_csv, netchop_dirs, netmhcpan_files, expression_file)
        }
        | ADD_FINAL_SCORE
}
