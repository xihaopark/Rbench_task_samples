# Case 059: pharmaverse/admiral/compute_bmi

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_bmi`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform compute bmi using the admiral clinical task contract.

Input: height.tsv, weight.tsv
Output: result.csv


Required columns for result.csv: height, weight, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### height.tsv (19 bytes)
height
170
180
165

### weight.tsv (16 bytes)
weight
70
80
60
```

## Input Data

### `height.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bmi/inputs/height.tsv`
- Size: 19 bytes

```text
height
170
180
165
```

### `weight.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bmi/inputs/weight.tsv`
- Size: 16 bytes

```text
weight
70
80
60
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bmi/solution.R`
- Size: 528 bytes

```r
suppressPackageStartupMessages(library(admiral))

height <- as.numeric(read.delim(file.path("inputs", "height.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
weight <- as.numeric(read.delim(file.path("inputs", "weight.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
result <- admiral::compute_bmi(height = height, weight = weight)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(height = height, weight = weight, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bmi/outputs/result.csv`
- Size: 99 bytes

```csv
"height","weight","result"
170,70,24.2214532871972
180,80,24.6913580246914
165,60,22.0385674931129
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
height_df <- read_tsv(
  file = file.path("inputs", "height.tsv"),
  col_types = cols(),
  show_col_types = FALSE
)

weight_df <- read_tsv(
  file = file.path("inputs", "weight.tsv"),
  col_types = cols(),
  show_col_types = FALSE
)

# Join and compute BMI (height in cm -> m)
result_df <- bind_cols(height_df, weight_df) %>%
  mutate(
    result = weight / ( (height / 100) ^ 2 )
  ) %>%
  select(height, weight, result)

# Write output
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_bmi/sample_00/case_01/llm_outputs/result.csv`
- Size: 98 bytes

```csv
height,weight,result
170,70,24.221453287197235
180,80,24.691358024691358
165,60,22.03856749311295
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_bmi/sample_00/case_01/stderr.txt`
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
