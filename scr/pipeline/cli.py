import argparse

import pandas as pd
from preprocessing.transcript_builder import process_sample_mutations


def main():
    parser = argparse.ArgumentParser(description="Neoantigen mutation processor")

    parser.add_argument("--sample_id", required=True)
    parser.add_argument("--maf", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    maf = pd.read_csv(args.maf)

    if maf.empty:
        raise ValueError(f"MAF file is empty: {args.maf}")

    output_path = process_sample_mutations(args.sample_id, maf, args.output)

    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()
