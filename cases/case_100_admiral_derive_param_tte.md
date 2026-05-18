# Case 100: pharmaverse/admiral/derive_param_tte

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_param_tte`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform derive param tte using the admiral clinical task contract.

Input: dataset_adsl.tsv
Output: result.csv


Required columns for result.csv: USUBJID, STUDYID, EVNTDESC, SRCDOM, SRCVAR, CNSR, ADT, STARTDT, PARAMCD, PARAM
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset_adsl.tsv (158 bytes)
USUBJID	STUDYID	TRTSDT	DTHFL	DTHDT	LSALVDT
01	STUDY1	2021-01-01	Y	2021-04-01	2021-04-01
02	STUDY1	2021-01-02	N		2021-03-15
03	STUDY1	2021-01-05	N		2021-02-20
```

## Input Data

### `dataset_adsl.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_param_tte/inputs/dataset_adsl.tsv`
- Size: 158 bytes

```text
USUBJID	STUDYID	TRTSDT	DTHFL	DTHDT	LSALVDT
01	STUDY1	2021-01-01	Y	2021-04-01	2021-04-01
02	STUDY1	2021-01-02	N		2021-03-15
03	STUDY1	2021-01-05	N		2021-02-20
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_param_tte/solution.R`
- Size: 821 bytes

```r
adsl <- read.delim(
  file.path("inputs", "dataset_adsl.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE,
  na.strings = c("", "NA")
)
for (col in c("TRTSDT", "DTHDT", "LSALVDT")) {
  adsl[[col]] <- as.Date(adsl[[col]])
}

is_death <- adsl$DTHFL == "Y"
result <- data.frame(
  USUBJID = adsl$USUBJID,
  STUDYID = adsl$STUDYID,
  EVNTDESC = ifelse(is_death, "DEATH", "LAST KNOWN ALIVE"),
  SRCDOM = "ADSL",
  SRCVAR = ifelse(is_death, "DTHDT", "LSALVDT"),
  CNSR = ifelse(is_death, 0L, 1L),
  ADT = ifelse(is_death, as.character(adsl$DTHDT), as.character(adsl$LSALVDT)),
  STARTDT = as.character(adsl$TRTSDT),
  PARAMCD = "OS",
  PARAM = "Overall Survival",
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE, na = "")
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_param_tte/outputs/result.csv`
- Size: 374 bytes

```csv
"USUBJID","STUDYID","EVNTDESC","SRCDOM","SRCVAR","CNSR","ADT","STARTDT","PARAMCD","PARAM"
1,"STUDY1","DEATH","ADSL","DTHDT",0,"2021-04-01","2021-01-01","OS","Overall Survival"
2,"STUDY1","LAST KNOWN ALIVE","ADSL","LSALVDT",1,"2021-03-15","2021-01-02","OS","Overall Survival"
3,"STUDY1","LAST KNOWN ALIVE","ADSL","LSALVDT",1,"2021-02-20","2021-01-05","OS","Overall Survival"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(lubridate)

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input ADSL
adsl <- read_tsv(
  file = file.path("inputs", "dataset_adsl.tsv"),
  col_types = cols(.default = col_character())
)

# Convert dates
adsl <- adsl %>%
  mutate(
    TRTSDT   = ymd(TRTSDT),
    DTHDT    = ymd(DTHDT),
    LSALVDT  = ymd(LSALVDT)
  )

# Derive ADT (event/analysis date) and censoring
res <- adsl %>%
  mutate(
    # Event description and source
    EVNTDESC = "Time to Death",
    SRCDOM   = "ADSL",
    SRCVAR   = "DTHDT",
    # Event date: death date if death flag Y, otherwise last alive date
    ADT = case_when(
      DTHFL == "Y" & !is.na(DTHDT) ~ DTHDT,
      TRUE ~ LSALVDT
    ),
    # Censoring: 0 = event (death), 1 = censored
    CNSR = if_else(DTHFL == "Y" & !is.na(DTHDT), 0L, 1L),
    # Start date
    STARTDT = TRTSDT,
    # Parameter
    PARAMCD = "TTEDEATH",
    PARAM   = "Time to Death"
  ) %>%
  select(
    USUBJID,
    STUDYID,
    EVNTDESC,
    SRCDOM,
    SRCVAR,
    CNSR,
    ADT,
    STARTDT,
    PARAMCD,
    PARAM
  )

# Write result
write_csv(res, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_param_tte/sample_00/case_01/llm_outputs/result.csv`
- Size: 316 bytes

```csv
USUBJID,STUDYID,EVNTDESC,SRCDOM,SRCVAR,CNSR,ADT,STARTDT,PARAMCD,PARAM
01,STUDY1,Time to Death,ADSL,DTHDT,0,2021-04-01,2021-01-01,TTEDEATH,Time to Death
02,STUDY1,Time to Death,ADSL,DTHDT,1,2021-03-15,2021-01-02,TTEDEATH,Time to Death
03,STUDY1,Time to Death,ADSL,DTHDT,1,2021-02-20,2021-01-05,TTEDEATH,Time to Death
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_param_tte/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: EVNTDESC"
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
            "reason": "Value mismatch in column: EVNTDESC"
          }
        }
      }
    }
  ]
}
```
