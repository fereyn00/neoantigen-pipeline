import os
import pandas as pd
from bioreactor.cohort_data import *
from bioreactor.mutations import *


def remove_duplicate_positions_keep_highest_AF(df):
    if "gnomADg_AF" not in df.columns:
        return df.drop_duplicates(subset=["Protein_position"], keep="first")
    return (
        df.sort_values(by="gnomADg_AF", ascending=False)
          .drop_duplicates(subset=["Protein_position"], keep="first")
          .sort_values(by="Protein_position")
    )


def collapse_mutations(muts):
    """
    muts: list of (pos, amino_acids, vaf)
    keeps first mutation per position, sorts by position
    """
    seen = {}
    for pos, aa, vaf in muts:
        if pos not in seen:
            seen[pos] = (aa, vaf)
    collapsed = [(pos, aa, vaf) for pos, (aa, vaf) in seen.items()]
    collapsed.sort(key=lambda x: x[0])
    return collapsed


def process_sample_mutations(sample_id, dna_protein_affecting_mutations, output_dir="results"):

    cohort = dS3Cohort(
        bucket='patients-data',
        cohort_id='Early_Adopters',
        patients=[sample_id]
    )

    def filter_mutations(df):
        return df[
            (df["LDT_PASS"] == 'PASS') &
            (df["Variant_Classification"].isin(dna_protein_affecting_mutations)) &
            (df["Variant_Classification"].isin([
                'In_Frame_Ins',
                'In_Frame_Del',
                'Missense_Mutation'
            ]))
        ].copy()

    gmaf = filter_mutations(cohort.gmaf)
    maf = filter_mutations(cohort.maf)

    results = []
    grouped = maf.groupby(["Sample", "Hugo_Symbol", "Transcript_ID"])

    for (sample_id, gene, transcript_id), tumor_group in grouped:
        try:
            ref_seq = get_protein_sequence(transcript_id)
            aligned_germline_seq = ref_seq
            aligned_tumor_seq = ref_seq

            germline_mutations = gmaf[
                (gmaf["Sample"] == sample_id) &
                (gmaf["Hugo_Symbol"] == gene) &
                (gmaf["Transcript_ID"] == transcript_id)
            ]
            germline_mutations = remove_duplicate_positions_keep_highest_AF(germline_mutations)
            tumor_mutations_df = remove_duplicate_positions_keep_highest_AF(tumor_group)

            def split_mutations(df):
                return {
                    "missense": df[df["Variant_Classification"] == "Missense_Mutation"],
                    "deletions": df[df["Variant_Classification"].str.contains("Del")],
                    "insertions": df[df["Variant_Classification"].str.contains("Ins")]
                }

            gm = split_mutations(germline_mutations)
            tm = split_mutations(tumor_mutations_df)

            germline_out = []
            tumor_out = []

            for mut_type in ["missense", "deletions", "insertions"]:
    print(f"Result saved: {output_path}")
