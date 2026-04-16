
def write_fasta(path, records):
    with open(path, "w") as f:
        for header, seq in records:
            f.write(header + "\\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i:i+60] + "\\n")
