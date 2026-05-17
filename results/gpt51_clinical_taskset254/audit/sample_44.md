# Sample 44: pharmaverse/admiraldev/assert_expr

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiraldev/assert_expr`
- package/function: `admiraldev` / `assert_expr`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Validate an **rlang** expression with `admiraldev::assert_expr`. Load `library(admiraldev)`.

Read inputs per `solution.R` and mirror its `tryCatch` / success string.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Prompt
```text
Write R code to assert argument is an expression using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/arg_name.tsv. Use admiraldev's assert_expr function with the following parameters: arg_name (By default the expression specified for `arg` is used.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error if `arg` is not an expression, i.e. either a symbol or a call, or returns the input invisibly otherwise. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### arg.tsv (24 bytes)
arg
2020-01-15T08:30:00

### arg_name.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Simple Prompt
```text
Create R script to perform assert expr using the admiraldev clinical task contract.

Input: arg.tsv, arg_name.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### arg.tsv (24 bytes)
arg
2020-01-15T08:30:00

### arg_name.tsv (24 bytes)
arg
2020-01-15T08:30:00

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
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(1, 4) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(admiraldev))

# 1. 读取输入数据 / Read input data
arg_name_path <- file.path("inputs", "arg_name.tsv")
if (!file.exists(arg_name_path)) {
  stop("arg_name.tsv is required input")
}
arg_name <- read.delim(arg_name_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("arg_name")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }

# 3. 执行函数实现 / Execute function implementation
# 提取 arg 参数值（从 arg_name 数据框）
arg <- if(is.data.frame(arg_name) && ncol(arg_name) > 0 && nrow(arg_name) > 0) {
  # 提取第一列的值，并尝试转换为表达式
  val <- arg_name[[1]]
  if (is.character(val)) {
    rlang::parse_expr(val[1])
  } else {
    rlang::sym(as.character(val[1]))
  }
} else {
  rlang::sym("x")  # 默认表达式
}

result <- tryCatch({
  admiraldev::assert_expr(arg = arg)
}, error = function(e) {
  # 如果出错，返回错误信息
  paste("Error:", conditionMessage(e))
})

# 4. 创建结果数据框 / Create result dataframe
# assert_expr 返回 invisible，所以需要特殊处理
if (is.null(result) || inherits(result, "name") || inherits(result, "call")) {
  # 表达式类型，转换为字符串
  result_df <- data.frame(
    result = as.character(result),
    status = "success",
    stringsAsFactors = FALSE)
} else if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    id = seq_along(result),
    result = result,
    stringsAsFactors = FALSE)
} else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(
    result = as.character(result),
    stringsAsFactors = FALSE)
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
    w
```

