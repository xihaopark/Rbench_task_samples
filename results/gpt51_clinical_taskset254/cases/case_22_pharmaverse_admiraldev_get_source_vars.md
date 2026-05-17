# Case 22 - `pharmaverse/admiraldev/get_source_vars`

**Package:** `admiraldev`  **Function:** `get_source_vars`  **Expected artifacts:** `outputs/result.csv, outputs/result.rds`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `Medium`

## Audit Evidence

Task requires exact `outputs/result.csv` and `outputs/result.rds`; current prompt only says save "as appropriate", and current code writes `source_vars.rds` with `result.csv: File not generated`. Evaluation also compares `summary.csv`, reflecting the long template output not captured by the current/simple prompts.

## Task Prompt From `task.json`

```text
Write R code to implement the **Get source vars** workflow using the `admiraldev` package.
At the beginning, load required packages: library(admiraldev).

**Inputs:**
- `inputs/expressions.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'expressions.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiraldev::get_source_vars` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use `admiraldev::get_source_vars` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
Write R code to get source variables from a list of expressions using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data file is stored in inputs/expressions.tsv. Use admiraldev's get_source_vars function with the following parameters: expressions (A list of expressions). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: A list of expressions. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### expressions.tsv (31 bytes)
expressions
AVAL
CHG
PCHG
BASE

```

## Simple Generated Prompt

```text
Create R script to perform get source vars using the admiraldev clinical task contract.

Input: expressions.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### expressions.tsv (31 bytes)
expressions
AVAL
CHG
PCHG
BASE

```

## Actual Input Files

**`expressions.tsv`**

```tsv
expressions
"x + y"
"a * b"
"sum(z)"
"mean(values)"
"max(data)"

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
expressions_path <- file.path("inputs", "expressions.tsv")
if (!file.exists(expressions_path)) {
  stop("expressions.tsv is required input")
}
expressions <- read.delim(expressions_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("expressions")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }

# 3. 执行函数实现 / Execute function implementation
# 转换 expressions 为 named list of expressions
expressions_list <- if(is.data.frame(expressions)) {
  # 将 data frame 转换为 named list
  if(ncol(expressions) > 0 && nrow(expressions) > 0) {
    # 使用列名作为名称，值转换为表达式
    result_list <- list()
    for (col_name in names(expressions)) {
      if (col_name != "") {  # 跳过空列名
        # 提取列值并转换为表达式
        col_values <- expressions[[col_name]]
        if (length(col_values) > 0) {
          # 使用第一个值作为表达式
          if (is.character(col_values[1])) {
            result_list[[col_name]] <- rlang::parse_expr(col_values[1])
          } else {
            result_list[[col_name]] <- col_values[1]
          }
        }
      }
    }
    result_list
  } else {
    list()
  }
} else {
  expressions
}

result <- admiraldev::get_source_vars(expressions = expressions_list)

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
library(admiraldev)

# Set paths
in_file <- "inputs/expressions.tsv"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Safe read with validation
stopifnot(file.exists(in_file))

expr_df <- tryCatch(
  read.delim(
    in_file,
    header = TRUE,
    sep = "\t",
    stringsAsFactors = FALSE,
    check.names = FALSE,
    strip.white = TRUE
  ),
  error = function(e) {
    stop("Failed to read expressions.tsv: ", conditionMessage(e))
  }
)

# Basic validation of input structure
if (!("expressions" %in% names(expr_df))) {
  stop("Input file must contain a column named 'expressions'.")
}

if (nrow(expr_df) == 0L) {
  stop("No expressions found in input file.")
}

# Convert character expressions to call objects
expr_list <- lapply(expr_df$expressions, function(x) {
  if (is.na(x) || trimws(x) == "") {
    stop("Empty or NA expression encountered.")
  }
  parsed <- tryCatch(parse(text = x), error = function(e) e)
  if (inherits(parsed, "error")) {
    stop("Failed to parse expression '", x, "': ", conditionMessage(parsed))
  }
  if (length(parsed) != 1L) {
    stop("Expression '", x, "' produced ", length(parsed),
         " expressions; each row must contain exactly one.")
  }
  parsed[[1]]
})

