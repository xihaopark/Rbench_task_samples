# Case 092: pharmaverse/admiral/default_qtc_paramcd

## Case Metadata

- Task ID: `pharmaverse/admiral/default_qtc_paramcd`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: QTC mapping not specified; package-specific convention

## Prompt

```text
Write an R script to perform default qtc paramcd using the admiral clinical task contract.

Input: method.tsv
Output: result.csv


Required columns for result.csv: method, PARAMCD
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### method.tsv (14 bytes)
method
Bazett
```

## Input Data

### `method.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/default_qtc_paramcd/inputs/method.tsv`
- Size: 14 bytes

```text
method
Bazett
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/default_qtc_paramcd/solution.R`
- Size: 391 bytes

```r
suppressPackageStartupMessages(library(admiral))

method <- as.character(read.delim(file.path("inputs", "method.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$method[[1]])
result <- admiral::default_qtc_paramcd(method)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(method = method, PARAMCD = result$PARAMCD), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/default_qtc_paramcd/outputs/result.csv`
- Size: 36 bytes

```csv
"method","PARAMCD"
"Bazett","QTCBR"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input method file
method_path <- file.path("inputs", "method.tsv")
method_df <- read_tsv(method_path, show_col_types = FALSE)

# Default mapping of QTC methods to PARAMCD per admiral conventions
# Extend this mapping as needed
qtc_paramcd_map <- tibble(
  method = c("Bazett", "Fridericia", "Framingham", "Hodges"),
  PARAMCD = c("QTCB", "QTCF", "QTCFRM", "QTCH")
)

# Join and derive PARAMCD
result <- method_df %>%
  left_join(qtc_paramcd_map, by = "method") %>%
  mutate(PARAMCD = if_else(is.na(PARAMCD), NA_character_, PARAMCD)) %>%
  select(method, PARAMCD)

# Write output
output_path <- file.path("outputs", "result.csv")
write_csv(result, output_path)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__default_qtc_paramcd/sample_00/case_01/llm_outputs/result.csv`
- Size: 27 bytes

```csv
method,PARAMCD
Bazett,QTCB
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__default_qtc_paramcd/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: PARAMCD"
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
            "reason": "Value mismatch in column: PARAMCD"
          }
        }
      }
    }
  ]
}
```
