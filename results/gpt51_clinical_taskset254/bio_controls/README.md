# Bio/Omics Control Cases

These pages add a small proteomics/omics control set beside the GPT-5.1 clinical taskset254 audit. The goal is not to replace the clinical audit, but to provide contrast: these bio tasks come from the same RBioBench release family and the same GPT-5.1 run style, while their prompts and expected artifacts are generally more direct.

Source run: `openai_gpt_5.1_proteomics_pass5_20260118_093231.jsonl`  
Archive root: `archive/legacy_public_runs/evaluation_outputs/openai_gpt-5.1_20260118_093231/`

Important limitation: the archived proteomics run preserved generated R code, stdout/stderr, comparison JSON, and LLM output files. It did not preserve the concrete dynamic input files or reference output files from each generated test case. For those, these pages show the exact task prompt, expected artifact contract, input factory registration, reference solution, comparison record, and archived LLM output snippets.

## Selected Controls

| control | task | sample shown | 5-sample result | why included |
|---|---|---:|---|---|
| [01](control_01_S102_log_transform_proteomics.md) | `transpror/S102_log_transform_proteomics` | 0 | PASS=5 | Clean PASS control: base-R transformation, exact output artifact, 5/5 samples passed. |
| [02](control_02_S103_normalize_proteomics.md) | `transpror/S103_normalize_proteomics` | 0 | PASS=5 | Clean PASS control with required Bioconductor-style package usage: limma quantile normalization, 5/5 samples passed. |
| [03](control_03_S105_impute_missing.md) | `transpror/S105_impute_missing` | 0 | PASS=5 | Clean PASS control with package call and deterministic expected artifact: impute::impute.knn, 5/5 samples passed. |
| [04](control_04_S101_prep_limma.md) | `transpror/S101_prep_limma` | 1 | FAIL=1, PASS=4 | Mixed control: 4/5 samples passed; the selected sample fails only one generated case, useful for seeing small exactness drift. |
| [05](control_05_S109_correlation_proteomics.md) | `transpror/S109_correlation_proteomics` | 3 | FAIL=1, PASS=4 | Mixed control: 4/5 samples passed; selected sample shows how extra QC logic can drop one protein and fail exact schema matching. |
| [06](control_06_S104_filter_proteins.md) | `transpror/S104_filter_proteins` | 0 | FAIL=5 | LLM-error control: prompt/reference contract is coherent, but every sample fails because the model invented an unavailable JSON config. |

## Full Proteomics Run Context

The control pages were selected from the full proteomics pass5 run: 14 tasks, 70 generated samples total.

| task | PASS | FAIL |
|---|---:|---:|
| `transpror/S101_prep_limma` | 4 | 1 |
| `transpror/S102_log_transform_proteomics` | 5 | 0 |
| `transpror/S103_normalize_proteomics` | 5 | 0 |
| `transpror/S104_filter_proteins` | 0 | 5 |
| `transpror/S105_impute_missing` | 5 | 0 |
| `transpror/S106_limma_analysis` | 0 | 5 |
| `transpror/S107_t_test_proteomics` | 0 | 5 |
| `transpror/S108_ANOVA_proteomics` | 0 | 5 |
| `transpror/S109_correlation_proteomics` | 4 | 1 |
| `transpror/S110_PCA_proteomics` | 0 | 5 |
| `transpror/S111_feature_selection` | 0 | 5 |
| `transpror/S113_cross_validation` | 0 | 5 |
| `transpror/S114_ROC_analysis` | 0 | 5 |
| `transpror/S115_biomarker_discovery` | 0 | 5 |

## Contrast With Clinical Taskset254

The clinical audit found that 44/50 sampled failures were benchmark-side prompt/reference/data issues. These proteomics controls show a different pattern: several tasks pass cleanly under the same model family, and the selected failures are mostly conventional model exactness errors, such as adding an extra input file or dropping a row during QC.

## Control-Set Takeaways

- Direct bio preprocessing tasks can pass at high rates when the prompt, reference solution, expected artifact, and evaluator agree.
- The failing bio controls are useful because they fail for interpretable LLM behavior, not because the prompt asks for a different function than the reference implements.
- This supports reporting clinical taskset254 separately from cleaner omics controls when discussing GPT-5.1 performance.

