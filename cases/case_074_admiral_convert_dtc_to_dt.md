# Case 074: pharmaverse/admiral/convert_dtc_to_dt

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_dtc_to_dt`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform convert dtc to dt using the admiral clinical task contract.

Input: dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dtc.tsv (31 bytes)
dtc
2020-01-01
2020-06
2020
NA
```

## Input Data

### `dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_dtc_to_dt/inputs/dtc.tsv`
- Size: 31 bytes

```text
dtc
2020-01-01
2020-06
2020
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_dtc_to_dt/solution.R`
- Size: 462 bytes

```r
suppressPackageStartupMessages(library(admiral))

dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE, blank.lines.skip = FALSE)$dtc)
complete_date <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", dtc)
result <- as.Date(ifelse(complete_date, dtc, NA_character_))

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(dtc = dtc, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_dtc_to_dt/outputs/result.csv`
- Size: 68 bytes

```csv
"dtc","result"
"2020-01-01",2020-01-01
"2020-06",NA
"2020",NA
NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
dtc_df <- read_tsv(
  file = file.path("inputs", "dtc.tsv"),
  col_types = cols(.default = col_character())
)

# Function to convert DTC to DT (YYYY-MM-DD) using CDISC/ADaM-like rules
convert_dtc_to_dt <- function(dtc) {
  if (is.na(dtc) || str_trim(dtc) == "") return(NA_character_)

  # Full date
  if (str_detect(dtc, "^\\d{4}-\\d{2}-\\d{2}$")) {
    return(dtc)
  }

  # Year-month only (YYYY-MM) -> assume day = 01
  if (str_detect(dtc, "^\\d{4}-\\d{2}$")) {
    return(paste0(dtc, "-01"))
  }

  # Year only (YYYY) -> assume month = 01, day = 01
  if (str_detect(dtc, "^\\d{4}$")) {
    return(paste0(dtc, "-01-01"))
  }

  # If pattern not recognized, return NA
  return(NA_character_)
}

result_df <- dtc_df %>%
  mutate(result = vapply(dtc, convert_dtc_to_dt, character(1))) %>%
  select(dtc, result)

# Write output
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_dtc_to_dt/sample_00/case_01/llm_outputs/result.csv`
- Size: 70 bytes

```csv
dtc,result
2020-01-01,2020-01-01
2020-06,2020-06-01
2020,2020-01-01
,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_dtc_to_dt/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result"
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
            "reason": "Value mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
