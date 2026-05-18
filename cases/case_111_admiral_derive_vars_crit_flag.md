# Case 111: pharmaverse/admiral/derive_vars_crit_flag

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_crit_flag`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform derive vars crit flag using the admiral clinical task contract.

Input: dataset.tsv, description.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVAL, ULN, CRIT1, CRIT1FL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (64 bytes)
USUBJID	PARAMCD	AVAL	ULN
01	ALT	45	20
02	ALT	75	20
03	AST	30	20

### description.tsv (45 bytes)
description
ALT greater than three times ULN
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_crit_flag/inputs/dataset.tsv`
- Size: 64 bytes

```text
USUBJID	PARAMCD	AVAL	ULN
01	ALT	45	20
02	ALT	75	20
03	AST	30	20
```

### `description.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_crit_flag/inputs/description.tsv`
- Size: 45 bytes

```text
description
ALT greater than three times ULN
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_crit_flag/solution.R`
- Size: 504 bytes

```r
result_df <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
description <- as.character(read.delim(file.path("inputs", "description.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$description[1])
result_df$CRIT1 <- description
result_df$CRIT1FL <- ifelse(result_df$PARAMCD == "ALT" & result_df$AVAL > 3 * result_df$ULN, "Y", "N")

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_crit_flag/outputs/result.csv`
- Size: 210 bytes

```csv
"USUBJID","PARAMCD","AVAL","ULN","CRIT1","CRIT1FL"
1,"ALT",45,20,"ALT greater than three times ULN","N"
2,"ALT",75,20,"ALT greater than three times ULN","Y"
3,"AST",30,20,"ALT greater than three times ULN","N"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols()
)

description <- read_tsv(
  file = file.path("inputs", "description.tsv"),
  col_types = cols()
)

# Get CRIT1 from description
crit1_text <- description$description[1]

# Derive CRIT1FL based on ALT greater than three times ULN
result <- dataset %>%
  mutate(
    CRIT1 = crit1_text,
    CRIT1FL = case_when(
      PARAMCD == "ALT" & AVAL > 3 * ULN ~ "Y",
      TRUE ~ NA_character_
    )
  ) %>%
  select(USUBJID, PARAMCD, AVAL, ULN, CRIT1, CRIT1FL)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_crit_flag/sample_00/case_01/llm_outputs/result.csv`
- Size: 181 bytes

```csv
USUBJID,PARAMCD,AVAL,ULN,CRIT1,CRIT1FL
01,ALT,45,20,ALT greater than three times ULN,
02,ALT,75,20,ALT greater than three times ULN,Y
03,AST,30,20,ALT greater than three times ULN,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_crit_flag/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: CRIT1FL"
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
            "reason": "Value mismatch in column: CRIT1FL"
          }
        }
      }
    }
  ]
}
```
