# Case 43 - `pharmaverse/admiraldev/assert_same_type`

**Package:** `admiraldev`  **Function:** `assert_same_type`  **Expected artifacts:** `outputs/result.csv, outputs/summary.csv`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_reference_mismatch`  **Confidence:** `high`

## Audit Evidence

Reference solution says no input files are required and calls `admiraldev::assert_same_type()` with no args, also writing `summary.csv`. Prompts expose `admiraldev.tsv`, leading solutions to validate or manufacture arguments and produce wrong/missing artifacts.

## Task Prompt From `task.json`

```text
Write R code to implement the **Assert same type** workflow using the `admiraldev` package.
At the beginning, load required packages: library(admiraldev).

**Inputs:**
- `inputs/admiraldev.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'admiraldev.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiraldev::assert_same_type` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use `admiraldev::assert_same_type` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
Write R code to are all arguments of the same type? using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data files are stored in inputs/ directory. Checks if all arguments are of the same type. Use admiraldev's assert_same_type function. The function returns: The function throws an error if not all arguments are of the same type.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### admiraldev.tsv (32 bytes)
admiraldev
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform assert same type using the admiraldev clinical task contract.

Input: admiraldev.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### admiraldev.tsv (32 bytes)
admiraldev
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`admiraldev.tsv`**

