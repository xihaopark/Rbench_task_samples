# Case 189: pharmaverse/metatools/validate_verbose

## Case Metadata

- Task ID: `pharmaverse/metatools/validate_verbose`
- Package: `metatools`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform validate verbose using the metatools clinical task contract.

Input: verbose.tsv
Output: result.csv


Required columns for result.csv: verbose, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### verbose.tsv (16 bytes)
verbose
message
```

## Input Data

### `verbose.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/validate_verbose/inputs/verbose.tsv`
- Size: 16 bytes

```text
verbose
message
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/validate_verbose/solution.R`
- Size: 531 bytes

```r
verbose_df <- read.delim(
  file.path("inputs", "verbose.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

choices <- c("message", "warn", "silent")
verbose <- as.character(verbose_df[[1]][1])
if (is.na(verbose) || !(verbose %in% choices)) {
  verbose <- "message"
}
result <- match.arg(verbose, choices)

result_df <- data.frame(
  verbose = verbose,
  result = result,
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/validate_verbose/outputs/result.csv`
- Size: 39 bytes

```csv
"verbose","result"
"message","message"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
verbose_path <- file.path("inputs", "verbose.tsv")
verbose_df <- read_tsv(verbose_path, show_col_types = FALSE)

# Determine result: must contain required column 'verbose'
# and values should be logical (TRUE/FALSE) or 0/1
result_df <- verbose_df %>%
  mutate(
    result = case_when(
      !("verbose" %in% colnames(verbose_df)) ~ FALSE,
      is.logical(verbose) ~ TRUE,
      is.numeric(verbose) & all(verbose %in% c(0, 1, NA)) ~ TRUE,
      TRUE ~ FALSE
    )
  ) %>%
  transmute(verbose, result)

# Write output
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__validate_verbose/sample_00/case_01/llm_outputs/result.csv`
- Size: 29 bytes

```csv
verbose,result
message,FALSE
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__validate_verbose/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result"
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
            "reason": "Value mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
