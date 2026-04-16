import numpy as np


def compute_peptide_score_df(df):
    df["MHCBindingScore"] = np.tanh(500.0 - df["IC50"])
    df["ProteasomalCleavageScore"] = np.tanh(
        df["NetChop_Tumor"]
    )

    df["CombineScore"] = (
        0.8 * df["MHCBindingScore"]
        + 0.2 * df["ProteasomalCleavageScore"]
    )

    df["PeptideScore"] = (
        df["CombineScore"] * df["ExpressionScore"]
    )

    return df.sort_values(
        by="PeptideScore", ascending=False
    )
