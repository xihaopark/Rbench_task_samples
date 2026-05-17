# GPT-5.1 Clinical Taskset254 Audit

Date: 2026-05-17

This directory captures the status analysis and root-cause audit for the GPT-5.1 clinical taskset254 experiment comparing the current structured prompt and a simple prompt.

## Frozen Strict Results

| prompt variant | tasks | passed | strict pass@1 |
|---|---:|---:|---:|
| current prompt + inputs | 254 | 0 | 0.0000 |
| simple prompt + inputs | 254 | 1 | 0.0039 |

The strict results should remain the reproducible baseline. They should not be treated alone as a clean measure of GPT-5.1 clinical coding ability, because the audit found many prompt, reference, artifact, and fixture contract defects.

## Main Finding

In a deterministic 50-task sample, failures were mostly benchmark/prompt/data contract issues rather than clear model implementation errors:

| root cause | count | share |
|---|---:|---:|
| `prompt_wrong` | 27 | 54% |
| `prompt_reference_mismatch` | 11 | 22% |
| `data_or_fixture_issue` | 6 | 12% |
| `llm_wrong` | 5 | 10% |
| `unclear_needs_rerun` | 1 | 2% |

Prompt/reference contract issues alone account for 38/50 audited samples. Including data/fixture issues, benchmark-side issues account for 44/50.

## Reports

- `summary.md` - concise 50-sample audit summary and recommended fixes.
- `current_results_and_eval_strategy.md` - frozen current result and proposed multi-layer evaluation policy.
- `status_distribution_analysis.md` - current vs simple full-task status/tier distribution.
- `contract_defect_analysis.md` - defect taxonomy with representative tasks and preflight checks.
- `evaluation_strategy_analysis.md` - current evaluator capabilities, gaps, and recommended final reporting layers.
- `group_1_audit.md` through `group_5_audit.md` - subagent-reviewed per-sample findings for the 50 sampled tasks.
- `sample_manifest.csv` - deterministic sample list and current/simple evaluation summaries.
- `sample_01.md` through `sample_50.md` - per-task audit bundles with prompts, evaluation snippets, reference solution heads, and generated solutions.
- `rubric.md` - root-cause labels used for the audit.

## Recommended Evaluation Policy

Do not replace strict pass@1. Add layered reporting:

1. Strict all-task pass@1, unchanged.
2. Tier distribution using `EXEC_FAIL -> NO_OUTPUT -> OUTPUT_BAD -> SCHEMA_OK -> CONTENT_OK -> PASS`.
3. Separately labeled normalized artifact regrade with `normalize_outputs=True`.
4. Contract-valid subset metric after task preflight.
5. Defect attribution table separating prompt/reference/data defects from true model errors.

## Immediate Next Steps

1. Preserve the exported JSONL results as the frozen strict baseline.
2. Run normalized artifact regrade for current and simple generated solutions.
3. Implement all-task contract preflight for the 254 clinical tasks.
4. Regenerate a corrected prompt variant from `task.json` `instruct_prompt` plus exact expected artifacts.
5. Validate the corrected prompt on a small stratified subset before a full rerun.
