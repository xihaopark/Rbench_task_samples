# Case 116: pharmaverse/admiral/derive_vars_duration

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_duration`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform derive vars duration using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, STARTDT, ENDDT, DURD
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (89 bytes)
USUBJID	STARTDT	ENDDT
01	2020-01-01	2020-01-10
02	2020-02-01	2020-02-01
03	2020-03-01	NA
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_duration/inputs/dataset.tsv`
- Size: 89 bytes

```text
USUBJID	STARTDT	ENDDT
01	2020-01-01	2020-01-10
02	2020-02-01	2020-02-01
03	2020-03-01	NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_duration/solution.R`
- Size: 566 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
startdt <- as.Date(dataset$STARTDT)
enddt <- as.Date(ifelse(toupper(dataset$ENDDT) == "NA", NA_character_, dataset$ENDDT))
durd <- ifelse(is.na(startdt) | is.na(enddt), NA_integer_, as.integer(enddt - startdt) + 1L)
result_df <- data.frame(USUBJID = dataset$USUBJID, STARTDT = startdt, ENDDT = enddt, DURD = durd, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_duration/outputs/result.csv`
- Size: 107 bytes

```csv
"USUBJID","STARTDT","ENDDT","DURD"
1,2020-01-01,2020-01-10,10
2,2020-02-01,2020-02-01,1
3,2020-03-01,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(lubridate)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
infile <- file.path("inputs", "dataset.tsv")
dat <- read_tsv(infile, show_col_types = FALSE, na = c("NA", ""))

# Derive duration in days (inclusive) per admiral-like approach
# DURD = ENDDT - STARTDT + 1, NA if either date is missing
result <- dat %>%
  mutate(
    STARTDT = ymd(STARTDT),
    ENDDT   = ymd(ENDDT),
    DURD    = if_else(
      !is.na(STARTDT) & !is.na(ENDDT),
      as.integer(ENDDT - STARTDT + 1L),
      NA_integer_
    )
  ) %>%
  select(USUBJID, STARTDT, ENDDT, DURD)

# Write output
outfile <- file.path("outputs", "result.csv")
write_csv(result, outfile, na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_duration/sample_00/case_01/llm_outputs/result.csv`
- Size: 98 bytes

```csv
USUBJID,STARTDT,ENDDT,DURD
01,2020-01-01,2020-01-10,10
02,2020-02-01,2020-02-01,1
03,2020-03-01,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_duration/sample_00/case_01/stderr.txt`
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
