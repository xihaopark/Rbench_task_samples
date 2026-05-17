# GPT-5.1 Taskset254 Contract Defect Analysis

Date: 2026-05-17

Source reports:
- `analysis/gpt51_taskset254_audit/summary.md`
- `analysis/gpt51_taskset254_audit/group_1_audit.md` through `group_5_audit.md`

Scope: 50 deterministic audit samples from `/tmp/gpt51_clinical_taskset254_export/current_prompt/evaluation_results.jsonl`, focused on prompt, reference, evaluator, and data contract defects rather than general model quality.

## Executive Summary

The 50-sample audit shows that failures are dominated by task-contract defects, not by GPT-5.1 simply writing incorrect R code.

Primary root-cause counts:

| primary root cause | count | share | attribution |
|---|---:|---:|---|
| `prompt_wrong` | 27 | 54% | benchmark/prompt defect |
| `prompt_reference_mismatch` | 11 | 22% | benchmark/reference/evaluator defect |
| `data_or_fixture_issue` | 6 | 12% | benchmark/data defect |
| `llm_wrong` | 5 | 10% | true LLM error under mostly coherent contract |
| `unclear_needs_rerun` | 1 | 2% | unresolved |

Benchmark/prompt/data contract defects account for 44/50 samples (88%) when fixture issues are included. Prompt/reference contract defects alone account for 38/50 samples (76%). Only 5/50 samples were classified as clear LLM implementation failures against a mostly coherent prompt/reference/data contract.

## Defect Taxonomy

### 1. Wrong API Surface or Wrong Abstraction in Prompt

Primary count: 27/50.

The generated prompt often asks for a public package routine, a generic "equivalent data transformation", or a documentation-style API workflow while the reference solution uses a narrower benchmark-specific behavior. This is a prompt-generation defect because the model is steered away from the artifact that the grader compares.

Representative tasks:

| task | contract defect | benchmark defect vs LLM error |
|---|---|---|
| `pharmaverse/aNCA/get_conversion_factor` | Reference computes `units::set_units(...)`; current prompt targets public `aNCA::get_conversion_factor`. | Benchmark/prompt defect. |
| `pharmaverse/aNCA/g_pkcg03_log` | Reference requires `aNCA:::g_pkcg03_log(data)` and ggplot-shaped outputs; prompt asks for direct data transformation. | Benchmark/prompt defect. |
| `pharmaverse/aNCA/add_qmd_plot` | Reference calls an internal helper and returns a one-row artifact; prompt asks for generic transformation. | Benchmark/prompt defect. |
| `pharmaverse/admiral/get_imputation_target_date` | Reference uses `get(..., asNamespace("admiral"))`; prompt says to call the helper directly. | Benchmark/prompt defect. |
| `pharmaverse/aNCA/calculate_f` | Reference coerces to `PKNCAresults` and calls `pknca_calculate_f`; prompt asks for public `calculate_f`. | Benchmark/prompt defect. |
| `pharmaverse/admiral/derive_vars_atc` | Reference constructs missing fields and fixed quosures in-script; prompt drives behavior from helper TSVs. | Benchmark/prompt defect. |

Common pattern: internal helpers, fallback wrappers, scalar extraction, and reference-specific side effects are missing or contradicted in the current prompt.

### 2. Prompt, Reference, Metadata, and Evaluator Disagree

Primary count: 11/50.

These tasks have conflicting contracts across `task.json`, prompt text, `solution.R`, and evaluator expectations. A model may satisfy the natural prompt and still fail because the grader expects a different artifact or reference behavior.

Representative tasks:

| task | contract defect | benchmark defect vs LLM error |
|---|---|---|
| `pharmaverse/tidytlg/check_file` | Prompt describes TRUE/FALSE helper behavior; reference writes the input `arg` to `outputs/result.csv`. | Benchmark/reference defect. |
| `pharmaverse/tidytlg/check_req_arg` | Same helper/boolean mismatch; expected output is the input value. | Benchmark/reference defect. |
| `pharmaverse/aNCA/dose_profile_duplicates` | Reference prompt mentions `result.rds`, while expected/comparison artifacts include `summary.csv`. | Benchmark/evaluator contract defect. |
| `pharmaverse/admiral/get_imputation_targets` | Task metadata expects both CSV/RDS, but reference prompt names CSV and uses hidden fixed imputation settings. | Benchmark/reference/evaluator defect. |
| `pharmaverse/admiraldev/assert_same_type` | Reference calls `assert_same_type()` with no inputs and writes `summary.csv`; prompts expose an unrelated TSV. | Benchmark/reference defect. |
| `pharmaverse/admiral/dthcaus_source` | Reference creates an in-script dataset/list; prompt requires many control TSVs and a named input dataset. | Benchmark/reference defect. |

