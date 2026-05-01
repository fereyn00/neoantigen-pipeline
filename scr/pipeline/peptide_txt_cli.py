import argparse

from preprocessing.peptide_txt_generator import generate_peptide_txt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args()

    generate_peptide_txt(input_csv=args.input_file, output_txt=args.output_file)


if __name__ == "__main__":
    main()
