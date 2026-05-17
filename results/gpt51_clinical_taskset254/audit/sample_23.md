# Sample 23: pharmaverse/admiraldev/squote

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiraldev/squote`
- package/function: `admiraldev` / `squote`
- expected_artifacts: `outputs/result.csv`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `NO_OUTPUT` tier=`exec_fail`

## Reference Prompt
```text
Quote with **single quotes**. Load `library(admiraldev)`.

**Computation:** **`admiraldev::squote(x)`**.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.

```

## Current Prompt
```text
Write R code to wrap a string in single quotes using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/x.tsv. Use admiraldev's squote function with the following parameters: x (A `character` vector). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: A `character` vector. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### x.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Simple Prompt
```text
Create R script to perform squote using the admiraldev clinical task contract.

Input: x.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### x.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=File not generated | summary.csv: match=False reason=File not generated"
}
```

## Simple Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "message": "No output files created",
  "returncode": 1,
  "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
  "comparison": ""
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(admiraldev))

# 1. 读取输入数据 / Read input data
x_path <- file.path("inputs", "x.tsv")
if (!file.exists(x_path)) {
  stop("x.tsv is required input")
}
x_df <- read.delim(x_path, check.names = FALSE, stringsAsFactors = FALSE)
x <- x_df$x

# 3. 执行函数实现 / Execute function implementation
x_path <- file.path("inputs", "x.tsv")
if (!file.exists(x_path)) {
  stop("x.tsv is required input")
}
x_df <- read.delim(x_path, check.names = FALSE, stringsAsFactors = FALSE)
x <- if(ncol(x_df) > 0 && nrow(x_df) > 0) x_df[[1]] else x_df
result <- admiraldev::squote(x)

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    x = x,
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

## Current Solution
```r
library(admiraldev)

#------------------------------
# Helper functions
#------------------------------

safe_read_tsv <- function(path) {
  if (!file.exists(path)) {
    stop(sprintf("Input file not found: %s", path))
  }
  df <- tryCatch(
    read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop(sprintf("Failed to read TSV file '%s': %s", path, e$message))
  )
  if (!is.data.frame(df) || nrow(df) == 0L) {
    stop(sprintf("Input TSV '%s' is empty or not a data frame.", path))
  }
  df
}

validate_x_column <- function(df, col = "x") {
  if (!col %in% names(df)) {
    stop(sprintf("Required column '%s' not found in input data.", col))
  }
  x <- df[[col]]
  if (!is.character(x)) {
    if (is.factor(x)) {
      x <- as.character(x)
    } else {
      x <- as.character(x)
      warning(sprintf("Column '%s' was not character; coerced to character.", col))
    }
  }
  if (anyNA(x)) {
    warning(sprintf("Column '%s' contains NA values; these will be processed as NA.", col))
  }
  x
}

safe_write_csv <- function(df, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  tryCatch(
    {
      write.csv(df, file = path, row.names = FALSE, na = "")
    },
    error = function(e) stop(sprintf("Failed to write CSV file '%s': %s", path, e$message))
  )
  if (!file.exists(path) || file.info(path)$size == 0L) {
    stop(sprintf("Written CSV file '%s' is missing or empty.", path))
  }
}

safe_write_rds <- function(obj, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  tryCatch(
    {
      saveRDS(obj, file = path)
    },
    error = function(e) stop(sprintf("Failed to write RDS file '%s': %s", path, e$message))
  )
  if (!file.exists(path) || file.info(path)$size == 0L) {
    stop(sprintf("Written RDS file '%s' is missing or empty.", path))
  }
}

check_unexpected_patterns <- function(original, quoted) {
  if (length(original) != length(quoted)) {
    stop("Length mismatch between original and quoted vectors; possible data misalignment.")
  }
  if (any(grepl("''", quoted))) {
    warning("Detected double single-quotes in output; inspect for unexpected escaping.")
  }
  if (any(!nzchar(original) & nzchar(quoted))) {
    warning("Empty original strings became non-empty after quoting; check parsing.")
  }
}

#------------------------------
# Main processing
#------------------------------

input_path  <- "inputs/x.tsv"
output_csv  <- "outputs/x_quoted.csv"
output_rds  <- "outputs/x_quoted.rds"

# Read and validate input
df_in <- safe_read_tsv(input_path)
x_vec <- validate_x_column(df_in, "x")

# Apply admiraldev::squote
x_quoted <- squote(x = x_vec)

if (!is.character(x_quoted)) {
  stop("Result of squote(x) is not a character vector as expected.")
}

# Basic sanity checks
check_unexpected_patterns(x_vec, x_quoted)

# Prepare output data frame
df_out <- data.frame(
  x_original = x_vec,
  x_quoted   = x_quoted,
  stringsAsFactors = FALSE
)

# Write outputs
safe_write_csv(df_out, output_csv)
safe_write_rds(x_quoted, output_rds)

# Post-write verification
df_check <- tryCatch(
  read.csv(output_csv, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) stop(sprintf("Failed to re-read written CSV '%s': %s", output_csv, e$message))
)

if (!all(df_check$x_quoted == df_out$x_quoted)) {
  stop("Re-read CSV content does not match in-memory data; possible write/read misalignment.")
}
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(admiraldev)
library(dplyr)
library(readr)
library(stringr)

# Input / output paths ----------------------------------------------------
in_file  <- file.path("inputs", "x.tsv")
out_file <- file.path("outputs", "result.csv")

# Ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input --------------------------------------------------------------
x <- read_tsv(in_file, show_col_types = FALSE)

# Perform squote using admiraldev clinical task contract ------------------
# Assumes a column named `x` in x.tsv containing the strings to squote.
result <- x %>%
  mutate(
    squote = format_squote(.data$x)
  )

# Write output ------------------------------------------------------------
write_csv(result, out_file)
```

## Current Candidate Prompt File
```text
Write R code to wrap a string in single quotes using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/x.tsv. Use admiraldev's squote function with the following parameters: x (A `character` vector). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: A `character` vector. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to wrap a string in single quotes using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/x.tsv. Use admiraldev's squote function with the following parameters: x (A `character` vector). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: A `character` vector. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```