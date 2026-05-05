import argparse
import re

from scoring.hla import hla_to_mixmhcpred


def read_hlas(hla_file):
    hlas = []
    with open(hla_file) as handle:
        for line in handle:
            for value in re.split(r"[,;\s]+", line.strip()):
                if not value:
                    continue
                hla = hla_to_mixmhcpred(value)
                if hla:
                    hlas.append(hla)
    return list(dict.fromkeys(hlas))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hla_file", required=True)
    args = parser.parse_args()

    hlas = read_hlas(args.hla_file)
    if not hlas:
        raise ValueError(f"No HLA alleles found in {args.hla_file}")
    print(",".join(hlas))


if __name__ == "__main__":
    main()
