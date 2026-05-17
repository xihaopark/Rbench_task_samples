# GPT-5.1 Clinical Taskset254 Evaluation Strategy Analysis

Date: 2026-05-17

## Scope

This report inspects the current release evaluation strategy for the GPT-5.1 clinical taskset254 run and recommends how final evaluation should change without rewriting or replacing strict pass@1.

Inputs reviewed:

- `analysis/gpt51_taskset254_audit/current_results_and_eval_strategy.md`
- `agents_run/release_runtime.py`
- `scripts/tools/compute_tiered_metrics.py`
- `scripts/evaluate_with_docker.py`
- `/tmp/gpt51_clinical_taskset254_export/summary.json`
- `/tmp/gpt51_clinical_taskset254_export/current_prompt/evaluation_results.jsonl`
- `/tmp/gpt51_clinical_taskset254_export/simple_prompt/evaluation_results.jsonl`

## Current Baseline

The current Docker-graded result should remain the strict reproducibility baseline.

| prompt variant | tasks | passed | strict pass@1 |
|---|---:|---:|---:|
| current prompt + inputs | 254 | 0 | 0.0000 |
| simple prompt + inputs | 254 | 1 | 0.0039 |

Status distribution in the exported JSONL files:

| prompt variant | PASS | FAIL | NO_OUTPUT | TIMEOUT | EXEC_FAIL |
|---|---:|---:|---:|---:|---:|
| current prompt + inputs | 0 | 83 | 81 | 88 | 2 |
| simple prompt + inputs | 1 | 113 | 52 | 88 | 0 |

Case-level tier distribution, using the evaluated test case tier rather than top-level status:

| prompt variant | pass | output_bad | exec_fail | no_output |
|---|---:|---:|---:|---:|
| current prompt + inputs | 0 | 83 | 169 | 2 |
| simple prompt + inputs | 1 | 113 | 140 | 0 |

The simple prompt mostly shifts non-output or execution failures into comparator-visible wrong outputs. It does not materially improve strict pass@1.

## Existing Capabilities

### `GradingTier`

`agents_run/release_runtime.py` defines a useful ordered grading hierarchy:

`EXEC_FAIL -> NO_OUTPUT -> OUTPUT_BAD -> SCHEMA_OK -> CONTENT_OK -> PASS`

This is the right primitive for final reporting because it separates:

- code that fails or times out in Docker
- code that runs but produces no expected artifacts
- code that produces artifacts with missing files, unreadable files, or schema mismatch
- code with correct schema but wrong content
- code with content-level equivalence
- exact strict pass

`validate_release_task()` propagates per-case tiers and computes an overall tier internally. `compare_files()` also returns tier information for tabular, RDS, and binary outputs.

### `normalize_outputs`

`validate_release_task(..., normalize_outputs=True)` already supports a deliberately narrow post-hoc artifact normalization layer through `_populate_llm_outputs_dir()`:

- copy generated outputs into the comparison directory
- if there is exactly one non-`summary.csv` reference and exactly one generated non-summary output with the same suffix, alias the generated file to the expected reference filename
- if `summary.csv` is expected but missing, synthesize it from a single tabular output by recording row count, column count, and column names

This is appropriate for measuring artifact-name drift separately. It is not a semantic relaxation: it does not repair wrong columns, wrong rows, wrong values, wrong object structure, or wrong API behavior.

### Docker Release Evaluation

`scripts/evaluate_with_docker.py` routes release-manifest evaluations through `DockerRBenchEvaluator.evaluate_release_sample()`, which calls `validate_release_task()` and exposes the `--normalize-outputs` CLI flag. It also supports resume behavior and concurrent release evaluation workers.

### Tiered Metrics Script

`scripts/tools/compute_tiered_metrics.py` can summarize tier counts, percentages, by-agent breakdowns, and by-track breakdowns. It imports the same `GradingTier` enum, so the reporting vocabulary is aligned with the runtime.

## Gaps

1. Top-level tier is missing from the exported task rows.

   The local taskset254 JSONL rows have `tier` only inside `test_cases`, not at the top level. `compute_tiered_metrics.py` prefers top-level `tier`; when it is absent, it maps top-level status to tiers. That mapping loses information. For the current prompt, the script reports 90 `exec_fail` and 81 `no_output`, while case-level tiers show 169 `exec_fail` and 2 `no_output`.

2. `NO_OUTPUT` status currently mixes execution failures and true no-output cases.

   In `validate_release_task()`, a run with no output files is assigned case status `NO_OUTPUT` even when the tier is `EXEC_FAIL`. That is useful for the legacy status table, but final analysis should not use status alone to infer failure mode.

