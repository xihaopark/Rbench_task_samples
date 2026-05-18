# Case 191: pharmaverse/sdtm.oak/sbj_vars

## Case Metadata

- Task ID: `pharmaverse/sdtm.oak/sbj_vars`
- Package: `sdtm.oak`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform sbj vars using the sdtm.oak clinical task contract.

Input: none
Output: result.csv


Required columns for result.csv: position, variable
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.
```

## Input Data

No input files.

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/sbj_vars/solution.R`
- Size: 251 bytes

```r
vars <- c("STUDYID", "USUBJID", "SUBJID")
result <- data.frame(position = seq_along(vars), variable = vars, stringsAsFactors = FALSE)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/sbj_vars/outputs/result.csv`
- Size: 57 bytes

```csv
"position","variable"
1,"STUDYID"
2,"USUBJID"
3,"SUBJID"
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

# Helper to safely list and read SDTM-like files
sdtm_files <- list.files("inputs", pattern = "\\.csv$|\\.xpt$|\\.sas7bdat$|\\.tsv$",
                         full.names = TRUE, ignore.case = TRUE)

# Initialize empty data frame for variables
vars_df <- tibble(position = integer(), variable = character())

# Function to extract variables from a single file
extract_vars_from_file <- function(fpath) {
  fname <- basename(fpath)
  dom <- tools::file_path_sans_ext(fname)

  df <- tryCatch({
    if (grepl("\\.csv$", fpath, ignore.case = TRUE)) {
      suppressWarnings(readr::read_csv(fpath, col_types = cols(.default = col_guess())))
    } else if (grepl("\\.tsv$", fpath, ignore.case = TRUE)) {
      suppressWarnings(readr::read_tsv(fpath, col_types = cols(.default = col_guess())))
    } else if (grepl("\\.xpt$", fpath, ignore.case = TRUE)) {
      if (!requireNamespace("haven", quietly = TRUE)) return(NULL)
      haven::read_xpt(fpath)
    } else if (grepl("\\.sas7bdat$", fpath, ignore.case = TRUE)) {
      if (!requireNamespace("haven", quietly = TRUE)) return(NULL)
      haven::read_sas(fpath)
    } else {
      NULL
    }
  }, error = function(e) NULL)

  if (is.null(df)) return(NULL)

  tibble(
    variable = names(df)
  )
}

# Collect variables from all SDTM-like files
var_list <- lapply(sdtm_files, extract_vars_from_file)
var_list <- var_list[!vapply(var_list, is.null, logical(1))]

if (length(var_list) > 0) {
  vars_df <- bind_rows(var_list) %>%
    distinct(variable) %>%
    arrange(variable) %>%
    mutate(position = dplyr::row_number()) %>%
    select(position, variable)
}

# Ensure at least an empty structure with required columns
if (nrow(vars_df) == 0) {
  vars_df <- tibble(
    position = integer(),
    variable = character()
  )
}

# Write result
write_csv(vars_df, file = file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtm.oak__sbj_vars/sample_00/case_01/llm_outputs/result.csv`
- Size: 18 bytes

```csv
position,variable
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtm.oak__sbj_vars/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(3, 2) vs llm=(0, 2)"
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
            "reason": "Shape mismatch: ref=(3, 2) vs llm=(0, 2)"
          }
        }
      }
    }
  ]
}
```
