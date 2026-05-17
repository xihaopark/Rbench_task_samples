# GPT-5.1 Clinical Taskset254 Status Distribution Analysis

Date: 2026-05-17

Inputs:

- `/tmp/gpt51_clinical_taskset254_export/summary.json`
- `/tmp/gpt51_clinical_taskset254_export/current_prompt/evaluation_results.jsonl`
- `/tmp/gpt51_clinical_taskset254_export/simple_prompt/evaluation_results.jsonl`
- Existing audit notes in `analysis/gpt51_taskset254_audit/`

## Strict pass@1

| prompt variant | tasks | passed | strict pass@1 |
|---|---:|---:|---:|
| current prompt + inputs | 254 | 0 | 0.0000 |
| simple prompt + inputs | 254 | 1 | 0.0039 |

The only strict simple-prompt pass is `pharmaverse/admiral/filter_exist`. Current prompt has no strict passes.

## Status counts

| prompt variant | PASS | FAIL | NO_OUTPUT | TIMEOUT | EXEC_FAIL |
|---|---:|---:|---:|---:|---:|
| current prompt + inputs | 0 | 83 | 81 | 88 | 2 |
| simple prompt + inputs | 1 | 113 | 52 | 88 | 0 |

Status share:

| prompt variant | PASS | FAIL | NO_OUTPUT | TIMEOUT | EXEC_FAIL |
|---|---:|---:|---:|---:|---:|
| current prompt + inputs | 0.0% | 32.7% | 31.9% | 34.6% | 0.8% |
| simple prompt + inputs | 0.4% | 44.5% | 20.5% | 34.6% | 0.0% |

## Tier counts

Tier is taken from the first evaluated test case per task, with strict passes counted as `pass`.

| prompt variant | pass | output_bad | exec_fail | no_output |
|---|---:|---:|---:|---:|
| current prompt + inputs | 0 | 83 | 169 | 2 |
| simple prompt + inputs | 1 | 113 | 140 | 0 |

Tier share:

| prompt variant | pass | output_bad | exec_fail | no_output |
|---|---:|---:|---:|---:|
| current prompt + inputs | 0.0% | 32.7% | 66.5% | 0.8% |
| simple prompt + inputs | 0.4% | 44.5% | 55.1% | 0.0% |

## Simple vs current

The simple prompt is not meaningfully better by strict pass@1: it improves from 0/254 to 1/254. Its main effect is a distribution shift from non-output/execution failures into runnable-but-wrong outputs.

Paired status movements:

| movement | tasks |
|---|---:|
| TIMEOUT -> TIMEOUT | 73 |
| FAIL -> FAIL | 58 |
| NO_OUTPUT -> FAIL | 46 |
| NO_OUTPUT -> NO_OUTPUT | 28 |
| FAIL -> NO_OUTPUT | 16 |
| FAIL -> TIMEOUT | 9 |
| TIMEOUT -> FAIL | 8 |
| TIMEOUT -> NO_OUTPUT | 7 |
| NO_OUTPUT -> TIMEOUT | 6 |
| NO_OUTPUT -> PASS | 1 |
| EXEC_FAIL -> FAIL | 1 |
| EXEC_FAIL -> NO_OUTPUT | 1 |

Paired tier movements show the same pattern:

| movement | tasks |
|---|---:|
| exec_fail -> exec_fail | 115 |
| output_bad -> output_bad | 58 |
| exec_fail -> output_bad | 53 |
| output_bad -> exec_fail | 25 |
| no_output -> output_bad | 2 |
| exec_fail -> pass | 1 |

Net changes from current to simple:

- Strict pass: +1 task.
- `NO_OUTPUT`: -29 tasks.
- `FAIL` / `output_bad`: +30 tasks.
- `TIMEOUT`: unchanged at 88 tasks.
- Execution-tier failures: -29 tasks, from 171 combined current non-output/execution-tier failures to 140 simple `exec_fail` tasks.

## Interpretation

The simple prompt makes more tasks produce comparator-visible artifacts, but those artifacts usually do not match expected outputs. That is why `FAIL` and `output_bad` rise while strict pass barely changes.

The unchanged timeout count is important: simple prompting does not address the large timeout failure mode. It mostly converts some `NO_OUTPUT`/execution failures into wrong-output failures.

The existing 50-task audit indicates that many failures are benchmark/prompt contract issues rather than clean model implementation errors. In that sample, prompt/contract/data issues accounted for 44/50 cases, with prompt/contract issues alone accounting for 38/50. Therefore the strict all-task score is a reproducible run result, but it should not be treated as an isolated measure of GPT-5.1 clinical coding capability.

## Concise takeaways

- Current prompt strict pass@1 is 0.0000; simple prompt strict pass@1 is 0.0039.
- Both variants fail almost all tasks under strict grading.
- Simple prompt shifts failures toward `FAIL`/`output_bad`, which suggests improved artifact production but not correct clinical task behavior.
- Timeout remains the largest single status bucket for both variants at 88/254.
- The result supports reporting multiple views: strict pass@1, tier distribution, and separate benchmark/prompt-contract attribution.
