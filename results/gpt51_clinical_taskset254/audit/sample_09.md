# Sample 09: pharmaverse/metatools/dash_to_eq

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/metatools/dash_to_eq`
- package/function: `metatools` / `dash_to_eq`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `NO_OUTPUT` tier=`exec_fail`

## Reference Prompt
```text
Write R code to implement the **Dash to eq** workflow using the `metatools` package.
At the beginning, load required packages: library(metatools).

**Inputs:**
- `inputs/strin.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'strin.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Dash To Eq** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
Write R code to dash to equation using metatools. At the beginning, load the required packages: library(metatools). The input data file is stored in inputs/strin.tsv. Converts strings that are #-# style to a logical expression (but in a string format) Use metatools's dash_to_eq function with the following parameters: strin (g). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: string. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### strin.tsv (27 bytes)
strin
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform dash to eq using the metatools clinical task contract.

Input: strin.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### strin.tsv (27 bytes)
strin
AVAL
AVISITN
USUBJID

```

## Current Evaluation
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
suppressPackageStartupMessages(library(metatools))

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(stringr))

# 1. 读取输入数据 / Read input data
strin_path <- file.path("inputs", "strin.tsv")
if (!file.exists(strin_path)) {
  stop("strin.tsv is required input")
}
strin <- read.delim(strin_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("strin")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }

# 3. 执行函数实现 / Execute function implementation
# 读取 string 参数（从输入文件）
string <- if(is.data.frame(strin)) strin[[1]][1] else strin
front <- str_extract(string, "^.*(?=\\-)")
front_eq <- if_else(str_detect(front, "<|>|="), front, paste0(">=", front))
back <- str_extract(string, "(?<=\\-).*$")
back_eq <- if_else(str_detect(back, "<|>|="), back, paste0("<=", back))
result <- paste0("x", front_eq, " & x", back_eq)

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    id = seq_along(result),
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# 5. 生成汇总统计 / Generate summary statistics
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

# 6. 保存输出 / Save outputs
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
if (exi
```

## Current Solution
```r
library(metatools)

#-----------------------------
# Helper functions
#-----------------------------
safe_read_tsv <- function(path) {
  if (!file.exists(path)) {
    stop("Input file does not exist: ", path)
  }
  df <- tryCatch(
    read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop("Failed to read TSV: ", conditionMessage(e))
  )
  if (!"strin" %in% names(df)) {
    stop("Input TSV must contain a column named 'strin'.")
  }
  if (any(is.na(df$strin))) {
    warning("NA values detected in 'strin' column; these will be passed to dash_to_eq as-is.")
  }
  df
}

safe_write_csv <- function(df, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  tryCatch(
    {
      write.csv(df, path, row.names = FALSE, na = "")
      if (!file.exists(path)) stop("CSV file was not written: ", path)
    },
    error = function(e) stop("Failed to write CSV: ", conditionMessage(e))
  )
}

safe_write_rds <- function(obj, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  tryCatch(
    {
      saveRDS(obj, path)
      if (!file.exists(path)) stop("RDS file was not written: ", path)
    },
    error = function(e) stop("Failed to write RDS: ", conditionMessage(e))
  )
}

#-----------------------------
# Read input
#-----------------------------
input_path <- "inputs/strin.tsv"
strin_df   <- safe_read_tsv(input_path)

# Basic validation
if (!is.character(strin_df$strin)) {
  stop("'strin' column must be of type character.")
}
if (length(strin_df$strin) == 0L) {
  stop("'strin' column is empty; nothing to process.")
}

#-----------------------------
# Apply dash_to_eq
#-----------------------------
g <- strin_df$strin

result <- tryCatch(
  dash_to_eq(strin = g),
  error = function(e) stop("dash_to_eq failed: ", conditionMessage(e))
)

#-----------------------------
# Inspect result for issues
#-----------------------------
if (is.character(result)) {
  if (any(grepl("[^[:print:]]", result))) {
    warning("Non-printable characters detected in dash_to_eq output.")
  }
  if (any(is.na(result))) {
    warning("NA values detected in dash_to_eq output.")
  }
} else if (is.data.frame(result)) {
  if (nrow(result) != length(g)) {
    warning("Row count of result does not match length of input 'strin'; possible misalignment.")
  }
}

#-----------------------------
# Save outputs
#-----------------------------
if (is.data.frame(result)) {
  out_csv <- "outputs/strin_dash_to_eq.csv"
  safe_write_csv(result, out_csv)
} else {
  out_rds <- "outputs/strin_dash_to_eq.rds"
  safe_write_rds(result, out_rds)
}

#-----------------------------
# Post-write verification
#-----------------------------
if (exists("out_csv") && file.exists(out_csv)) {
  verify_df <- tryCatch(
    read.csv(out_csv, stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop("Failed to re-read written CSV: ", conditionMessage(e))
  )
  if (nrow(verify_df) == 0L) {
    warning("Written CSV has zero rows; possible issue with serialization.")
  }
}

if (exists("out_rds") && file.exists(out_rds)) {
  verify_obj <- tryCatch(
    readRDS(out_rds),
    error = function(e) stop("Failed to re-read written RDS: ", conditionMessage(e))
  )
  if (!identical(class(verify_obj), class(result))) {
    warning("Class of object read from RDS differs from original; check serialization.")
  }
}
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(metatools)
library(dplyr)
library(readr)

# Paths
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read STRIN file
strin_path <- file.path(in_dir, "strin.tsv")
strin <- read.delim(strin_path, stringsAsFactors = FALSE)

# Prepare clinical task contract object
# Assumes metatools clinical task contract for dash->eq uses a function `dash_to_eq`
# that accepts a vector of strings and returns a data frame with mapped results.
# Adjust function name/arguments if your specific contract differs.

# Example: metatools contract style
# result <- dash_to_eq(strings = strin$strin)

# Since the exact contract implementation is environment-specific,
# here is a generic wrapper that calls the expected contract function.
if (!exists("dash_to_eq", mode = "function")) {
  stop("dash_to_eq function (clinical task contract) not found in metatools environment.")
}

result <- dash_to_eq(strings = strin$strin)

# Ensure result is a data frame
result <- as.data.frame(result, stringsAsFactors = FALSE)

# Write result
out_path <- file.path(out_dir, "result.csv")
write_csv(result, out_path)
```

## Current Candidate Prompt File
```text
Write R code to dash to equation using metatools. At the beginning, load the required packages: library(metatools). The input data file is stored in inputs/strin.tsv. Converts strings that are #-# style to a logical expression (but in a string format) Use metatools's dash_to_eq function with the following parameters: strin (g). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: string. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to dash to equation using metatools. At the beginning, load the required packages: library(metatools). The input data file is stored in inputs/strin.tsv. Converts strings that are #-# style to a logical expression (but in a string format) Use metatools's dash_to_eq function with the following parameters: strin (g). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: string. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```