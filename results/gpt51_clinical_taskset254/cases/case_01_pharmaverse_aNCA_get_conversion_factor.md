# Case 01 - `pharmaverse/aNCA/get_conversion_factor`

**Package:** `aNCA`  **Function:** `get_conversion_factor`  **Expected artifacts:** `outputs/result.csv, outputs/summary.csv`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `high`

## Audit Evidence

Reference prompt says to compute `units::set_units(1, initial_unit, mode='standard')` and not require exported `aNCA::get_conversion_factor`; current prompt instead targets the public `get_conversion_factor` routine. Comparison: `result.csv` ref `(5, 3)` vs current `(0, 1)`, simple `(1, 1)`, and `summary.csv` missing.

## Task Prompt From `task.json`

```text
Write R code to compute a **numeric conversion factor** between two unit strings. Load `library(units)` and optionally `library(aNCA)`.

**Inputs:** `inputs/initial_unit.tsv`, `inputs/target_unit.tsv` — read unit strings from the named columns.

**Computation:** The reference converts **1** from `initial_unit` to `target_unit` using **`units::set_units(..., mode='standard')`** and `as.numeric`, returning `1` when units match and `NA` when conversion is invalid. Do **not** require an exported `aNCA::get_conversion_factor`; match the reference numeric output.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.

```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for get conversion factor. The available input files are `inputs/initial_unit.tsv`, `inputs/target_unit.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `get_conversion_factor`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### initial_unit.tsv (34 bytes)
initial_unit
AVAL
AVISITN
USUBJID

### target_unit.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Simple Generated Prompt

```text
Create R script to perform get conversion factor using the aNCA clinical task contract.

Input: initial_unit.tsv, target_unit.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### initial_unit.tsv (34 bytes)
initial_unit
AVAL
AVISITN
USUBJID

### target_unit.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Actual Input Files

**`initial_unit.tsv`**

```tsv
initial_unit
"yes"
"no"
"true"
"false"
"active"

```

**`target_unit.tsv`**

```tsv
target_unit
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"

```

## Reference Output Files

**`result.csv`**

```csv
"initial_unit","target_unit","result"
"yes","item_a",NA
"no","item_b",NA
"true","item_c",NA
"false","item_d",NA
"active","item_e",NA

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"initial_unit, target_unit, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
initial_unit_path <- file.path("inputs", "initial_unit.tsv")
if (!file.exists(initial_unit_path)) {
  stop("initial_unit.tsv is required input")
}
initial_unit_df <- read.delim(initial_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
initial_unit <- initial_unit_df$initial_unit
target_unit_path <- file.path("inputs", "target_unit.tsv")
if (!file.exists(target_unit_path)) {
  stop("target_unit.tsv is required input")
}
target_unit_df <- read.delim(target_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
target_unit <- target_unit_df$target_unit

# 2. 执行函数实现 / Execute function implementation
result <- tryCatch({
  conversion <- units::set_units(
    units::set_units(1, initial_unit, mode = "standard"),
    target_unit, mode = "standard"
  )
  unname(as.numeric(conversion))
}, error = function(e) {
  if (isTRUE(paste0(initial_unit) == paste0(target_unit))) {
    1
  } else {
    NA
  }
})

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    initial_unit = initial_unit, target_unit = target_unit,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# 4. 生成汇总统计 / Generate summary statistics
if (is.data.frame(result_df)) {
  summary_stats <- data.frame(
    n_rows = nrow(result_df),
    n_cols = ncol(result_df),
    col_names = paste(colnames(result_df), collapse = ", "),
    stringsAsFactors = FALSE)
  } else if (is.vector(result) || is.numeric(result)) {
  summary_stats <- data.frame(
    n_values = length(result),
    mean_value = mean(result, na.rm = TRUE),
    min_value = min(result, na.rm = TRUE),
    max_value = max(result, na.rm = TRUE),
    median_value = median(result, na.rm = TRUE),
    stringsAsFactors = FALSE)
  } else {
  summary_stats <- data.frame(
    result_type = class(result)[1],
    stringsAsFactors = FALSE
  )
}

# 5. 保存输出 / Save outputs
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
if (exists("result_df") && is.data.frame(result_df)) {
  write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (exists("result")) {
  if (is.data.frame(result)) {
    write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (is.list(result)) {
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  } else if (is.vector(result) || is.numeric(result) || is.character(result)) {
    result_df <- data.frame(result = result, stringsAsFactors = FALSE)
    write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else {
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  }
} else {
  stop("No result variable found. Function implementation may not have returned a value.")
}
if (exists("summary_stats")) {
  write.csv(summary_stats, file.path(outputs_dir, "summary.csv"), row.names = FALSE)
}
```

## Current Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  # load any required packages here if needed
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
}

