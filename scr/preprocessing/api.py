import requests


def get_protein_sequence(transcript_id: str) -> str:
    url = f"https://rest.ensembl.org/sequence/id/{transcript_id}?type=protein"
    headers = {"Content-Type": "text/plain"}

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise Exception(
            f"Ensembl request error: {response.status_code} - {response.text}"
        )

    return response.text.strip()
