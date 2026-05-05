import os
import sys
import tempfile
import unittest

import pandas as pd

sys.path.insert(0, os.path.abspath("scr"))

from pipeline.add_final_scores import add_mhcflurry_scores, add_mixmhcpred_scores
from scoring.hla import (
    hla_to_mhcflurry,
    hla_to_mixmhcpred,
    normalize_hla,
    normalize_peptide,
)
from scoring.mhcflurry import parse_mhcflurry_output
from scoring.mixmhcpred import parse_mixmhcpred_output
from scoring.peptide_score import add_peptide_score


class PredictorMergeTests(unittest.TestCase):
    def test_hla_and_peptide_normalization(self):
        self.assertEqual(normalize_hla("HLA-A*01:01"), "A0101")
        self.assertEqual(normalize_hla("HLA-A01:01"), "A0101")
        self.assertEqual(normalize_hla("A0101"), "A0101")
        self.assertEqual(hla_to_mhcflurry("HLA-B08:01"), "HLA-B*08:01")
        self.assertEqual(hla_to_mixmhcpred("HLA-B08:01"), "B0801")
        self.assertEqual(normalize_peptide("AA-C "), "AAC")

    def test_mhcflurry_parser_and_join(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as handle:
            handle.write(
                "allele,peptide,mhcflurry_affinity,"
                "mhcflurry_affinity_percentile,"
                "mhcflurry_processing_score,"
                "mhcflurry_presentation_score,"
                "mhcflurry_presentation_percentile\n"
            )
            handle.write("HLA-A*01:01,PEPTIDE,12.3,0.4,0.1,0.8,0.2\n")
            path = handle.name

        try:
            parsed = parse_mhcflurry_output(path)
            self.assertEqual(parsed.loc[0, "MHCflurry_Affinity"], 12.3)

            df = pd.DataFrame({
                "HLA": ["HLA-A01:01", "HLA-B08:01"],
                "Peptide": ["PEPTIDE", "PEPTIDE"],
            })
            merged = add_mhcflurry_scores(df, path)
            self.assertEqual(merged.loc[0, "MHCflurry_PresentationScore"], 0.8)
            self.assertTrue(pd.isna(merged.loc[1, "MHCflurry_Affinity"]))
        finally:
            os.unlink(path)

    def test_mixmhcpred_parser_and_join(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as handle:
            handle.write(
                "Peptide\tBestAllele\t%Rank_bestAllele\tScore_bestAllele\t"
                "%Rank_A0101\tScore_A0101\t%Rank_B0801\tScore_B0801\n"
            )
            handle.write("PEPTIDE\tA0101\t0.5\t0.9\t0.5\t0.9\t8.0\t0.1\n")
            path = handle.name

        try:
            parsed = parse_mixmhcpred_output(path)
            self.assertEqual(set(parsed["HLA"]), {"A0101", "B0801"})

            df = pd.DataFrame({
                "HLA": ["HLA-A01:01", "HLA-B08:01"],
                "Peptide": ["PEPTIDE", "PEPTIDE"],
            })
            merged = add_mixmhcpred_scores(df, path)
            self.assertEqual(merged.loc[0, "MixMHCpred_PercentileRank"], 0.5)
            self.assertEqual(merged.loc[1, "MixMHCpred_Score"], 0.1)
        finally:
            os.unlink(path)

    def test_peptide_score_does_not_filter_high_ic50(self):
        df = pd.DataFrame({
            "IC50": [50.0, 5000.0],
            "NetChop_Tumor": [0.5, 0.5],
            "ExpressionScore": [1.0, 1.0],
        })

        scored = add_peptide_score(df)
        self.assertEqual(len(scored), 2)
        self.assertTrue((scored["IC50"] == 5000.0).any())


if __name__ == "__main__":
    unittest.main()
