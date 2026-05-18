# Case 133: pharmaverse/admiral/extract_unit

## Case Metadata

- Task ID: `pharmaverse/admiral/extract_unit`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform extract unit using the admiral clinical task contract.

Input: x.tsv
Output: result.csv


Required columns for result.csv: x, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### x.tsv (120 bytes)
x
"Systolic blood pressure (mmHg)"
"Dose normalized AUC (h*ng/mL)"
"Body weight (kg)"
"QT interval (msec)"
"Heart rate"
```

## Input Data

### `x.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extract_unit/inputs/x.tsv`
- Size: 120 bytes

```text
x
"Systolic blood pressure (mmHg)"
"Dose normalized AUC (h*ng/mL)"
"Body weight (kg)"
"QT interval (msec)"
"Heart rate"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extract_unit/solution.R`
- Size: 450 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(stringr))

x_df <- read.delim(file.path("inputs", "x.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
x <- as.character(x_df[[ncol(x_df)]])
if (length(x) == 0) x <- "10 (mg)"

result <- admiral::extract_unit(x)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(x = x, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extract_unit/outputs/result.csv`
- Size: 163 bytes

```csv
"x","result"
"Systolic blood pressure (mmHg)","mmHg"
"Dose normalized AUC (h*ng/mL)","h*ng/mL"
"Body weight (kg)","kg"
"QT interval (msec)","msec"
"Heart rate",NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)
library(fs)

# Create outputs directory if it doesn't exist
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read input
x <- read_tsv("inputs/x.tsv", show_col_types = FALSE)

# Simple unit extraction using patterns common in clinical text
extract_unit <- function(text) {
  # Look for parentheses content
  unit_paren <- str_match(text, "\\(([^()]*)\\)")[, 2]
  unit_paren <- str_trim(unit_paren)

  # If parentheses exist and are not empty, use them
  if (!is.na(unit_paren) && unit_paren != "") {
    return(unit_paren)
  }

  # Otherwise return blank
  return(NA_character_)
}

result <- x %>%
  mutate(result = vapply(x, extract_unit, character(1))) %>%
  select(x, result)

# Write output
write_csv(result, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__extract_unit/sample_00/case_01/llm_outputs/result.csv`
- Size: 139 bytes

```csv
x,result
Systolic blood pressure (mmHg),mmHg
Dose normalized AUC (h*ng/mL),h*ng/mL
Body weight (kg),kg
QT interval (msec),msec
Heart rate,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__extract_unit/sample_00/case_01/stderr.txt`
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
