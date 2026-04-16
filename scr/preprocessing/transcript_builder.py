def generate_mutant_transcript(protein_seq, position, ref_aa, alt_aa, flank=15):
    """
    Build WT and mutant peptide windows around mutation site.

    Parameters
    ----------
    protein_seq : str
        Full protein sequence.
    position : int
        1-based amino acid position.
    ref_aa : str
        Reference amino acid.
    alt_aa : str
        Mutant amino acid.
    flank : int
        Number of residues on each side.
    """
    idx = position - 1

    left = max(0, idx - flank)
    right = min(len(protein_seq), idx + flank + 1)

    wt_seq = protein_seq[left:right]

    mut_full = list(protein_seq)
    mut_full[idx] = alt_aa
    mut_seq = "".join(mut_full[left:right])

    return wt_seq, mut_seq


def generate_sliding_peptides(sequence, lengths=(8, 9, 10, 11)):
    peptides = []

    for k in lengths:
        for i in range(len(sequence) - k + 1):
            peptides.append({
                "start": i + 1,
                "length": k,
                "peptide": sequence[i:i+k]
            })

    return peptides
