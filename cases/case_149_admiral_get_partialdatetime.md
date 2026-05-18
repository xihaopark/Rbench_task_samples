# Case 149: pharmaverse/admiral/get_partialdatetime

## Case Metadata

- Task ID: `pharmaverse/admiral/get_partialdatetime`
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
Write an R script to perform get partialdatetime using the admiral clinical task contract.

Input: dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, year, month, day, hour, minute, second
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dtc.tsv (68 bytes)
dtc
2020
2020-06
2020-06-15
2020-06-15T12:30
2020-06-15T12:30:00
... [1 more lines omitted]
```

## Input Data

### `dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_partialdatetime/inputs/dtc.tsv`
- Size: 68 bytes

```text
dtc
2020
2020-06
2020-06-15
2020-06-15T12:30
2020-06-15T12:30:00
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_partialdatetime/solution.R`
- Size: 958 bytes

```r
dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$dtc)
missing <- is.na(dtc) | toupper(dtc) == "NA" | dtc == ""
year <- ifelse(missing, NA_integer_, as.integer(substr(dtc, 1, 4)))
month <- ifelse(nchar(dtc) >= 7 & !missing, as.integer(substr(dtc, 6, 7)), NA_integer_)
day <- ifelse(nchar(dtc) >= 10 & !missing, as.integer(substr(dtc, 9, 10)), NA_integer_)
hour <- ifelse(nchar(dtc) >= 13 & !missing, as.integer(substr(dtc, 12, 13)), NA_integer_)
minute <- ifelse(nchar(dtc) >= 16 & !missing, as.integer(substr(dtc, 15, 16)), NA_integer_)
second <- ifelse(nchar(dtc) >= 19 & !missing, as.integer(substr(dtc, 18, 19)), NA_integer_)
result_df <- data.frame(dtc = dtc, year = year, month = month, day = day, hour = hour, minute = minute, second = second, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_partialdatetime/outputs/result.csv`
- Size: 239 bytes

```csv
"dtc","year","month","day","hour","minute","second"
"2020",2020,NA,NA,NA,NA,NA
"2020-06",2020,6,NA,NA,NA,NA
"2020-06-15",2020,6,15,NA,NA,NA
"2020-06-15T12:30",2020,6,15,12,30,NA
"2020-06-15T12:30:00",2020,6,15,12,30,0
NA,NA,NA,NA,NA,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# create outputs dir if needed
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# read input
dt <- read_tsv(
  file = file.path("inputs", "dtc.tsv"),
  col_types = cols(.default = col_character())
)

# helper to split ISO 8601 partial datetime (YYYY, YYYY-MM, YYYY-MM-DD, etc.)
parse_partial_dtc <- function(dtc) {
  # separate date and time parts
  date_part  <- ifelse(str_detect(dtc, "T"), str_extract(dtc, "^[^T]+"), dtc)
  time_part  <- ifelse(str_detect(dtc, "T"), str_extract(dtc, "(?<=T).*$"), NA_character_)

  # split date
  ymd <- str_split_fixed(date_part, "-", 3)
  year  <- ifelse(ymd[, 1] == "", NA_character_, ymd[, 1])
  month <- ifelse(ymd[, 2] == "", NA_character_, ymd[, 2])
  day   <- ifelse(ymd[, 3] == "", NA_character_, ymd[, 3])

  # split time
  hms <- ifelse(
    is.na(time_part),
    NA_character_,
    time_part
  )
  hms_split <- str_split_fixed(coalesce(hms, ""), ":", 3)
  hour   <- ifelse(hms_split[, 1] == "" | is.na(hms), NA_character_, hms_split[, 1])
  minute <- ifelse(hms_split[, 2] == "" | is.na(hms), NA_character_, hms_split[, 2])
  second <- ifelse(hms_split[, 3] == "" | is.na(hms), NA_character_, hms_split[, 3])

  tibble(
    year   = year,
    month  = month,
    day    = day,
    hour   = hour,
    minute = minute,
    second = second
  )
}

result <- dt %>%
  mutate(parsed = parse_partial_dtc(dtc)) %>%
  bind_cols(select(., dtc), .$parsed) %>%
  select(dtc, year, month, day, hour, minute, second)

write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_partialdatetime/sample_00/case_01/stderr.txt`
- Size: 2632 bytes

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
New names:
• `dtc` -> `dtc...1`
• `dtc` -> `dtc...3`
Error in `select()`:
! Can't select columns that don't exist.
✖ Column `dtc` doesn't exist.
Backtrace:
     ▆
  1. ├─... %>% select(dtc, year, month, day, hour, minute, second)
  2. ├─dplyr::select(., dtc, year, month, day, hour, minute, second)
  3. ├─dplyr:::select.data.frame(., dtc, year, month, day, hour, minute, second)
  4. │ └─tidyselect::eval_select(expr(c(...)), data = .data, error_call = error_call)
  5. │   └─tidyselect:::eval_select_impl(...)
  6. │     ├─tidyselect:::with_subscript_errors(...)
  7. │     │ └─base::withCallingHandlers(...)
  8. │     └─tidyselect:::vars_select_eval(...)
  9. │       └─tidyselect:::walk_data_tree(expr, data_mask, context_mask)
 10. │         └─tidyselect:::eval_c(expr, data_mask, context_mask)
 11. │           └─tidyselect:::reduce_sels(node, data_mask, context_mask, init = init)
 12. │             └─tidyselect:::walk_data_tree(new, data_mask, context_mask)
 13. │               └─tidyselect:::as_indices_sel_impl(...)
 14. │                 └─tidyselect:::as_indices_impl(...)
 15. │                   └─tidyselect:::chr_as_locations(x, vars, call = call, arg = arg)
 16. │                     └─vctrs::vec_as_location(...)
 17. └─vctrs (local) `<fn>`()
 18.   └─vctrs:::stop_subscript_oob(...)
 19.     └─vctrs:::stop_subscript(...)
 20.       └─rlang::abort(...)
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
