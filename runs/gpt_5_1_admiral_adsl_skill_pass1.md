# GPT-5.1 + `admiral-adsl` Skill Context: Pass1 Run

Run date: 2026-05-15

This run used the same model family as the prior GPT-5.1 direct-LLM samples, but prepended a compact `RConsortium/pharma-skills/admiral-adsl` skill context to the five curated RBioBench task prompts.

Important caveat: this is prompt-injected skill context, not native Claude Code skill execution. The goal was to test whether the skill instructions alone help the same LLM satisfy these function-level RBioBench tasks.

## Setup

- Model: `openai/gpt-5.1`
- Samples: 1 per task
- Temperature: `1.0`
- Skill context: compact `admiral-adsl` guidance plus relevant admiral function notes
- Evaluation: RBioBench Docker release evaluator against `rbiobench_stable_v1`, `clinical_pilot`, package `admiral`

Local artifacts were written under:

```text
runs/direct_llm/skill_admiral_adsl/gpt_5.1/pass1/
```

## Results

| # | Task | Result | Main failure |
|---|------|--------|--------------|
| 01 | `derive_vars_dt` | FAIL | Generated code set `new_vars_prefix <- NULL`; `derive_vars_dt()` then failed inside the admiral/stub imputation path. |
| 02 | `derive_vars_dtm` | FAIL | Same imputation-path failure from `derive_vars_dtm()`. |
| 03 | `compute_age_years` | FAIL | Used uppercase column names `AGE` / `AGE_UNIT`; actual fixtures are lowercase `age` / `age_unit`. |
| 04 | `compute_bmi` | FAIL | Code executed, but output columns were `height, weight, bmi`; reference expects `id, result`. |
| 05 | `derive_vars_period` | FAIL | Code executed, but fallback `STUDYID`/`USUBJID` values did not match reference contract (`STUDY1`, `1..5`). |

Pass rate: **0/5**.

## Interpretation

The skill context helped the model stay closer to admiral APIs and avoid some earlier schema over-assumptions, but it did not solve RBioBench's strict output-contract requirements. The remaining failures are mostly benchmark-contract failures: exact fallback values, exact output column names, and exact fixture column casing.

This supports the distinction we discussed earlier:

- `admiral-adsl` skill is useful for real ADSL workflow structure and admiral idioms.
- RBioBench microtasks additionally test exact file paths, fixture interpretation, fallback behavior, and output schemas.
- Passing these tasks likely needs task-specific contract awareness in addition to the high-level ADSL skill.
