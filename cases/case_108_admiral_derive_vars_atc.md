# Case 108: pharmaverse/admiral/derive_vars_atc

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_atc`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform derive vars atc using the admiral clinical task contract.

Input: cm.tsv, facm.tsv
Output: result.csv


Required columns for result.csv: USUBJID, CMREFID, CMTRT, ATC1, ATC2
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### cm.tsv (74 bytes)
USUBJID	CMREFID	CMTRT
01	CM1	ASPIRIN
01	CM2	METFORMIN
02	CM3	ATORVASTATIN

### facm.tsv (114 bytes)
USUBJID	FAREFID	FATESTCD	FASTRESC
01	CM1	ATC1	B01AC06
01	CM1	ATC2	ASPIRIN
01	CM2	ATC1	A10BA02
02	CM3	ATC1	C10AA05
```

## Input Data

### `cm.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_atc/inputs/cm.tsv`
- Size: 74 bytes

```text
USUBJID	CMREFID	CMTRT
01	CM1	ASPIRIN
01	CM2	METFORMIN
02	CM3	ATORVASTATIN
```

### `facm.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_atc/inputs/facm.tsv`
- Size: 114 bytes

```text
USUBJID	FAREFID	FATESTCD	FASTRESC
01	CM1	ATC1	B01AC06
01	CM1	ATC2	ASPIRIN
01	CM2	ATC1	A10BA02
02	CM3	ATC1	C10AA05
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_atc/solution.R`
- Size: 600 bytes

```r
cm <- read.delim(file.path("inputs", "cm.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
facm <- read.delim(file.path("inputs", "facm.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result_df <- cm
for (code in sort(unique(facm$FATESTCD))) {
  result_df[[code]] <- NA_character_
}
for (i in seq_len(nrow(facm))) {
  hit <- result_df$USUBJID == facm$USUBJID[i] & result_df$CMREFID == facm$FAREFID[i]
  result_df[[facm$FATESTCD[i]]][hit] <- facm$FASTRESC[i]
}

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE, na = "")
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_atc/outputs/result.csv`
- Size: 145 bytes

```csv
"USUBJID","CMREFID","CMTRT","ATC1","ATC2"
1,"CM1","ASPIRIN","B01AC06","ASPIRIN"
1,"CM2","METFORMIN","A10BA02",
2,"CM3","ATORVASTATIN","C10AA05",
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tidyr)
library(stringr)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input data
cm <- read_tsv(
  file = file.path("inputs", "cm.tsv"),
  col_types = cols(.default = col_character())
)

facm <- read_tsv(
  file = file.path("inputs", "facm.tsv"),
  col_types = cols(.default = col_character())
)

# Prepare FACM: keep only ATC1/ATC2 and pivot to wide
facm_wide <- facm %>%
  filter(FATESTCD %in% c("ATC1", "ATC2")) %>%
  select(USUBJID, FAREFID, FATESTCD, FASTRESC) %>%
  mutate(FATESTCD = str_trim(FATESTCD)) %>%
  pivot_wider(
    id_cols = c(USUBJID, FAREFID),
    names_from = FATESTCD,
    values_from = FASTRESC
  ) %>%
  rename(
    CMREFID = FAREFID
  )

# Merge with CM and select required columns
result <- cm %>%
  left_join(facm_wide, by = c("USUBJID", "CMREFID")) %>%
  select(USUBJID, CMREFID, CMTRT, ATC1, ATC2)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_atc/sample_00/case_01/llm_outputs/result.csv`
- Size: 118 bytes

```csv
USUBJID,CMREFID,CMTRT,ATC1,ATC2
01,CM1,ASPIRIN,B01AC06,ASPIRIN
01,CM2,METFORMIN,A10BA02,
02,CM3,ATORVASTATIN,C10AA05,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_atc/sample_00/case_01/stderr.txt`
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
