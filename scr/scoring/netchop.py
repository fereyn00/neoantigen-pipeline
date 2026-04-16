def parse_netchop(netchop_file):
    scores = {}

    with open(netchop_file) as f:
        for line in f:
            line = line.strip()

            if not line or not line.startswith("ENST"):
                continue

            parts = line.split()
            if len(parts) < 5:
                continue

            try:
                pos = int(parts[1])
                score = float(parts[4])
                scores[pos] = score
            except ValueError:
                continue

    return scores
  
def netchop_score_for_peptide(start, length, netchop_dict):
    n_term = start - 1
    c_term = start + length - 1

    return (
        netchop_dict.get(n_term, 0.0)
        * netchop_dict.get(c_term, 0.0)
    )
