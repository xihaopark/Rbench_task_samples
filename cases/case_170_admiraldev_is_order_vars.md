# Case 170: pharmaverse/admiraldev/is_order_vars

## Case Metadata

- Task ID: `pharmaverse/admiraldev/is_order_vars`
- Package: `admiraldev`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform is order vars using the admiraldev clinical task contract.

Input: arg.tsv
Output: result.csv


Required columns for result.csv: is_order_vars
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### arg.tsv (24 bytes)
var
USUBJID
AVISITN
ADT
```

## Input Data

### `arg.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/is_order_vars/inputs/arg.tsv`
- Size: 24 bytes

```text
var
USUBJID
AVISITN
ADT
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/is_order_vars/solution.R`
- Size: 458 bytes

```r
suppressPackageStartupMessages(library(admiraldev))
suppressPackageStartupMessages(library(rlang))

vars <- read.delim(file.path("inputs", "arg.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$var
arg <- as.list(lapply(vars, sym))
class(arg) <- c("quosures", "list")
result <- data.frame(is_order_vars = admiraldev::is_order_vars(arg))
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/is_order_vars/outputs/result.csv`
- Size: 21 bytes

```csv
"is_order_vars"
TRUE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
arg <- read_tsv(
  file = file.path("inputs", "arg.tsv"),
  col_types = cols(.default = col_character())
)

vars <- arg$var

# Define is_order_vars according to admiraldev clinical conventions
is_order_vars <- vars %in% c("USUBJID", "STUDYID", "SUBJID", "SITEID") |
  str_detect(vars, "^TRTSTDT$|^TRTEDT$|^TRT[A-Z]*STDT$|^TRT[A-Z]*EDT$") |
  str_detect(vars, "DT$|DTM$|TM$|DY$|N$")

# Assemble result
result <- tibble(is_order_vars = is_order_vars)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__is_order_vars/sample_00/case_01/llm_outputs/result.csv`
- Size: 29 bytes

```csv
is_order_vars
TRUE
TRUE
TRUE
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__is_order_vars/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(1, 1) vs llm=(3, 1)"
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
            "reason": "Shape mismatch: ref=(1, 1) vs llm=(3, 1)"
          }
        }
      }
    }
  ]
}
```
