# Case 056: pharmaverse/admiral/censor_source

## Case Metadata

- Task ID: `pharmaverse/admiral/censor_source`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform censor source using the admiral clinical task contract.

Input: spec.tsv
Output: result.csv


Required columns for result.csv: field, value
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### spec.tsv (103 bytes)
field	value
dataset_name	adsl
filter	SAFFL == "Y"
date	ADT
censor	1
set_var	CNSR
... [2 more lines omitted]
```

## Input Data

### `spec.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/censor_source/inputs/spec.tsv`
- Size: 103 bytes

```text
field	value
dataset_name	adsl
filter	SAFFL == "Y"
date	ADT
censor	1
set_var	CNSR
set_value	1
order	ADT
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/censor_source/solution.R`
- Size: 1277 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

spec <- read.delim(file.path("inputs", "spec.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
vals <- stats::setNames(spec$value, spec$field)
obj <- admiral::censor_source(
  dataset_name = vals[["dataset_name"]],
  filter = parse_expr(vals[["filter"]]),
  date = sym(vals[["date"]]),
  censor = as.integer(vals[["censor"]]),
  set_values_to = exprs(!!sym(vals[["set_var"]]) := as.integer(vals[["set_value"]])),
  order = exprs(!!sym(vals[["order"]]))
)
result <- data.frame(
  field = c("class", "dataset_name", "filter", "date", "censor", "set_values_to", "order"),
  value = c(
    paste(class(obj), collapse = "|"),
    obj$dataset_name,
    paste(deparse(obj$filter), collapse = " "),
    paste(deparse(obj$date), collapse = " "),
    as.character(obj$censor),
    paste(names(obj$set_values_to), vapply(obj$set_values_to, function(x) paste(deparse(x), collapse = " "), character(1)), sep = "=", collapse = ";"),
    paste(vapply(obj$order, function(x) paste(deparse(x), collapse = " "), character(1)), collapse = ",")
  ),
  stringsAsFactors = FALSE
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/censor_source/outputs/result.csv`
- Size: 242 bytes

```csv
"field","value"
"class","censor_source|tte_source|source|list"
"dataset_name","adsl"
"filter","parse_expr(vals[[""filter""]])"
"date","sym(vals[[""date""]])"
"censor","1"
"set_values_to","CNSR=as.integer(vals[[""set_value""]])"
"order","ADT"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tidyr)
  library(stringr)
  library(fs)
})

# Create outputs directory if needed
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read spec
spec_path <- file.path("inputs", "spec.tsv")
spec <- read_tsv(spec_path, show_col_types = FALSE)

# Pivot spec to name-value pairs
spec_long <- spec %>%
  select(field, value) %>%
  filter(!is.na(field), field != "") %>%
  distinct()

# Write result
write_csv(spec_long, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__censor_source/sample_00/case_01/llm_outputs/result.csv`
- Size: 107 bytes

```csv
field,value
dataset_name,adsl
filter,"SAFFL == ""Y"""
date,ADT
censor,1
set_var,CNSR
set_value,1
order,ADT
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__censor_source/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: field"
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
            "reason": "Value mismatch in column: field"
          }
        }
      }
    }
  ]
}
```
