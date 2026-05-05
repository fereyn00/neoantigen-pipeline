import re

import pandas as pd


MIXMHCPRED_COLUMNS = [
    "MixMHCpred_Score",
    "MixMHCpred_PercentileRank",
]


def _empty_mixmhcpred_predictions():
    return pd.DataFrame(columns=["HLA", "Peptide", *MIXMHCPRED_COLUMNS])


def _read_mixmhcpred_table(path):
    df = pd.read_csv(path, sep="\t", comment="#")
    if len(df.columns) == 1:
        df = pd.read_csv(path, sep=r"\s+", comment="#", engine="python")
    return df


def parse_mixmhcpred_output(path):
    df = _read_mixmhcpred_table(path)
    if df.empty:
        return _empty_mixmhcpred_predictions()

    peptide_col = "Peptide" if "Peptide" in df.columns else df.columns[0]
    alleles = set()

    for column in df.columns:
        match = re.fullmatch(r"(Score|%Rank)_(.+)", str(column))
        if not match:
            continue

        allele = match.group(2)
        if allele.lower() == "bestallele":
            continue
        alleles.add(allele)

    if not alleles:
        return _empty_mixmhcpred_predictions()

    frames = []
    for allele in sorted(alleles):
        score_col = f"Score_{allele}"
        rank_col = f"%Rank_{allele}"
        parsed = pd.DataFrame({
            "HLA": allele,
            "Peptide": df[peptide_col],
            "MixMHCpred_Score": pd.to_numeric(
                df[score_col], errors="coerce"
            ) if score_col in df.columns else pd.NA,
            "MixMHCpred_PercentileRank": pd.to_numeric(
                df[rank_col], errors="coerce"
            ) if rank_col in df.columns else pd.NA,
        })
        frames.append(parsed)

    return pd.concat(frames, ignore_index=True)
