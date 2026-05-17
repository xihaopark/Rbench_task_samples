# Case 05 - `pharmaverse/tidytlg/check_req_arg`

**Package:** `tidytlg`  **Function:** `check_req_arg`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Audit root cause:** `prompt_reference_mismatch`  **Confidence:** `high`

## Audit Evidence

Reference solution evaluates `!is.null(arg)` but then overwrites with `result <- arg`, so expected `result.csv` is the input value. Current prompt says `check_req_arg` returns TRUE/FALSE, and current solution writes `check_req_arg_result.csv`/RDS, not the required reference artifact.

## Task Prompt From `task.json`

```text
Write R code to implement the **Check req arg** workflow using the `tidytlg` package.
At the beginning, load required packages: library(tidytlg).

**Inputs:**
- `inputs/arg.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'arg.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Check Req Arg** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
Write R code to check_req_arg using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/arg.tsv. Use tidytlg's check_req_arg function with the following parameters: arg (required argument to check). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: TRUE/FALSE based on if argument is NULL. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### arg.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Simple Generated Prompt

```text
Create R script to perform check req arg using the tidytlg clinical task contract.

Input: arg.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### arg.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Actual Input Files

**`arg.tsv`**

```tsv
arg
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"id","result"
1,"test_value"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"id, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(tidytlg))

# 1. 读取输入数据 / Read input data
arg_path <- file.path("inputs", "arg.tsv")
if (!file.exists(arg_path)) {
  stop("arg.tsv is required input")
}
arg <- read.delim(arg_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("arg")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }

# 3. 执行函数实现 / Execute function implementation
arg <- arg[[1]]
  !is.null(arg)
result <- arg

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
if (exists("summary_stats")) {
  write.csv(summary_stats, file.path(outputs_dir, "summary.csv"), row.names = FALSE)
}
}
```

## Current Prompt LLM Code

```r
library(tidytlg)

# Create required directories if they don't exist
if (!dir.exists("inputs")) dir.create("inputs", recursive = TRUE, showWarnings = FALSE)
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE, showWarnings = FALSE)

# Robust reader for TSV
safe_read_tsv <- function(path) {
  if (!file.exists(path)) {
    stop(sprintf("Input file not found: %s", path))
  }
  
  df <- tryCatch(
    {
      read.delim(
        file = path,
        header = TRUE,
        sep = "\t",
        stringsAsFactors = FALSE,
        check.names = FALSE,
        quote = "",
        comment.char = "",
        na.strings = c("", "NA", "NaN", "NULL")
      )
    },
    error = function(e) {
      stop(sprintf("Error reading %s: %s", path, e$message))
    }
  )
  
  if (!is.data.frame(df)) {
    stop("Parsed object is not a data.frame; possible parsing/misalignment issue.")
  }
  
  # Basic validation: at least one row, one column, and required column "arg"
  if (nrow(df) < 1L || ncol(df) < 1L) {
    stop("Input data has no rows or no columns; check file content.")
  }
  
  if (!"arg" %in% colnames(df)) {
    stop("Required column 'arg' not found in input data; check header or delimiter.")
  }
  
  # Check for row shifts: more than one non-NA value in first row may indicate misalignment
  non_na_first_row <- sum(!is.na(df[1, ]))
  if (non_na_first_row != 1L) {
    warning("Unexpected number of non-NA entries in first row; possible column misalignment.")
  }
  
  df
}

# Read input
input_path <- file.path("inputs", "arg.tsv")
arg_df <- safe_read_tsv(input_path)

# Extract argument to check
# Expecting a single value in column 'arg'
if (nrow(arg_df) != 1L) {
  warning(sprintf(
    "Expected exactly 1 row in 'arg.tsv', found %d. Using the first row only.",
    nrow(arg_df)
  ))
}
arg_value <- arg_df$arg[1]

# Apply tidytlg::check_req_arg
result <- tryCatch(
  {
    tidytlg::check_req_arg(arg = arg_value)
  },
  error = function(e) {
    stop(sprintf("Error in check_req_arg: %s", e$message))
  }
)

# Determine output file name and format
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

# Since the function returns a logical scalar (not a data frame), save as RDS
out_rds_path <- file.path(out_dir, "check_req_arg_result.rds")
saveRDS(result, out_rds_path)

# Also create a simple one-row data.frame summary and save as CSV for convenience
result_df <- data.frame(
  arg = arg_value,
  is_not_null = as.logical(result),
  stringsAsFactors = FALSE
)

