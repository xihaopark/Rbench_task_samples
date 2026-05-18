# Case 132: pharmaverse/admiral/extract_duplicate_records

## Case Metadata

- Task ID: `pharmaverse/admiral/extract_duplicate_records`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform extract duplicate records using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVISIT, AVAL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (113 bytes)
USUBJID	PARAMCD	AVISIT	AVAL
01	ALT	Week 1	10
01	ALT	Week 1	10
02	ALT	Week 1	20
03	AST	Week 1	30
03	AST	Week 1	31
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extract_duplicate_records/inputs/dataset.tsv`
- Size: 113 bytes

```text
USUBJID	PARAMCD	AVISIT	AVAL
01	ALT	Week 1	10
01	ALT	Week 1	10
02	ALT	Week 1	20
03	AST	Week 1	30
03	AST	Week 1	31
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extract_duplicate_records/solution.R`
- Size: 390 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
key <- paste(dataset$USUBJID, dataset$PARAMCD, dataset$AVISIT, sep = "\r")
result_df <- dataset[duplicated(key) | duplicated(key, fromLast = TRUE), , drop = FALSE]

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extract_duplicate_records/outputs/result.csv`
- Size: 116 bytes

```csv
"USUBJID","PARAMCD","AVISIT","AVAL"
1,"ALT","Week 1",10
1,"ALT","Week 1",10
3,"AST","Week 1",30
3,"AST","Week 1",31
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input data
input_path <- file.path("inputs", "dataset.tsv")
dat <- read_tsv(input_path, col_types = cols())

# Find duplicated records based on all required columns
dup_flag <- duplicated(dat[, c("USUBJID", "PARAMCD", "AVISIT", "AVAL")]) |
  duplicated(dat[, c("USUBJID", "PARAMCD", "AVISIT", "AVAL")], fromLast = TRUE)

result <- dat[dup_flag, c("USUBJID", "PARAMCD", "AVISIT", "AVAL")]

# Write output
output_path <- file.path("outputs", "result.csv")
write_csv(result, output_path)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__extract_duplicate_records/sample_00/case_01/llm_outputs/result.csv`
- Size: 62 bytes

```csv
USUBJID,PARAMCD,AVISIT,AVAL
01,ALT,Week 1,10
01,ALT,Week 1,10
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__extract_duplicate_records/sample_00/case_01/stderr.txt`
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
  "failure_stage": "schema_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "schema_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "schema_mismatch",
          "reason": "Shape mismatch: ref=(4, 4) vs llm=(2, 4)"
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
            "stage": "schema_mismatch",
            "tier": "output_bad",
            "reason": "Shape mismatch: ref=(4, 4) vs llm=(2, 4)"
          }
        }
      }
    }
  ]
}
```
