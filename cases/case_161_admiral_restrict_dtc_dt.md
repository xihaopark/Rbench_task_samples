# Case 161: pharmaverse/admiral/restrict_imputed_dtc_dt

## Case Metadata

- Task ID: `pharmaverse/admiral/restrict_imputed_dtc_dt`
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
Write an R script to perform restrict imputed dtc dt using the admiral clinical task contract.

Input: imputed_dtc.tsv
Output: result.csv


Required columns for result.csv: dtc, imputed_dtc, min_date, max_date, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### imputed_dtc.tsv (141 bytes)
dtc	imputed_dtc	min_date	max_date
2020-01	2020-01-15	2020-01-20	NA
2020-02	2020-02-15	NA	2020-02-10
2020-03	2020-03-15	2020-03-01	2020-03-31
```

## Input Data

### `imputed_dtc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/restrict_imputed_dtc_dt/inputs/imputed_dtc.tsv`
- Size: 141 bytes

```text
dtc	imputed_dtc	min_date	max_date
2020-01	2020-01-15	2020-01-20	NA
2020-02	2020-02-15	NA	2020-02-10
2020-03	2020-03-15	2020-03-01	2020-03-31
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/restrict_imputed_dtc_dt/solution.R`
- Size: 711 bytes

```r
data <- read.delim(file.path("inputs", "imputed_dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
to_date <- function(x) {
  x[x == "NA" | x == ""] <- NA_character_
  as.Date(x)
}
imputed <- to_date(data$imputed_dtc)
min_date <- to_date(data$min_date)
max_date <- to_date(data$max_date)
result <- imputed
result[!is.na(min_date) & result < min_date] <- min_date[!is.na(min_date) & result < min_date]
result[!is.na(max_date) & result > max_date] <- max_date[!is.na(max_date) & result > max_date]
result_df <- data.frame(data, result = as.character(result), stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/restrict_imputed_dtc_dt/outputs/result.csv`
- Size: 217 bytes

```csv
"dtc","imputed_dtc","min_date","max_date","result"
"2020-01","2020-01-15","2020-01-20",NA,"2020-01-20"
"2020-02","2020-02-15",NA,"2020-02-10","2020-02-10"
"2020-03","2020-03-15","2020-03-01","2020-03-31","2020-03-15"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(lubridate)

# Create output directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
imputed <- read_tsv(
  file = file.path("inputs", "imputed_dtc.tsv"),
  col_types = cols(
    dtc = col_character(),
    imputed_dtc = col_character(),
    min_date = col_character(),
    max_date = col_character()
  )
)

# Helper to safely parse dates, returning NA if parsing fails
parse_safe <- function(x) {
  ifelse(is.na(x) | x == "" | x == "NA",
         NA_Date_,
         ymd(x, quiet = TRUE)
  )
}

result <- imputed %>%
  mutate(
    imputed_dtc_date = parse_safe(imputed_dtc),
    min_date_date    = parse_safe(min_date),
    max_date_date    = parse_safe(max_date),
    result = case_when(
      # both bounds available: check inclusive within range
      !is.na(min_date_date) & !is.na(max_date_date) &
        !is.na(imputed_dtc_date) &
        imputed_dtc_date >= min_date_date &
        imputed_dtc_date <= max_date_date ~ "Y",

      # only min bound: imputed must be on/after min
      !is.na(min_date_date) & is.na(max_date_date) &
        !is.na(imputed_dtc_date) &
        imputed_dtc_date >= min_date_date ~ "Y",

      # only max bound: imputed must be on/before max
      is.na(min_date_date) & !is.na(max_date_date) &
        !is.na(imputed_dtc_date) &
        imputed_dtc_date <= max_date_date ~ "Y",

      TRUE ~ "N"
    )
  ) %>%
  select(dtc, imputed_dtc, min_date, max_date, result)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__restrict_imputed_dtc_dt/sample_00/case_01/llm_outputs/result.csv`
- Size: 150 bytes

```csv
dtc,imputed_dtc,min_date,max_date,result
2020-01,2020-01-15,2020-01-20,,N
2020-02,2020-02-15,,2020-02-10,N
2020-03,2020-03-15,2020-03-01,2020-03-31,Y
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__restrict_imputed_dtc_dt/sample_00/case_01/stderr.txt`
- Size: 1466 bytes

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


Attaching package: ‘lubridate’

The following objects are masked from ‘package:base’:

    date, intersect, setdiff, union
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
