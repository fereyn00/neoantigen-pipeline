# Neoantigen Discovery Pipeline

This pipeline processes somatic and germline mutations to identify and rank neoantigen candidates based on MHC binding affinity, proteasomal cleavage, and gene expression.

## Workflow
1. **Sequence Generation**: Fetch wild-type sequences from Ensembl and apply mutations.
2. **Peptide Extraction**: Generate all possible 8-14mer peptides overlapping mutation sites.
3. **Tool Integration**: Integrates results from `NetChop` (cleavage) and `NetMHCpan` (binding).
4. **Scoring**: Ranks candidates using a hyperbolic tangent weighted scoring system.

## Run
```bash
python -m src.pipeline.run_pipeline
