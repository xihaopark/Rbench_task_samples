# Case 07 - `pharmaverse/admiral/compute_age_years`

**Package:** `admiral`  **Function:** `compute_age_years`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `TIMEOUT` / tier `exec_fail`  
**Simple prompt status:** `TIMEOUT` / tier `exec_fail`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `medium`

## Audit Evidence

Reference requires exact `outputs/result.csv` with columns `age, age_unit, result`. Current candidate prompt omits the exact required path and says save in an appropriate format; current solution writes `outputs/age_years.csv` and `outputs/age_years.rds`, while simple writes `AGE,AGEU` instead of the reference schema.

## Task Prompt From `task.json`

```text
Write R code to convert age to **years** for ADaM. Load `library(admiral)`.

**Inputs:** `inputs/age.tsv`, `inputs/age_unit.tsv` — numeric age and a unit string (`years`, `months`, `weeks`, `days`, `hours`, `minutes`, `seconds`); invalid units fall back to `years` in the reference.

**Computation:** **`admiral::compute_age_years(age, age_unit)`** — public API.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.

```

## Current Generated Prompt

```text
Write R code to compute age in years using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/age.tsv, inputs/age_unit.tsv). Converts a set of age values from the specified time unit to years. `"seconds"`, `NA_character_`. Additional details: that passing `NA_character_` as a unit will result in an `NA` value for the outputted age. Also note, underlying computations assume an equal number of days in each year (365.25). Use admiral's compute_age_years function with the following parameters: age (The ages to convert. A numeric vector is expected.), age_unit (Age unit.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The ages contained in `age` converted to years.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### age.tsv (39 bytes)
age
67.9
64.2
72.7
69.8
55.8
51.4
76.3

### age_unit.tsv (15 bytes)
age_unit
years

```

## Simple Generated Prompt

```text
Create R script to perform compute age years using the admiral clinical task contract.

Input: age.tsv, age_unit.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### age.tsv (39 bytes)
age
67.9
64.2
72.7
69.8
55.8
51.4
76.3

### age_unit.tsv (15 bytes)
age_unit
years

```

## Actual Input Files

**`age.tsv`**

```tsv
age
0.1
1.5
10.0
100.0
1000.0

```

**`age_unit.tsv`**

