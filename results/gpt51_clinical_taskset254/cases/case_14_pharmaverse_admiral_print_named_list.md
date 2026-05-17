# Case 14 - `pharmaverse/admiral/print_named_list`

**Package:** `admiral`  **Function:** `print_named_list`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `TIMEOUT` / tier `exec_fail`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `high`

## Audit Evidence

Task prompt explicitly says the gold has "no call to a `print_*` export"; current prompt says "Use admiral's print_named_list", which is side-effect-oriented and mismatches the tabular reference output.

## Task Prompt From `task.json`

```text
Prepare tabular output from **`list.tsv`** with an **indent** level. Load `library(admiral)`, `library(rlang)`.

**Computation:** The reference validates `list_df`, then coerces **`list_df`** to a result data.frame (no call to a `print_*` export in the gold); copy that coercion and output paths.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Generated Prompt

```text
Write R code to print named list using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/list.tsv, inputs/indent.tsv). Use admiral's print_named_list function with the following parameters: list (A named list), indent (Indent The output is indented by the specified number of characters.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: No return value, called for side effects. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### indent.tsv (28 bytes)
indent
AVAL
AVISITN
USUBJID

### list.tsv (26 bytes)
list
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform print named list using the admiral clinical task contract.

Input: indent.tsv, list.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### indent.tsv (28 bytes)
indent
AVAL
AVISITN
USUBJID

### list.tsv (26 bytes)
list
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`indent.tsv`**

```tsv
indent
"yes"
"no"
"true"
"false"
"active"

```

**`list.tsv`**

```tsv
list
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"list"
"test_value"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,1,"list"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))

suppressPackageStartupMessages(library(rlang))

# 1. 读取输入数据 / Read input data
list_path <- file.path("inputs", "list.tsv")
if (!file.exists(list_path)) {
  stop("list.tsv is required input")
}
list_df <- read.delim(list_path, check.names = FALSE, stringsAsFactors = FALSE)
indent_path <- file.path("inputs", "indent.tsv")
if (!file.exists(indent_path)) {
  stop("indent.tsv is required input")
}
indent_df <- read.delim(indent_path, check.names = FALSE, stringsAsFactors = FALSE)
indent <- suppressWarnings(as.numeric(if ("indent" %in% names(indent_df)) indent_df$indent[1] else indent_df[[1]][1]))
if (is.na(indent)) indent <- 0

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("list_df")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  if (is.data.frame(list_df) && nrow(list_df) > 0) {
    list_df
  } else if (is.list(list_df)) {
    as.data.frame(list_df, stringsAsFactors = FALSE)
  } else {
    data.frame(value = as.character(list_df), stringsAsFactors = FALSE)
  }
}, error = function(e) data.frame(input = paste(capture.output(print(list_df)), collapse = "\n"), stringsAsFactors = FALSE))

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    indent = indent,
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
```

## Current Prompt LLM Code

