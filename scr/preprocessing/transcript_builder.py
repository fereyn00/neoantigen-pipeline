import os

import pandas as pd
from preprocessing.api import get_protein_sequence
from preprocessing.utils import (
    apply_mutation_with_alignment,
    normalize_position,
    parse_protein_change,
)


def process_sample_mutations(sample_id, maf, output_dir="neoantigen_candid_from_paper"):
    results = []

    grouped = maf.groupby(["Gene", "Transcript_id"])

    for (gene, transcript_id), group in grouped:
        try:
            ref_seq = get_protein_sequence(transcript_id)

            for mut_type in [
                "Inframe_variant",
                "missense_variant",
                "protein_altering_variant",
            ]:
                tm = group[
                    group["Consequence"].str.contains(mut_type, case=False, na=False)
                ]

                for _, row in tm.iterrows():
                    if (
                        pd.isna(row["Protein_change"])
                        or "/" not in row["Protein_change"]
                    ):
                        continue

                    pos = normalize_position(row["Protein_position"])
                    if pos is None or pos < 1 or pos > len(ref_seq):
                        continue

                    ref_aa, alt_aa = row["Protein_change"].split("/", 1)
                    ref_aa, alt_seq = parse_protein_change(ref_aa, alt_aa)

                    ref_seq_aa = ref_seq[pos - 1 : pos - 1 + len(ref_aa)]
                    if ref_aa != "-" and ref_aa != ref_seq_aa:
                        continue

                    try:
                        tumor_seq, _ = apply_mutation_with_alignment(
                            ref_seq, pos, ref_aa, alt_seq
                        )

                        results.append(
                            {
                                "Sample": sample_id,
                                "Gene": gene,
                                "Transcript_ID": transcript_id,
                                "Protein_position": pos,
                                "Tumor_Mutated_Amino_Acids": row["Protein_change"],
                                "Tumor_Protein": tumor_seq,
                            }
                        )

                    except Exception as e:
                        print(f"Skipping {gene}:{transcript_id}:{pos} -> {e}")

        except Exception as e:
            print(f"Transcript error {sample_id}, {gene}, {transcript_id}: {e}")

    df_result = pd.DataFrame(results).drop_duplicates()

    output_path = f"{sample_id}_transcripts.csv"
    df_result.to_csv(output_path, index=False)

    return output_path
