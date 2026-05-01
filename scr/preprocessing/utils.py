import pandas as pd


def normalize_position(protein_position):
    if pd.isna(protein_position):
        return None

    if isinstance(protein_position, str):
        if "-" in protein_position:
            part = protein_position.split("-")[0]
        elif "/" in protein_position:
            part = protein_position.split("/")[0]
        else:
            part = protein_position
    else:
        part = str(protein_position)

    try:
        return int(float(part))
    except (ValueError, TypeError):
        return None


def apply_mutation_with_alignment(seq, pos, ref_aa, alt_aa):
    if ref_aa.startswith("-") and not alt_aa.startswith("-"):
        ref_aa = ""
        alt_aa = alt_aa.replace("-", "")
    elif alt_aa.startswith("-") and not ref_aa.startswith("-"):
        ref_aa = ref_aa.replace("-", "")
        alt_aa = ""

    idx = pos - 1
    ref_len = len(ref_aa)
    alt_len = len(alt_aa)

    left = seq[:idx]
    right = seq[idx + ref_len :]

    if alt_len == ref_len:
        mutated_seq = left + alt_aa + right
        aligned_original_seq = seq

    elif alt_len > ref_len:
        gap_count = alt_len - ref_len
        mutated_seq = left + alt_aa + right
        aligned_original_seq = left + ref_aa + ("-" * gap_count) + right

    else:
        gap_count = ref_len - alt_len
        mutated_seq = left + alt_aa + ("-" * gap_count) + right
        aligned_original_seq = seq

    if len(mutated_seq) != len(aligned_original_seq):
        raise AssertionError("Sequence length mismatch after mutation")

    return mutated_seq, aligned_original_seq


def parse_protein_change(ref_aa, alt_aa):
    """
    Minimal safe parser. Adjust if your format is more complex.
    """
    return ref_aa, alt_aa


def generate_mutation_centered_peptides(
    tumor_seq: str, mutation_position: int, alt_sequence: str, peptide_length: int
):
    peptides = []

    seq_len = len(tumor_seq)

    mut_start = mutation_position - 1
    mut_len = len(alt_sequence)
    mut_end = mut_start + mut_len - 1

    for window_start in range(mut_start - peptide_length + 1, mut_end + 1):
        window_end = window_start + peptide_length

        if window_start < 0 or window_end > seq_len:
            continue

        peptide = tumor_seq[window_start:window_end]

        if window_end > mut_start and window_start <= mut_end:
            peptides.append(peptide)

    return peptides


def parse_alt_sequence(protein_change: str):
    if pd.isna(protein_change):
        return None

    if "/" not in str(protein_change):
        return None

    ref, alt = str(protein_change).split("/", 1)

    if len(ref) == 0 or len(alt) == 0:
        return None

    return alt


def write_fasta(path, records):
    with open(path, "w") as f:
        for header, seq in records:
            f.write(header + "\\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i : i + 60] + "\\n")
