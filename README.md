# Rbench Task Samples

Clinical-track RBioBench task samples and new pharmaverse task designs. Stable clinical cases include prompts, inputs, reference code/output, GPT-5.1 direct-LLM code/output, and evaluation records.

## Stable Benchmark Cases

| # | Task | Package | Level | GPT-5.1 Status |
|---|---|---|---:|---|
| 1 | [pharmaverse/admiral/derive_vars_cat](cases/case_01_derive_vars_cat.md) | `admiral` | L2 | `NO_OUTPUT` |
| 2 | [pharmaverse/admiral/derive_var_pchg](cases/case_02_derive_var_pchg.md) | `admiral` | L1 | `NO_OUTPUT` |
| 3 | [pharmaverse/admiral/compute_qtc](cases/case_03_compute_qtc.md) | `admiral` | L2 | `FAIL` |
| 4 | [pharmaverse/admiral/compute_map](cases/case_04_compute_map.md) | `admiral` | L2 | `FAIL` |
| 5 | [pharmaverse/admiral/compute_rr](cases/case_05_compute_rr.md) | `admiral` | L1 | `FAIL` |
| 6 | [pharmaverse/admiral/compute_age_years](cases/case_06_compute_age_years.md) | `admiral` | L2 | `NO_OUTPUT` |
| 7 | [pharmaverse/admiral/compute_qual_imputation_dec](cases/case_07_compute_qual_imputation_dec.md) | `admiral` | L1 | `FAIL` |
| 8 | [pharmaverse/admiral/default_qtc_paramcd](cases/case_08_default_qtc_paramcd.md) | `admiral` | L1 | `NO_OUTPUT` |
| 9 | [pharmaverse/admiral/convert_dtc_to_dt](cases/case_09_convert_dtc_to_dt.md) | `admiral` | L1 | `FAIL` |
| 10 | [pharmaverse/admiral/convert_dtc_to_dtm](cases/case_10_convert_dtc_to_dtm.md) | `admiral` | L1 | `FAIL` |
| 11 | [pharmaverse/admiral/convert_blanks_to_na](cases/case_11_convert_blanks_to_na.md) | `admiral` | L1 | `FAIL` |
| 12 | [pharmaverse/admiral/convert_na_to_blanks](cases/case_12_convert_na_to_blanks.md) | `admiral` | L1 | `FAIL` |
| 13 | [pharmaverse/admiral/convert_ranges](cases/case_13_convert_ranges.md) | `admiral` | L2 | `NO_OUTPUT` |
| 14 | [pharmaverse/admiral/convert_simple_units](cases/case_14_convert_simple_units.md) | `admiral` | L2 | `NO_OUTPUT` |
| 15 | [pharmaverse/admiral/convert_time_units](cases/case_15_convert_time_units.md) | `admiral` | L2 | `NO_OUTPUT` |
| 16 | [pharmaverse/admiral/filter_extreme](cases/case_16_filter_extreme.md) | `admiral` | L2 | `NO_OUTPUT` |
| 17 | [pharmaverse/admiral/filter_exist](cases/case_17_filter_exist.md) | `admiral` | L2 | `NO_OUTPUT` |
| 18 | [pharmaverse/admiral/impute_dtc_dt](cases/case_18_impute_dtc_dt.md) | `admiral` | L3 | `NO_OUTPUT` |
| 19 | [pharmaverse/admiral/chr2vars](cases/case_19_chr2vars.md) | `admiral` | L1 | `FAIL` |
| 20 | [pharmaverse/admiral/get_highest_imputation_level](cases/case_20_get_highest_imputation_level.md) | `admiral` | L1 | `NO_OUTPUT` |

## New Package Task Designs

| # | Task | Package | Status |
|---|---|---|---|
| 21 | [metalite.ae/rate_compare_sum](cases/case_21_metalite_ae_rate_compare_sum.md) | `metalite.ae` | design reviewed |
| 22 | [metalite.ae/prepare_ae_summary](cases/case_22_metalite_ae_prepare_ae_summary.md) | `metalite.ae` | design reviewed |
| 23 | [metalite.ae/extend_ae_specific_inference](cases/case_23_metalite_ae_extend_ae_specific_inference.md) | `metalite.ae` | design reviewed |
| 24 | [r2rtf/rtf_body](cases/case_24_r2rtf_rtf_body.md) | `r2rtf` | design reviewed |
| 25 | [r2rtf/rtf_colheader](cases/case_25_r2rtf_rtf_colheader.md) | `r2rtf` | design reviewed |
