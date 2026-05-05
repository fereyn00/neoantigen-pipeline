import argparse

import pandas as pd

from scoring.hla import hla_to_mhcflurry, normalize_peptide


def peptide_column(df):
    if "Tumor_Peptide" in df.columns:
        return "Tumor_Peptide"
    if "Peptide" in df.columns:
        return "Peptide"
    raise ValueError("Input CSV must contain Peptide or Tumor_Peptide")


def write_mhcflurry_input(input_file, output_file):
    df = pd.read_csv(input_file)
    pep_col = peptide_column(df)

    if "HLA" not in df.columns:
        raise ValueError("Input CSV must contain HLA")

    output = pd.DataFrame({
        "allele": df["HLA"].map(hla_to_mhcflurry),
        "peptide": df[pep_col].map(normalize_peptide),
    })
    output = output[(output["allele"] != "") & (output["peptide"] != "")]
    output = output.drop_duplicates()
    output.to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()
    write_mhcflurry_input(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
