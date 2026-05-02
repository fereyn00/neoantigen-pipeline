nextflow.enable.dsl=2

include { NETCHOP } from './modules/netchop.nf'
include { MAKE_FASTA } from './modules/netchop.nf'
workflow {

    maf_ch = Channel
        .fromPath("data/processed/*_transcripts.csv")
        .map { file ->
            tuple(file.baseName, file)
        }

    fasta_ch = MAKE_FASTA(maf_ch)

    NETCHOP(fasta_ch)
}
