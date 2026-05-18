# Case 096: pharmaverse/admiral/derive_param_bsa

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_param_bsa`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive param BSA using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVAL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (75 bytes)
USUBJID	PARAMCD	AVAL
01	HEIGHT	170
01	WEIGHT	70
02	HEIGHT	180
02	WEIGHT	80
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_param_bsa/inputs/dataset.tsv`
- Size: 75 bytes

```text
USUBJID	PARAMCD	AVAL
01	HEIGHT	170
01	WEIGHT	70
02	HEIGHT	180
02	WEIGHT	80
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_param_bsa/solution.R`
- Size: 493 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
wide <- reshape(dataset, idvar = "USUBJID", timevar = "PARAMCD", direction = "wide")
result_df <- data.frame(
  USUBJID = wide$USUBJID,
  PARAMCD = "BSA",
  AVAL = sqrt(as.numeric(wide$AVAL.HEIGHT) * as.numeric(wide$AVAL.WEIGHT) / 3600),
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_param_bsa/outputs/result.csv`
- Size: 62 bytes

```csv
"USUBJID","PARAMCD","AVAL"
1,"BSA",1.81811868577262
2,"BSA",2
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required packages
library(dplyr)
library(readr)
library(stringr)
library(fs)

# Create outputs directory if it doesn't exist
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read input dataset
input_df <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  show_col_types = FALSE
)

# Pivot HEIGHT and WEIGHT, then derive BSA using Mosteller formula:
# BSA (m^2) = sqrt( (height(cm) * weight(kg)) / 3600 )
bsa_df <- input_df %>%
  filter(PARAMCD %in% c("HEIGHT", "WEIGHT")) %>%
  select(USUBJID, PARAMCD, AVAL) %>%
  tidyr::pivot_wider(
    id_cols = USUBJID,
    names_from = PARAMCD,
    values_from = AVAL
  ) %>%
  mutate(
    AVAL = sqrt((HEIGHT * WEIGHT) / 3600),
    PARAMCD = "BSA"
  ) %>%
  select(USUBJID, PARAMCD, AVAL)

# Write result
write_csv(bsa_df, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_param_bsa/sample_00/case_01/llm_outputs/result.csv`
- Size: 55 bytes

```csv
USUBJID,PARAMCD,AVAL
01,BSA,1.818118685772619
02,BSA,2
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_param_bsa/sample_00/case_01/stderr.txt`
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
