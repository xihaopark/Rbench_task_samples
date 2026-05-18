# Case 148: pharmaverse/admiral/get_joined_sub_data

## Case Metadata

- Task ID: `pharmaverse/admiral/get_joined_sub_data`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform get joined sub data using the admiral clinical task contract.

Input: left.tsv, right.tsv
Output: result.csv


Required columns for result.csv: USUBJID, AVAL, TRT01A
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### left.tsv (31 bytes)
USUBJID	AVAL
01	10
02	20
03	30

### right.tsv (36 bytes)
USUBJID	TRT01A
01	Drug A
02	Placebo
```

## Input Data

### `left.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_joined_sub_data/inputs/left.tsv`
- Size: 31 bytes

```text
USUBJID	AVAL
01	10
02	20
03	30
```

### `right.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_joined_sub_data/inputs/right.tsv`
- Size: 36 bytes

```text
USUBJID	TRT01A
01	Drug A
02	Placebo
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_joined_sub_data/solution.R`
- Size: 397 bytes

```r
left <- read.delim(file.path("inputs", "left.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
right <- read.delim(file.path("inputs", "right.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result_df <- merge(left, right, by = "USUBJID", all.x = TRUE, sort = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_joined_sub_data/outputs/result.csv`
- Size: 63 bytes

```csv
"USUBJID","AVAL","TRT01A"
1,10,"Drug A"
2,20,"Placebo"
3,30,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input data
left <- read_tsv(
  file = file.path("inputs", "left.tsv"),
  col_types = cols(.default = col_character())
)

right <- read_tsv(
  file = file.path("inputs", "right.tsv"),
  col_types = cols(.default = col_character())
)

# Perform left join by USUBJID (admiral-like join on key)
result <- left %>%
  inner_join(right, by = "USUBJID") %>%
  select(USUBJID, AVAL, TRT01A)

# Write result
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_joined_sub_data/sample_00/case_01/llm_outputs/result.csv`
- Size: 47 bytes

```csv
USUBJID,AVAL,TRT01A
01,10,Drug A
02,20,Placebo
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_joined_sub_data/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(3, 3) vs llm=(2, 3)"
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
            "reason": "Shape mismatch: ref=(3, 3) vs llm=(2, 3)"
          }
        }
      }
    }
  ]
}
```
