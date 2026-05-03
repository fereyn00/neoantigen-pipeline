import argparse

import pandas as pd

from scoring.peptide_score import add_peptide_score


def process_file(input_file, output_file):
    df = pd.read_csv(input_file)
    df = add_peptide_score(df)
    df.to_csv(output_file, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args()
    process_file(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
