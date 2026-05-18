# Case 090: pharmaverse/admiral/create_period_dataset

## Case Metadata

- Task ID: `pharmaverse/admiral/create_period_dataset`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform create period dataset using the admiral clinical task contract.

Input: periods.tsv
Output: result.csv


Required columns for result.csv: USUBJID, APERIOD, APERSDT, APEREDT
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### periods.tsv (113 bytes)
USUBJID	APERIOD	APERSDT	APEREDT
01	1	2020-01-01	2020-01-31
01	2	2020-02-01	2020-02-28
02	1	2020-01-05	2020-01-20
```

## Input Data

### `periods.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/create_period_dataset/inputs/periods.tsv`
- Size: 113 bytes

```text
USUBJID	APERIOD	APERSDT	APEREDT
01	1	2020-01-01	2020-01-31
01	2	2020-02-01	2020-02-28
02	1	2020-01-05	2020-01-20
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/create_period_dataset/solution.R`
- Size: 426 bytes

```r
periods <- read.delim(file.path("inputs", "periods.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result_df <- data.frame(
  USUBJID = periods$USUBJID,
  APERIOD = as.integer(periods$APERIOD),
  APERSDT = as.Date(periods$APERSDT),
  APEREDT = as.Date(periods$APEREDT),
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/create_period_dataset/outputs/result.csv`
- Size: 118 bytes

```csv
"USUBJID","APERIOD","APERSDT","APEREDT"
1,1,2020-01-01,2020-01-31
1,2,2020-02-01,2020-02-28
2,1,2020-01-05,2020-01-20
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
periods <- read_tsv(
  file = file.path("inputs", "periods.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    APERIOD = col_integer(),
    APERSDT = col_date(format = ""),
    APEREDT = col_date(format = "")
  )
)

# Select required columns (and ensure order)
result <- periods %>%
  select(USUBJID, APERIOD, APERSDT, APEREDT)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__create_period_dataset/sample_00/case_01/llm_outputs/result.csv`
- Size: 113 bytes

```csv
USUBJID,APERIOD,APERSDT,APEREDT
01,1,2020-01-01,2020-01-31
01,2,2020-02-01,2020-02-28
02,1,2020-01-05,2020-01-20
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__create_period_dataset/sample_00/case_01/stderr.txt`
- Size: 1333 bytes

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
