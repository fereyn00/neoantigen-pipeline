#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { MAKE_FASTA } from './modules/netchop.nf'

workflow {

    Channel
        .fromPath('/Users/user390/Documents/GitHub/neoantigen-pipeline/data/processed/*_transcripts.csv')
        .map { file ->
            tuple(file.baseName.replace('_transcripts',''), file)
        }
        .view()
        | MAKE_FASTA
}
