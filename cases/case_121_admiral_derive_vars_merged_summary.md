# Case 121: pharmaverse/admiral/derive_vars_merged_summary

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_merged_summary`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive vars merged summary using the admiral clinical task contract.

Input: dataset.tsv, summary.tsv
Output: result.csv


Required columns for result.csv: USUBJID, AVISIT, AVAL, MEAN_BASE
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (72 bytes)
USUBJID	AVISIT	AVAL
01	Week 1	10
01	Week 2	15
02	Week 1	20
02	Week 2	18

### summary.tsv (34 bytes)
USUBJID	MEAN_BASE
01	12.5
02	19.0
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_summary/inputs/dataset.tsv`
- Size: 72 bytes

```text
USUBJID	AVISIT	AVAL
01	Week 1	10
01	Week 2	15
02	Week 1	20
02	Week 2	18
```

### `summary.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_summary/inputs/summary.tsv`
- Size: 34 bytes

```text
USUBJID	MEAN_BASE
01	12.5
02	19.0
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_summary/solution.R`
- Size: 412 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
summary <- read.delim(file.path("inputs", "summary.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result_df <- merge(dataset, summary, by = "USUBJID", all.x = TRUE, sort = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged_summary/outputs/result.csv`
- Size: 110 bytes

```csv
"USUBJID","AVISIT","AVAL","MEAN_BASE"
1,"Week 1",10,12.5
1,"Week 2",15,12.5
2,"Week 1",20,19
2,"Week 2",18,19
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input data
dataset <- read.delim(
  file = "inputs/dataset.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

summary_df <- read.delim(
  file = "inputs/summary.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

# Derive vars merged summary (merge MEAN_BASE onto dataset by USUBJID)
result <- dataset %>%
  left_join(summary_df, by = "USUBJID") %>%
  select(USUBJID, AVISIT, AVAL, MEAN_BASE)

# Write output as CSV
write.csv(
  result,
  file = "outputs/result.csv",
  row.names = FALSE,
  na = ""
)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_merged_summary/sample_00/case_01/llm_outputs/result.csv`
- Size: 110 bytes

```csv
"USUBJID","AVISIT","AVAL","MEAN_BASE"
1,"Week 1",10,12.5
1,"Week 2",15,12.5
2,"Week 1",20,19
2,"Week 2",18,19
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_merged_summary/sample_00/case_01/stderr.txt`
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
