# GPT-5.1 Clinical Taskset254 50-Sample Audit Summary

Date: 2026-05-17

Sample: 50 tasks selected with deterministic seed `20260517` from `/tmp/gpt51_clinical_taskset254_export/current_prompt/evaluation_results.jsonl`.

## Headline

The failures are mostly not "LLM just wrote bad code". In this 50-task sample, the dominant failure mode is benchmark contract drift: the generated prompts often do not preserve the exact `task.json`/`solution.R` behavior, artifact names, internal helper calls, or benchmark-specific fallback logic.

## Root Cause Counts

| root cause | count | share |
|---|---:|---:|
| `prompt_wrong` | 27 | 54% |
| `prompt_reference_mismatch` | 11 | 22% |
| `data_or_fixture_issue` | 6 | 12% |
| `llm_wrong` | 5 | 10% |
| `unclear_needs_rerun` | 1 | 2% |

Combined prompt/contract issues: 38 / 50 = 76%.

## Main Patterns

1. Current prompts often ask for the wrong API surface.
   Many aNCA/admiral tasks require internal helpers or reference-specific workarounds, but the generated current prompt asks the model to call a public routine or perform a generic "equivalent data transformation". Examples: `aNCA/get_conversion_factor`, `aNCA/calculate_f`, `aNCA/g_pkcg01_log`, `aNCA/g_pkcg02_lin`, `aNCA/g_pkcg03_log`, `admiral/get_imputation_target_date`.

2. Prompt/reference/expected artifacts disagree.
   Several tasks have `task.json`, prompt text, reference `solution.R`, and evaluator comparisons asking for different outputs or behavior. Examples: `aNCA/dose_profile_duplicates`, `admiral/get_imputation_targets`, `admiraldev/assert_same_type`, `tidytlg/check_file`, `tidytlg/check_req_arg`.

3. Exact output filenames are not consistently preserved.
   Some prompts say "save as appropriate" or imply natural filenames. Generated code then writes plausible files like `x_unit.csv`, `source_vars.rds`, `datase_trt.csv`, `df_indented.csv`, or helper-specific RDS files, while the grader only checks `outputs/result.csv`, `outputs/result.rds`, and sometimes `outputs/summary.csv`.

4. Some embedded fixtures look stale or semantically wrong.
   Multiple inputs contain placeholder columns or values such as `AVAL`, `AVISITN`, `USUBJID`, `set_values_to`, or even multi-line R code where a clinical parameter code is expected. Examples: `admiral/count_vals`, `admiral/derive_param_rr`, `gridify/gpar_args`, `logrx/parse_log`, `admiraldev/assert_unit`, `tidytlg/add_indent`.

5. True LLM implementation failures exist, but are a minority.
   In 5 cases, prompt/reference/data looked mostly coherent and the generated code chose the wrong output path, wrong columns, or invented extra processing. Examples: `tidytlg/replace_na_with_blank`, `sdtm.oak/str_to_anycase`, `admiral/extract_unit`, `admiraldev/squote`, `ggsurvfit/scale_ggsurvfit`.

## Priority Fixes

1. Regenerate clinical prompts directly from `task.json` `instruct_prompt` plus exact expected artifacts.
   Do not paraphrase into public routine / generic transformation language unless the reference prompt already says that.

2. Add a preflight contract checker for each clinical task:
   - required artifact paths in prompt vs `task.json expected.artifacts`
   - evaluator comparison files vs `task.json expected.artifacts`
   - reference `solution.R` output files vs `task.json expected.artifacts`
   - mentions of internal helpers, `:::`, or `get(..., asNamespace(...))` preserved in generated prompt

3. Quarantine or repair fixture-defective tasks before scoring model quality.
   The data issue examples should be treated as task defects or require prompt text that explicitly explains the placeholder/fallback behavior.

4. Split result reporting into benchmark-defect and model-defect buckets.
   The current aggregate pass@1 is dominated by benchmark/prompt contract problems, so it should not be interpreted as GPT-5.1 clinical coding ability without this correction.

## Per-Sample Reports

- `group_1_audit.md`: samples 01-10
- `group_2_audit.md`: samples 11-20
- `group_3_audit.md`: samples 21-30
- `group_4_audit.md`: samples 31-40
- `group_5_audit.md`: samples 41-50

The generated single-sample bundles are `sample_01.md` through `sample_50.md`; `sample_manifest.csv` contains the sampled task list and current/simple evaluation summaries.
