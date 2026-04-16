import pandas as pd


def normalize_position(protein_position):
    if pd.isna(protein_position):
        return None

    if isinstance(protein_position, str):
        if "-" in protein_position:
            part = protein_position.split("-")[0]
        elif "/" in protein_position:
            part = protein_position.split("/")[0]
        else:
            part = protein_position
    else:
        part = str(protein_position)

    try:
        return int(float(part))
    except ValueError:
        return None

def remove_duplicate_positions_keep_highest_AF(df):
    if "gnomADg_AF" not in df.columns:
        return df.drop_duplicates(
            subset=["Protein_position"], keep="first"
        )

    return (
        df.sort_values(by="gnomADg_AF", ascending=False)
          .drop_duplicates(subset=["Protein_position"], keep="first")
          .sort_values(by="Protein_position")
    )
