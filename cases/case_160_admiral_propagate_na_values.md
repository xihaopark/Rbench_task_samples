# Case 160: pharmaverse/admiral/propagate_na_values

## Case Metadata

- Task ID: `pharmaverse/admiral/propagate_na_values`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform propagate na values using the admiral clinical task contract.

Input: partial.tsv
Output: result.csv


Required columns for result.csv: year, month, day, hour, minute, second
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### partial.tsv (94 bytes)
year	month	day	hour	minute	second
2020	05	NA	10	30	45
2021	NA	12	09	15	00
2022	07	04	NA	20	30
```

## Input Data

### `partial.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/propagate_na_values/inputs/partial.tsv`
- Size: 94 bytes

```text
year	month	day	hour	minute	second
2020	05	NA	10	30	45
2021	NA	12	09	15	00
2022	07	04	NA	20	30
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/propagate_na_values/solution.R`
- Size: 574 bytes

```r
result_df <- read.delim(file.path("inputs", "partial.tsv"), check.names = FALSE, stringsAsFactors = FALSE, na.strings = c("NA", ""))
cols <- c("year", "month", "day", "hour", "minute", "second")
for (i in seq_len(nrow(result_df))) {
  missing_seen <- FALSE
  for (col in cols) {
    if (missing_seen || is.na(result_df[[col]][i]) || result_df[[col]][i] == "") {
      result_df[[col]][i] <- NA_character_
      missing_seen <- TRUE
    }
  }
}

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE, na = "")
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/propagate_na_values/outputs/result.csv`
- Size: 85 bytes

```csv
"year","month","day","hour","minute","second"
2020,"5",,,,
2021,,,,,
2022,"7","4",,,
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(stringr)

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
df <- readr::read_tsv(
  file = file.path("inputs", "partial.tsv"),
  col_types = cols(
    year   = col_integer(),
    month  = col_character(),
    day    = col_character(),
    hour   = col_character(),
    minute = col_character(),
    second = col_character()
  )
)

# Propagate NA values (NA in any component → all components NA)
df_out <- df %>%
  mutate(
    any_na = if_else(
      is.na(year) | is.na(month) | is.na(day) |
        is.na(hour) | is.na(minute) | is.na(second),
      TRUE, FALSE
    )
  ) %>%
  mutate(
    year   = if_else(any_na, NA_integer_, year),
    month  = if_else(any_na, NA_character_, month),
    day    = if_else(any_na, NA_character_, day),
    hour   = if_else(any_na, NA_character_, hour),
    minute = if_else(any_na, NA_character_, minute),
    second = if_else(any_na, NA_character_, second)
  ) %>%
  select(year, month, day, hour, minute, second)

# Write output
readr::write_csv(df_out, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__propagate_na_values/sample_00/case_01/llm_outputs/result.csv`
- Size: 52 bytes

```csv
year,month,day,hour,minute,second
,,,,,
,,,,,
,,,,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__propagate_na_values/sample_00/case_01/stderr.txt`
- Size: 1333 bytes

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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union
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
          "reason": "Numeric missingness mismatch in column: year"
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
            "reason": "Numeric missingness mismatch in column: year"
          }
        }
      }
    }
  ]
}
```
