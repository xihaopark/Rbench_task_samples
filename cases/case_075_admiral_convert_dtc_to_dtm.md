# Case 075: pharmaverse/admiral/convert_dtc_to_dtm

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_dtc_to_dtm`
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
Write an R script to perform convert dtc to dtm using the admiral clinical task contract.

Input: dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dtc.tsv (40 bytes)
dtc
2020-01-01T12:30:00
2020-06
2020
NA
```

## Input Data

### `dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_dtc_to_dtm/inputs/dtc.tsv`
- Size: 40 bytes

```text
dtc
2020-01-01T12:30:00
2020-06
2020
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_dtc_to_dtm/solution.R`
- Size: 517 bytes

```r
suppressPackageStartupMessages(library(admiral))

dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE, blank.lines.skip = FALSE)$dtc)
complete_dtm <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", dtc)
result <- as.POSIXct(ifelse(complete_dtm, sub("T", " ", dtc), NA_character_), tz = "UTC")

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(dtc = dtc, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_dtc_to_dtm/outputs/result.csv`
- Size: 86 bytes

```csv
"dtc","result"
"2020-01-01T12:30:00",2020-01-01 12:30:00
"2020-06",NA
"2020",NA
NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
dtc <- read_tsv(
  file = file.path("inputs", "dtc.tsv"),
  col_types = cols(
    dtc = col_character()
  )
)

# Function to convert DTC -> DTM per CDISC/ADaM rules
convert_dtc_to_dtm <- function(x) {
  if (is.na(x) || str_trim(x) == "") return(NA_character_)

  # Keep original
  orig <- x

  # Split date/time
  parts <- str_split_fixed(orig, "T", 2)
  date_part <- parts[, 1]
  time_part <- ifelse(parts[, 2] == "", NA_character_, parts[, 2])

  # Derive full date (YYYY-MM-DD)
  date_len <- nchar(date_part)
  if (date_len >= 10) {
    full_date <- substr(date_part, 1, 10)
  } else if (date_len == 7) {
    # YYYY-MM
    full_date <- paste0(date_part, "-01")
  } else if (date_len == 4) {
    # YYYY
    full_date <- paste0(date_part, "-01-01")
  } else {
    return(NA_character_)
  }

  # Derive full time (HH:MM:SS)
  if (is.na(time_part) || time_part == "") {
    full_time <- "00:00:00"
  } else {
    # Handle time that might be HH, HH:MM, HH:MM:SS
    t_split <- str_split_fixed(time_part, ":", 3)
    h <- t_split[, 1]
    m <- ifelse(t_split[, 2] == "", "00", t_split[, 2])
    s <- ifelse(t_split[, 3] == "", "00", t_split[, 3])

    # Truncate to two digits each
    h <- str_sub(h, 1, 2)
    m <- str_sub(m, 1, 2)
    s <- str_sub(s, 1, 2)

    full_time <- paste(h, m, s, sep = ":")
  }

  paste(full_date, full_time)
}

result <- dtc %>%
  mutate(
    result = vapply(dtc, convert_dtc_to_dtm, character(1))
  ) %>%
  select(dtc, result)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_dtc_to_dtm/sample_00/case_01/llm_outputs/result.csv`
- Size: 106 bytes

```csv
dtc,result
2020-01-01T12:30:00,2020-01-01 12:30:00
2020-06,2020-06-01 00:00:00
2020,2020-01-01 00:00:00
,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_dtc_to_dtm/sample_00/case_01/stderr.txt`
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
