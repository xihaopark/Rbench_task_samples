# Case 144: pharmaverse/admiral/get_hori_data

## Case Metadata

- Task ID: `pharmaverse/admiral/get_hori_data`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform get hori data using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, ALT, AST, BILI
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (85 bytes)
USUBJID	PARAMCD	AVAL
01	ALT	20
01	AST	18
01	BILI	0.7
02	ALT	40
02	AST	35
... [1 more lines omitted]
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_hori_data/inputs/dataset.tsv`
- Size: 85 bytes

```text
USUBJID	PARAMCD	AVAL
01	ALT	20
01	AST	18
01	BILI	0.7
02	ALT	40
02	AST	35
02	BILI	1.1
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_hori_data/solution.R`
- Size: 587 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
subjects <- sort(unique(dataset$USUBJID))
params <- sort(unique(dataset$PARAMCD))
result_df <- data.frame(USUBJID = subjects, stringsAsFactors = FALSE)
for (param in params) {
  result_df[[param]] <- NA_real_
}
for (i in seq_len(nrow(dataset))) {
  row <- match(dataset$USUBJID[i], result_df$USUBJID)
  result_df[[dataset$PARAMCD[i]]][row] <- dataset$AVAL[i]
}

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_hori_data/outputs/result.csv`
- Size: 53 bytes

```csv
"USUBJID","ALT","AST","BILI"
1,20,18,0.7
2,40,35,1.1
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tidyr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
infile <- file.path("inputs", "dataset.tsv")
dat <- read_tsv(infile, show_col_types = FALSE)

# Pivot to get horizontal data
res <- dat %>%
  mutate(PARAMCD = toupper(PARAMCD)) %>%
  filter(PARAMCD %in% c("ALT", "AST", "BILI")) %>%
  pivot_wider(
    id_cols = USUBJID,
    names_from = PARAMCD,
    values_from = AVAL
  ) %>%
  select(USUBJID, ALT, AST, BILI)

# Write output
outfile <- file.path("outputs", "result.csv")
write_csv(res, outfile)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_hori_data/sample_00/case_01/llm_outputs/result.csv`
- Size: 47 bytes

```csv
USUBJID,ALT,AST,BILI
01,20,18,0.7
02,40,35,1.1
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_hori_data/sample_00/case_01/stderr.txt`
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
