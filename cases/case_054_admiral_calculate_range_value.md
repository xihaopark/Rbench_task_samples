# Case 054: pharmaverse/admiral/calculate_range_value

## Case Metadata

- Task ID: `pharmaverse/admiral/calculate_range_value`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform calculate range value using the admiral clinical task contract.

Input: end_val.tsv, range_method.tsv, start_val.tsv
Output: result.csv


Required columns for result.csv: start_val, end_val, range_method, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### end_val.tsv (15 bytes)
end_val
10
6
8

### range_method.tsv (22 bytes)
range_method
midpoint

### start_val.tsv (16 bytes)
start_val
0
2
4
```

## Input Data

### `end_val.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/calculate_range_value/inputs/end_val.tsv`
- Size: 15 bytes

```text
end_val
10
6
8
```

### `range_method.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/calculate_range_value/inputs/range_method.tsv`
- Size: 22 bytes

```text
range_method
midpoint
```

### `start_val.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/calculate_range_value/inputs/start_val.tsv`
- Size: 16 bytes

```text
start_val
0
2
4
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/calculate_range_value/solution.R`
- Size: 775 bytes

```r
suppressPackageStartupMessages(library(admiral))

start_val <- as.numeric(read.delim(file.path("inputs", "start_val.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
end_val <- as.numeric(read.delim(file.path("inputs", "end_val.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
range_method <- as.character(read.delim(file.path("inputs", "range_method.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]][1])
result <- switch(range_method, start = start_val, end = end_val, midpoint = (start_val + end_val) / 2, (start_val + end_val) / 2)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(start_val = start_val, end_val = end_val, range_method = range_method, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/calculate_range_value/outputs/result.csv`
- Size: 98 bytes

```csv
"start_val","end_val","range_method","result"
0,10,"midpoint",5
2,6,"midpoint",4
4,8,"midpoint",6
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)
library(tidyr)
library(purrr)
library(fs)

# Create outputs directory if it does not exist
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read inputs
end_val <- read_tsv("inputs/end_val.tsv", show_col_types = FALSE)
start_val <- read_tsv("inputs/start_val.tsv", show_col_types = FALSE)
range_method <- read_tsv("inputs/range_method.tsv", show_col_types = FALSE)

# Basic checks
if (!"end_val" %in% names(end_val)) stop("Missing end_val column")
if (!"start_val" %in% names(start_val)) stop("Missing start_val column")
if (!"range_method" %in% names(range_method)) stop("Missing range_method column")

# Expand inputs to same length (assume row-wise pairing)
n <- max(nrow(start_val), nrow(end_val))
if (nrow(start_val) != n) {
  start_val <- start_val %>%
    slice(rep(1:nrow(.), length.out = n))
}
if (nrow(end_val) != n) {
  end_val <- end_val %>%
    slice(rep(1:nrow(.), length.out = n))
}

# Use single method for all rows (per admiral-style parameterization)
method <- range_method$range_method[1]

res <- tibble(
  start_val = start_val$start_val,
  end_val   = end_val$end_val
) %>%
  mutate(
    range_method = method,
    result = case_when(
      str_to_lower(range_method) == "midpoint" ~ (start_val + end_val) / 2,
      TRUE ~ NA_real_
    )
  )

write_csv(res, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__calculate_range_value/sample_00/case_01/llm_outputs/result.csv`
- Size: 84 bytes

```csv
start_val,end_val,range_method,result
0,10,midpoint,5
2,6,midpoint,4
4,8,midpoint,6
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__calculate_range_value/sample_00/case_01/stderr.txt`
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
