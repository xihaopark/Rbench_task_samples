# Case 138: pharmaverse/admiral/flag_event

## Case Metadata

- Task ID: `pharmaverse/admiral/flag_event`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform flag event using the admiral clinical task contract.

Input: spec.tsv
Output: result.csv


Required columns for result.csv: field, value
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### spec.tsv (74 bytes)
field	value
dataset_name	adlb
condition	AVAL > 10
by_vars	USUBJID,PARAMCD
```

## Input Data

### `spec.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/flag_event/inputs/spec.tsv`
- Size: 74 bytes

```text
field	value
dataset_name	adlb
condition	AVAL > 10
by_vars	USUBJID,PARAMCD
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/flag_event/solution.R`
- Size: 935 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

spec <- read.delim(file.path("inputs", "spec.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
vals <- stats::setNames(spec$value, spec$field)
by_syms <- strsplit(vals[["by_vars"]], ",", fixed = TRUE)[[1]]
obj <- admiral::flag_event(
  dataset_name = vals[["dataset_name"]],
  condition = parse_expr(vals[["condition"]]),
  by_vars = as.list(lapply(by_syms, sym))
)
result <- data.frame(
  field = c("class", "dataset_name", "condition", "by_vars"),
  value = c(
    paste(class(obj), collapse = "|"),
    obj$dataset_name,
    paste(deparse(obj$condition), collapse = " "),
    paste(vapply(obj$by_vars, function(x) paste(deparse(x), collapse = " "), character(1)), collapse = ",")
  ),
  stringsAsFactors = FALSE
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/flag_event/outputs/result.csv`
- Size: 147 bytes

```csv
"field","value"
"class","flag_event|source|list"
"dataset_name","adlb"
"condition","parse_expr(vals[[""condition""]])"
"by_vars","USUBJID,PARAMCD"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(purrr)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read spec
spec <- read_tsv(
  file = file.path("inputs", "spec.tsv"),
  show_col_types = FALSE
)

# Convert spec to named vector for easy access
spec_list <- setNames(spec$value, spec$field)

dataset_name <- spec_list[["dataset_name"]]
condition    <- spec_list[["condition"]]
by_vars_raw  <- spec_list[["by_vars"]]

# Parse by_vars into character vector
by_vars <- if (!is.na(by_vars_raw) && nzchar(by_vars_raw)) {
  str_split(by_vars_raw, ",")[[1]] |> str_trim()
} else {
  character(0)
}

# Prepare output
result <- tribble(
  ~field,          ~value,
  "dataset_name",  dataset_name,
  "condition",     condition,
  "by_vars",       paste(by_vars, collapse = ",")
)

# Write result
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__flag_event/sample_00/case_01/llm_outputs/result.csv`
- Size: 76 bytes

```csv
field,value
dataset_name,adlb
condition,AVAL > 10
by_vars,"USUBJID,PARAMCD"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__flag_event/sample_00/case_01/stderr.txt`
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
  "failure_stage": "schema_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "schema_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "schema_mismatch",
          "reason": "Shape mismatch: ref=(4, 2) vs llm=(3, 2)"
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
            "stage": "schema_mismatch",
            "tier": "output_bad",
            "reason": "Shape mismatch: ref=(4, 2) vs llm=(3, 2)"
          }
        }
      }
    }
  ]
}
```
