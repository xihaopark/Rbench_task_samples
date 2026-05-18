# Case 120: pharmaverse/admiral/derive_vars_merged_lookup

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_merged_lookup`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform derive vars merged lookup using the admiral clinical task contract.

Input: dataset.tsv, lookup.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVAL, PARAM
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (53 bytes)
USUBJID	PARAMCD	AVAL
01	ALT	10
02	AST	20
03	BILI	1.2

### lookup.tsv (74 bytes)
PARAMCD	PARAM
ALT	Alanine aminotransferase
AST	Aspartate aminotransferase
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_lookup/inputs/dataset.tsv`
- Size: 53 bytes

```text
USUBJID	PARAMCD	AVAL
01	ALT	10
02	AST	20
03	BILI	1.2
```

### `lookup.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_lookup/inputs/lookup.tsv`
- Size: 74 bytes

```text
PARAMCD	PARAM
ALT	Alanine aminotransferase
AST	Aspartate aminotransferase
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_lookup/solution.R`
- Size: 476 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
lookup <- read.delim(file.path("inputs", "lookup.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result_df <- merge(dataset, lookup, by = "PARAMCD", all.x = TRUE, sort = FALSE)
result_df <- result_df[, c("USUBJID", "PARAMCD", "AVAL", "PARAM")]

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_lookup/outputs/result.csv`
- Size: 129 bytes

```csv
"USUBJID","PARAMCD","AVAL","PARAM"
1,"ALT",10,"Alanine aminotransferase"
2,"AST",20,"Aspartate aminotransferase"
3,"BILI",1.2,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input datasets
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols()
)

lookup <- read_tsv(
  file = file.path("inputs", "lookup.tsv"),
  col_types = cols()
)

# Derive variables via merged lookup
result <- dataset %>%
  left_join(lookup, by = "PARAMCD") %>%
  select(USUBJID, PARAMCD, AVAL, PARAM)

# Write result to outputs
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_merged_lookup/sample_00/case_01/llm_outputs/result.csv`
- Size: 112 bytes

```csv
USUBJID,PARAMCD,AVAL,PARAM
01,ALT,10,Alanine aminotransferase
02,AST,20,Aspartate aminotransferase
03,BILI,1.2,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_merged_lookup/sample_00/case_01/stderr.txt`
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
