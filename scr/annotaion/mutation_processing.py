import os
            germline_mutations = remove_duplicate_positions_keep_highest_AF(germline_mutations)
            tumor_mutations_df = remove_duplicate_positions_keep_highest_AF(tumor_group)

            def split_mutations(df):
                return {
                    "missense": df[df["Variant_Classification"] == "Missense_Mutation"],
                    "deletions": df[df["Variant_Classification"].str.contains("Del")],
                    "insertions": df[df["Variant_Classification"].str.contains("Ins")]
                }

            gm = split_mutations(germline_mutations)
            tm = split_mutations(tumor_mutations_df)

            germline_out = []
            tumor_out = []

            for mut_type in ["missense", "deletions", "insertions"]:
                for _, row in gm[mut_type].iterrows():
                    pos = normalize_position(row["Protein_position"])
                    if pos is None or pd.isna(row["Amino_acids"]) or '/' not in row["Amino_acids"]:
                        continue

                    ref_aa, alt_aa = row["Amino_acids"].split('/')
                    ref_seq_aa = ref_seq[pos - 1:pos - 1 + len(ref_aa)]

                    if ref_aa != '-' and ref_aa != ref_seq_aa:
                        continue

                    germline_out.append((pos, row["Amino_acids"], row["Tumor_VAF"]))

                    try:
                        aligned_germline_seq, _ = apply_mutation_with_alignment(
                            aligned_germline_seq, pos, ref_aa, alt_aa
                        )
                        aligned_tumor_seq = aligned_germline_seq
                    except ValueError:
                        continue

                for _, row in tm[mut_type].iterrows():
                    pos = normalize_position(row["Protein_position"])
                    if pos is None or pd.isna(row["Amino_acids"]) or '/' not in row["Amino_acids"]:
                        continue

                    ref_aa, alt_aa = row["Amino_acids"].split('/')
                    tumor_out.append((pos, row["Amino_acids"], row["Tumor_VAF"]))

                    try:
                        aligned_tumor_seq, _ = apply_mutation_with_alignment(
                            aligned_tumor_seq, pos, ref_aa, alt_aa
                        )
                        if mut_type == "insertions" and len(alt_aa) > len(ref_aa):
                            aligned_germline_seq = (
                                aligned_germline_seq[:pos - 1]
                                + '-' * (len(alt_aa) - len(ref_aa))
                                + aligned_germline_seq[pos - 1:]
                            )
                    except ValueError:
                        continue

            germline_collapsed = collapse_mutations(germline_out)
            tumor_collapsed = collapse_mutations(tumor_out)

            results.append({
                "Sample": sample_id,
                "Gene": gene,
                "Transcript_ID": transcript_id,
                "Germline_Mutated_Amino_Acids": ",".join(a for _, a, _ in germline_collapsed),
                "Germline_Positions": ",".join(str(p) for p, _, _ in germline_collapsed),
                "Germline_VAF": ",".join(str(v) for _, _, v in germline_collapsed),
                "Tumor_Mutated_Amino_Acids": ",".join(a for _, a, _ in tumor_collapsed),
                "Tumor_Positions": ",".join(str(p) for p, _, _ in tumor_collapsed),
                "Tumor_VAF": ",".join(str(v) for _, _, v in tumor_collapsed),
                "Germline_Protein": aligned_germline_seq,
                "Tumor_Protein": aligned_tumor_seq
            })

        except Exception as e:
            print(f"Ошибка для {sample_id}, {gene}, {transcript_id}: {e}")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{sample_id}_transcripts.csv")
    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"Result saved: {output_path}")
