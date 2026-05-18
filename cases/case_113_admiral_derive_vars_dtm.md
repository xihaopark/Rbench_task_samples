# Case 113: pharmaverse/admiral/derive_vars_dtm

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_dtm`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform derive vars dtm using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, DTC, ADTM
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (75 bytes)
USUBJID	DTC
01	2020-01-15T08:30:00
02	2020-02-20T14:45:00
03	2020-03
04	NA
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_dtm/inputs/dataset.tsv`
- Size: 75 bytes

```text
USUBJID	DTC
01	2020-01-15T08:30:00
02	2020-02-20T14:45:00
03	2020-03
04	NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_dtm/solution.R`
- Size: 534 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dtc <- as.character(dataset$DTC)
complete_dtm <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", dtc)
adtm <- as.POSIXct(ifelse(complete_dtm, sub("T", " ", dtc), NA_character_), tz = "UTC")
result_df <- data.frame(USUBJID = dataset$USUBJID, DTC = dtc, ADTM = adtm, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_dtm/outputs/result.csv`
- Size: 134 bytes

```csv
"USUBJID","DTC","ADTM"
1,"2020-01-15T08:30:00",2020-01-15 08:30:00
2,"2020-02-20T14:45:00",2020-02-20 14:45:00
3,"2020-03",NA
4,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)
library(lubridate)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
df <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    DTC = col_character()
  )
)

# Helper to parse partial ISO8601-like dates
parse_partial_iso <- function(x) {
  if (is.na(x) || x == "") return(NA_character_)

  # Full datetime with time and 'T'
  if (str_detect(x, "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}$")) {
    dt <- ymd_hms(x, quiet = TRUE)
    return(format(dt, "%Y-%m-%dT%H:%M:%S"))
  }

  # Date only (YYYY-MM-DD)
  if (str_detect(x, "^\\d{4}-\\d{2}-\\d{2}$")) {
    dt <- ymd(x, quiet = TRUE)
    return(if (!is.na(dt)) paste0(format(dt, "%Y-%m-%d"), "T00:00:00") else NA_character_)
  }

  # Year-month only (YYYY-MM)
  if (str_detect(x, "^\\d{4}-\\d{2}$")) {
    dt <- ymd(paste0(x, "-01"), quiet = TRUE)
    return(if (!is.na(dt)) paste0(format(dt, "%Y-%m-%d"), "T00:00:00") else NA_character_)
  }

  # Year only (YYYY)
  if (str_detect(x, "^\\d{4}$")) {
    dt <- ymd(paste0(x, "-01-01"), quiet = TRUE)
    return(if (!is.na(dt)) paste0(format(dt, "%Y-%m-%d"), "T00:00:00") else NA_character_)
  }

  NA_character_
}

# Derive ADTM from DTC per admiral-like logic (assuming local time, no TZ)
result <- df %>%
  mutate(
    DTC = na_if(DTC, "NA"),
    ADTM = vapply(DTC, parse_partial_iso, character(1))
  ) %>%
  select(USUBJID, DTC, ADTM)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_dtm/sample_00/case_01/llm_outputs/result.csv`
- Size: 139 bytes

```csv
USUBJID,DTC,ADTM
01,2020-01-15T08:30:00,2020-01-15T08:30:00
02,2020-02-20T14:45:00,2020-02-20T14:45:00
03,2020-03,2020-03-01T00:00:00
04,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_dtm/sample_00/case_01/stderr.txt`
- Size: 1466 bytes

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


Attaching package: ‘lubridate’

The following objects are masked from ‘package:base’:

    date, intersect, setdiff, union
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
          "reason": "Value mismatch in column: ADTM"
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
            "reason": "Value mismatch in column: ADTM"
          }
        }
      }
    }
  ]
}
```
