# Case 06 - `pharmaverse/admiral/count_vals`

**Package:** `admiral`  **Function:** `count_vals`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `TIMEOUT` / tier `exec_fail`  
**Simple prompt status:** `TIMEOUT` / tier `exec_fail`  
**Audit root cause:** `data_or_fixture_issue`  **Confidence:** `medium`

## Audit Evidence

Reference task is scalar `admiral::count_vals(var, val)` and fixture output is `count=1`; sample prompt preview shows unrelated-looking columns (`var.tsv` header `by_vars`, `val.tsv` header `set_values_to`). Generated solutions treat the inputs as grouping/expression metadata and even look for an extra analysis dataset.

## Task Prompt From `task.json`

```text
Count occurrences of a **single value** in a vector (ADaM-style). Load `library(admiral)`.

**Inputs:** `inputs/var.tsv` (vector to search), `inputs/val.tsv` (scalar value to count).

**Computation:** **`admiral::count_vals(var, val)`** — exported API; write the scalar count to `outputs/result.csv` as in the reference.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.

```

## Current Generated Prompt

```text
Write R code to count number of observations where a variable equals a value using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/var.tsv, inputs/val.tsv). Count number of observations where a variable equals a value. Use admiral's count_vals function with the following parameters: var (A vector), val (A value). Ensure that you carefully read and process the input data according to the parameter requirements. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### val.tsv (51 bytes)
set_values_to
exprs(AVAL = mean(AVAL, na.rm=TRUE))

### var.tsv (23 bytes)
by_vars
USUBJID
AVISIT

```

## Simple Generated Prompt

```text
Create R script to perform count vals using the admiral clinical task contract.

Input: val.tsv, var.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### val.tsv (51 bytes)
set_values_to
exprs(AVAL = mean(AVAL, na.rm=TRUE))

### var.tsv (23 bytes)
by_vars
USUBJID
AVISIT

```

## Actual Input Files

**`val.tsv`**

```tsv
val
"test_value"

```

**`var.tsv`**

```tsv
var
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"count"
1

```

## Reference Code

**`solution.R`**

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
write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)

```

## Current Prompt LLM Code

```r
library(admiral)
library(readr)
library(dplyr)
library(purrr)
library(rlang)
library(stringr)

# Create outputs directory if not exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#-----------------------------
# Helper functions
#-----------------------------

stop_if_not_file <- function(path) {
  if (!file.exists(path)) {
    stop(paste0("Required input file not found: ", path), call. = FALSE)
  }
}

safe_write_csv <- function(x, path) {
  tryCatch(
    {
      write_csv(x, path)
      if (!file.exists(path)) stop(paste0("Failed to write CSV: ", path), call. = FALSE)
    },
    error = function(e) stop(paste0("Error writing CSV '", path, "': ", e$message), call. = FALSE)
  )
}

safe_save_rds <- function(x, path) {
  tryCatch(
    {
      saveRDS(x, path)
      if (!file.exists(path)) stop(paste0("Failed to write RDS: ", path), call. = FALSE)
    },
    error = function(e) stop(paste0("Error writing RDS '", path, "': ", e$message), call. = FALSE)
  )
}

#-----------------------------
# Read and validate input files
#-----------------------------

var_path <- file.path("inputs", "var.tsv")
val_path <- file.path("inputs", "val.tsv")

stop_if_not_file(var_path)
stop_if_not_file(val_path)

var_tbl <- tryCatch(
  read_tsv(var_path, show_col_types = FALSE),
  error = function(e) stop(paste0("Error reading ", var_path, ": ", e$message), call. = FALSE)
)

val_tbl <- tryCatch(
  read_tsv(val_path, show_col_types = FALSE),
  error = function(e) stop(paste0("Error reading ", val_path, ": ", e$message), call. = FALSE)
)

if (!"by_vars" %in% names(var_tbl)) {
  stop("`var.tsv` must contain a column named 'by_vars'.", call. = FALSE)
}

if (!"set_values_to" %in% names(val_tbl)) {
  stop("`val.tsv` must contain a column named 'set_values_to'.", call. = FALSE)
}

# Extract var (vector of variable names)
var_vec <- var_tbl$by_vars %>%
  discard(is.na) %>%
  str_trim()

if (length(var_vec) == 0L) {
  stop("No variable names found in `var.tsv` column 'by_vars'.", call. = FALSE)
}

# Extract val expression string
val_str <- val_tbl$set_values_to %>%
  discard(is.na) %>%
  paste(collapse = " ")

if (val_str == "") {
  stop("No value expression found in `val.tsv` column 'set_values_to'.", call. = FALSE)
}

# Parse val as expression safely
val_expr <- tryCatch(
  parse_expr(val_str),
  error = function(e) stop(paste0("Failed to parse 'set_values_to' expression: ", e$message), call. = FALSE)
)

#-----------------------------
# Prepare mock input data
#-----------------------------
# NOTE: Replace this with reading your actual analysis dataset, e.g.:
# adsl <- read_xpt("inputs/adsl.xpt") etc.
# Here we construct a minimal example to allow count_vals to run.

set.seed(123)
adsl <- tibble(
  USUBJID = sprintf("SUBJ%03d", 1:100),
  AVISIT  = sample(c("BASELINE", "WEEK 4", "WEEK 8"), 100, replace = TRUE),
  AVAL    = rnorm(100, mean = 10, sd = 2)
)

