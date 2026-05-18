# Case 141: pharmaverse/admiral/get_dt_dtm_range

## Case Metadata

- Task ID: `pharmaverse/admiral/get_dt_dtm_range`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform get dt dtm range using the admiral clinical task contract.

Input: dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, lower, upper
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dtc.tsv (51 bytes)
dtc
2020
2020-06
2020-06-15
2020-06-15T12:30:00
NA
```

## Input Data

### `dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_dt_dtm_range/inputs/dtc.tsv`
- Size: 51 bytes

```text
dtc
2020
2020-06
2020-06-15
2020-06-15T12:30:00
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_dt_dtm_range/solution.R`
- Size: 1241 bytes

```r
dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$dtc)
missing <- is.na(dtc) | toupper(dtc) == "NA" | dtc == ""
lower <- upper <- rep(NA_character_, length(dtc))
year_only <- grepl("^[0-9]{4}$", dtc)
month_only <- grepl("^[0-9]{4}-[0-9]{2}$", dtc)
date_only <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", dtc)
complete_dtm <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", dtc)
lower[year_only] <- paste0(dtc[year_only], "-01-01")
upper[year_only] <- paste0(dtc[year_only], "-12-31")
lower[month_only] <- paste0(dtc[month_only], "-01")
upper[month_only] <- as.character(as.Date(paste0(dtc[month_only], "-01")) + 32)
upper[month_only] <- as.character(as.Date(format(as.Date(upper[month_only]), "%Y-%m-01")) - 1)
lower[date_only] <- dtc[date_only]
upper[date_only] <- dtc[date_only]
lower[complete_dtm] <- sub("T", " ", dtc[complete_dtm])
upper[complete_dtm] <- sub("T", " ", dtc[complete_dtm])
lower[missing] <- NA_character_
upper[missing] <- NA_character_
result_df <- data.frame(dtc = dtc, lower = lower, upper = upper, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_dt_dtm_range/outputs/result.csv`
- Size: 205 bytes

```csv
"dtc","lower","upper"
"2020","2020-01-01","2020-12-31"
"2020-06","2020-06-01","2020-06-30"
"2020-06-15","2020-06-15","2020-06-15"
"2020-06-15T12:30:00","2020-06-15 12:30:00","2020-06-15 12:30:00"
NA,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)
library(lubridate)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
dtc_path <- file.path("inputs", "dtc.tsv")
dtc_df <- read_tsv(dtc_path, show_col_types = FALSE, na = c("", "NA"))

# Function to derive lower and upper bounds from DTC (partial datetime)
derive_dtm_range <- function(dtc) {
  if (is.na(dtc) || dtc == "") {
    return(list(lower = NA_character_, upper = NA_character_))
  }

  # Detect format based on pattern
  # Year only: YYYY
  if (str_detect(dtc, "^\\d{4}$")) {
    year <- as.integer(dtc)
    lower <- ymd_hms(sprintf("%04d-01-01 00:00:00", year), tz = "UTC")
    upper <- ymd_hms(sprintf("%04d-12-31 23:59:59", year), tz = "UTC")
  } else if (str_detect(dtc, "^\\d{4}-\\d{2}$")) {
    # Year-month: YYYY-MM
    year <- as.integer(str_sub(dtc, 1, 4))
    month <- as.integer(str_sub(dtc, 6, 7))
    # Lower bound: first day of month 00:00:00
    lower <- ymd_hms(sprintf("%04d-%02d-01 00:00:00", year, month), tz = "UTC")
    # Upper bound: last day of month 23:59:59
    last_day <- days_in_month(ymd(sprintf("%04d-%02d-01", year, month)))
    upper <- ymd_hms(sprintf("%04d-%02d-%02d 23:59:59", year, month, last_day), tz = "UTC")
  } else if (str_detect(dtc, "^\\d{4}-\\d{2}-\\d{2}$")) {
    # Full date: YYYY-MM-DD
    lower <- ymd_hms(paste0(dtc, " 00:00:00"), tz = "UTC")
    upper <- ymd_hms(paste0(dtc, " 23:59:59"), tz = "UTC")
  } else if (str_detect(dtc, "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:?\\d{0,2}$")) {
    # Full datetime (up to seconds)
    # Normalize to "YYYY-MM-DDTHH:MM:SS"
    parts <- str_split_fixed(dtc, "T", 2)
    date_part <- parts[, 1]
    time_part <- parts[, 2]

    # If seconds missing, add ":00"
    if (str_detect(time_part, "^\\d{2}:\\d{2}$")) {
      time_part <- paste0(time_part, ":00")
    }

    dt_full <- ymd_hms(paste(date_part, time_part), tz = "UTC")
    lower <- dt_full
    upper <- dt_full
  } else {
    # Unrecognized pattern
    return(list(lower = NA_character_, upper = NA_character_))
  }

  list(
    lower = format(lower, "%Y-%m-%dT%H:%M:%S"),
    upper = format(upper, "%Y-%m-%dT%H:%M:%S")
  )
}

res <- dtc_df %>%
  mutate(
    tmp = lapply(dtc, derive_dtm_range),
    lower = vapply(tmp, function(x) x$lower, character(1)),
    upper = vapply(tmp, function(x) x$upper, character(1))
  ) %>%
  select(dtc, lower, upper)

# Write output
write_csv(res, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_dt_dtm_range/sample_00/case_01/llm_outputs/result.csv`
- Size: 223 bytes

```csv
dtc,lower,upper
2020,2020-01-01T00:00:00,2020-12-31T23:59:59
2020-06,2020-06-01T00:00:00,2020-06-30T23:59:59
2020-06-15,2020-06-15T00:00:00,2020-06-15T23:59:59
2020-06-15T12:30:00,2020-06-15T12:30:00,2020-06-15T12:30:00
,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_dt_dtm_range/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: lower"
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
            "reason": "Value mismatch in column: lower"
          }
        }
      }
    }
  ]
}
```
