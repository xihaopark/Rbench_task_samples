# Case 061: pharmaverse/admiral/compute_dtf

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_dtf`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform compute dtf using the admiral clinical task contract.

Input: dt.tsv, dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, dt, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dt.tsv (39 bytes)
dt
2020-01-01
2020-06-01
2020-01-01
NA

### dtc.tsv (31 bytes)
dtc
2020-01-01
2020-06
2020
NA
```

## Input Data

### `dt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_dtf/inputs/dt.tsv`
- Size: 39 bytes

```text
dt
2020-01-01
2020-06-01
2020-01-01
NA
```

### `dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_dtf/inputs/dtc.tsv`
- Size: 31 bytes

```text
dtc
2020-01-01
2020-06
2020
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_dtf/solution.R`
- Size: 551 bytes

```r
suppressPackageStartupMessages(library(admiral))

dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE, blank.lines.skip = FALSE)$dtc)
dt_raw <- read.delim(file.path("inputs", "dt.tsv"), check.names = FALSE, stringsAsFactors = FALSE, blank.lines.skip = FALSE)$dt
dt <- as.Date(dt_raw)
result <- admiral::compute_dtf(dtc = dtc, dt = dt)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(dtc = dtc, dt = dt, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_dtf/outputs/result.csv`
- Size: 103 bytes

```csv
"dtc","dt","result"
"2020-01-01",2020-01-01,NA
"2020-06",2020-06-01,"D"
"2020",2020-01-01,"M"
NA,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(lubridate)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
dt   <- read_tsv("inputs/dt.tsv", col_types = cols(.default = col_character()))
dtc  <- read_tsv("inputs/dtc.tsv", col_types = cols(.default = col_character()))

# Ensure same length
n <- max(nrow(dt), nrow(dtc))
dt  <- dt  %>% slice_head(n = n)
dtc <- dtc %>% slice_head(n = n)

# Parse dt as Date
dt_parsed <- ymd(dt$dt)

# Function to parse dtc as Date (ADaM-like partial date handling)
parse_dtc <- function(x) {
  x <- str_trim(x)
  ifelse(
    is.na(x) | x == "",
    NA_Date_,
    ifelse(
      str_detect(x, "^\\d{4}-\\d{2}-\\d{2}$"),
      ymd(x),
      ifelse(
        str_detect(x, "^\\d{4}-\\d{2}$"),
        ymd(paste0(x, "-01")),
        ifelse(
          str_detect(x, "^\\d{4}$"),
          ymd(paste0(x, "-01-01")),
          NA_Date_
        )
      )
    )
  )
}

dtc_parsed <- parse_dtc(dtc$dtc)

# Compute dtf: difference in days (dt - dtc) per ADaM-style
# If either is NA, result is NA
result <- ifelse(is.na(dt_parsed) | is.na(dtc_parsed),
                 NA_integer_,
                 as.integer(dt_parsed - dtc_parsed))

# Assemble result
out <- tibble(
  dtc    = dtc$dtc,
  dt     = dt$dt,
  result = result
)

# Write output
write_csv(out, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_dtf/sample_00/case_01/llm_outputs/result.csv`
- Size: 80 bytes

```csv
dtc,dt,result
2020-01-01,2020-01-01,0
2020-06,2020-06-01,0
2020,2020-01-01,0
,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_dtf/sample_00/case_01/stderr.txt`
- Size: 1213 bytes

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
Warning messages:
1:  2 failed to parse.
2:  3 failed to parse.
3:  3 failed to parse.
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
