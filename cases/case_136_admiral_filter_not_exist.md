# Case 136: pharmaverse/admiral/filter_not_exist

## Case Metadata

- Task ID: `pharmaverse/admiral/filter_not_exist`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform filter not exist using the admiral clinical task contract.

Input: dataset.tsv, dataset_add.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVAL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (51 bytes)
USUBJID	PARAMCD	AVAL
01	ALT	20
02	ALT	35
03	AST	18

### dataset_add.tsv (71 bytes)
USUBJID	PARAMCD	AVAL
01	ALT	20
02	ALT	35
03	AST	18
04	ALT	42
05	AST	22
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_not_exist/inputs/dataset.tsv`
- Size: 51 bytes

```text
USUBJID	PARAMCD	AVAL
01	ALT	20
02	ALT	35
03	AST	18
```

### `dataset_add.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_not_exist/inputs/dataset_add.tsv`
- Size: 71 bytes

```text
USUBJID	PARAMCD	AVAL
01	ALT	20
02	ALT	35
03	AST	18
04	ALT	42
05	AST	22
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_not_exist/solution.R`
- Size: 487 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dataset_add <- read.delim(file.path("inputs", "dataset_add.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
key <- function(data) paste(data$USUBJID, data$PARAMCD, sep = "\r")
result_df <- dataset_add[!(key(dataset_add) %in% key(dataset)), , drop = FALSE]

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_not_exist/outputs/result.csv`
- Size: 49 bytes

```csv
"USUBJID","PARAMCD","AVAL"
4,"ALT",42
5,"AST",22
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input datasets
dataset <- read.delim(
  file = "inputs/dataset.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

dataset_add <- read.delim(
  file = "inputs/dataset_add.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

# Filter not exist: records in dataset_add that are not in dataset
result <- dataset_add %>%
  anti_join(dataset, by = c("USUBJID", "PARAMCD", "AVAL")) %>%
  select(USUBJID, PARAMCD, AVAL)

# Write result
write.csv(result, file = "outputs/result.csv", row.names = FALSE, na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__filter_not_exist/sample_00/case_01/llm_outputs/result.csv`
- Size: 49 bytes

```csv
"USUBJID","PARAMCD","AVAL"
4,"ALT",42
5,"AST",22
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__filter_not_exist/sample_00/case_01/stderr.txt`
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
