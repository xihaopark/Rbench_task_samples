# Case 154: pharmaverse/admiral/impute_dtc_dt

## Case Metadata

- Task ID: `pharmaverse/admiral/impute_dtc_dt`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform impute dtc dt using the admiral clinical task contract.

Input: date_imputation.tsv, dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### date_imputation.tsv (22 bytes)
date_imputation
first

### dtc.tsv (31 bytes)
dtc
2020-06-15
2020-06
2020
NA
```

## Input Data

### `date_imputation.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/impute_dtc_dt/inputs/date_imputation.tsv`
- Size: 22 bytes

```text
date_imputation
first
```

### `dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/impute_dtc_dt/inputs/dtc.tsv`
- Size: 31 bytes

```text
dtc
2020-06-15
2020-06
2020
NA
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/impute_dtc_dt/solution.R`
- Size: 595 bytes

```r
dtc <- as.character(read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$dtc)
missing <- is.na(dtc) | toupper(dtc) == "NA" | dtc == ""
result_chr <- ifelse(grepl("^[0-9]{4}$", dtc), paste0(dtc, "-01-01"),
  ifelse(grepl("^[0-9]{4}-[0-9]{2}$", dtc), paste0(dtc, "-01"),
    ifelse(grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", dtc), dtc, NA_character_)))
result <- as.Date(ifelse(missing, NA_character_, result_chr))

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(dtc = dtc, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/impute_dtc_dt/outputs/result.csv`
- Size: 84 bytes

```csv
"dtc","result"
"2020-06-15",2020-06-15
"2020-06",2020-06-01
"2020",2020-01-01
NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
date_imp <- read_tsv(
  file = file.path("inputs", "date_imputation.tsv"),
  show_col_types = FALSE
)

dtc_df <- read_tsv(
  file = file.path("inputs", "dtc.tsv"),
  show_col_types = FALSE
)

# Determine imputation rule from date_imputation
# Assume "first" -> impute missing month/day with "01"
imp_type <- tolower(date_imp$date_imputation[1])

impute_dtc <- function(dtc, imp_type = "first") {
  if (is.na(dtc) || dtc == "") return(NA_character_)

  # If already full date (YYYY-MM-DD), return as is
  if (str_detect(dtc, "^\\d{4}-\\d{2}-\\d{2}$")) {
    return(dtc)
  }

  # Year-month (YYYY-MM)
  if (str_detect(dtc, "^\\d{4}-\\d{2}$")) {
    if (imp_type == "first") {
      return(paste0(dtc, "-01"))
    } else {
      return(NA_character_)
    }
  }

  # Year only (YYYY)
  if (str_detect(dtc, "^\\d{4}$")) {
    if (imp_type == "first") {
      return(paste0(dtc, "-01-01"))
    } else {
      return(NA_character_)
    }
  }

  NA_character_
}

result_df <- dtc_df %>%
  mutate(
    result = vapply(dtc, impute_dtc, character(1), imp_type = imp_type)
  ) %>%
  select(dtc, result)

write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__impute_dtc_dt/sample_00/case_01/llm_outputs/result.csv`
- Size: 70 bytes

```csv
dtc,result
2020-06-15,2020-06-15
2020-06,2020-06-01
2020,2020-01-01
,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__impute_dtc_dt/sample_00/case_01/stderr.txt`
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
  "status": "PASS",
  "failure_stage": "pass",
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "tier": "pass",
      "tier_value": "pass",
      "failure_stage": "pass",
      "comparison": {
        "result.csv": {
          "match": true,
          "tier": "pass",
          "failure_stage": "pass"
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
        "comparison_reasons": {}
      }
    }
  ]
}
```
