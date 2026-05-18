# Case 140: pharmaverse/admiral/get_admiral_option

## Case Metadata

- Task ID: `pharmaverse/admiral/get_admiral_option`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform get admiral option using the admiral clinical task contract.

Input: option.tsv
Output: result.csv


Required columns for result.csv: option, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### option.tsv (22 bytes)
option
"subject_keys"
```

## Input Data

### `option.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_admiral_option/inputs/option.tsv`
- Size: 22 bytes

```text
option
"subject_keys"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_admiral_option/solution.R`
- Size: 546 bytes

```r
suppressPackageStartupMessages(library(admiral))

option_df <- read.delim(file.path("inputs", "option.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
option <- as.character(option_df[[ncol(option_df)]][1])

valid_opts <- c("subject_keys", "signif_digits", "max_n_char")
if (!option %in% valid_opts) option <- valid_opts[1]

result <- admiral::get_admiral_option(option)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(option = option, result = as.character(result)), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_admiral_option/outputs/result.csv`
- Size: 68 bytes

```csv
"option","result"
"subject_keys","STUDYID"
"subject_keys","USUBJID"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(admiral)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read options
opt_df <- read_tsv(
  file = file.path("inputs", "option.tsv"),
  show_col_types = FALSE
)

# Helper to safely get admiral option value as character
get_admiral_option_value <- function(opt_name) {
  val <- get_admiral_option(opt_name)
  if (is.null(val)) {
    return(NA_character_)
  }
  if (is.atomic(val) && length(val) == 1) {
    return(as.character(val))
  }
  # For non-scalar options, serialize to JSON-like string
  paste(capture.output(str(val, give.attr = FALSE)), collapse = " ")
}

result <- opt_df %>%
  mutate(
    result = vapply(option, get_admiral_option_value, character(1))
  ) %>%
  select(option, result)

write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_admiral_option/sample_00/case_01/llm_outputs/result.csv`
- Size: 77 bytes

```csv
option,result
subject_keys,List of 2  $ : symbol STUDYID  $ : symbol USUBJID
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_admiral_option/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(2, 2) vs llm=(1, 2)"
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
            "reason": "Shape mismatch: ref=(2, 2) vs llm=(1, 2)"
          }
        }
      }
    }
  ]
}
```