```r
library(admiral)

# Directories
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

#-----------------------------
# Safe readers with validation
#-----------------------------
read_single_column <- function(path, col_name_expected) {
  if (!file.exists(path)) {
    stop(sprintf("File not found: %s", path))
  }
  df <- tryCatch(
    read.csv(path, sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop(sprintf("Failed to read %s: %s", path, e$message))
  )
  if (!is.data.frame(df) || ncol(df) != 1L) {
    stop(sprintf("File %s must contain exactly one column.", path))
  }
  if (!identical(names(df), col_name_expected)) {
    stop(sprintf("File %s must have a single column named '%s', found: %s",
                 path, col_name_expected, paste(names(df), collapse = ", ")))
  }
  if (anyNA(df[[1]])) {
    stop(sprintf("File %s contains NA values in column '%s'.", path, col_name_expected))
  }
  df[[1]]
}

#-----------------------------
# Read and validate inputs
#-----------------------------
list_path   <- file.path(in_dir, "list.tsv")
indent_path <- file.path(in_dir, "indent.tsv")

list_vals   <- read_single_column(list_path,   "list")
indent_vals <- read_single_column(indent_path, "indent")

# Validate that both vectors are identical; otherwise, warn of possible misalignment
if (!identical(list_vals, indent_vals)) {
  warning("Values in list.tsv and indent.tsv differ; data may be misaligned.")
}

# Construct a named list from the 'list' values
# Use the values as both names and elements (example construction)
named_list <- as.list(list_vals)
names(named_list) <- list_vals

#-----------------------------
# Derive indent value
#-----------------------------
# Using the number of rows in indent.tsv as indent width
indent_width <- length(indent_vals)

if (!is.numeric(indent_width) || length(indent_width) != 1L || indent_width < 0) {
  stop("Derived indent width is invalid.")
}

#-----------------------------
# Use admiral::print_named_list
#-----------------------------
# Capture output to check for issues and then print
print_output <- capture.output(
  admiral::print_named_list(
    list   = named_list,
    indent = indent_width
  )
)

# Also print to console (side effect as intended)
cat(paste0(print_output, collapse = "\n"), "\n")

#-----------------------------
# Save outputs
#-----------------------------

# 1) Save the named list (complex object) as RDS
rds_path <- file.path(out_dir, "named_list.rds")
saveRDS(named_list, rds_path)

# 2) Save the printed representation as a data frame to CSV
print_df <- data.frame(
  line_number = seq_along(print_output),
  text        = print_output,
  stringsAsFactors = FALSE
)

csv_path <- file.path(out_dir, "print_named_list_output.csv")
write.csv(print_df, csv_path, row.names = FALSE)

#-----------------------------
# Post-write verification
#-----------------------------
# Check that files exist and are readable
if (!file.exists(rds_path)) {
  stop("RDS output file was not created.")
}
if (!file.exists(csv_path)) {
  stop("CSV output file was not created.")
}

# Re-load and perform simple integrity checks
reloaded_list <- tryCatch(
  readRDS(rds_path),
  error = function(e) stop("Failed to read back RDS file: ", e$message)
)

if (!is.list(reloaded_list)) {
  stop("Reloaded RDS object is not a list; possible corruption or save error.")
}

reloaded_csv <- tryCatch(
  read.csv(csv_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) stop("Failed to read back CSV file: ", e$message)
)

if (!all(c("line_number", "text") %in% names(reloaded_csv))) {
  stop("Reloaded CSV does not have expected columns; possible misalignment.")
}

# Basic pattern checks for unexpected issues
if (anyNA(reloaded_csv$line_number) || anyNA(reloaded_csv$text)) {
  warning("NA values detected in reloaded CSV; possible parsing or write issues.")
}

# Heuristic check: look for obviously malformed indentation (e.g., tabs instead of spaces)
if (any(grepl("\t", reloaded_csv$text))) {
  warning("Tab characters detected in printed output; indentation may not match expectations.")
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
   AVAL: "AVAL"
   AVISITN: "AVISITN"
   USUBJID: "USUBJID" 

```

## Current Prompt Output Files

**`named_list.rds`**

```text
[binary artifact: named_list.rds, 105 bytes]
```

**`print_named_list_output.csv`**

```csv
"line_number","text"
1,"   AVAL: ""AVAL"""
2,"   AVISITN: ""AVISITN"""
3,"   USUBJID: ""USUBJID"""

```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(purrr)
library(stringr)

# Paths
indent_path <- file.path("inputs", "indent.tsv")
list_path   <- file.path("inputs", "list.tsv")
out_path    <- file.path("outputs", "result.csv")

# Read inputs
indent_vec <- read_tsv(indent_path, col_types = cols(.default = col_character())) %>%
  pull(1) %>%
  discard(is.na)

list_vec <- read_tsv(list_path, col_types = cols(.default = col_character())) %>%
  pull(1) %>%
  discard(is.na)

# Remove header labels if present
indent_vec <- indent_vec[indent_vec != "indent"]
list_vec   <- list_vec[list_vec != "list"]

# Build named list
named_list <- as.list(list_vec)
names(named_list) <- indent_vec

# Convert named list to a tibble for export
result_df <- tibble(
  name  = names(named_list),
  value = unlist(named_list, use.names = FALSE)
)

# Ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Write result
write_csv(result_df, out_path)
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
name,value
AVAL,AVAL
AVISITN,AVISITN
USUBJID,USUBJID

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiral/print_named_list",
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
  "task_id": "pharmaverse/admiral/print_named_list",
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
      "reason": "Shape mismatch: ref=(1, 1) vs llm=(3, 2)"
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