```tsv
age_unit
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"age","age_unit","result"
0.1,"years",0.1
1.5,"years",1.5
10,"years",10
100,"years",100
1000,"years",1000

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"age, age_unit, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))

# 1. 读取输入数据 / Read input data
age_path <- file.path("inputs", "age.tsv")
if (!file.exists(age_path)) {
  stop("age.tsv is required input")
}
age_df <- read.delim(age_path, check.names = FALSE, stringsAsFactors = FALSE)
age_col <- if ("age" %in% names(age_df)) age_df$age else age_df[[1]]
age <- suppressWarnings(as.numeric(as.character(age_col)))
age_unit_path <- file.path("inputs", "age_unit.tsv")
if (!file.exists(age_unit_path)) {
  stop("age_unit.tsv is required input")
}
age_unit_df <- read.delim(age_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
age_unit <- tolower(as.character(age_unit_df[[1]][1]))
valid_units <- c("years", "months", "weeks", "days", "hours", "minutes", "seconds")
if (!age_unit %in% valid_units) age_unit <- "years"

# 3. 执行函数实现 / Execute function implementation
result <- admiral::compute_age_years(age, age_unit)

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    age = age, age_unit = age_unit,
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
library(admiral)

# Create output directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

#-------------------------
# Helper: safe file read
#-------------------------
safe_read_tsv <- function(path, ...) {
  if (!file.exists(path)) {
    stop(sprintf("Input file not found: %s", path))
  }
  out <- tryCatch(
    read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, ...),
    error = function(e) stop(sprintf("Failed to read %s: %s", path, e$message))
  )
  if (!is.data.frame(out)) {
    stop(sprintf("Unexpected object type from %s (not a data.frame).", path))
  }
  out
}

#-------------------------
# Read and validate inputs
#-------------------------
age_df <- safe_read_tsv("inputs/age.tsv")
age_unit_df <- safe_read_tsv("inputs/age_unit.tsv")

# Basic structure checks
required_age_cols <- "age"
required_age_unit_cols <- "age_unit"

if (!all(required_age_cols %in% colnames(age_df))) {
  stop("Column 'age' not found in inputs/age.tsv.")
}
if (!all(required_age_unit_cols %in% colnames(age_unit_df))) {
  stop("Column 'age_unit' not found in inputs/age_unit.tsv.")
}

# Coerce and validate 'age'
if (!is.numeric(age_df$age)) {
  suppressWarnings(age_df$age <- as.numeric(age_df$age))
}
if (anyNA(age_df$age)) {
  warning("Some age values could not be coerced to numeric and are NA.")
}

# Interpret age_unit:
# - If only one unit is provided, recycle it to match length of age
# - If multiple, ensure length matches
age_unit_vec <- age_unit_df$age_unit

if (length(age_unit_vec) == 0L) {
  stop("No age_unit values found in inputs/age_unit.tsv.")
}

if (length(age_unit_vec) == 1L) {
  age_unit_full <- rep(age_unit_vec, length(age_df$age))
} else if (length(age_unit_vec) == nrow(age_df)) {
  age_unit_full <- age_unit_vec
} else {
  stop(
    sprintf(
      "Length mismatch: %d age values but %d age_unit values.",
      nrow(age_df), length(age_unit_vec)
    )
  )
}

# Ensure character vector; allow NA_character_ to propagate
age_unit_full <- as.character(age_unit_full)

#-------------------------
# Compute age in years
#-------------------------
# compute_age_years assumes an equal number of days per year (365.25)
# and will return NA for entries where age_unit is NA_character_.
age_years <- tryCatch(
  compute_age_years(
    age      = age_df$age,
    age_unit = age_unit_full
  ),
  error = function(e) {
    stop(sprintf("Error in compute_age_years: %s", e$message))
  }
)

#-------------------------
# Assemble result
#-------------------------
result_df <- data.frame(
  age        = age_df$age,
  age_unit   = age_unit_full,
  age_years  = age_years,
  stringsAsFactors = FALSE
)

#-------------------------
# Sanity checks on result
#-------------------------
if (nrow(result_df) != nrow(age_df)) {
  stop("Row count mismatch between input ages and result.")
}

# Check for unexpected NAs (beyond those caused by NA age or NA age_unit)
na_expected <- is.na(age_df$age) | is.na(age_unit_full)
na_unexpected <- is.na(result_df$age_years) & !na_expected

if (any(na_unexpected)) {
  warning("Unexpected NA values in computed age_years not explained by missing age or age_unit.")
}

# Optional basic pattern checks
if (any(result_df$age_years < 0, na.rm = TRUE)) {
  warning("Negative values detected in age_years; check input data.")
}

#-------------------------
# Write outputs
#-------------------------
out_csv <- "outputs/age_years.csv"
out_rds <- "outputs/age_years.rds"

write.csv(result_df, file = out_csv, row.names = FALSE)
saveRDS(result_df, file = out_rds)

# Verify files written correctly
if (!file.exists(out_csv)) {
  stop("Failed to write CSV output: outputs/age_years.csv")
}
if (!file.exists(out_rds)) {
  stop("Failed to write RDS output: outputs/age_years.rds")
}

# Quick read-back check to ensure no obvious corruption
csv_check <- tryCatch(
  read.csv(out_csv, stringsAsFactors = FALSE),
  error = function(e) stop(sprintf("Failed to re-read CSV output: %s", e$message))
)
rds_check <- tryCatch(
  readRDS(out_rds),
  error = function(e) stop(sprintf("Failed to re-read RDS output: %s", e$message))
)

if (!is.data.frame(csv_check) || !is.data.frame(rds_check)) {
  stop("Re-read outputs are not data.frames, indicating possible write/read issues.")
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

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

**`age_years.csv`**

```csv
"age","age_unit","age_years"
67.9,"years",67.9
64.2,"years",64.2
72.7,"years",72.7
69.8,"years",69.8
55.8,"years",55.8
51.4,"years",51.4
76.3,"years",76.3

```

**`age_years.rds`**

```text
[binary artifact: age_years.rds, 190 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tidyr)
library(admiral)

# Create inputs/ and outputs/ if they don't exist
if (!dir.exists("inputs")) dir.create("inputs", recursive = TRUE)
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
age_df <- read_tsv(
  file = file.path("inputs", "age.tsv"),
  col_types = cols()
)

age_unit_df <- read_tsv(
  file = file.path("inputs", "age_unit.tsv"),
  col_types = cols()
)

# Ensure one row age_unit and replicate to match age rows
if (nrow(age_unit_df) != 1) {
  stop("age_unit.tsv must contain exactly one row.")
}

age_unit_val <- age_unit_df$age_unit[1]

df <- age_df %>%
  mutate(age_unit = age_unit_val)

# Use admiral-style age computation (age in years as numeric)
# Here age is already numeric and in years, so we standardize
result <- df %>%
  mutate(
    AGE = as.numeric(age),
    AGEU = age_unit
  ) %>%
  select(AGE, AGEU)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
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


```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
AGE,AGEU
67.9,years
64.2,years
72.7,years
69.8,years
55.8,years
51.4,years
76.3,years

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiral/compute_age_years",
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
  "task_id": "pharmaverse/admiral/compute_age_years",
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
