# Case 151: pharmaverse/admiral/get_unified_time_unit

## Case Metadata

- Task ID: `pharmaverse/admiral/get_unified_time_unit`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform get unified time unit using the admiral clinical task contract.

Input: time_unit.tsv
Output: result.csv


Required columns for result.csv: time_unit, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### time_unit.tsv (53 bytes)
time_unit
HOURS
hour
hr
DAYS
day
... [3 more lines omitted]
```

## Input Data

### `time_unit.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_unified_time_unit/inputs/time_unit.tsv`
- Size: 53 bytes

```text
time_unit
HOURS
hour
hr
DAYS
day
min
minutes
seconds
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_unified_time_unit/solution.R`
- Size: 621 bytes

```r
time_unit <- as.character(read.delim(file.path("inputs", "time_unit.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$time_unit)
key <- tolower(trimws(time_unit))
result <- ifelse(key %in% c("h", "hr", "hrs", "hour", "hours"), "hours",
  ifelse(key %in% c("d", "day", "days"), "days",
    ifelse(key %in% c("m", "min", "mins", "minute", "minutes"), "minutes",
      ifelse(key %in% c("s", "sec", "secs", "second", "seconds"), "seconds", NA_character_))))

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(time_unit = time_unit, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_unified_time_unit/outputs/result.csv`
- Size: 148 bytes

```csv
"time_unit","result"
"HOURS","hours"
"hour","hours"
"hr","hours"
"DAYS","days"
"day","days"
"min","minutes"
"minutes","minutes"
"seconds","seconds"
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

# Read input
time_unit_df <- readr::read_tsv(
  file = file.path("inputs", "time_unit.tsv"),
  show_col_types = FALSE
)

# Function to map to unified time unit (based on admiral conventions)
map_time_unit <- function(x) {
  x_std <- str_trim(toupper(x))

  case_when(
    x_std %in% c("H", "HR", "HOUR", "HOURS", "HRS") ~ "HOURS",
    x_std %in% c("D", "DAY", "DAYS") ~ "DAYS",
    x_std %in% c("W", "WK", "WEEK", "WEEKS") ~ "WEEKS",
    x_std %in% c("MON", "MONTH", "MONTHS", "MO") ~ "MONTHS",
    x_std %in% c("Y", "YR", "YEAR", "YEARS") ~ "YEARS",
    TRUE ~ NA_character_
  )
}

result_df <- time_unit_df %>%
  mutate(result = map_time_unit(time_unit)) %>%
  select(time_unit, result)

# Write output
readr::write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_unified_time_unit/sample_00/case_01/llm_outputs/result.csv`
- Size: 91 bytes

```csv
time_unit,result
HOURS,HOURS
hour,HOURS
hr,HOURS
DAYS,DAYS
day,DAYS
min,
minutes,
seconds,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_unified_time_unit/sample_00/case_01/stderr.txt`
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
