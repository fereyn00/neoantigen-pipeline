import argparse

import pandas as pd

from scoring.expression_score import add_expression_score


def expression_lookup(expression_file):
    df = pd.read_csv(expression_file)
    if df.empty:
        return pd.DataFrame(columns=["Gene", "gene_abundance"])

    first_row = df.iloc[0]
    rows = []
    for gene, value in first_row.items():
        if str(gene).startswith("Unnamed:"):
            continue
        rows.append((gene, value))

    expr = pd.DataFrame(rows, columns=["Gene", "gene_abundance"])
    expr["gene_abundance"] = pd.to_numeric(expr["gene_abundance"], errors="coerce").fillna(0.0)
    return expr


def add_expression(input_file, expression_file, output_file):
    df = pd.read_csv(input_file)
    expr = expression_lookup(expression_file)

    if "gene_abundance" in df.columns:
        df = df.drop(columns=["gene_abundance"])
    if "ExpressionScore" in df.columns:
        df = df.drop(columns=["ExpressionScore"])

    merged = df.merge(expr, on="Gene", how="left")
    merged["gene_abundance"] = merged["gene_abundance"].fillna(0.0)
    merged = add_expression_score(merged)
    merged.to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--expression_file", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args()
    add_expression(args.input_file, args.expression_file, args.output_file)


if __name__ == "__main__":
    main()
