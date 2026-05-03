def parse_netchop_line(parts):
    if not parts:
        return None

    try:
        return int(parts[0]), float(parts[3])
    except (IndexError, ValueError):
        pass

    try:
        return int(parts[1]), float(parts[4])
    except (IndexError, ValueError):
        return None


def parse_netchop(netchop_file):
    scores = {}

    with open(netchop_file) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#") or line.startswith("-"):
                continue

            parts = line.split()
            parsed = parse_netchop_line(parts)
            if parsed is None:
                continue

            pos, score = parsed
            scores[pos] = score

    return scores


def netchop_score_for_peptide(start, length, netchop_dict):
    try:
        start = int(start)
        length = int(length)
    except (TypeError, ValueError):
        return 0.0

    if start <= 0 or length <= 0:
        return 0.0

    n_term = start - 1
    c_term = start + length - 1

    return (
        netchop_dict.get(n_term, 0.0)
        * netchop_dict.get(c_term, 0.0)
    )