```tsv
admiraldev
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
""

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
0,0,""

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiraldev))

# 1. 读取输入数据 / Read input data
# No input files required

# 3. 执行函数实现 / Execute function implementation
result <- admiraldev::assert_same_type()

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
library(admiraldev)

# Create required directories if they do not exist
if (!dir.exists("inputs")) dir.create("inputs", recursive = TRUE)
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Load input data
admiraldev_path <- file.path("inputs", "admiraldev.tsv")
if (!file.exists(admiraldev_path)) {
  stop("Input file not found: ", admiraldev_path)
}

admiraldev_tbl <- tryCatch(
  {
    read.delim(
      admiraldev_path,
      header = FALSE,
      sep = "\t",
      stringsAsFactors = FALSE,
      col.names = "value"
    )
  },
  error = function(e) {
    stop("Failed to read 'admiraldev.tsv': ", conditionMessage(e))
  }
)

# Basic validation on input data
if (!is.data.frame(admiraldev_tbl)) {
  stop("'admiraldev_tbl' is not a data.frame after import.")
}
if (!"value" %in% names(admiraldev_tbl)) {
  stop("Expected column 'value' not found in 'admiraldev_tbl'.")
}
if (nrow(admiraldev_tbl) == 0L) {
  stop("'admiraldev_tbl' has zero rows; cannot proceed.")
}

# Prepare arguments for type check (use the column as a vector)
arg1 <- admiraldev_tbl$value
arg2 <- as.character(admiraldev_tbl$value)
arg3 <- paste0(admiraldev_tbl$value)

# The following call should succeed (all character vectors)
res_same_type_ok <- tryCatch(
  {
    assert_same_type(arg1, arg2, arg3)
  },
  error = function(e) {
    stop("Unexpected error in assert_same_type for same-type arguments: ", conditionMessage(e))
  }
)

# Also attempt a failing example for robustness checking (numeric vs character)
# This is wrapped in tryCatch to avoid stopping the script
arg_num <- seq_len(nrow(admiraldev_tbl))
res_same_type_fail <- tryCatch(
  {
    assert_same_type(arg1, arg_num)
  },
  error = function(e) {
    # Capture error message as a character vector
    structure(
      list(
        success = FALSE,
        message = conditionMessage(e)
      ),
      class = "assert_same_type_error"
    )
  }
)

# Determine object classes to choose output format
class_ok <- class(res_same_type_ok)
class_fail <- class(res_same_type_fail)

# Helper function: write object based on its type
write_output_object <- function(obj, base_name) {
  out_rds <- file.path("outputs", paste0(base_name, ".rds"))
  out_csv <- file.path("outputs", paste0(base_name, ".csv"))

  # If it's a data.frame, write CSV and RDS
  if (is.data.frame(obj)) {
    tryCatch(
      {
        write.csv(obj, out_csv, row.names = FALSE)
      },
      error = function(e) {
        stop("Failed to write CSV '", out_csv, "': ", conditionMessage(e))
      }
    )
    tryCatch(
      {
        saveRDS(obj, out_rds)
      },
      error = function(e) {
        stop("Failed to write RDS '", out_rds, "': ", conditionMessage(e))
      }
    )
    return(invisible(list(csv = out_csv, rds = out_rds)))
  }

  # For non-data.frame (e.g., logical, list, custom objects), write only RDS
  tryCatch(
    {
      saveRDS(obj, out_rds)
    },
    error = function(e) {
      stop("Failed to write RDS '", out_rds, "': ", conditionMessage(e))
    }
  )
  invisible(list(rds = out_rds))
}

# Write outputs
files_ok   <- write_output_object(res_same_type_ok,   "assert_same_type_ok")
files_fail <- write_output_object(res_same_type_fail, "assert_same_type_fail")

# Confirm that output files were written and perform basic validation
check_written_file <- function(path, type = c("rds", "csv")) {
  type <- match.arg(type)
  if (!file.exists(path)) {
    stop("Expected output file not found: ", path)
  }

  if (type == "rds") {
    obj <- tryCatch(
      {
        readRDS(path)
      },
      error = function(e) {
        stop("Failed to read back RDS '", path, "': ", conditionMessage(e))
      }
    )
    # Basic structural checks to detect obvious misalignment/parsing issues
    if (is.data.frame(obj)) {
      if (anyDuplicated(names(obj))) {
        stop("Duplicate column names detected in '", path, "'.")
      }
      if (any(vapply(obj, function(x) all(is.na(x)), logical(1L)))) {
        warning("One or more columns are entirely NA in '", path, "'. Check for possible parsing issues.")
      }
    }
  } else if (type == "csv") {
    obj <- tryCatch(
      {
        read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
      },
      error = function(e) {
        stop("Failed to read back CSV '", path, "': ", conditionMessage(e))
      }
    )
    if (!is.data.frame(obj)) {
      stop("CSV file '", path, "' did not read back as data.frame.")
    }
    if (anyDuplicated(names(obj))) {
      stop("Duplicate column names detected in CSV '", path, "'.")
    }
  }

  invisible(TRUE)
}

# Check RDS outputs
if (!is.null(files_ok$rds))   check_written_file(files_ok$rds,   "rds")
if (!is.null(files_fail$rds)) check_written_file(files_fail$rds, "rds")

# Check CSV outputs (if any)
if (!is.null(files_ok$csv))   check_written_file(files_ok$csv,   "csv")
if (!is.null(files_fail$csv)) check_written_file(files_fail$csv, "csv")
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

**`assert_same_type_fail.rds`**

```text
[binary artifact: assert_same_type_fail.rds, 212 bytes]
```

**`assert_same_type_ok.rds`**

```text
[binary artifact: assert_same_type_ok.rds, 44 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(admiraldev)

# Paths
in_file  <- file.path("inputs", "admiraldev.tsv")
out_file <- file.path("outputs", "result.csv")

# Read input (single column of variable names)
vars_tbl <- read_tsv(
  in_file,
  col_names = "var",
  show_col_types = FALSE
)

# Define expected types (example contract: all character)
# Adjust here if specific variables must be otherwise
type_contract <- tibble::tibble(
  var  = vars_tbl$var,
  type = "character"
)

# Create a dummy empty dataset with the required variables and types
create_col <- function(type) {
  switch(
    type,
    character = character(),
    numeric   = numeric(),
    integer   = integer(),
    logical   = logical(),
    factor    = factor(),
    character()
  )
}

dummy_data <- purrr::map_df(
  seq_len(nrow(type_contract)),
  ~ tibble::tibble(!!type_contract$var[.x] := create_col(type_contract$type[.x]))
)

# Perform assert_same_type using the clinical task contract
# (here we assert the dummy_data conforms to the contract defined above)
result <- tryCatch(
  {
    assert_same_type(
      data     = dummy_data,
      contract = type_contract,
      var_col  = "var",
      type_col = "type"
    )
    tibble::tibble(status = "pass")
  },
  error = function(e) {
    tibble::tibble(status = "fail", message = conditionMessage(e))
  }
)

# Ensure outputs dir exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Write result
write_csv(result, out_file)
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


Attaching package: ‘admiraldev’

The following object is masked from ‘package:dplyr’:

    filter_if


```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
status,message
fail,"Arguments `data`, `contract`, `var_col`, and `type_col` must be the same
type.
ℹ Argument types are `data` <list>, `contract` <list>, `var_col` <character>,
  `type_col` <character>"

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiraldev/assert_same_type",
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
      "reason": "File not generated"
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
  "task_id": "pharmaverse/admiraldev/assert_same_type",
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
      "reason": "Shape mismatch: ref=(0, 1) vs llm=(1, 2)"
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