3. Normalized grading has not been run in the provided export.

   The reviewed JSONL rows have no recorded normalizations. This means current strict results do not quantify how many failures are just expected-output filename drift or missing generated `summary.csv`.

4. `compute_tiered_metrics.py` does not inspect per-case tier fallback.

   The script should use top-level `tier` when present, otherwise derive the task tier from `test_cases` before falling back to status mapping. Without this, final tier reports can overstate true no-output failures and understate Docker execution failures.

5. There is no all-task contract-valid denominator yet.

   The 50-task audit found that prompt, reference, artifact, and fixture defects dominate the failures. Existing grading can report what happened under the current benchmark contract, but it cannot yet distinguish model failures from benchmark-contract failures across all 254 tasks.

6. Strict pass@1 is reproducible but not sufficient as a model-quality summary.

   The current aggregate score is dominated by contract and fixture issues. Replacing strict pass@1 would hide reproducibility; reporting it alone would overstate what can be concluded about GPT-5.1 clinical coding ability.

## Recommended Final Reporting Layers

### 1. Strict All-Task Pass@1

Keep the current definition unchanged:

- numerator: `status == PASS`
- denominator: all 254 tasks in the run
- label: strict all-task pass@1

This remains the immutable reproducibility and regression-tracking number.

### 2. Execution/Tier Distribution

Report the `GradingTier` distribution for each prompt variant:

- use top-level `tier` when present
- otherwise derive from per-case tiers
- only fall back to top-level status when neither tier source exists

This should be a diagnostic layer, not a replacement pass metric. It explains whether a prompt variant improves execution, artifact production, schema matching, or content matching.

### 3. Normalized Artifact Regrade

Regrade the same generated solutions with `--normalize-outputs` and label the result separately:

- strict pass@1 remains unchanged
- normalized artifact pass@1 is a secondary metric
- report count of tasks affected by each normalization string
- report transitions such as `output_bad -> pass`, `output_bad -> schema_ok`, and unchanged failures

This estimates how much exact filename and `summary.csv` drift matters without loosening semantic grading.

### 4. Contract-Valid Subset

Add a preflight contract checker and report a contract-valid denominator:

- prompt expected artifacts vs `task.json` expected artifacts
- evaluator comparison files vs expected artifacts
- reference `solution.R` written outputs vs expected artifacts
- preservation of internal helper calls such as `:::` or `get(..., asNamespace(...))`
- fixture sanity checks for placeholder or impossible clinical data

Final reporting should include:

- strict pass@1 on all 254 tasks
- strict pass@1 on the contract-valid subset
- number of excluded or quarantined benchmark-defect tasks by reason

This gives a fairer capability denominator while preserving the original all-task result.

### 5. Defect Attribution Layer

Publish a task-level attribution table, using the existing audit rubric:

- `prompt_wrong`
- `prompt_reference_mismatch`
- `data_or_fixture_issue`
- `evaluator_or_stub_issue`
- `llm_wrong`
- `unclear_needs_rerun`

The current 50-task audit estimates 44/50 prompt, contract, or data issues and 5/50 clean model implementation failures. The final release report should not extrapolate that sample as a replacement score, but it should use the taxonomy to explain why strict pass@1 is low.

## Concrete Next Steps

1. Preserve the current strict JSONL files and summary as the frozen baseline.

2. Regrade both generated solution files with `scripts/evaluate_with_docker.py --normalize-outputs`, using the same release manifest, track, Docker image, and taskset254 inputs. Write results to a separate output directory and label them as normalized artifact regrades.

3. Update or wrap `compute_tiered_metrics.py` so task tier derivation uses `row["tier"]`, then per-case `test_cases[*]["tier"]`, then status mapping. Do not change strict pass logic.

4. Implement a contract preflight script for all 254 clinical tasks and emit a machine-readable task classification with defect reason codes.

5. Produce a final report with four headline tables:

   - strict all-task pass@1
   - tier distribution by prompt variant
   - normalized artifact regrade deltas
   - strict pass@1 on contract-valid subset plus excluded-defect counts

6. Regenerate a corrected prompt variant from `task.json` `instruct_prompt` plus exact expected artifacts, then validate it on a small stratified subset before any full 254-task rerun.

## Recommendation

Final evaluation should become multi-layered, not more permissive. Strict pass@1 should remain unchanged and visible. The release should add tiered execution reporting, a separately labeled normalized artifact regrade, a contract-valid subset metric, and defect attribution. That structure preserves reproducibility while making the benchmark-quality and prompt-contract problems explicit.
