import argparse
import re
from pathlib import Path


def read_hlas(hla_file):
    hlas = []
    with open(hla_file) as handle:
        for line in handle:
            for value in re.split(r"[,;\s]+", line.strip()):
                hla = value.replace("*", "").strip()
                if not hla:
                    continue
                if not hla.startswith("HLA-"):
                    hla = f"HLA-{hla}"
                hlas.append(hla)
    return list(dict.fromkeys(hlas))


def read_peptides(peptide_file):
    peptides = []
    with open(peptide_file) as handle:
        for line in handle:
            peptide = line.strip()
            if peptide:
                peptides.append(peptide)
    return list(dict.fromkeys(peptides))


def write_batches(peptide_file, hla_file, output_dir, chunk_size):
    chunk_size = int(chunk_size)
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    peptides = read_peptides(peptide_file)
    hlas = read_hlas(hla_file)
    if not peptides:
        raise ValueError(f"No peptides found in {peptide_file}")
    if not hlas:
        raise ValueError(f"No HLA alleles found in {hla_file}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    chunk_count = (len(peptides) + chunk_size - 1) // chunk_size
    width = max(5, len(str(chunk_count)))

    for hla in hlas:
        for index, start in enumerate(range(0, len(peptides), chunk_size), start=1):
            batch = peptides[start : start + chunk_size]
            batch_path = output_path / f"{hla}__chunk_{index:0{width}d}.txt"
            with open(batch_path, "w") as handle:
                for peptide in batch:
                    handle.write(f"{peptide}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--peptide_file", required=True)
    parser.add_argument("--hla_file", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--chunk_size", type=int, required=True)

    args = parser.parse_args()
    write_batches(
        peptide_file=args.peptide_file,
        hla_file=args.hla_file,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
    )


if __name__ == "__main__":
    main()
