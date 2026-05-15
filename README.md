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
| [03](cases/case_03_compute_age_years.md) | `admiral::compute_age_years()` | age-unit normalization used before ADSL age derivations |
| [04](cases/case_04_compute_bmi.md) | `admiral::compute_bmi()` | BMI baseline value logic used in ADSL body-measure derivations |
| [05](cases/case_05_derive_vars_period.md) | `admiral::derive_vars_period()` | analysis-period start/end variables joined onto subject-level data |

## Prompt Hygiene

Cases 01-02 keep the original task family but make the benchmark contract explicit: read files from `inputs/`, and create the documented fallback columns before calling admiral. Cases 03-05 replace earlier examples whose prompts depended too heavily on hidden reference behavior or synthetic fixtures.

## Contributor Hygiene

This repository is intentionally initialized as a clean repository rather than copied from another repo. Commits should use the GitHub noreply identity for `xihaopark`:

```text
xihao park <103370372+xihaopark@users.noreply.github.com>
```
