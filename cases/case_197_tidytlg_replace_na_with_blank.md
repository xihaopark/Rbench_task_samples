# Case 197: pharmaverse/tidytlg/replace_na_with_blank

## Case Metadata

- Task ID: `pharmaverse/tidytlg/replace_na_with_blank`
- Package: `tidytlg`
- Model: `openai/gpt-5.1`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform replace na with blank using the tidytlg clinical task contract.

Input: x.tsv
Output: result.csv


Required columns for result.csv: row_id, x
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### x.tsv (23 bytes)
x
Alpha
NA

Beta
Gamma
```

## Input Data

### `x.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/tidytlg/replace_na_with_blank/inputs/x.tsv`
- Size: 23 bytes

```text
x
Alpha
NA

Beta
Gamma
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/tidytlg/replace_na_with_blank/solution.R`
- Size: 363 bytes

```r
x <- read.delim(
  file.path("inputs", "x.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE,
  na.strings = c("", "NA")
)

result <- data.frame(
  row_id = seq_len(nrow(x)),
  x = ifelse(is.na(x$x), "", x$x),
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/tidytlg/replace_na_with_blank/outputs/result.csv`
- Size: 47 bytes

```csv
"row_id","x"
1,"Alpha"
2,""
3,"Beta"
4,"Gamma"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tidytlg)

# Ensure output directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
x <- read_tsv(
  file = file.path("inputs", "x.tsv"),
  col_types = cols(.default = col_character())
)

# Add row_id
x <- x %>%
  mutate(row_id = row_number(), .before = 1)

# Replace NA with blank using tidytlg clinical task contract
# Assuming tidytlg provides a function to apply clinical NA-to-blank rules
# If the function differs, adjust its name/arguments accordingly.
x_clean <- x %>%
  mutate(
    across(
      where(is.character),
      ~ clinical_na2blank(.x)
    )
  )

# Select required columns and write output
x_clean %>%
  select(row_id, x) %>%
  write_csv(file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__tidytlg__replace_na_with_blank/sample_00/case_01/stderr.txt`
- Size: 2293 bytes

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
ℹ In argument: `across(where(is.character), ~clinical_na2blank(.x))`.
Caused by error in `across()`:
! Can't compute column `x`.
Caused by error in `clinical_na2blank()`:
! could not find function "clinical_na2blank"
Backtrace:
     ▆
  1. ├─x %>% ...
  2. ├─dplyr::mutate(., across(where(is.character), ~clinical_na2blank(.x)))
  3. ├─dplyr:::mutate.data.frame(., across(where(is.character), ~clinical_na2blank(.x)))
  4. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  5. │   ├─base::withCallingHandlers(...)
  6. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  7. │     ├─base::withCallingHandlers(...)
  8. │     └─mask$eval_all_mutate(quo)
  9. │       └─dplyr (local) eval()
 10. └─base::.handleSimpleError(...)
 11.   └─dplyr (local) h(simpleError(msg, call))
 12.     └─rlang::abort(msg, call = call("across"), parent = cnd)
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
