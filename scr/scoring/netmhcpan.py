import re
import pandas as pd


def parse_netmhcpan_output(text):
    lines = text.strip().split("\\n")
    rows = []
    headers_found = False

    for line in lines:
        if line.startswith("#") or not line.strip():
            continue

        if "------" in line:
            headers_found = True
            continue

        if headers_found and re.match(r"\\s*\\d+\\s+", line):
            parts = re.split(r"\\s+", line.strip())

            if len(parts) < 17:
                parts += [None] * (17 - len(parts))
            elif len(parts) > 17:
                parts = parts[:16] + [" ".join(parts[16:])]

            rows.append(parts)

    columns = [
        "Pos", "MHC", "Peptide", "Core", "Of", "Gp", "Gl",
        "Ip", "Il", "Icore", "Identity", "Score_EL", "Rank_EL",
        "Score_BA", "Rank_BA", "Aff_nM", "BindLevel"
    ]

    return pd.DataFrame(rows, columns=columns)
