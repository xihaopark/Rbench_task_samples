# Case 122: pharmaverse/admiral/derive_vars_period

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_period`
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
Write an R script to perform derive vars period using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, ADT, APERIOD
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (210 bytes)
USUBJID	ADT	P1SDT	P1EDT	P2SDT	P2EDT
01	2020-01-10	2020-01-01	2020-01-31	2020-02-01	2020-02-28
02	2020-02-15	2020-01-01	2020-01-31	2020-02-01	2020-02-28
03	2020-03-01	2020-01-01	2020-01-31	2020-02-01	2020-02-28
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_period/inputs/dataset.tsv`
- Size: 210 bytes

```text
USUBJID	ADT	P1SDT	P1EDT	P2SDT	P2EDT
01	2020-01-10	2020-01-01	2020-01-31	2020-02-01	2020-02-28
02	2020-02-15	2020-01-01	2020-01-31	2020-02-01	2020-02-28
03	2020-03-01	2020-01-01	2020-01-31	2020-02-01	2020-02-28
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_period/solution.R`
- Size: 580 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
adt <- as.Date(dataset$ADT)
p1s <- as.Date(dataset$P1SDT); p1e <- as.Date(dataset$P1EDT)
p2s <- as.Date(dataset$P2SDT); p2e <- as.Date(dataset$P2EDT)
aperiod <- ifelse(adt >= p1s & adt <= p1e, 1L, ifelse(adt >= p2s & adt <= p2e, 2L, NA_integer_))
result_df <- data.frame(USUBJID = dataset$USUBJID, ADT = adt, APERIOD = aperiod, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_period/outputs/result.csv`
- Size: 72 bytes

```csv
"USUBJID","ADT","APERIOD"
1,2020-01-10,1
2,2020-02-15,2
3,2020-03-01,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(admiral)
library(dplyr)
library(readr)
library(lubridate)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
adsl <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    ADT     = col_date(format = "%Y-%m-%d"),
    P1SDT   = col_date(format = "%Y-%m-%d"),
    P1EDT   = col_date(format = "%Y-%m-%d"),
    P2SDT   = col_date(format = "%Y-%m-%d"),
    P2EDT   = col_date(format = "%Y-%m-%d")
  )
)

# Derive period variable using admiral
adsl_period <- adsl %>%
  derive_vars_period(
    new_var = APERIOD,
    reference_date = ADT,
    start_date = exprs(
      P1SDT,
      P2SDT
    ),
    end_date = exprs(
      P1EDT,
      P2EDT
    ),
    period_source = "number"
  )

# Select required columns and write output
adsl_period %>%
  select(USUBJID, ADT, APERIOD) %>%
  mutate(
    ADT = format(ADT, "%Y-%m-%d")
  ) %>%
  write_csv(file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_period/sample_00/case_01/stderr.txt`
- Size: 1704 bytes

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

Error in derive_vars_period(., new_var = APERIOD, reference_date = ADT,  :
  unused arguments (reference_date = ADT, start_date = exprs(P1SDT, P2SDT), end_date = exprs(P1EDT, P2EDT), period_source = "number")
Calls: %>%
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
