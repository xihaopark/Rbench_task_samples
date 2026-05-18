# Case 083: pharmaverse/admiral/convert_simple_units

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_simple_units`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform convert simple units using the admiral clinical task contract.

Input: xxtpt.tsv
Output: result.csv


Required columns for result.csv: xxtpt, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### xxtpt.tsv (64 bytes)
xxtpt
0.5 h
30 min post dose
2 hours after dose
90 mins
1.25 hr
```

## Input Data

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_simple_units/inputs/xxtpt.tsv`
- Size: 64 bytes

```text
xxtpt
0.5 h
30 min post dose
2 hours after dose
90 mins
1.25 hr
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_simple_units/solution.R`
- Size: 859 bytes

```r
xxtpt <- as.character(read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])

convert_one <- function(x) {
  value <- trimws(tolower(x))
  hour_match <- regexec("^([0-9]+(?:\\.[0-9]+)?)\\s*h(?:r|our)?s?(?:\\s+(?:post|after)(?:\\s*-?\\s*dose)?)?$", value)
  hour <- regmatches(value, hour_match)[[1]]
  if (length(hour) > 0) {
    return(as.numeric(hour[2]))
  }
  min_match <- regexec("^([0-9]+(?:\\.[0-9]+)?)\\s*m(?:in|inute)?s?(?:\\s+(?:post|after)(?:\\s*-?\\s*dose)?)?$", value)
  minute <- regmatches(value, min_match)[[1]]
  if (length(minute) > 0) {
    return(as.numeric(minute[2]) / 60)
  }
  NA_real_
}

result <- vapply(xxtpt, convert_one, numeric(1))

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(xxtpt = xxtpt, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_simple_units/outputs/result.csv`
- Size: 104 bytes

```csv
"xxtpt","result"
"0.5 h",0.5
"30 min post dose",0.5
"2 hours after dose",2
"90 mins",1.5
"1.25 hr",1.25
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# read input
xxtpt_df <- read_tsv(
  file = file.path("inputs", "xxtpt.tsv"),
  col_types = cols(.default = col_character())
)

# function to convert textual time to hours
convert_to_hours <- function(x) {
  x_clean <- tolower(trimws(x))
  # extract first numeric value
  num <- suppressWarnings(as.numeric(str_extract(x_clean, "-?\\d*\\.?\\d+")))
  if (is.na(num)) return(NA_real_)

  # determine unit: look at presence of hour/min keywords
  if (str_detect(x_clean, "hour|hr|hrs|h(\\b|$)")) {
    val <- num
  } else if (str_detect(x_clean, "min")) {
    val <- num / 60
  } else {
    # default: assume hours if "dose" with a decimal number, otherwise NA
    val <- num
  }
  val
}

result_df <- xxtpt_df %>%
  mutate(
    result = convert_to_hours(xxtpt)
  ) %>%
  select(xxtpt, result)

write_csv(result_df, file.path("outputs", "result.csv"))
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_simple_units/sample_00/case_01/stderr.txt`
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
ℹ In argument: `result = convert_to_hours(xxtpt)`.
Caused by error in `if (is.na(num)) ...`:
! the condition has length > 1
Backtrace:
     ▆
  1. ├─... %>% select(xxtpt, result)
  2. ├─dplyr::select(., xxtpt, result)
  3. ├─dplyr::mutate(., result = convert_to_hours(xxtpt))
  4. ├─dplyr:::mutate.data.frame(., result = convert_to_hours(xxtpt))
  5. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  6. │   ├─base::withCallingHandlers(...)
  7. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  8. │     └─mask$eval_all_mutate(quo)
  9. │       └─dplyr (local) eval()
 10. ├─global convert_to_hours(xxtpt)
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