out_csv_path <- file.path(out_dir, "check_req_arg_result.csv")
write.csv(result_df, out_csv_path, row.names = FALSE, na = "")

# Verify written files
verify_output_file <- function(path, type = c("RDS", "CSV")) {
  type <- match.arg(type)
  
  if (!file.exists(path)) {
    stop(sprintf("Expected output file not found: %s", path))
  }
  
  if (type == "RDS") {
    obj <- tryCatch(readRDS(path), error = function(e) e)
    if (inherits(obj, "error")) {
      stop(sprintf("Error reading RDS file %s: %s", path, obj$message))
    }
    if (!is.logical(obj) || length(obj) != 1L) {
      warning(sprintf(
        "RDS output at %s is not a logical scalar; type/shape mismatch.",
        path
      ))
    }
  } else if (type == "CSV") {
    df <- tryCatch(
      read.csv(path, stringsAsFactors = FALSE, check.names = FALSE),
      error = function(e) e
    )
    if (inherits(df, "error")) {
      stop(sprintf("Error reading CSV file %s: %s", path, df$message))
    }
    if (!all(c("arg", "is_not_null") %in% colnames(df))) {
      warning(sprintf(
        "CSV output at %s does not contain expected columns 'arg' and 'is_not_null'.",
        path
      ))
    }
    if (nrow(df) != 1L) {
      warning(sprintf(
        "CSV output at %s has %d rows; expected 1. Possible duplication or miswrite.",
        path, nrow(df)
      ))
    }
  }
}

verify_output_file(out_rds_path, "RDS")
verify_output_file(out_csv_path, "CSV")
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
Error in value[[3L]](cond) : 
  Error in check_req_arg: 'check_req_arg' is not an exported object from 'namespace:tidytlg'
Calls: tryCatch -> tryCatchList -> tryCatchOne -> <Anonymous>
Execution halted

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

_No files found._

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(lubridate)
})

#--------------------------------------------------------------------
# Paths
#--------------------------------------------------------------------
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

arg_file    <- file.path(in_dir, "arg.tsv")
result_file <- file.path(out_dir, "result.csv")

#--------------------------------------------------------------------
# Helpers
#--------------------------------------------------------------------
check_required_arg <- function(df, col_name = "arg") {
  res <- tibble(
    check_name   = "required_arg_present",
    status       = NA_character_,
    message      = NA_character_,
    arg_value    = NA_character_,
    parsed_valid = NA
  )

  if (!col_name %in% names(df)) {
    res$status  <- "FAIL"
    res$message <- sprintf("Missing required column '%s' in arg.tsv", col_name)
    return(res)
  }

  val <- df[[col_name]][1]

  if (is.na(val) || val == "") {
    res$status  <- "FAIL"
    res$message <- "Required argument is missing or empty"
    res$arg_value <- NA_character_
    res$parsed_valid <- FALSE
    return(res)
  }

  # basic ISO-8601 datetime check (tidytlg clinical contract style)
  dt <- suppressWarnings(ymd_hms(val, quiet = TRUE))
  if (is.na(dt)) {
    res$status  <- "FAIL"
    res$message <- "Argument is not a valid ISO-8601 datetime (YYYY-MM-DDThh:mm:ss)"
    res$arg_value <- val
    res$parsed_valid <- FALSE
  } else {
    res$status  <- "PASS"
    res$message <- "Required argument present and valid"
    res$arg_value <- val
    res$parsed_valid <- TRUE
  }

  res
}

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------
if (!file.exists(arg_file)) {
  result <- tibble(
    check_name   = "required_arg_present",
    status       = "FAIL",
    message      = "Input file inputs/arg.tsv not found",
    arg_value    = NA_character_,
    parsed_valid = NA
  )
} else {
  arg_df <- suppressMessages(read_tsv(arg_file, show_col_types = FALSE))
  result <- check_required_arg(arg_df, "arg")
}

write_csv(result, result_file)
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
Error in as.POSIXlt.character(x, tz, ...) : 
  character string is not in a standard unambiguous format
Calls: check_required_arg ... as.POSIXct.default -> as.POSIXct -> as.POSIXlt -> as.POSIXlt.character
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
  "task_id": "pharmaverse/tidytlg/check_req_arg",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "returncode": 1,
  "comparison": null,
  "normalizations": null
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/tidytlg/check_req_arg",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "returncode": 1,
  "comparison": null,
  "normalizations": null
}
```
