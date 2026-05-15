# Rbench Task Samples

Curated RBioBench clinical-track task samples for discussing how benchmark tasks relate to agent skills, especially `RConsortium/pharma-skills`.

## Current Focus

The first group is ordered to match lower-level admiral primitives that appear inside the `pharma-skills/admiral-adsl` workflow.

Each case contains:

- task prompt
- input files
- reference code and reference output
- LLM code and LLM output

## Admiral / ADSL Skill Comparison Cases

| # | Task | Why it maps to `admiral-adsl` |
|---|------|-------------------------------|
| [01](cases/case_01_derive_vars_dt.md) | `admiral::derive_vars_dt()` | analysis date variables from SDTM `--DTC` |
| [02](cases/case_02_derive_vars_dtm.md) | `admiral::derive_vars_dtm()` | analysis datetime variables from SDTM `--DTC` |
| [03](cases/case_03_derive_vars_dy.md) | `admiral::derive_vars_dy()` | study-day variables relative to treatment start |
| [04](cases/case_04_derive_var_trtdurd.md) | `admiral::derive_var_trtdurd()` | treatment duration after treatment dates exist |
| [05](cases/case_05_derive_vars_computed.md) | `admiral::derive_vars_computed()` | parameterized baseline/computed-variable derivation pattern |

## Contributor Hygiene

This repository is intentionally initialized as a clean repository rather than copied from another repo. Commits should use the GitHub noreply identity for `xihaopark`:

```text
xihao park <103370372+xihaopark@users.noreply.github.com>
```
