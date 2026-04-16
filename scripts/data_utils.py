import pandas as pd
import requests

def get_protein_sequence(transcript_id):
    url = f"https://rest.ensembl.org/sequence/id/{transcript_id}?type=protein"
    headers = {'Content-Type': 'text/plain'}
    response = requests.get(url, headers=headers)
    if not response.ok:
        return None
    return response.text.strip()

def normalize_position(protein_position):
    if pd.isna(protein_position): return None
    part = str(protein_position).split('-')[0].split('/')[0]
    try:
        return int(float(part))
    except (ValueError, TypeError):
        return None

def collapse_mutations(muts):
    seen = {}
    for pos, aa, vaf in muts:
        if pos not in seen: seen[pos] = (aa, vaf)
    collapsed = sorted([(pos, aa, vaf) for pos, (aa, vaf) in seen.items()], key=lambda x: x[0])
    return collapsed
