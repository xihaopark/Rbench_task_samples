# Case 104: pharmaverse/admiral/derive_var_pchg

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_var_pchg`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive var pchg using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVISIT, AVAL, BASE, PCHG
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (111 bytes)
USUBJID	PARAMCD	AVISIT	AVAL	BASE
01	ALT	Week 1	12	10
01	ALT	Week 2	15	10
02	ALT	Week 1	18	20
03	ALT	Week 1	5	0
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_pchg/inputs/dataset.tsv`
- Size: 111 bytes

```text
USUBJID	PARAMCD	AVISIT	AVAL	BASE
01	ALT	Week 1	12	10
01	ALT	Week 2	15	10
02	ALT	Week 1	18	20
03	ALT	Week 1	5	0
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_pchg/solution.R`
- Size: 442 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
base <- as.numeric(dataset$BASE)
aval <- as.numeric(dataset$AVAL)
pchg <- ifelse(is.na(base) | base == 0, NA_real_, 100 * (aval - base) / base)
result_df <- data.frame(dataset, PCHG = pchg, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_pchg/outputs/result.csv`
- Size: 153 bytes

```csv
"USUBJID","PARAMCD","AVISIT","AVAL","BASE","PCHG"
1,"ALT","Week 1",12,10,20
1,"ALT","Week 2",15,10,50
2,"ALT","Week 1",18,20,-10
3,"ALT","Week 1",5,0,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
adsl <- read.delim(
  file = file.path("inputs", "dataset.tsv"),
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

# Derive percent change from baseline
result <- adsl %>%
  mutate(
    PCHG = dplyr::if_else(
      !is.na(AVAL) & !is.na(BASE) & BASE != 0,
      (AVAL - BASE) / BASE * 100,
      NA_real_
    )
  ) %>%
  select(USUBJID, PARAMCD, AVISIT, AVAL, BASE, PCHG)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_pchg/sample_00/case_01/llm_outputs/result.csv`
- Size: 123 bytes

```csv
USUBJID,PARAMCD,AVISIT,AVAL,BASE,PCHG
1,ALT,Week 1,12,10,20
1,ALT,Week 2,15,10,50
2,ALT,Week 1,18,20,-10
3,ALT,Week 1,5,0,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_pchg/sample_00/case_01/stderr.txt`
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
