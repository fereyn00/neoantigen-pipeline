import numpy as np


def compute_peptide_score_df(df):
    df["MHCBindingScore"] = np.tanh((500.0 - df["IC50"]) / 200.0)
    df["ProteasomalCleavageScore"] = np.tanh(df["NetChop_Tumor"] * 3.0)
    df["CombineScore"] = (
        0.8 * df["MHCBindingScore"]
        + 0.2 * df["ProteasomalCleavageScore"]
    )
    df["PeptideScore"] = df["CombineScore"] * df["ExpressionScore"]
    return df


def add_peptide_score(df):
    if "NetChop_Tumor" not in df.columns and "NetChop_score" in df.columns:
        df = df.rename(columns={"NetChop_score": "NetChop_Tumor"})

    required_cols = {"IC50", "NetChop_Tumor", "ExpressionScore"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df[df["IC50"] < 500].copy()
    df = compute_peptide_score_df(df)
    return df.sort_values(by="PeptideScore", ascending=False)
