import numpy as np


def add_expression_score(df):
    nonzero = df.loc[df["gene_abundance"] > 0, "gene_abundance"]

    if len(nonzero) == 0:
        q1, q3 = 0, 0
    else:
        q1 = np.percentile(nonzero, 25)
        q3 = np.percentile(nonzero, 75)

    def expr_score(tpm):
        if tpm == 0:
            return 0
        elif tpm <= q1:
            return 0.33
        elif tpm <= q3:
            return 0.66
        return 1

    df["ExpressionScore"] = df["gene_abundance"].apply(expr_score)
    return df
