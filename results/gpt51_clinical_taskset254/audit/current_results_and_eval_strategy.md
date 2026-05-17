# GPT-5.1 Clinical Taskset254: Current Result and Evaluation Strategy

Date: 2026-05-17

## Freeze Current Result

Use the current Docker grader result as the strict reproducible baseline:

| prompt variant | tasks | passed | strict pass@1 |
|---|---:|---:|---:|
| current prompt + inputs | 254 | 0 | 0.0000 |
| simple prompt + inputs | 254 | 1 | 0.0039 |

Status distribution:

| prompt variant | PASS | FAIL | NO_OUTPUT | TIMEOUT | EXEC_FAIL |
|---|---:|---:|---:|---:|---:|
| current prompt + inputs | 0 | 83 | 81 | 88 | 2 |
| simple prompt + inputs | 1 | 113 | 52 | 88 | 0 |

Interpretation:

- The strict result is valid as a reproducibility record of the exact run.
- It should not be interpreted as a clean measure of GPT-5.1 clinical coding ability, because the 50-task audit found that most failures are benchmark/prompt contract defects.

## What the Audit Says

From the deterministic 50-task sample:

| root cause | count | share |
|---|---:|---:|
| prompt_wrong | 27 | 54% |
| prompt_reference_mismatch | 11 | 22% |
| data_or_fixture_issue | 6 | 12% |
| llm_wrong | 5 | 10% |
| unclear_needs_rerun | 1 | 2% |

Prompt/contract/data issues: 44 / 50 = 88%.

Prompt/contract issues alone: 38 / 50 = 76%.

## Recommended Final Evaluation Policy

Do not replace the strict score. Add layered reporting.

### 1. Strict Pass@1

Keep the current `status == PASS` score unchanged.

Purpose:

- exact reproducibility
- regression tracking
- compatibility with previous RBioBench result tables

For this run:

- current prompt strict pass@1: 0 / 254
- simple prompt strict pass@1: 1 / 254

### 2. Tiered Execution Metric

Report existing `GradingTier` distribution:

`EXEC_FAIL -> NO_OUTPUT -> OUTPUT_BAD -> SCHEMA_OK -> CONTENT_OK -> PASS`

Purpose:

- distinguish "did not run" from "ran but wrong output"
- show that simple prompt mostly shifts `NO_OUTPUT` into `OUTPUT_BAD`, not into true pass

Implementation already exists:

- `agents_run/release_runtime.py`
- `scripts/tools/compute_tiered_metrics.py`

### 3. Normalized Artifact Metric

Run a secondary regrade with `normalize_outputs=True`, but label it separately.

This is appropriate for cases where:

- one non-summary output exists with the wrong filename but correct suffix
- `summary.csv` can be mechanically generated from the primary tabular output

This should not fix:

- wrong columns
- wrong rows
- wrong API behavior
- wrong semantic content

Purpose:

- avoid over-penalizing output filename drift
- estimate how much of the failure is merely artifact naming

Important: normalized results are not strict pass and should not overwrite the baseline.

### 4. Contract-Valid Subset Metric

Before treating failures as model failures, run a task contract preflight. Exclude or separately label tasks with:

- prompt/reference/expected artifact disagreement
- reference solution writes files not listed in `expected.artifacts`
- evaluator compares files not listed in `expected.artifacts`
- generated prompt omits required internal helper calls such as `:::` or `get(..., asNamespace(...))`
- fixtures with placeholder or impossible data for the documented task

Report:

- strict pass@1 on all 254
- strict pass@1 on contract-valid subset
- number of excluded benchmark-defect tasks by reason

This is the fairest model-capability denominator.

### 5. Defect Attribution Report

For failed samples, publish a breakdown:

- benchmark/prompt defect
- data/fixture defect
- evaluator/artifact-normalization issue
- model implementation error
- unclear/requires rerun

Purpose:

- prevent aggregate pass@1 from hiding benchmark quality issues
- make prompt repair work measurable

## Concrete Next Step

The next engineering task should not be to loosen the comparator globally.

Instead:

1. Implement a contract preflight script for all 254 clinical tasks.
2. Regrade current/simple outputs with `normalize_outputs=True` as a labeled secondary metric.
3. Regenerate a corrected prompt variant directly from `task.json` `instruct_prompt` plus exact expected artifacts.
4. Rerun a small validation subset before a full 254 rerun.

The strict current result remains fixed; the final evaluation strategy should become multi-view rather than post-hoc modified.
