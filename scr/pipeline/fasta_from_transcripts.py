import argparse
import os

import pandas as pd
from preprocessing.utils import write_fasta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.input, sep=",", engine="python", on_bad_lines="skip")
    df.columns = df.columns.str.strip()

    sample_id = (
        os.path.basename(args.input).replace("_transcripts.csv", "").replace(".txt", "")
    )

    patient_dir = args.output_dir
    os.makedirs(patient_dir, exist_ok=True)

    seen = set()

    for _, row in df.iterrows():
        gene = row.get("Gene")
        enst = row.get("Transcript_ID")
        protein = row.get("Tumor_Protein")

        if pd.isna(gene) or pd.isna(enst) or pd.isna(protein):
            continue

        protein = str(protein).replace("-", "").strip()
        if not protein:
            continue

        key = (gene, enst)
        if key in seen:
            continue
        seen.add(key)

        header = f">{sample_id}|{gene}|{enst}|TUMOR"

        out_file = os.path.join(patient_dir, f"{gene}_{enst}_tumor.fasta")

        write_fasta(out_file, [(header, protein)])


if __name__ == "__main__":
    main()
