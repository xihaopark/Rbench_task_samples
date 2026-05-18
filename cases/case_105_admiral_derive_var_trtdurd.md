# Case 105: pharmaverse/admiral/derive_var_trtdurd

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_var_trtdurd`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive var trtdurd using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, TRTSDT, TRTEDT, TRTDURD
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (89 bytes)
USUBJID	TRTSDT	TRTEDT
01	2020-01-01	2020-01-10
02	2020-02-01	2020-02-01
03	2020-03-01	NA
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_trtdurd/inputs/dataset.tsv`
- Size: 89 bytes

```text
USUBJID	TRTSDT	TRTEDT
01	2020-01-01	2020-01-10
02	2020-02-01	2020-02-01
03	2020-03-01	NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_trtdurd/solution.R`
- Size: 576 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
trtsdt <- as.Date(dataset$TRTSDT)
trtedt <- as.Date(ifelse(toupper(dataset$TRTEDT) == "NA", NA_character_, dataset$TRTEDT))
trtdurd <- ifelse(is.na(trtsdt) | is.na(trtedt), NA_integer_, as.integer(trtedt - trtsdt) + 1L)
result_df <- data.frame(USUBJID = dataset$USUBJID, TRTSDT = trtsdt, TRTEDT = trtedt, TRTDURD = trtdurd, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_trtdurd/outputs/result.csv`
- Size: 110 bytes

```csv
"USUBJID","TRTSDT","TRTEDT","TRTDURD"
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
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
adsl <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    TRTSDT  = col_character(),
    TRTEDT  = col_character()
  )
)

# Derive TRTSDT and TRTEDT as Date
adsl_der <- adsl %>%
  mutate(
    TRTSDT = ymd(TRTSDT),
    TRTEDT = ymd(TRTEDT)
  ) %>%
  mutate(
    TRTDURD = if_else(
      !is.na(TRTSDT) & !is.na(TRTEDT),
      as.integer(TRTEDT - TRTSDT) + 1L,
      NA_integer_
    )
  ) %>%
  select(USUBJID, TRTSDT, TRTEDT, TRTDURD)

# Write output
write_csv(adsl_der, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_trtdurd/sample_00/case_01/llm_outputs/result.csv`
- Size: 101 bytes

```csv
USUBJID,TRTSDT,TRTEDT,TRTDURD
01,2020-01-01,2020-01-10,10
02,2020-02-01,2020-02-01,1
03,2020-03-01,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_trtdurd/sample_00/case_01/stderr.txt`
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
