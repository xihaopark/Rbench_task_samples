# Case 145: pharmaverse/admiral/get_imputation_target_date

## Case Metadata

- Task ID: `pharmaverse/admiral/get_imputation_target_date`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform get imputation target date using the admiral clinical task contract.

Input: date_imputation.tsv, month.tsv
Output: result.csv


Required columns for result.csv: date_imputation, month, target_month, target_day
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### date_imputation.tsv (31 bytes)
date_imputation
mid
first
last

### month.tsv (15 bytes)
month
02
02
02
```

## Input Data

### `date_imputation.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_target_date/inputs/date_imputation.tsv`
- Size: 31 bytes

```text
date_imputation
mid
first
last
```

### `month.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_target_date/inputs/month.tsv`
- Size: 15 bytes

```text
month
02
02
02
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_target_date/solution.R`
- Size: 843 bytes

```r
date_imputation <- as.character(read.delim(file.path("inputs", "date_imputation.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$date_imputation)
month <- sprintf("%02d", as.integer(read.delim(file.path("inputs", "month.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$month))
last_day <- function(mm) {
  start <- as.Date(sprintf("2020-%s-01", mm))
  as.integer(format(as.Date(format(start + 32, "%Y-%m-01")) - 1, "%d"))
}
target_day <- ifelse(date_imputation == "first", 1L, ifelse(date_imputation == "mid", 15L, vapply(month, last_day, integer(1))))
result_df <- data.frame(date_imputation = date_imputation, month = month, target_month = month, target_day = as.integer(target_day), stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_target_date/outputs/result.csv`
- Size: 113 bytes

```csv
"date_imputation","month","target_month","target_day"
"mid","02","02",15
"first","02","02",1
"last","02","02",29
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(lubridate)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
date_imp <- read_tsv(
  file = file.path("inputs", "date_imputation.tsv"),
  col_types = cols(.default = col_character())
)

month_df <- read_tsv(
  file = file.path("inputs", "month.tsv"),
  col_types = cols(.default = col_character())
)

# Ensure same row count
n <- min(nrow(date_imp), nrow(month_df))
date_imp <- date_imp[seq_len(n), , drop = FALSE]
month_df <- month_df[seq_len(n), , drop = FALSE]

df <- bind_cols(date_imp, month_df)

# Helper to compute target day according to admiral mid/first/last rules
get_target_day <- function(date_imputation, month) {
  # default NA for invalid/missing
  if (is.na(date_imputation) || is.na(month) || month == "") return(NA_integer_)
  m_int <- suppressWarnings(as.integer(month))
  if (is.na(m_int) || m_int < 1 || m_int > 12) return(NA_integer_)

  # use 2000 as reference year (leap year for Feb)
  days_in_month <- days_in_month(ymd(sprintf("2000-%02d-01", m_int)))

  if (tolower(date_imputation) == "first") {
    return(1L)
  } else if (tolower(date_imputation) == "last") {
    return(as.integer(days_in_month))
  } else if (tolower(date_imputation) == "mid") {
    return(as.integer(ceiling(days_in_month / 2)))
  } else {
    return(NA_integer_)
  }
}

df <- df %>%
  mutate(
    target_day = mapply(get_target_day, date_imputation, month),
    target_month = month
  ) %>%
  select(date_imputation, month, target_month, target_day)

# Write output
write_csv(df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_imputation_target_date/sample_00/case_01/llm_outputs/result.csv`
- Size: 87 bytes

```csv
date_imputation,month,target_month,target_day
mid,02,02,15
first,02,02,1
last,02,02,29
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_imputation_target_date/sample_00/case_01/stderr.txt`
- Size: 1123 bytes

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
```

## Evaluation Result

```json
{
  "status": "PASS",
  "failure_stage": "pass",
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "tier": "pass",
      "tier_value": "pass",
      "failure_stage": "pass",
      "comparison": {
        "result.csv": {
          "match": true,
          "tier": "pass",
          "failure_stage": "pass"
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
        "comparison_reasons": {}
      }
    }
  ]
}
```
