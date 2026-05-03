import re

import pandas as pd
from preprocessing.utils import generate_mutation_centered_peptides, parse_alt_sequence


def read_hla_file(hla_file):
    hla_list = []
    with open(hla_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = re.split(r"[,\s;]+", line)
            for hla in parts:
                hla = hla.replace("*", "")
                if hla:
                    hla_list.append(hla)

    return list(dict.fromkeys(hla_list))


def generate_peptide_file(input_csv, output_csv, hla_file=None, min_len=8, max_len=14):

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
                include_positions=True,
            )

            for pep, tumor_start_position in peptides:
                all_peptides.append(
                    {
                        "Sample": row["Sample"],
                        "Gene": row["Gene"],
                        "Transcript_ID": row["Transcript_ID"],
                        "Protein_position": pos,
                        "Mutation": row["Tumor_Mutated_Amino_Acids"],
                        "Peptide_Length": peptide_length,
                        "Tumor_start_position": tumor_start_position,
                        "Peptide": pep,
                    }
                )

    peptides_df = pd.DataFrame(all_peptides)
    if not peptides_df.empty:
        dedupe_columns = [
            column
            for column in peptides_df.columns
            if column != "Tumor_start_position"
        ]
        peptides_df = peptides_df.drop_duplicates(subset=dedupe_columns)

        if hla_file:
            hla_list = read_hla_file(hla_file)
            if not hla_list:
                raise ValueError(f"No HLA alleles found in {hla_file}")

            hla_df = pd.DataFrame({"HLA": hla_list})
            peptides_df = peptides_df.merge(hla_df, how="cross")

    peptides_df.to_csv(output_csv, index=False)
    print(f"Saved peptides → {output_csv}")
