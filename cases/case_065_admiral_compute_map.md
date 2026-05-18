# Case 065: pharmaverse/admiral/compute_map

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_map`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform compute map using the admiral clinical task contract.

Input: diabp.tsv, hr.tsv, sysbp.tsv
Output: result.csv


Required columns for result.csv: diabp, sysbp, hr, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### diabp.tsv (18 bytes)
diabp
80
85
70
95

### hr.tsv (16 bytes)
hr
60
75
90
110

### sysbp.tsv (22 bytes)
sysbp
120
135
110
160
```

## Input Data

### `diabp.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_map/inputs/diabp.tsv`
- Size: 18 bytes

```text
diabp
80
85
70
95
```

### `hr.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_map/inputs/hr.tsv`
- Size: 16 bytes

```text
hr
60
75
90
110
```

### `sysbp.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_map/inputs/sysbp.tsv`
- Size: 22 bytes

```text
sysbp
120
135
110
160
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_map/solution.R`
- Size: 646 bytes

```r
suppressPackageStartupMessages(library(admiral))

diabp <- as.numeric(read.delim(file.path("inputs", "diabp.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$diabp)
sysbp <- as.numeric(read.delim(file.path("inputs", "sysbp.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$sysbp)
hr <- as.numeric(read.delim(file.path("inputs", "hr.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$hr)
result <- admiral::compute_map(diabp = diabp, sysbp = sysbp, hr = hr)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(diabp = diabp, sysbp = sysbp, hr = hr, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_map/outputs/result.csv`
- Size: 139 bytes

```csv
"diabp","sysbp","hr","result"
80,120,60,92.7395237619899
85,135,75,103.240653638352
70,110,90,85.9752811815739
95,160,110,123.186790537475
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
diabp <- read_tsv(
  file = file.path("inputs", "diabp.tsv"),
  col_types = cols()
)

sysbp <- read_tsv(
  file = file.path("inputs", "sysbp.tsv"),
  col_types = cols()
)

hr <- read_tsv(
  file = file.path("inputs", "hr.tsv"),
  col_types = cols()
)

# Combine and compute MAP
result <- bind_cols(diabp, sysbp, hr) |>
  mutate(result = (2 * diabp + sysbp) / 3)

# Write result
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_map/sample_00/case_01/llm_outputs/result.csv`
- Size: 137 bytes

```csv
diabp,sysbp,hr,result
80,120,60,93.33333333333333
85,135,75,101.66666666666667
70,110,90,83.33333333333333
95,160,110,116.66666666666667
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_map/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric mismatch in column: result"
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
            "reason": "Numeric mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
