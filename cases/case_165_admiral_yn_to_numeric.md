# Case 165: pharmaverse/admiral/yn_to_numeric

## Case Metadata

- Task ID: `pharmaverse/admiral/yn_to_numeric`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform yn to numeric using the admiral clinical task contract.

Input: arg.tsv
Output: result.csv


Required columns for result.csv: arg, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### arg.tsv (20 bytes)
arg
Y
N
y
n
UNKNOWN
```

## Input Data

### `arg.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/yn_to_numeric/inputs/arg.tsv`
- Size: 20 bytes

```text
arg
Y
N
y
n
UNKNOWN
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/yn_to_numeric/solution.R`
- Size: 354 bytes

```r
suppressPackageStartupMessages(library(admiral))

arg <- as.character(read.delim(file.path("inputs", "arg.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
result <- admiral::yn_to_numeric(arg)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(arg = arg, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/yn_to_numeric/outputs/result.csv`
- Size: 54 bytes

```csv
"arg","result"
"Y",1
"N",0
"y",NA
"n",NA
"UNKNOWN",NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required package(s)
suppressPackageStartupMessages({
  if (!requireNamespace("readr", quietly = TRUE)) {
    stop("Package 'readr' is required but not installed.")
  }
  if (!requireNamespace("dplyr", quietly = TRUE)) {
    stop("Package 'dplyr' is required but not installed.")
  }
})

library(readr)
library(dplyr)

# Define input/output paths
input_path  <- file.path("inputs", "arg.tsv")
output_dir  <- "outputs"
output_path <- file.path(output_dir, "result.csv")

# Create outputs directory if it does not exist
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Read input
arg_df <- readr::read_tsv(
  input_path,
  col_types = cols(
    arg = col_character()
  )
)

# Y/N to numeric according to admiral-style logic:
# - Case-insensitive
# - "Y" -> 1
# - "N" -> 0
# - All other values -> NA
yn_to_numeric <- function(x) {
  x_up <- toupper(x)
  dplyr::case_when(
    x_up == "Y" ~ 1,
    x_up == "N" ~ 0,
    TRUE        ~ NA_real_
  )
}

result_df <- arg_df %>%
  mutate(result = yn_to_numeric(arg)) %>%
  select(arg, result)

# Write output
readr::write_csv(result_df, output_path, na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__yn_to_numeric/sample_00/case_01/llm_outputs/result.csv`
- Size: 36 bytes

```csv
arg,result
Y,1
N,0
y,1
n,0
UNKNOWN,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__yn_to_numeric/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric missingness mismatch in column: result"
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
            "reason": "Numeric missingness mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
