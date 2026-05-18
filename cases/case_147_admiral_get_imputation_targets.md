# Case 147: pharmaverse/admiral/get_imputation_targets

## Case Metadata

- Task ID: `pharmaverse/admiral/get_imputation_targets`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform get imputation targets using the admiral clinical task contract.

Input: partial.tsv
Output: result.csv


Required columns for result.csv: partial, year, month, day, hour, minute, second
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### partial.tsv (35 bytes)
partial
2020
2020-02
2020-02-20T14
```

## Input Data

### `partial.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_targets/inputs/partial.tsv`
- Size: 35 bytes

```text
partial
2020
2020-02
2020-02-20T14
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_targets/solution.R`
- Size: 773 bytes

```r
partial <- as.character(read.delim(file.path("inputs", "partial.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$partial)
year <- substr(partial, 1, 4)
month <- ifelse(nchar(partial) >= 7, substr(partial, 6, 7), "06")
day <- ifelse(nchar(partial) >= 10, substr(partial, 9, 10), "15")
hour <- ifelse(nchar(partial) >= 13, substr(partial, 12, 13), "00")
minute <- ifelse(nchar(partial) >= 16, substr(partial, 15, 16), "00")
second <- ifelse(nchar(partial) >= 19, substr(partial, 18, 19), "00")
result_df <- data.frame(partial = partial, year = year, month = month, day = day, hour = hour, minute = minute, second = second, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_imputation_targets/outputs/result.csv`
- Size: 185 bytes

```csv
"partial","year","month","day","hour","minute","second"
"2020","2020","06","15","00","00","00"
"2020-02","2020","02","15","00","00","00"
"2020-02-20T14","2020","02","20","14","00","00"
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

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
partial_df <- readr::read_tsv(
  file = file.path("inputs", "partial.tsv"),
  col_types = cols(
    partial = col_character()
  )
)

# Helper to parse partial datetime strings
parse_partial <- function(x) {
  # Initialize all as NA
  year   <- rep(NA_integer_, length(x))
  month  <- rep(NA_integer_, length(x))
  day    <- rep(NA_integer_, length(x))
  hour   <- rep(NA_integer_, length(x))
  minute <- rep(NA_integer_, length(x))
  second <- rep(NA_integer_, length(x))

  # Detect patterns using regex
  # 1) Year only: YYYY
  idx_year <- str_detect(x, "^\\d{4}$")
  year[idx_year] <- as.integer(x[idx_year])

  # 2) Year-month: YYYY-MM
  idx_ym <- str_detect(x, "^\\d{4}-\\d{2}$")
  year[idx_ym]  <- as.integer(str_sub(x[idx_ym], 1, 4))
  month[idx_ym] <- as.integer(str_sub(x[idx_ym], 6, 7))

  # 3) Year-month-dayThour: YYYY-MM-DDThh
  idx_ymdh <- str_detect(x, "^\\d{4}-\\d{2}-\\d{2}T\\d{2}$")
  year[idx_ymdh]  <- as.integer(str_sub(x[idx_ymdh], 1, 4))
  month[idx_ymdh] <- as.integer(str_sub(x[idx_ymdh], 6, 7))
  day[idx_ymdh]   <- as.integer(str_sub(x[idx_ymdh], 9, 10))
  hour[idx_ymdh]  <- as.integer(str_sub(x[idx_ymdh], 12, 13))

  tibble(
    year   = year,
    month  = month,
    day    = day,
    hour   = hour,
    minute = minute,
    second = second
  )
}

result <- partial_df %>%
  mutate(
    parse_partial(partial)
  ) %>%
  select(partial, year, month, day, hour, minute, second)

# Write output
readr::write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_imputation_targets/sample_00/case_01/llm_outputs/result.csv`
- Size: 105 bytes

```csv
partial,year,month,day,hour,minute,second
2020,2020,,,,,
2020-02,2020,2,,,,
2020-02-20T14,2020,2,20,14,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_imputation_targets/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric missingness mismatch in column: month"
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
            "reason": "Numeric missingness mismatch in column: month"
          }
        }
      }
    }
  ]
}
```