# Helper to read TSV with header, keep types simple
read_tsv_simple <- function(path) {
  read.table(
    file = path,
    header = TRUE,
    sep = "\t",
    quote = "",
    comment.char = "",
    check.names = FALSE,
    stringsAsFactors = FALSE
  )
}

# Read inputs
initial_unit_df <- read_tsv_simple("inputs/initial_unit.tsv")
target_unit_df  <- read_tsv_simple("inputs/target_unit.tsv")

# Convert 1-column, multi-row tables to vectors; 1-row tables to scalars
as_arg <- function(df) {
  if (nrow(df) == 1 && ncol(df) == 1) {
    return(df[[1]][1])
  }
  if (ncol(df) == 1) {
    return(df[[1]])
  }
  df
}

initial_unit_arg <- as_arg(initial_unit_df)
target_unit_arg  <- as_arg(target_unit_df)

# Load aNCA and call get_conversion_factor
if (!requireNamespace("aNCA", quietly = TRUE)) {
  stop("Package 'aNCA' is required but not installed.")
}

# Call public routine; adjust argument names as required by aNCA
# Here we assume signature like get_conversion_factor(initial_unit, target_unit, ...)
full_result <- aNCA::get_conversion_factor(
  initial_unit = initial_unit_arg,
  target_unit  = target_unit_arg
)

# Normalize result for grading:
# - if scalar or vector, make a 1-column data.frame
# - if matrix/array, coerce to data.frame
# - if list, try to simplify; else store in RDS only
normalize_for_csv <- function(x) {
  if (is.data.frame(x)) {
    return(x)
  }
  if (is.matrix(x) || is.array(x)) {
    return(as.data.frame(x, stringsAsFactors = FALSE))
  }
  if (is.atomic(x)) {
    return(data.frame(result = x, check.names = FALSE))
  }
  # fallback for complex objects: attempt as.data.frame
  df <- try(as.data.frame(x, stringsAsFactors = FALSE), silent = TRUE)
  if (!inherits(df, "try-error")) {
    return(df)
  }
  # last resort: character summary
  data.frame(result = I(list(x)), check.names = FALSE)
}

result_df <- normalize_for_csv(full_result)

# Write compact, inspectable CSV
write.csv(
  result_df,
  file = "outputs/result.csv",
  row.names = FALSE,
  na = ""
)

# Also store full object as RDS when required
saveRDS(full_result, file = "outputs/result.rds")
```

## Current Prompt Execution Logs

**`stderr.txt`**

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
Registered S3 method overwritten by 'tern':
  method   from 
  tidy.glm broom

```

**`stdout.txt`**

```text
NULL

```

## Current Prompt Output Files

**`result.csv`**

```csv
"result"




```

**`result.rds`**

```text
[binary artifact: result.rds, 49 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

# aNCA clinical task contract: get conversion factor
# Inputs:
#   inputs/initial_unit.tsv  (column: initial_unit)
#   inputs/target_unit.tsv   (column: arg, row 2 = target unit or context)
# Output:
#   outputs/result.csv       (single numeric: conversion factor)

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
initial_path <- file.path("inputs", "initial_unit.tsv")
target_path  <- file.path("inputs", "target_unit.tsv")

initial_df <- readr::read_tsv(initial_path, show_col_types = FALSE)
target_df  <- readr::read_tsv(target_path,  show_col_types = FALSE)

# Extract initial and target "units" according to contract
# Here we treat the first non-header value of `initial_unit` as the initial unit
# and the second row of `arg` as the target spec.
initial_unit <- NA_character_
if ("initial_unit" %in% names(initial_df)) {
  vals <- initial_df$initial_unit
  vals <- vals[!is.na(vals) & vals != ""]
  if (length(vals) > 0) initial_unit <- vals[1]
}

target_unit <- NA_character_
if ("arg" %in% names(target_df) && nrow(target_df) >= 2) {
  target_unit <- target_df$arg[2]
}

# Placeholder: determine conversion factor
# In absence of a defined mapping, default factor = 1
conversion_factor <- 1

# Optionally, you could implement specific mappings here, for example:
# if (!is.na(initial_unit) && !is.na(target_unit)) {
#   if (initial_unit == target_unit) {
#     conversion_factor <- 1
#   } else {
#     # add specific mapping rules here
#   }
# }

# Write result
result_path <- file.path("outputs", "result.csv")
readr::write_csv(
  tibble::tibble(conversion_factor = conversion_factor),
  result_path
)
```

## Simple Prompt Execution Logs

**`stderr.txt`**

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

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
conversion_factor
1

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/get_conversion_factor",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "returncode": 0,
  "comparison": {
    "result.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "Shape mismatch: ref=(5, 3) vs llm=(0, 1)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    }
  },
  "normalizations": []
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/aNCA/get_conversion_factor",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "returncode": 0,
  "comparison": {
    "result.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "Shape mismatch: ref=(5, 3) vs llm=(1, 1)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    }
  },
  "normalizations": []
}
```
