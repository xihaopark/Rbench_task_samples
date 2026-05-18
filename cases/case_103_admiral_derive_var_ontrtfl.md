# Case 103: pharmaverse/admiral/derive_var_ontrtfl

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_var_ontrtfl`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive var ontrtfl using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, ADT, TRTSDT, TRTEDT, ONTRTFL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (174 bytes)
USUBJID	ADT	TRTSDT	TRTEDT
P01	2020-02-24	2020-01-01	2020-03-01
P02	2020-01-01	2020-01-01	2020-03-01
P03	2019-12-31	2020-01-01	2020-03-01
P04	2020-03-05	2020-01-01	2020-03-01
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_ontrtfl/inputs/dataset.tsv`
- Size: 174 bytes

```text
USUBJID	ADT	TRTSDT	TRTEDT
P01	2020-02-24	2020-01-01	2020-03-01
P02	2020-01-01	2020-01-01	2020-03-01
P03	2019-12-31	2020-01-01	2020-03-01
P04	2020-03-05	2020-01-01	2020-03-01
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_ontrtfl/solution.R`
- Size: 496 bytes

```r
suppressPackageStartupMessages(library(admiral))

dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
for (col in c("ADT", "TRTSDT", "TRTEDT")) {
  dataset[[col]] <- as.Date(dataset[[col]])
}

result <- admiral::derive_var_ontrtfl(
  dataset,
  start_date = ADT,
  ref_start_date = TRTSDT,
  ref_end_date = TRTEDT
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE, na = "")
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_ontrtfl/outputs/result.csv`
- Size: 210 bytes

```csv
"USUBJID","ADT","TRTSDT","TRTEDT","ONTRTFL"
"P01",2020-02-24,2020-01-01,2020-03-01,"Y"
"P02",2020-01-01,2020-01-01,2020-03-01,"Y"
"P03",2019-12-31,2020-01-01,2020-03-01,
"P04",2020-03-05,2020-01-01,2020-03-01,
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(lubridate)

# Ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
adsl <- read.delim(
  file = file.path("inputs", "dataset.tsv"),
  sep = "\t",
  header = TRUE,
  stringsAsFactors = FALSE
)

# Convert dates
adsl <- adsl %>%
  mutate(
    ADT    = ymd(ADT),
    TRTSDT = ymd(TRTSDT),
    TRTEDT = ymd(TRTEDT)
  )

# Derive ONTRTFL per admiral logic (ADT between TRTSDT and TRTEDT inclusive)
result <- adsl %>%
  mutate(
    ONTRTFL = if_else(!is.na(ADT) & !is.na(TRTSDT) & !is.na(TRTEDT) &
                        ADT >= TRTSDT & ADT <= TRTEDT,
                      "Y", NA_character_)
  ) %>%
  select(USUBJID, ADT, TRTSDT, TRTEDT, ONTRTFL)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_ontrtfl/sample_00/case_01/llm_outputs/result.csv`
- Size: 188 bytes

```csv
USUBJID,ADT,TRTSDT,TRTEDT,ONTRTFL
P01,2020-02-24,2020-01-01,2020-03-01,Y
P02,2020-01-01,2020-01-01,2020-03-01,Y
P03,2019-12-31,2020-01-01,2020-03-01,
P04,2020-03-05,2020-01-01,2020-03-01,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_ontrtfl/sample_00/case_01/stderr.txt`
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
