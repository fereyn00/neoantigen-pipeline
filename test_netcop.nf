nextflow.enable.dsl=2

include { NETCHOP } from './modules/netchop.nf'
include { MAKE_FASTA } from './modules/netchop.nf'
workflow {

    maf_ch = Channel
        .fromPath("data/processed/*_transcripts.csv")
        .map { file ->
            tuple(file.baseName.replaceFirst(/_transcripts$/, ''), file)
        }

    fasta_ch = MAKE_FASTA(maf_ch)
        .flatMap { sample_id, fasta_files ->
            def files = fasta_files instanceof Collection ? fasta_files : [fasta_files]
            files.collect { fasta -> tuple(sample_id, fasta) }
        }

    NETCHOP(fasta_ch)
}
