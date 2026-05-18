# Case 112: pharmaverse/admiral/derive_vars_dt

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_dt`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform derive vars dt using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, DTC, ADT
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (51 bytes)
USUBJID	DTC
01	2020-01-15
02	2020-02
03	2020
04	NA
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_dt/inputs/dataset.tsv`
- Size: 51 bytes

```text
USUBJID	DTC
01	2020-01-15
02	2020-02
03	2020
04	NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_dt/solution.R`
- Size: 476 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dtc <- as.character(dataset$DTC)
complete_date <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", dtc)
adt <- as.Date(ifelse(complete_date, dtc, NA_character_))
result_df <- data.frame(USUBJID = dataset$USUBJID, DTC = dtc, ADT = adt, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_dt/outputs/result.csv`
- Size: 83 bytes

```csv
"USUBJID","DTC","ADT"
1,"2020-01-15",2020-01-15
2,"2020-02",NA
3,"2020",NA
4,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required package
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(lubridate)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
infile <- file.path("inputs", "dataset.tsv")
df <- read_tsv(infile, show_col_types = FALSE)

# Derive ADT from DTC according to partial date rules
df_out <- df %>%
  mutate(
    DTC = na_if(DTC, "NA"),
    ADT = case_when(
      is.na(DTC) ~ as.Date(NA),
      str_detect(DTC, "^\\d{4}-\\d{2}-\\d{2}$") ~ ymd(DTC),
      str_detect(DTC, "^\\d{4}-\\d{2}$") ~ ymd(paste0(DTC, "-01")),
      str_detect(DTC, "^\\d{4}$") ~ ymd(paste0(DTC, "-01-01")),
      TRUE ~ as.Date(NA)
    )
  ) %>%
  select(USUBJID, DTC, ADT)

# Write output
outfile <- file.path("outputs", "result.csv")
write_csv(df_out, outfile, na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_dt/sample_00/case_01/llm_outputs/result.csv`
- Size: 87 bytes

```csv
USUBJID,DTC,ADT
01,2020-01-15,2020-01-15
02,2020-02,2020-02-01
03,2020,2020-01-01
04,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_dt/sample_00/case_01/stderr.txt`
- Size: 1355 bytes

```text
[RBioBench Library Aliases] Library aliasing disabled (using stub layer)
[Admiraldev Stub] Created admiraldev namespace with 10 stub functions
[RBioBench Stub Layer] Loaded admiraldev stubs
[aNCA Stub] Created aNCA namespace with 57 stub functions
[RBioBench Stub Layer] Loaded aNCA stubs
[Logrx Stub] Created logrx namespace with 2 stub functions
[RBioBench Stub Layer] Loaded logrx stubs
[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions
[RBioBench Stub Layer] Loaded sdtmchecks stubs
[Other Stubs] Registered 5 stub functions from 5 packages
[RBioBench Stub Layer] Loaded other package stubs
[RBioBench Stub Layer] Registered attach hook for admiral
[Admiral Stub] Injected 40 functions into admiral namespace
[Admiral Stub] Injected 40 functions into admiral namespace
[RBioBench Stub Layer] Stubs registered in admiral namespace
[Admiral Stub] Injected 40 functions into admiral namespace
[Admiral Stub] Injected 40 functions into admiral namespace
[RBioBench Stub Layer] Stubs registered in admiral namespace
[RBioBench Stub Layer] .Rprofile loaded. Stubs will be auto-injected when admiral loads.
Warning message:
There were 3 warnings in `mutate()`.
The first warning was:
ℹ In argument: `ADT = case_when(...)`.
Caused by warning:
!  2 failed to parse.
ℹ Run `dplyr::last_dplyr_warnings()` to see the 2 remaining warnings.
```

## Evaluation Result

```json
{
  "status": "FAIL",
  "failure_stage": "value_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "schema_ok",
      "tier_value": "schema_ok",
      "failure_stage": "value_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "schema_ok",
          "failure_stage": "value_mismatch",
          "reason": "Value mismatch in column: ADT"
        }
      },
      "returncode": 0,
      "normalizations": [],
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [
          "result.csv"
        ],
        "staged_artifacts": [
          "result.csv"
        ],
        "missing_artifacts": [],
        "extra_artifacts": [],
        "comparison_reasons": {
          "result.csv": {
            "stage": "value_mismatch",
            "tier": "schema_ok",
            "reason": "Value mismatch in column: ADT"
          }
        }
      }
    }
  ]
}
```
