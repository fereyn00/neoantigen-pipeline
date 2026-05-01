import argparse
import os

import pandas as pd
from preprocessing.utils import write_fasta


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    output_folder = os.path.abspath(args.output_dir)
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(args.input)
    df = pd.read_csv(args.input)

    sample_id = filename.replace("_transcripts.csv", "")

    tumor_records = []
    seen_tumor = set()

    for _, row in df.iterrows():
        gene = row["Gene"]
        transcript = row["Transcript_ID"]

        tumor = row.get("Tumor_Protein")
        if isinstance(tumor, str):
            tumor = tumor.replace("-", "").strip()
            if tumor and tumor not in seen_tumor:
                header = f">{sample_id}|{gene}|{transcript}|TUMOR"
                tumor_records.append((header, tumor))
                seen_tumor.add(tumor)

    # всегда создаём файл (чтобы Nextflow не падал)
    out_file = os.path.join(output_folder, f"{sample_id}_tumor.fasta")

    if tumor_records:
        write_fasta(out_file, tumor_records)
    else:
        open(out_file, "w").close()


if __name__ == "__main__":
    main()
