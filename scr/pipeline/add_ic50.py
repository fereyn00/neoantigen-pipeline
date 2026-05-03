import argparse

import pandas as pd

from scoring.netmhcpan import parse_netmhcpan_output


def peptide_column(df):
    if "Tumor_Peptide" in df.columns:
        return "Tumor_Peptide"
    if "Peptide" in df.columns:
        return "Peptide"
    raise ValueError("Input CSV must contain Peptide or Tumor_Peptide")


def normalize_hla(value):
    return str(value).replace("*", "").replace(":", "")


def normalize_peptide(value):
    return str(value).replace("-", "")


def add_ic50(input_file, netmhcpan_file, output_file):
    df = pd.read_csv(input_file)
    pep_col = peptide_column(df)

    with open(netmhcpan_file) as f:
        df_netmhc = parse_netmhcpan_output(f.read())

    if df_netmhc.empty:
        df["IC50"] = pd.NA
        df.to_csv(output_file, index=False)
        return

    df = df.copy()
    df_netmhc = df_netmhc.copy()

    df["_merge_hla"] = df["HLA"].map(normalize_hla)
    df["_merge_peptide"] = df[pep_col].map(normalize_peptide)
    df_netmhc["_merge_hla"] = df_netmhc["MHC"].map(normalize_hla)
    df_netmhc["_merge_peptide"] = df_netmhc["Peptide"].map(normalize_peptide)
    df_netmhc = df_netmhc.drop_duplicates(["_merge_hla", "_merge_peptide"])

    merged = pd.merge(
        df,
        df_netmhc[["_merge_hla", "_merge_peptide", "Affinity(nM)"]],
        on=["_merge_hla", "_merge_peptide"],
        how="left",
    )

    merged = merged.rename(columns={"Affinity(nM)": "IC50"})
    merged = merged.drop(columns=["_merge_hla", "_merge_peptide"])
    merged.to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--netmhcpan_file", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args()
    add_ic50(args.input_file, args.netmhcpan_file, args.output_file)


if __name__ == "__main__":
    main()
