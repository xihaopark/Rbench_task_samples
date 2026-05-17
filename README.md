# Rbench Task Samples: GPT-5.1 Clinical Taskset254 Review

This `review` branch contains the GPT-5.1 clinical taskset254 result export and audit notes for the current structured prompt versus a simple prompt.

Base branch: `main`  
Review branch: `review`

## What This Branch Adds

The new material is under:

```text
results/gpt51_clinical_taskset254/
```

Top-level files:

| path | contents |
|---|---|
| `summary.json` | Experiment metadata and strict pass@1 summary. |
| `current_prompt/generated_solutions.jsonl` | GPT-5.1 generated R code for the current structured prompt. |
| `current_prompt/evaluation_results.jsonl` | Docker evaluation results for the current structured prompt. |
| `simple_prompt/generated_solutions.jsonl` | GPT-5.1 generated R code for the simple prompt. |
| `simple_prompt/evaluation_results.jsonl` | Docker evaluation results for the simple prompt. |
| `audit/` | 50-sample root-cause audit and evaluation-strategy reports. |

## Frozen Strict Results

These are the strict Docker-grader results for the exported run. They should be treated as the reproducible baseline, not post-hoc edited scores.

| prompt variant | tasks | passed | strict pass@1 |
|---|---:|---:|---:|
| current prompt + inputs | 254 | 0 | 0.0000 |
| simple prompt + inputs | 254 | 1 | 0.0039 |

The only strict pass in the simple-prompt run is:

```text
pharmaverse/admiral/filter_exist
```

The taskset is `clinical_pilot_taskset254`: 254 clinical tasks from the 260-task current release, excluding six tasks absent from the older GPT-5.1 run.

## Audit Summary

A deterministic 50-task sample was reviewed manually with subagents. The audit indicates that failures are dominated by benchmark/prompt/data contract problems rather than clear LLM implementation errors.

| root cause | count | share |
|---|---:|---:|
| `prompt_wrong` | 27 | 54% |
| `prompt_reference_mismatch` | 11 | 22% |
| `data_or_fixture_issue` | 6 | 12% |
| `llm_wrong` | 5 | 10% |
| `unclear_needs_rerun` | 1 | 2% |

Prompt/reference contract issues alone account for 38/50 audited samples. Including data/fixture issues, benchmark-side issues account for 44/50.

## Rich Case Reviews

The richer per-case pages are here:

- [`cases/README.md`](results/gpt51_clinical_taskset254/cases/README.md)

Each sampled case page includes the task prompt, actual input files, reference output files, reference code, current/simple generated code, execution logs, generated output files, compact evaluation records, and audit root-cause evidence.


## Bio/Omics Controls

A small proteomics control set was added to show how GPT-5.1 behaves on cleaner bio tasks with direct input/output contracts:

- [`bio_controls/README.md`](results/gpt51_clinical_taskset254/bio_controls/README.md)

These controls include passing, mixed, and failing proteomics tasks from `openai_gpt_5.1_proteomics_pass5_20260118_093231`. They help separate clinical taskset contract defects from ordinary LLM implementation errors.

## Audit Reports

Start here:

- [`audit/README.md`](results/gpt51_clinical_taskset254/audit/README.md)
- [`audit/summary.md`](results/gpt51_clinical_taskset254/audit/summary.md)
- [`audit/simple_prompt_diagnostic_and_cleanup_guideline.md`](results/gpt51_clinical_taskset254/audit/simple_prompt_diagnostic_and_cleanup_guideline.md)
- [`audit/contract_manifest_summary.md`](results/gpt51_clinical_taskset254/audit/contract_manifest_summary.md)
- [`audit/current_results_and_eval_strategy.md`](results/gpt51_clinical_taskset254/audit/current_results_and_eval_strategy.md)

Detailed reports:

- [`audit/status_distribution_analysis.md`](results/gpt51_clinical_taskset254/audit/status_distribution_analysis.md)
- [`audit/contract_defect_analysis.md`](results/gpt51_clinical_taskset254/audit/contract_defect_analysis.md)
- [`audit/evaluation_strategy_analysis.md`](results/gpt51_clinical_taskset254/audit/evaluation_strategy_analysis.md)

Per-sample materials:

- `audit/sample_manifest.csv`
- `audit/group_1_audit.md` through `audit/group_5_audit.md`
- `audit/sample_01.md` through `audit/sample_50.md`

## Evaluation Recommendation

Do not replace strict pass@1. Add layered reporting:

1. Strict all-task pass@1, unchanged.
2. Tier distribution using `EXEC_FAIL -> NO_OUTPUT -> OUTPUT_BAD -> SCHEMA_OK -> CONTENT_OK -> PASS`.
3. Separately labeled normalized artifact regrade with `normalize_outputs=True`.
4. Contract-valid subset metric after task preflight.
5. Defect attribution separating prompt/reference/data defects from true model errors.

## Historical Case Notes

The older curated case notes remain under `cases/`. They are not the main object of this review branch; this branch is focused on the taskset254 result export and audit package above.
