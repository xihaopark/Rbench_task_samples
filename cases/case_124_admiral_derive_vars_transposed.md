# Case 124: pharmaverse/admiral/derive_vars_transposed

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_transposed`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform derive vars transposed using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, IDVAR, IDVARVAL, LBDTC, LBFAST
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (157 bytes)
USUBJID	IDVAR	IDVARVAL	QNAM	QVAL
01	LBSEQ	1	LBDTC	2020-01-01
01	LBSEQ	1	LBFAST	Y
01	LBSEQ	2	LBDTC	2020-01-15
02	LBSEQ	1	LBDTC	2020-02-01
02	LBSEQ	1	LBFAST	N
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_transposed/inputs/dataset.tsv`
- Size: 157 bytes

```text
USUBJID	IDVAR	IDVARVAL	QNAM	QVAL
01	LBSEQ	1	LBDTC	2020-01-01
01	LBSEQ	1	LBFAST	Y
01	LBSEQ	2	LBDTC	2020-01-15
02	LBSEQ	1	LBDTC	2020-02-01
02	LBSEQ	1	LBFAST	N
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_transposed/solution.R`
- Size: 710 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
keys <- unique(dataset[c("USUBJID", "IDVAR", "IDVARVAL")])
keys <- keys[order(keys$USUBJID, keys$IDVARVAL), , drop = FALSE]
qnames <- sort(unique(dataset$QNAM))
result_df <- keys
for (qname in qnames) {
  result_df[[qname]] <- NA_character_
}
for (i in seq_len(nrow(dataset))) {
  hit <- result_df$USUBJID == dataset$USUBJID[i] &
    result_df$IDVAR == dataset$IDVAR[i] &
    result_df$IDVARVAL == dataset$IDVARVAL[i]
  result_df[[dataset$QNAM[i]]][hit] <- dataset$QVAL[i]
}

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE, na = "")
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_transposed/outputs/result.csv`
- Size: 130 bytes

```csv
"USUBJID","IDVAR","IDVARVAL","LBDTC","LBFAST"
1,"LBSEQ",1,"2020-01-01","Y"
1,"LBSEQ",2,"2020-01-15",
2,"LBSEQ",1,"2020-02-01","N"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(tidyr)
library(readr)
library(stringr)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
adsl_long <- read.delim(
  file = file.path("inputs", "dataset.tsv"),
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

# Pivot to wide (derive vars transposed equivalent)
result <- adsl_long %>%
  mutate(
    QNAM = str_trim(QNAM),
    QVAL = str_trim(QVAL)
  ) %>%
  pivot_wider(
    id_cols = c(USUBJID, IDVAR, IDVARVAL),
    names_from = QNAM,
    values_from = QVAL
  ) %>%
  select(USUBJID, IDVAR, IDVARVAL, LBDTC, LBFAST)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_transposed/sample_00/case_01/llm_outputs/result.csv`
- Size: 104 bytes

```csv
USUBJID,IDVAR,IDVARVAL,LBDTC,LBFAST
1,LBSEQ,1,2020-01-01,Y
1,LBSEQ,2,2020-01-15,
2,LBSEQ,1,2020-02-01,N
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_transposed/sample_00/case_01/stderr.txt`
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