Common pattern: the benchmark contract exists only in `solution.R`, not in the prompt. Documentation-correct generated code fails against benchmark-specific reference artifacts.

### 3. Output Artifact Contract Not Preserved

Primary count: not exclusive; explicit in many prompt and LLM-error cases.

The grader usually checks fixed paths such as `outputs/result.csv`, `outputs/result.rds`, and sometimes `outputs/summary.csv`. Many current prompts say "save as appropriate" or imply natural helper-specific filenames. Generated solutions then write plausible but ungraded files.

Representative alternate filenames:

| task | generated or prompted wrong artifact | expected artifact problem |
|---|---|---|
| `pharmaverse/admiral/compute_age_years` | `outputs/age_years.csv`, `outputs/age_years.rds` | Missing exact `outputs/result.csv` schema. |
| `pharmaverse/tidytlg/replace_na_with_blank` | `outputs/x_clean.csv`, `outputs/x_clean.rds` | Coherent task, but wrong output path. |
| `pharmaverse/sdtm.oak/str_to_anycase` | `outputs/x_anycase_regexps.csv` | Coherent task, wrong output path. |
| `pharmaverse/admiral/extract_unit` | `outputs/x_unit.csv` | Coherent task, wrong output path. |
| `pharmaverse/admiraldev/get_source_vars` | `source_vars.rds` | Prompt omitted exact `result.csv`, `result.rds`, and `summary.csv` requirements. |
| `pharmaverse/admiraldev/squote` | `x_quoted.csv`, `x_quoted.rds` | Straightforward computation, wrong output path. |
| `pharmaverse/admiral/derive_var_trtdurd` | `datase_trt.csv`, RDS | Prompt exposed wrong signature and missed exact result artifact. |
| `pharmaverse/admiral/derive_vars_atc` | `datase_with_atc.csv` | Prompt used wrong parameter contract and missed exact artifact. |
| `pharmaverse/tidytlg/add_indent` | `df_indented.csv` | Fixture and prompt contract broken; wrong artifact compounds failure. |

This category cuts across root causes. In the true LLM-error bucket, wrong artifact names are the dominant failure mechanism for `replace_na_with_blank`, `str_to_anycase`, `extract_unit`, and `squote`.

### 4. Invalid, Stale, or Semantically Wrong Fixtures

Primary count: 6/50.

Some input fixtures do not match the target API's data contract, contain placeholder clinical column names, or contain values from an unrelated task. These should be treated as data contract defects or quarantined until repaired.

Representative tasks:

| task | fixture defect | benchmark defect vs LLM error |
|---|---|---|
| `pharmaverse/admiral/count_vals` | Scalar-counting task has inputs with headers like `by_vars` and `set_values_to`, steering models toward grouping metadata. | Data contract defect. |
| `pharmaverse/admiral/derive_param_rr` | `hr_code.tsv` contains multi-line R code instead of an HR `PARAMCD`. | Data contract defect. |
| `pharmaverse/gridify/gpar_args` | `gpar.tsv` contains `AVAL`, `AVISITN`, `USUBJID`, not a `grid::gpar` object/argument set. | Data contract defect. |
| `pharmaverse/logrx/parse_log` | `nested_log.tsv` contains bare clinical placeholders rather than a nested log object. | Data contract defect. |
| `pharmaverse/admiraldev/assert_unit` | Unit fixtures contain clinical placeholders and parameter-like values, not usable unit specs. | Data contract defect. |
| `pharmaverse/tidytlg/add_indent` | `df.tsv` contains expression metadata, not TLG rows with `row_type`/`label`. | Data contract defect. |

Common pattern: placeholders such as `AVAL`, `AVISITN`, `USUBJID`, and `set_values_to` appear where the function requires typed domain objects, unit expressions, or output table schemas.

### 5. True LLM Implementation Errors Under Coherent Contracts

Primary count: 5/50.

These are the clearest model errors because prompt, reference, and data are mostly aligned. Even here, most failures are mundane contract-following failures rather than complex clinical reasoning failures.

Representative tasks:

