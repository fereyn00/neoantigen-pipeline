import pandas as pd


def generate_peptide_txt(input_csv, output_txt):
    df = pd.read_csv(input_csv)

    if "Peptide" not in df.columns:
        raise ValueError("Column 'Peptide' not found in input CSV")

    peptides = (
        df["Peptide"]
        .dropna()
        .astype(str)
        .str.strip()
        .drop_duplicates()
    )

    with open(output_txt, "w") as f:
        for pep in peptides:
            if pep:
                f.write(f"{pep}\n")

    print(f"Saved peptides to {output_txt}")
