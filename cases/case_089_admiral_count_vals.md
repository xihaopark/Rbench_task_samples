# Case 089: pharmaverse/admiral/count_vals

## Case Metadata

- Task ID: `pharmaverse/admiral/count_vals`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform count vals using the admiral clinical task contract.

Input: val.tsv, var.tsv
Output: result.csv


Required columns for result.csv: count
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### val.tsv (8 bytes)
val
"Y"

### var.tsv (24 bytes)
var
"Y"
"N"
"Y"
"Y"
"N"
```

## Input Data

### `val.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/count_vals/inputs/val.tsv`
- Size: 8 bytes

```text
val
"Y"
```

### `var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/count_vals/inputs/var.tsv`
- Size: 24 bytes

```text
var
"Y"
"N"
"Y"
"Y"
"N"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/count_vals/solution.R`
- Size: 877 bytes

```r
suppressPackageStartupMessages(library(admiral))

# 1. 读取输入数据 / Read input data
var_path <- file.path("inputs", "var.tsv")
if (!file.exists(var_path)) {
  stop("var.tsv is required input")
}
var_df <- read.delim(var_path, check.names = FALSE, stringsAsFactors = FALSE)
var <- var_df[[1]]

val_path <- file.path("inputs", "val.tsv")
if (!file.exists(val_path)) {
  stop("val.tsv is required input")
}
val_df <- read.delim(val_path, check.names = FALSE, stringsAsFactors = FALSE)
val <- val_df[[1]][1]

# 2. 执行函数实现 / Execute function implementation
result <- admiral::count_vals(var, val)

# 3. 创建结果并保存 / Create result and save
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
result_df <- data.frame(count = result, stringsAsFactors = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/count_vals/outputs/result.csv`
- Size: 10 bytes

```csv
"count"
3
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
val <- read_tsv(
  file = file.path("inputs", "val.tsv"),
  show_col_types = FALSE
)

var <- read_tsv(
  file = file.path("inputs", "var.tsv"),
  show_col_types = FALSE
)

# Perform count vals using admiral clinical task contract interpretation:
# Count how many rows in var match the value in val
target_val <- val$val[1]
count_res <- var %>%
  filter(var == target_val) %>%
  summarise(count = n())

# Write result
write_csv(count_res, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__count_vals/sample_00/case_01/llm_outputs/result.csv`
- Size: 8 bytes

```csv
count
3
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__count_vals/sample_00/case_01/stderr.txt`
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