| task | LLM error |
|---|---|
| `pharmaverse/tidytlg/replace_na_with_blank` | Writes helper-specific `x_clean` artifacts instead of required `outputs/result.csv`. |
| `pharmaverse/sdtm.oak/str_to_anycase` | Current solution writes alternate filename; simple solution computes wrong case conversion output. |
| `pharmaverse/admiral/extract_unit` | Writes `x_unit.csv` instead of the required result artifact. |
| `pharmaverse/admiraldev/squote` | Computes a straightforward quoting task but uses wrong artifact names. |
| `pharmaverse/ggsurvfit/scale_ggsurvfit` | Builds an example survival plot or wrong summary shape instead of the one-row reference result. |

Interpretation: these are valid model-quality failures, but they represent a small minority of the audited failures.

### 6. Unresolved Runner or Timeout Ambiguity

Primary count: 1/50.

`pharmaverse/admiral/convert_predose_patterns` timed out in both current and simple runs without enough stderr or comparison detail to distinguish model code, fixture contract, or runner behavior. This sample should be rerun with timeout diagnostics and captured generated code before assigning blame.

## Benchmark Defect vs True LLM Error

Recommended reporting split:

| bucket | samples | interpretation |
|---|---:|---|
| Benchmark/prompt/reference/data defect | 44 | Should not be counted as clean evidence of GPT-5.1 inability without task repair or contract-aware rescoring. |
| True LLM error | 5 | Fair to count as model implementation failures under current evidence. |
| Needs rerun | 1 | Exclude or mark unresolved until diagnostics are available. |

For benchmark-quality reporting, the 44 defect samples should be split further into:
- prompt-generation defects: 27
- reference/evaluator contract mismatches: 11
- fixture/data defects: 6

For model-quality reporting, use the 5 true LLM-error samples as the primary numerator, and separately report artifact-path sensitivity because 4 of those 5 involve missing or wrong fixed output paths.

## Recommended Task-Contract Preflight Checks

Run these checks before scoring model outputs or publishing pass rates.

1. Artifact path consistency
   - Parse `task.json expected.artifacts`.
   - Parse evaluator comparison targets.
   - Scan `solution.R` for `outputs/...` writes.
   - Require exact agreement on `result.csv`, `result.rds`, `summary.csv`, and any side-effect files.
   - Fail preflight if the prompt says only "save as appropriate" while the evaluator requires fixed filenames.

2. Prompt/reference behavior preservation
   - Compare current prompt against original `task.json` `instruct_prompt`.
   - Flag dropped mentions of `:::`, `get(..., asNamespace(...))`, `do.call`, fixed scalar extraction, fallback/no-op behavior, and explicitly named helper calls.
   - Flag prompts that replace a reference helper call with "equivalent data transformation directly".

3. Exported vs internal API validation
   - Detect package calls in `solution.R`.
   - Verify whether each call is exported.
   - If a reference uses non-exported helpers, require the prompt to say so explicitly and show the namespace access pattern.
   - If the prompt asks for a public routine that does not match the reference helper, fail preflight.

4. Output schema validation
   - Run `solution.R` in a controlled environment and record artifact names, row counts, column names, and classes.
   - Compare that manifest to `task.json` and evaluator expectations.
   - Require prompts to include exact required output paths and enough schema detail for fixed benchmark artifacts.

5. Fixture semantic validation
   - Check input headers and first values against the function contract.
   - Flag generic placeholders (`AVAL`, `AVISITN`, `USUBJID`, `set_values_to`) when the target API expects typed objects, units, dates, parameter codes, expressions, or nested objects.
   - Flag multi-line R code inside scalar domain-code fixtures unless the task explicitly asks for expression parsing.

6. Reference fallback/no-op detection
   - Detect references that ignore input TSVs, construct synthetic in-script data, overwrite computed results, or catch errors and return the input.
   - Require the prompt to describe this benchmark-specific behavior, or quarantine the task as not measuring the public API described by docs.

7. Roxygen/docstring contamination check
   - Flag prompts with copied roxygen fragments, unused argument lists, or signatures inconsistent with the input files.
   - Require a single executable contract: inputs, transformation, output artifacts, and any permitted package/internal calls.

8. Timeout diagnostics
   - For `TIMEOUT` cases, capture generated code, stderr, package loading logs, and last executed output write.
   - Rerun timeout-only samples before classifying them as model, prompt, data, or runner failures.

## Repair Priorities

1. Regenerate prompts from the original task instruction plus exact expected artifacts rather than from package documentation.
2. Quarantine the 6 fixture-defective tasks until inputs are semantically repaired.
3. Repair or remove tasks where reference behavior is a benchmark wrapper/no-op but the prompt asks for public API behavior.
4. Make fixed output paths non-negotiable in every prompt.
5. Report benchmark-defect and true-model-error rates separately for this taskset.

