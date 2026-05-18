# Case 077: pharmaverse/admiral/convert_min_pre_eot

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_min_pre_eot`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform convert min pre eot using the admiral clinical task contract.

Input: treatment_duration.tsv, xxtpt.tsv
Output: result.csv


Required columns for result.csv: xxtpt, treatment_duration, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### treatment_duration.tsv (25 bytes)
treatment_duration
2
3
4

### xxtpt.tsv (59 bytes)
xxtpt
10 min pre eoi
15 minutes before eot
30 mins pre eot
```

## Input Data

### `treatment_duration.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_pre_eot/inputs/treatment_duration.tsv`
- Size: 25 bytes

```text
treatment_duration
2
3
4
```

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_pre_eot/inputs/xxtpt.tsv`
- Size: 59 bytes

```text
xxtpt
10 min pre eoi
15 minutes before eot
30 mins pre eot
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_pre_eot/solution.R`
- Size: 834 bytes

```r
xxtpt <- as.character(read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
treatment_duration <- as.numeric(read.delim(file.path("inputs", "treatment_duration.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])

convert_one <- function(x, duration) {
  value <- trimws(tolower(x))
  match <- regexec("^([0-9]+(?:\\.[0-9]+)?)\\s*m(?:in|inute)?s?\\s+(?:pre|before)\\s+eo[it]$", value)
  parsed <- regmatches(value, match)[[1]]
  if (length(parsed) > 0) {
    return(duration - as.numeric(parsed[2]) / 60)
  }
  NA_real_
}

result <- mapply(convert_one, xxtpt, treatment_duration)

dir.create("outputs", showWarnings = FALSE)
write.csv(
  data.frame(xxtpt = xxtpt, treatment_duration = treatment_duration, result = result),
  file.path("outputs", "result.csv"),
  row.names = FALSE
)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_pre_eot/outputs/result.csv`
- Size: 129 bytes

```csv
"xxtpt","treatment_duration","result"
"10 min pre eoi",2,1.83333333333333
"15 minutes before eot",3,2.75
"30 mins pre eot",4,3.5
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
treatment_duration <- read_tsv(
  file = file.path("inputs", "treatment_duration.tsv"),
  show_col_types = FALSE
)

xxtpt <- read_tsv(
  file = file.path("inputs", "xxtpt.tsv"),
  show_col_types = FALSE
)

# Helper to extract minutes and reference (pre eoi/eot)
parse_xxtpt <- function(x) {
  x_clean <- tolower(trimws(x))
  tibble(
    xxtpt = x,
    minutes = as.numeric(str_extract(x_clean, "\\d+")),
    ref = case_when(
      str_detect(x_clean, "eoi") ~ "eoi",
      str_detect(x_clean, "eot") ~ "eot",
      TRUE ~ NA_character_
    )
  )
}

parsed <- parse_xxtpt(xxtpt$xxtpt)

# For "convert min pre eot using the admiral clinical task contract"
# we will convert all "pre eoi" times to equivalent "pre eot" by:
# result = treatment_duration - (time from eot)
# For rows already "pre eot", result = minutes.
# For rows "pre eoi", assume EOI at time 0 and EOT at treatment_duration,
# so a sample taken N minutes pre eoi is at time -N relative to EOI,
# which corresponds to treatment_duration - N minutes pre eot.
#
# Since no explicit mapping between rows is given, use rowwise pairing
# by position between xxtpt and treatment_duration.

df <- parsed %>%
  bind_cols(treatment_duration = treatment_duration$treatment_duration[seq_len(n())]) %>%
  mutate(
    result = case_when(
      ref == "eot" ~ minutes,
      ref == "eoi" ~ treatment_duration - minutes,
      TRUE ~ NA_real_
    )
  ) %>%
  select(xxtpt, treatment_duration, result)

# Write output
write_csv(df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_min_pre_eot/sample_00/case_01/stderr.txt`
- Size: 1798 bytes

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
Error in `n()`:
! Must only be used inside data-masking verbs like `mutate()`,
  `filter()`, and `group_by()`.
Backtrace:
     ▆
  1. ├─... %>% select(xxtpt, treatment_duration, result)
  2. ├─dplyr::select(., xxtpt, treatment_duration, result)
  3. ├─dplyr::mutate(...)
  4. ├─dplyr::bind_cols(., treatment_duration = treatment_duration$treatment_duration[seq_len(n())])
  5. │ └─rlang::list2(...)
  6. └─dplyr::n()
  7.   └─dplyr:::peek_mask()
  8.     └─dplyr:::context_peek(...)
  9.       ├─context_peek_bare(name) %||% ...
 10.       └─rlang::abort(glue("Must only be used inside {location}."), call = call)
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
