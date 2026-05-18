# Case 139: pharmaverse/admiral/format_imputed_dtc

## Case Metadata

- Task ID: `pharmaverse/admiral/format_imputed_dtc`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform format imputed dtc using the admiral clinical task contract.

Input: imputed.tsv
Output: result.csv


Required columns for result.csv: imputed, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### imputed.tsv (44 bytes)
imputed
2020-06-15
2020-06-01
2020-01-01
NA
```

## Input Data

### `imputed.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/format_imputed_dtc/inputs/imputed.tsv`
- Size: 44 bytes

```text
imputed
2020-06-15
2020-06-01
2020-01-01
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/format_imputed_dtc/solution.R`
- Size: 433 bytes

```r
imputed <- as.character(read.delim(file.path("inputs", "imputed.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$imputed)
dates <- as.Date(ifelse(toupper(imputed) == "NA", NA_character_, imputed))
result <- ifelse(is.na(dates), NA_character_, format(dates, "%Y-%m-%d"))

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(imputed = imputed, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/format_imputed_dtc/outputs/result.csv`
- Size: 103 bytes

```csv
"imputed","result"
"2020-06-15","2020-06-15"
"2020-06-01","2020-06-01"
"2020-01-01","2020-01-01"
NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(admiral)
library(dplyr)
library(readr)
library(stringr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
imputed_df <- read_tsv(
  file = file.path("inputs", "imputed.tsv"),
  col_types = cols(imputed = col_character())
)

# Assume imputed dates are already imputed and in ISO format (YYYY-MM-DD)
# Use admiral's format_imputed_dtc to ensure proper formatting behavior
result_df <- imputed_df %>%
  mutate(
    result = if_else(
      is.na(imputed) | imputed == "" | imputed == "NA",
      NA_character_,
      format_imputed_dtc(
        dtc = imputed,
        impute_year = "first",
        impute_month = "first",
        impute_day = "first",
        flag_imputation = FALSE
      )
    )
  ) %>%
  select(imputed, result)

# Write output
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__format_imputed_dtc/sample_00/case_01/stderr.txt`
- Size: 2215 bytes

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

Error in `mutate()`:
ℹ In argument: `result = if_else(...)`.
Caused by error in `format_imputed_dtc()`:
! could not find function "format_imputed_dtc"
Backtrace:
     ▆
  1. ├─... %>% select(imputed, result)
  2. ├─dplyr::select(., imputed, result)
  3. ├─dplyr::mutate(...)
  4. ├─dplyr:::mutate.data.frame(...)
  5. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  6. │   ├─base::withCallingHandlers(...)
  7. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  8. │     └─mask$eval_all_mutate(quo)
  9. │       └─dplyr (local) eval()
 10. ├─dplyr::if_else(...)
 11. │ └─vctrs::vec_if_else(...)
 12. └─base::.handleSimpleError(...)
 13.   └─dplyr (local) h(simpleError(msg, call))
 14.     └─rlang::abort(message, class = error_class, parent = parent, call = error_call)
Execution halted
```

## Evaluation Result

```json
{
  "status": "NO_OUTPUT",
  "failure_stage": "execution_failure",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "tier": "exec_fail",
      "failure_stage": "execution_failure",
      "message": "No output files created",
      "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
      "returncode": 1,
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [],
        "missing_artifacts": [
          "result.csv"
        ]
      }
    }
  ]
}
```
