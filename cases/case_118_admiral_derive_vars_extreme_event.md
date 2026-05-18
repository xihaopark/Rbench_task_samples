# Case 118: pharmaverse/admiral/derive_vars_extreme_event

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_extreme_event`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform derive vars extreme event using the admiral clinical task contract.

Input: dataset.tsv, mode.tsv, source_datasets.tsv
Output: result.csv


Required columns for result.csv: STUDYID, USUBJID, TRTSDT, EXTDT, EXTTERM, EXTGR
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (74 bytes)
STUDYID	USUBJID	TRTSDT
S1	01	2020-01-01
S1	02	2020-01-05
S1	03	2020-01-10

### mode.tsv (11 bytes)
mode
first

### source_datasets.tsv (179 bytes)
STUDYID	USUBJID	ADT	AESEQ	AETERM	AETOXGR
S1	01	2020-01-03	1	HEADACHE	1
S1	01	2020-01-08	2	NAUSEA	3
S1	02	2020-01-07	1	RASH	2
S1	02	2020-01-08	2	FEVER	1
S1	03	2020-01-15	1	COUGH	2
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_extreme_event/inputs/dataset.tsv`
- Size: 74 bytes

```text
STUDYID	USUBJID	TRTSDT
S1	01	2020-01-01
S1	02	2020-01-05
S1	03	2020-01-10
```

### `mode.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_extreme_event/inputs/mode.tsv`
- Size: 11 bytes

```text
mode
first
```

### `source_datasets.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_extreme_event/inputs/source_datasets.tsv`
- Size: 179 bytes

```text
STUDYID	USUBJID	ADT	AESEQ	AETERM	AETOXGR
S1	01	2020-01-03	1	HEADACHE	1
S1	01	2020-01-08	2	NAUSEA	3
S1	02	2020-01-07	1	RASH	2
S1	02	2020-01-08	2	FEVER	1
S1	03	2020-01-15	1	COUGH	2
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_extreme_event/solution.R`
- Size: 1141 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(rlang))

dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
ae <- read.delim(file.path("inputs", "source_datasets.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
mode <- read.delim(file.path("inputs", "mode.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$mode[1]

dataset$TRTSDT <- as.Date(dataset$TRTSDT)
ae$ADT <- as.Date(ae$ADT)

grade2_event <- admiral::event(
  dataset_name = "ae",
  condition = AETOXGR >= 2,
  set_values_to = rlang::exprs(EVNTDESC = "Grade 2 or higher adverse event")
)

result <- admiral::derive_vars_extreme_event(
  dataset = dataset,
  by_vars = rlang::exprs(STUDYID, USUBJID),
  events = list(grade2_event),
  source_datasets = list(ae = ae),
  order = rlang::exprs(dplyr::desc(AETOXGR), ADT, AESEQ),
  mode = mode,
  new_vars = rlang::exprs(EXTDT = ADT, EXTTERM = AETERM, EXTGR = AETOXGR)
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_extreme_event/outputs/result.csv`
- Size: 172 bytes

```csv
"STUDYID","USUBJID","TRTSDT","EXTDT","EXTTERM","EXTGR"
"S1",1,2020-01-01,2020-01-08,"NAUSEA",3
"S1",2,2020-01-05,2020-01-07,"RASH",2
"S1",3,2020-01-10,2020-01-15,"COUGH",2
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(lubridate)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input files
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(
    STUDYID = col_character(),
    USUBJID = col_character(),
    TRTSDT = col_character()
  )
)

mode_df <- read_tsv(
  file = file.path("inputs", "mode.tsv"),
  col_types = cols(
    mode = col_character()
  )
)

src <- read_tsv(
  file = file.path("inputs", "source_datasets.tsv"),
  col_types = cols(
    STUDYID = col_character(),
    USUBJID = col_character(),
    ADT = col_character(),
    AESEQ = col_double(),
    AETERM = col_character(),
    AETOXGR = col_character()
  )
)

# Convert dates
dataset <- dataset %>%
  mutate(
    TRTSDT = ymd(TRTSDT)
  )

src <- src %>%
  mutate(
    ADT = ymd(ADT)
  )

mode_val <- mode_df$mode[1]

# Derive extreme event per subject based on mode
# Interpretation:
#   - "first": earliest AE after or on TRTSDT
#   - "last":  latest AE after or on TRTSDT
#   - "worst": highest AETOXGR after or on TRTSDT; ties by earliest date then lowest AESEQ
# If mode is unrecognized, default to "first"

get_extreme_event <- function(adsl_row, ae_df, mode_val) {
  sub_ae <- ae_df %>%
    filter(
      STUDYID == adsl_row$STUDYID,
      USUBJID == adsl_row$USUBJID,
      !is.na(ADT),
      ADT >= adsl_row$TRTSDT
    )

  if (nrow(sub_ae) == 0) {
    return(tibble(
      STUDYID = adsl_row$STUDYID,
      USUBJID = adsl_row$USUBJID,
      TRTSDT  = adsl_row$TRTSDT,
      EXTDT   = as.Date(NA),
      EXTTERM = NA_character_,
      EXTGR   = NA_character_
    ))
  }

  mode_use <- ifelse(mode_val %in% c("first","last","worst"), mode_val, "first")

  ext_row <- switch(
    mode_use,
    "first" = sub_ae %>%
      arrange(ADT, AESEQ) %>%
      slice(1),
    "last" = sub_ae %>%
      arrange(desc(ADT), desc(AESEQ)) %>%
      slice(1),
    "worst" = {
      sub_ae %>%
        mutate(AETOXGR_NUM = suppressWarnings(as.numeric(AETOXGR))) %>%
        arrange(desc(AETOXGR_NUM), ADT, AESEQ) %>%
        slice(1)
    }
  )

  tibble(
    STUDYID = adsl_row$STUDYID,
    USUBJID = adsl_row$USUBJID,
    TRTSDT  = adsl_row$TRTSDT,
    EXTDT   = ext_row$ADT,
    EXTTERM = ext_row$AETERM,
    EXTGR   = ext_row$AETOXGR
  )
}

result <- dataset %>%
  rowwise() %>%
  do(get_extreme_event(., src, mode_val)) %>%
  ungroup() %>%
  mutate(
    TRTSDT = format(TRTSDT, "%Y-%m-%d"),
    EXTDT  = ifelse(is.na(EXTDT), NA_character_, format(EXTDT, "%Y-%m-%d"))
  ) %>%
  select(STUDYID, USUBJID, TRTSDT, EXTDT, EXTTERM, EXTGR)

write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_extreme_event/sample_00/case_01/llm_outputs/result.csv`
- Size: 153 bytes

```csv
STUDYID,USUBJID,TRTSDT,EXTDT,EXTTERM,EXTGR
S1,01,2020-01-01,2020-01-03,HEADACHE,1
S1,02,2020-01-05,2020-01-07,RASH,2
S1,03,2020-01-10,2020-01-15,COUGH,2
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_extreme_event/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: EXTDT"
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
            "reason": "Value mismatch in column: EXTDT"
          }
        }
      }
    }
  ]
}
```