# Validate that requested vars exist in data
missing_vars <- setdiff(var_vec, names(adsl))
if (length(missing_vars) > 0L) {
  stop(
    paste0(
      "Variables not found in input dataset: ",
      paste(missing_vars, collapse = ", ")
    ),
    call. = FALSE
  )
}

#-----------------------------
# Use admiral::count_vals
#-----------------------------

# count_vals() is typically used inside derive_summary_records / derivations;
# here we call it directly with the requested parameters `var` and `val`.

count_result <- tryCatch(
  admiral::count_vals(
    var = var_vec,
    val = val_expr
  ),
  error = function(e) stop(paste0("Error in admiral::count_vals: ", e$message), call. = FALSE)
)

#-----------------------------
# Save outputs
#-----------------------------

# Save var and val objects for traceability
safe_write_csv(
  tibble(var = var_vec),
  file.path("outputs", "var_vector.csv")
)

safe_save_rds(
  val_expr,
  file.path("outputs", "val_expression.rds")
)

# Save count_vals result
if (is.data.frame(count_result)) {
  out_path <- file.path("outputs", "count_vals_result.csv")
  safe_write_csv(count_result, out_path)
} else {
  out_path <- file.path("outputs", "count_vals_result.rds")
  safe_save_rds(count_result, out_path)
}

#-----------------------------
# Basic validation / sanity checks
#-----------------------------

# Reload outputs to confirm integrity
if (grepl("\\.csv$", out_path)) {
  reloaded <- tryCatch(
    read_csv(out_path, show_col_types = FALSE),
    error = function(e) stop(paste0("Error re-reading output CSV: ", e$message), call. = FALSE)
  )
} else {
  reloaded <- tryCatch(
    readRDS(out_path),
    error = function(e) stop(paste0("Error re-reading output RDS: ", e$message), call. = FALSE)
  )
}

if (is.data.frame(reloaded) && nrow(reloaded) == 0L) {
  warning("Output contains zero rows; check if this is expected given the input data and criteria.")
}

if (is.data.frame(reloaded)) {
  if (anyNA(reloaded)) {
    warning("Detected NA values in the output; verify if these are expected.")
  }
}

# Simple alignment check: if data frame, ensure no duplicated column names
if (is.data.frame(reloaded)) {
  if (any(duplicated(names(reloaded)))) {
    warning("Detected duplicated column names in the output data; this may indicate misalignment.")
  }
}
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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union


Attaching package: ‘rlang’

The following objects are masked from ‘package:purrr’:

    flatten, flatten_chr, flatten_dbl, flatten_int, flatten_lgl,
    flatten_raw, invoke, splice


```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

**`count_vals_result.rds`**

```text
[binary artifact: count_vals_result.rds, 49 bytes]
```

**`val_expression.rds`**

```text
[binary artifact: val_expression.rds, 98 bytes]
```

**`var_vector.csv`**

```csv
var
USUBJID
AVISIT

```

## Simple Prompt LLM Code

```r
# count_vals.R

library(dplyr)
library(readr)
library(stringr)
library(rlang)

# Create outputs dir if not exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read task contract pieces
val_path <- file.path("inputs", "val.tsv")
var_path <- file.path("inputs", "var.tsv")

val_df <- readr::read_tsv(val_path, show_col_types = FALSE, col_names = FALSE)
var_df <- readr::read_tsv(var_path, show_col_types = FALSE, col_names = FALSE)

set_values_to <- val_df$X1[val_df$X1 != "set_values_to"]
by_vars      <- var_df$X1[var_df$X1 != "by_vars"]

# Build expression from set_values_to
# Expecting something like: exprs(AVAL = mean(AVAL, na.rm=TRUE))
set_values_str <- paste(set_values_to, collapse = "\n")
set_values_expr <- rlang::parse_expr(set_values_str)

# Evaluate exprs() to get a named list of expressions
set_values_list <- eval(set_values_expr)

# Convert by_vars character vector to symbols
by_syms <- rlang::syms(by_vars)

# Read analysis dataset
# Expect standard ADaM-style input: a single ADaM file under inputs/adsl/adtte/etc.
# Here, assume "inputs/adsl.csv" or "inputs/adam.csv" not specified,
# so we assume a generic "inputs/input.csv".
# Adjust path as needed for your environment.
input_candidates <- list.files("inputs", pattern = "\\.(csv|tsv)$", full.names = TRUE)
input_candidates <- setdiff(input_candidates, c(val_path, var_path))

if (length(input_candidates) != 1) {
  stop("Expected exactly one analysis dataset file in inputs/ (besides val.tsv and var.tsv).")
}

adam_path <- input_candidates[1]

if (grepl("\\.tsv$", adam_path, ignore.case = TRUE)) {
  adam <- readr::read_tsv(adam_path, show_col_types = FALSE)
} else {
  adam <- readr::read_csv(adam_path, show_col_types = FALSE)
}

# Summarise by the requested BY variables and set_values_to expressions
result <- adam %>%
  group_by(!!!by_syms) %>%
  summarise(!!!set_values_list, .groups = "drop")

# Write result
readr::write_csv(result, file.path("outputs", "result.csv"))
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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error: Expected exactly one analysis dataset file in inputs/ (besides val.tsv and var.tsv).
Execution halted

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

_No files found._

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiral/count_vals",
  "status": "TIMEOUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "returncode": null,
  "comparison": null,
  "normalizations": null
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/admiral/count_vals",
  "status": "TIMEOUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "returncode": null,
  "comparison": null,
  "normalizations": null
}
```
