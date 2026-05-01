import pandas as pd
from preprocessing.utils import generate_mutation_centered_peptides, parse_alt_sequence


def generate_peptide_file(input_csv, output_csv, min_len=8, max_len=14):

    df = pd.read_csv(input_csv)
    all_peptides = []

    for _, row in df.iterrows():
        alt_seq = parse_alt_sequence(row["Tumor_Mutated_Amino_Acids"])
        if not alt_seq:
            continue

        tumor_seq = str(row["Tumor_Protein"]).replace("-", "")
        pos = int(row["Protein_position"])

        for peptide_length in range(min_len, max_len + 1):
            peptides = generate_mutation_centered_peptides(
                tumor_seq=tumor_seq,
                mutation_position=pos,
                alt_sequence=alt_seq,
                peptide_length=peptide_length,
            )

            for pep in peptides:
                all_peptides.append(
                    {
                        "Sample": row["Sample"],
                        "Gene": row["Gene"],
                        "Transcript_ID": row["Transcript_ID"],
                        "Protein_position": pos,
                        "Mutation": row["Tumor_Mutated_Amino_Acids"],
                        "Peptide_Length": peptide_length,
                        "Peptide": pep,
                    }
                )

    pd.DataFrame(all_peptides).drop_duplicates().to_csv(output_csv, index=False)
    print(f"Saved peptides → {output_csv}")
