
def extract_peptide_aligned(seq, start_index, peptide_length=9):
    peptide = ""
    real_aa_count = 0
    extend_end = start_index

    while real_aa_count < peptide_length and extend_end < len(seq):
        char = seq[extend_end]

        if char == "-":
            return None

        peptide += char
        real_aa_count += 1
        extend_end += 1

    return peptide if len(peptide) == peptide_length else None


def find_position(sequence, peptide):
    idx = sequence.find(peptide)
    return idx + 1 if idx != -1 else None
