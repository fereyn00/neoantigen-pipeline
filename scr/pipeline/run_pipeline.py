import pandas as pd
from src.scoring.expression_score import add_expression_score
from src.scoring.peptide_score import compute_peptide_score_df


def process_file(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df = df[df["IC50"] < 500].copy()
    df = add_expression_score(df)
    df = compute_peptide_score_df(df)
    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    print("Pipeline ready")