## Current Solution
```r
library(admiraldev)
library(readr)
library(dplyr)
library(rlang)
library(tools)

# Directories
input_dir <- "inputs"
output_dir <- "outputs"

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

#---------------------------
# Helper functions
#---------------------------

safe_read_tsv_single_col <- function(path, expected_col) {
  if (!file.exists(path)) {
    stop("Input file does not exist: ", path)
  }
  dat <- tryCatch(
    readr::read_tsv(path, col_types = cols(.default = "c")),
    error = function(e) stop("Failed to read TSV file: ", path, " - ", conditionMessage(e))
  )
  if (!is.data.frame(dat) || ncol(dat) != 1L) {
    stop("Input file must have exactly one column: ", path)
  }
  if (!identical(colnames(dat), expected_col)) {
    stop(
      "Unexpected column name(s) in ", path, ". Expected: ",
      paste(expected_col, collapse = ","), "; Got: ",
      paste(colnames(dat), collapse = ",")
    )
  }
  if (nrow(dat) != 1L) {
    stop("Input file must have exactly one data row: ", path)
  }
  dat
}

write_output <- function(obj, base_name) {
  if (is.data.frame(obj)) {
    out_path <- file.path(output_dir, paste0(base_name, ".csv"))
    tryCatch(
      {
        write.csv(obj, out_path, row.names = FALSE)
      },
      error = function(e) stop("Failed to write CSV output: ", out_path, " - ", conditionMessage(e))
    )
  } else {
    out_path <- file.path(output_dir, paste0(base_name, ".rds"))
    tryCatch(
      {
        saveRDS(obj, out_path)
      },
      error = function(e) stop("Failed to write RDS output: ", out_path, " - ", conditionMessage(e))
    )
  }
  out_path
}

check_written_file <- function(path) {
  if (!file.exists(path)) {
    stop("Output file was not written: ", path)
  }
  info <- file.info(path)
  if (is.na(info$size) || info$size <= 0) {
    stop("Output file appears empty or invalid: ", path)
  }
  ext <- tolower(file_ext(path))
  if (ext == "csv") {
    dat <- tryCatch(
      readr::read_csv(path, show_col_types = FALSE),
      error = function(e) stop("Failed to re-read written CSV: ", path, " - ", conditionMessage(e))
    )
    if (!is.data.frame(dat)) {
      stop("Re-read CSV is not a data frame: ", path)
    }
    if (anyNA(names(dat)) || any(names(dat) == "")) {
      stop("Unexpected column names in re-read CSV: ", path)
    }
  } else if (ext == "rds") {
    obj <- tryCatch(
      readRDS(path),
      error = function(e) stop("Failed to re-read written RDS: ", path, " - ", conditionMessage(e))
    )
    if (is.null(obj)) {
      stop("Re-read RDS object is NULL: ", path)
    }
  }
  invisible(TRUE)
}

#---------------------------
# Read and validate input
#---------------------------

arg_name_path <- file.path(input_dir, "arg_name.tsv")
arg_name_tbl <- safe_read_tsv_single_col(arg_name_path, expected_col = "arg")

# Extract the string representing the expression
arg_string <- arg_name_tbl$arg[[1]]

if (is.na(arg_string) || !nzchar(arg_string)) {
  stop("Argument string is missing or empty in arg_name.tsv")
}

# Parse string to expression (symbol or call)
expr_parsed <- tryCatch(
  parse(text = arg_string),
  error = function(e) stop("Failed to parse argument string as R expression: ", conditionMessage(e))
)

if (length(expr_parsed) != 1L) {
  stop("Parsed expression must have length 1. Got length: ", length(expr_parsed))
}

arg_expr <- expr_parsed[[1]]

#---------------------------
# Use admiraldev::assert_expr
#---------------------------

result <- tryCatch(
  admiraldev::assert_expr(arg = arg_expr, arg_name = "arg"),
  error = function(e) {
    stop("assert_expr failed: ", conditionMessage(e))
  }
)

#---------------------------
# Save result
#---------------------------

out_file <- write_output(result, base_name = "assert_expr_result")

#---------------------------
# Verify output
#---------------------------

check_written_file(out_file)
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(admiraldev)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input arguments
arg_df <- read_tsv(
  file = file.path("inputs", "arg.tsv"),
  col_types = cols(.default = col_character())
)

arg_name_df <- read_tsv(
  file = file.path("inputs", "arg_name.tsv"),
  col_types = cols(.default = col_character())
)

# Extract argument value and name
arg_value <- arg_df$arg[1]
arg_name <- arg_name_df$arg[1]

# Perform assert_expr using admiraldev clinical task contract
# Here we assert that the argument is not missing (as an example expression)
result <- tryCatch(
  {
    assert_expr(
      expr = !is.na(arg_value) && nzchar(arg_value),
      expr_name = arg_name
    )
    tibble(
      status = "PASS",
      expr_name = arg_name,
      expr = "!is.na(arg_value) && nzchar(arg_value)",
      message = NA_character_
    )
  },
  error = function(e) {
    tibble(
      status = "FAIL",
      expr_name = arg_name,
      expr = "!is.na(arg_value) && nzchar(arg_value)",
      message = conditionMessage(e)
    )
  }
)

# Write result
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## Current Candidate Prompt File
```text
Write R code to assert argument is an expression using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/arg_name.tsv. Use admiraldev's assert_expr function with the following parameters: arg_name (By default the expression specified for `arg` is used.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error if `arg` is not an expression, i.e. either a symbol or a call, or returns the input invisibly otherwise. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to assert argument is an expression using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/arg_name.tsv. Use admiraldev's assert_expr function with the following parameters: arg_name (By default the expression specified for `arg` is used.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error if `arg` is not an expression, i.e. either a symbol or a call, or returns the input invisibly otherwise. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```