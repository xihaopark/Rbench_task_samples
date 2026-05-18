# Case 156: pharmaverse/admiral/is_partial_datetime

## Case Metadata

- Task ID: `pharmaverse/admiral/is_partial_datetime`
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
Write an R script to perform is partial datetime using the admiral clinical task contract.

Input: dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, result
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/is_partial_datetime/inputs/dtc.tsv`
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/is_partial_datetime/solution.R`
- Size: 690 bytes

```r
dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$dtc)
is_missing <- is.na(dtc) | dtc == "" | toupper(dtc) == "NA"
complete_date <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", dtc)
complete_dtm <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", dtc)
partial_date <- grepl("^[0-9]{4}(-[0-9]{2})?$", dtc)
partial_dtm <- grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}(:[0-9]{2})?$", dtc)
result <- !is_missing & (partial_date | partial_dtm) & !(complete_date | complete_dtm)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(dtc = dtc, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/is_partial_datetime/outputs/result.csv`
- Size: 122 bytes

```csv
"dtc","result"
"2020",TRUE
"2020-06",TRUE
"2020-06-15",FALSE
"2020-06-15T12:30",TRUE
"2020-06-15T12:30:00",FALSE
NA,FALSE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
dtc_df <- read_tsv(
  file = "inputs/dtc.tsv",
  col_types = cols(
    dtc = col_character()
  )
)

# Function to determine if partial datetime according to ADaM/ADmiral rules
is_partial_dtc <- function(x) {
  x <- str_trim(x)

  # Missing or blank is not a datetime (return NA)
  is_blank <- x == "" | is.na(x)
  ifelse(
    is_blank, NA,
    # Year only (YYYY)
    ifelse(str_detect(x, "^\\d{4}$"), TRUE,
    # Year-month only (YYYY-MM)
    ifelse(str_detect(x, "^\\d{4}-\\d{2}$"), TRUE,
    # Year-month-day only (YYYY-MM-DD)
    ifelse(str_detect(x, "^\\d{4}-\\d{2}-\\d{2}$"), TRUE,
    # Date + hour:minute (YYYY-MM-DDThh:mm)
    ifelse(str_detect(x, "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}$"), TRUE,
    # Date + hour:minute:second (full datetime, not partial)
    ifelse(str_detect(x, "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}$"), FALSE,
    # Any other format treated as NA
    NA
    )))))
  )
}

# Apply function
result_df <- dtc_df %>%
  mutate(result = is_partial_dtc(dtc)) %>%
  select(dtc, result)

# Write output
write_csv(result_df, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__is_partial_datetime/sample_00/case_01/llm_outputs/result.csv`
- Size: 100 bytes

```csv
dtc,result
2020,TRUE
2020-06,TRUE
2020-06-15,TRUE
2020-06-15T12:30,TRUE
2020-06-15T12:30:00,FALSE
,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__is_partial_datetime/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric missingness mismatch in column: result"
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
            "reason": "Numeric missingness mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
