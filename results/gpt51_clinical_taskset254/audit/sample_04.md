# Sample 04: pharmaverse/tidytlg/check_file

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/tidytlg/check_file`
- package/function: `tidytlg` / `check_file`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `NO_OUTPUT` tier=`exec_fail`

## Reference Prompt
```text
Write R code to implement the **Check file** workflow using the `tidytlg` package.
At the beginning, load required packages: library(tidytlg).

**Inputs:**
- `inputs/arg.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'arg.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Check File** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
Write R code to check_arg_exists using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/arg.tsv. Use tidytlg's check_file function with the following parameters: arg (required argument to check). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: TRUE/FALSE based on if argument exists in df. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### arg.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Simple Prompt
```text
Create R script to perform check file using the tidytlg clinical task contract.

Input: arg.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### arg.tsv (24 bytes)
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
arg <- if(ncol(arg) >= 1 && nrow(arg) > 0) arg[[1]] else NULL
  if (is.null(arg)) {
    TRUE
  } else {
    result <- file.exists(arg)
  }
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

## Current Solution
```r
library(tidytlg)

#---- Setup ----
in_file  <- "inputs/arg.tsv"
out_dir  <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

#---- Error handling wrapper ----
safe_run <- function(expr) {
  tryCatch(
    expr,
    error = function(e) {
      message("ERROR: ", conditionMessage(e))
      quit(status = 1)
    },
    warning = function(w) {
      message("WARNING: ", conditionMessage(w))
      invokeRestart("muffleWarning")
    }
  )
}

safe_run({
  #---- Read input with validation ----
  if (!file.exists(in_file)) {
    stop("Input file does not exist: ", in_file)
  }

  df <- tryCatch(
    utils::read.delim(
      in_file,
      header = TRUE,
      sep = "\t",
      stringsAsFactors = FALSE,
      check.names = FALSE,
      quote = "",
      comment.char = ""
    ),
    error = function(e) {
      stop("Failed to read input TSV: ", conditionMessage(e))
    }
  )

  # Basic validation
  if (!is.data.frame(df)) stop("Input is not a data.frame after reading.")
  if (nrow(df) == 0L) warning("Input data frame has 0 rows.")
  if (ncol(df) == 0L) stop("Input data frame has 0 columns.")
  if (!"arg" %in% names(df)) {
    stop("Required column 'arg' is missing from input data.")
  }

  # Check for unexpected parsing issues (e.g., all NA, weird whitespace)
  arg_vals <- df$arg
  if (all(is.na(arg_vals))) {
    warning("'arg' column contains only NA values; possible parsing issue.")
  }
  if (any(grepl("^\\s+|\\s+$", arg_vals))) {
    warning("Leading or trailing whitespace detected in 'arg' values.")
  }

  #---- Use tidytlg's check_file to validate required argument ----
  # Assuming check_file signature: check_file(file, arg, ...)
  # and that it inspects the data frame/columns according to 'arg'.
  # Here arg is the required argument/column name to check.
  arg_name <- "arg"

  res <- tryCatch(
    check_file(file = df, arg = arg_name),
    error = function(e) {
      stop("check_file failed: ", conditionMessage(e))
    }
  )

  # Validate result type
  if (!is.logical(res) || length(res) != 1L || is.na(res)) {
    warning("Result from check_file is not a scalar non-NA logical; saving as RDS.")
    out_rds <- file.path(out_dir, "check_arg_exists_result.rds")
    saveRDS(res, out_rds)

    # Confirm file written
    if (!file.exists(out_rds)) stop("Failed to write output RDS: ", out_rds)
    msg <- paste("Wrote complex result to", out_rds)
    message(msg)

    # Basic sanity check for unexpected patterns
    str_res <- capture.output(str(res))
    if (length(str_res) == 0L) {
      warning("str() of result is empty; possible unexpected object structure.")
    }
  } else {
    # Scalar TRUE/FALSE: wrap into a data.frame and save as CSV
    out_df <- data.frame(check_arg_exists = res)
    out_csv <- file.path(out_dir, "check_arg_exists_result.csv")

    tryCatch(
      utils::write.csv(out_df, out_csv, row.names = FALSE, quote = TRUE),
      error = function(e) {
        stop("Failed to write output CSV: ", conditionMessage(e))
      }
    )

    # Confirm file written
    if (!file.exists(out_csv)) stop("Failed to write output CSV: ", out_csv)

    # Re-read to confirm and check for misalignment/parsing issues
    df_check <- tryCatch(
      utils::read.csv(out_csv, stringsAsFactors = FALSE, check.names = FALSE),
      error = function(e) {
        stop("Failed to re-read output CSV for verification: ", conditionMessage(e))
      }
    )

    if (!identical(names(df_check), "check_arg_exists")) {
      warning("Output CSV column names do not match expected 'check_arg_exists'.")
    }
    if (nrow(df_check) != 1L) {
      warning("Output CSV does not have exactly one row; possible misalignment.")
    }
    if (!is.logical(df_check$check_arg_exists) &&
        !all(df_check$check_arg_exists %in% c("TRUE", "FALSE"))) {
      warning("Output CSV 'check_arg_exists' column not purely logical/boolean.")
    }

    message("Wrote logical result to ", out_csv)
  }
})
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# paths
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# read arg file
arg_path <- file.path(in_dir, "arg.tsv")
arg_tbl  <- read_tsv(arg_path, show_col_types = FALSE)

if (!"arg" %in% names(arg_tbl)) {
  stop("arg.tsv must contain a column named 'arg'")
}

arg_value <- arg_tbl$arg[1]

# basic checks following tidytlg clinical task contract style
results <- tibble(
  check_id   = character(),
  status     = character(),
  message    = character(),
  arg_value  = character()
)

add_result <- function(id, status, msg, value = arg_value) {
  tibble(
    check_id  = id,
    status    = status,
    message   = msg,
    arg_value = value
  )
}

# check 1: non-missing
if (is.na(arg_value) || is.null(arg_value) || identical(arg_value, "")) {
  results <- bind_rows(
    results,
    add_result(
      "C001",
      "FAIL",
      "Argument value is missing or empty."
    )
  )
} else {
  results <- bind_rows(
    results,
    add_result(
      "C001",
      "PASS",
      "Argument value is present."
    )
  )
}

# check 2: ISO 8601-like datetime format
dt_parsed <- suppressWarnings(
  as.POSIXct(arg_value, format = "%Y-%m-%dT%H:%M:%S", tz = "UTC")
)

if (is.na(dt_parsed)) {
  results <- bind_rows(
    results,
    add_result(
      "C002",
      "FAIL",
      "Argument is not in expected datetime format 'YYYY-MM-DDThh:mm:ss'."
    )
  )
} else {
  results <- bind_rows(
    results,
    add_result(
      "C002",
      "PASS",
      "Argument matches expected datetime format 'YYYY-MM-DDThh:mm:ss'."
    )
  )
}

# check 3: datetime not in the future (relative to system time)
if (!is.na(dt_parsed)) {
  if (dt_parsed > Sys.time()) {
    results <- bind_rows(
      results,
      add_result(
        "C003",
        "FAIL",
        "Datetime argument is in the future relative to system time."
      )
    )
  } else {
    results <- bind_rows(
      results,
      add_result(
        "C003",
        "PASS",
        "Datetime argument is not in the future."
      )
    )
  }
} else {
  results <- bind_rows(
    results,
    add_result(
      "C003",
      "NA",
      "Datetime check not evaluated because parsing failed."
    )
  )
}

# order columns and write result
results <- results %>%
  select(check_id, status, message, arg_value)

write_csv(results, file.path(out_dir, "result.csv"), na = "")
```

## Current Candidate Prompt File
```text
Write R code to check_arg_exists using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/arg.tsv. Use tidytlg's check_file function with the following parameters: arg (required argument to check). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: TRUE/FALSE based on if argument exists in df. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to check_arg_exists using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/arg.tsv. Use tidytlg's check_file function with the following parameters: arg (required argument to check). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: TRUE/FALSE based on if argument exists in df. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```