names(expr_list) <- expr_df$expressions

# Call admiraldev::get_source_vars
src_vars <- tryCatch(
  get_source_vars(expressions = expr_list),
  error = function(e) {
    stop("get_source_vars() failed: ", conditionMessage(e))
  }
)

# Validate output
if (is.null(src_vars)) {
  stop("get_source_vars() returned NULL.")
}

# Determine output path and format
out_rds <- file.path(out_dir, "source_vars.rds")

# Save complex object as RDS
tryCatch(
  saveRDS(src_vars, out_rds),
  error = function(e) {
    stop("Failed to write RDS file: ", conditionMessage(e))
  }
)

# Post‑write verification
if (!file.exists(out_rds)) {
  stop("RDS output file was not created: ", out_rds)
}

test_read <- tryCatch(
  readRDS(out_rds),
  error = function(e) {
    stop("Failed to re‑read RDS output: ", conditionMessage(e))
  }
)

# Simple structural sanity checks
if (!identical(class(test_read), class(src_vars))) {
  warning("Class mismatch between original and re‑read src_vars object.")
}

# Optional: basic content inspection for unexpected patterns
if (is.list(test_read) && length(test_read) == 0L) {
  warning("Re‑read src_vars is an empty list; check input expressions.")
}

# If the object is (or contains) data.frames, also export CSVs for them
write_df_csv <- function(obj, prefix = "source_vars") {
  if (is.data.frame(obj)) {
    out_csv <- file.path(out_dir, paste0(prefix, ".csv"))
    tryCatch(
      {
        write.csv(obj, out_csv, row.names = FALSE)
        if (!file.exists(out_csv)) {
          warning("CSV output file was not created: ", out_csv)
        } else {
          chk <- tryCatch(
            read.csv(out_csv, stringsAsFactors = FALSE),
            error = function(e) e
          )
          if (inherits(chk, "error")) {
            warning("Failed to re‑read CSV file ", out_csv, ": ",
                    conditionMessage(chk))
          }
        }
      },
      error = function(e) {
        warning("Failed to write CSV file ", out_csv, ": ",
                conditionMessage(e))
      }
    )
  } else if (is.list(obj)) {
    for (nm in names(obj)) {
      if (!is.null(nm) && nzchar(nm)) {
        write_df_csv(obj[[nm]], paste0(prefix, "_", nm))
      }
    }
  }
}

write_df_csv(src_vars, "source_vars")
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

**`source_vars.rds`**

```text
[binary artifact: source_vars.rds, 100 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

# Load required packages
library(dplyr)
library(readr)
library(admiraldev)

# Define input and output paths
in_file <- file.path("inputs", "expressions.tsv")
out_file <- file.path("outputs", "result.csv")

# Read expressions
expr_df <- read_tsv(
  in_file,
  col_types = cols(.default = col_character())
)

# Create dummy input dataset for get_source_vars
# (Since only expressions are provided, we operate purely symbolically.)
dummy_ds <- tibble(admiral_source = "dummy")

# Apply get_source_vars to each expression
result <- expr_df %>%
  rename(expression = expressions) %>%
  mutate(
    vars = purrr::map(
      expression,
      ~ {
        res <- try(
          get_source_vars(
            dataset = dummy_ds,
            expr = rlang::parse_expr(.x)
          ),
          silent = TRUE
        )
        if (inherits(res, "try-error") || is.null(res)) {
          character()
        } else {
          unname(as.character(res))
        }
      }
    )
  ) %>%
  tidyr::unnest_longer(vars, values_to = "variable", indices_to = NULL, keep_empty = TRUE) %>%
  mutate(
    variable = ifelse(is.na(variable), "", variable)
  ) %>%
  select(expression, variable)

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

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
expression,variable
AVAL,
CHG,
PCHG,
BASE,

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiraldev/get_source_vars",
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
  "task_id": "pharmaverse/admiraldev/get_source_vars",
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
      "reason": "Shape mismatch: ref=(0, 1) vs llm=(4, 2)"
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
