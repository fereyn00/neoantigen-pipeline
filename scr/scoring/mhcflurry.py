import pandas as pd


MHCFLURRY_COLUMNS = [
    "MHCflurry_Affinity",
    "MHCflurry_AffinityPercentile",
    "MHCflurry_ProcessingScore",
    "MHCflurry_PresentationScore",
    "MHCflurry_PresentationPercentile",
]

MHCFLURRY_COLUMN_MAP = {
    "mhcflurry_affinity": "MHCflurry_Affinity",
    "mhcflurry_affinity_percentile": "MHCflurry_AffinityPercentile",
    "mhcflurry_processing_score": "MHCflurry_ProcessingScore",
    "mhcflurry_presentation_score": "MHCflurry_PresentationScore",
    "mhcflurry_presentation_percentile": "MHCflurry_PresentationPercentile",
}


def _empty_mhcflurry_predictions():
    return pd.DataFrame(columns=["HLA", "Peptide", *MHCFLURRY_COLUMNS])


def _first_matching_column(df, candidates):
    for column in candidates:
        if column in df.columns:
            return column
    return None


def parse_mhcflurry_output(path):
    df = pd.read_csv(path)
    if df.empty:
        return _empty_mhcflurry_predictions()

    allele_col = _first_matching_column(df, ["allele", "HLA", "hla"])
    peptide_col = _first_matching_column(df, ["peptide", "Peptide"])
    if allele_col is None or peptide_col is None:
        raise ValueError("MHCflurry output must contain allele and peptide columns")

    parsed = pd.DataFrame({
        "HLA": df[allele_col],
        "Peptide": df[peptide_col],
    })

    for source, target in MHCFLURRY_COLUMN_MAP.items():
        if source in df.columns:
            parsed[target] = pd.to_numeric(df[source], errors="coerce")
        else:
            parsed[target] = pd.NA

    return parsed
