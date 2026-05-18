# Case 190: pharmaverse/sdtm.oak/iso8601_sec

## Case Metadata

- Task ID: `pharmaverse/sdtm.oak/iso8601_sec`
- Package: `sdtm.oak`
- Model: `openai/gpt-5.1`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform ISO 8601 sec using the sdtm.oak clinical task contract.

Input: x.tsv
Output: result.csv


Required columns for result.csv: x, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### x.tsv (27 bytes)
x
PT1H2M3S
PT45S
PT2M
PT1H
```

## Input Data

### `x.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/iso8601_sec/inputs/x.tsv`
- Size: 27 bytes

```text
x
PT1H2M3S
PT45S
PT2M
PT1H
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/iso8601_sec/solution.R`
- Size: 595 bytes

```r
x <- as.character(read.delim(file.path("inputs", "x.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$x)
grab <- function(value, suffix) {
  m <- regexec(paste0("([0-9]+)", suffix), value)
  hit <- regmatches(value, m)[[1]]
  if (length(hit) == 0) 0L else as.integer(hit[[2]])
}
result <- vapply(x, function(value) grab(value, "H") * 3600L + grab(value, "M") * 60L + grab(value, "S"), integer(1))
result_df <- data.frame(x = x, result = result, stringsAsFactors = FALSE)
dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/iso8601_sec/outputs/result.csv`
- Size: 63 bytes

```csv
"x","result"
"PT1H2M3S",3723
"PT45S",45
"PT2M",120
"PT1H",3600
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
x_path <- file.path("inputs", "x.tsv")
df <- readr::read_tsv(x_path, show_col_types = FALSE)

# Function to convert ISO 8601 duration PT… to seconds
iso_to_seconds <- function(x) {
  if (is.na(x) | x == "") return(NA_real_)
  # Expecting time-based duration starting with PT
  m <- str_match(x, "^PT(?:(\\d+)H)?(?:(\\d+)M)?(?:(\\d+)S)?$")
  if (is.na(m[1,1])) return(NA_real_)
  h <- as.numeric(m[1,2])
  mnt <- as.numeric(m[1,3])
  s <- as.numeric(m[1,4])
  h[is.na(h)] <- 0
  mnt[is.na(mnt)] <- 0
  s[is.na(s)] <- 0
  h * 3600 + mnt * 60 + s
}

result <- df %>%
  mutate(result = iso_to_seconds(x)) %>%
  select(x, result)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtm.oak__iso8601_sec/sample_00/case_01/stderr.txt`
- Size: 2031 bytes

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
Error in `mutate()`:
ℹ In argument: `result = iso_to_seconds(x)`.
Caused by error in `if (is.na(x) | x == "") ...`:
! the condition has length > 1
Backtrace:
     ▆
  1. ├─df %>% mutate(result = iso_to_seconds(x)) %>% ...
  2. ├─dplyr::select(., x, result)
  3. ├─dplyr::mutate(., result = iso_to_seconds(x))
  4. ├─dplyr:::mutate.data.frame(., result = iso_to_seconds(x))
  5. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  6. │   ├─base::withCallingHandlers(...)
  7. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  8. │     └─mask$eval_all_mutate(quo)
  9. │       └─dplyr (local) eval()
 10. ├─global iso_to_seconds(x)
 11. └─base::.handleSimpleError(...)
 12.   └─dplyr (local) h(simpleError(msg, call))
 13.     └─rlang::abort(message, class = error_class, parent = parent, call = error_call)
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
