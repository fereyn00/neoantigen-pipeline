import argparse
import os
import re
from pathlib import Path

import pandas as pd

from scoring.netchop import netchop_score_for_peptide, parse_netchop


def peptide_column(df):
    if "Tumor_Peptide" in df.columns:
        return "Tumor_Peptide"
    if "Peptide" in df.columns:
        return "Peptide"
    raise ValueError("Input CSV must contain Peptide or Tumor_Peptide")


def transcript_id(value):
    if pd.isna(value):
        return None
    return str(value).split(".")[0]


def netchop_index(netchop_dir):
    index = {}
    for root, _, files in os.walk(netchop_dir, followlinks=True):
        if "netchop.txt" not in files:
            continue
        path = Path(root) / "netchop.txt"
        match = re.search(r"(ENST\d+)", str(path.parent))
        if match:
            index[match.group(1)] = parse_netchop(path)
    return index


def add_netchop_scores(input_file, netchop_dir, output_file):
    df = pd.read_csv(input_file)
    pep_col = peptide_column(df)
    scores_by_transcript = netchop_index(netchop_dir)

    scores = []
    for _, row in df.iterrows():
        enst = transcript_id(row.get("Transcript_ID"))
        netchop_scores = scores_by_transcript.get(enst, {})
        peptide = str(row.get(pep_col, "")).replace("-", "")
        length = row.get("Peptide_Length", len(peptide))
        start = row.get("Tumor_start_position")
        scores.append(netchop_score_for_peptide(start, length, netchop_scores))

    if "NetChop_score" in df.columns:
        df = df.drop(columns=["NetChop_score"])
    df["NetChop_Tumor"] = scores
    df.to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--netchop_dir", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args()
    add_netchop_scores(args.input_file, args.netchop_dir, args.output_file)


if __name__ == "__main__":
    main()
