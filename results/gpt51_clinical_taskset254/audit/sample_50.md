# Sample 50: pharmaverse/tidytlg/add_indent

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/tidytlg/add_indent`
- package/function: `tidytlg` / `add_indent`
- expected_artifacts: `outputs/result.csv`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Compute **indentation** for TLG rows. Load `library(tidytlg)`, `library(dplyr)`.

**Computation:** The reference uses **`dplyr::mutate` / `case_when`** on `row_type` (not necessarily the required functionality); reproduce that pipeline.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Prompt
```text
Write R code to add indentation variable to the results dataframe using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/df.tsv. Add the `indentme` variable to your results data. This drives the number of indents for the row label text (e.g. 0, 1, 2, etc.). Additional details: The `group_level` variable, which is added to the results dataframe by `freq()` and `univar()` calls, is needed to define indentation when by variables are used for summary. The `nested_level` variable, which is added to the results dataframe by `nested_freq()`, is needed to define indentation for each level of nesting. Both of these are added to the default indentation which is driven by `row_type`. | row_type | default indentation | | ----------------- |:-------------------:| | TABLE_BY_HEADER | 0 | | BY_HEADER\[1-9\] | 0 | | HEADER | 0 | | N | 1 | | VALUE | 2 | | NESTED | 0 | Use tidytlg's add_indent function with the following parameters: df (dataframe of results that contains `row_type` and `label` and the optional `nested_level` and `group_level` variables.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: dataframe with the `indentme` variable added.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### df.tsv (36 bytes)
set_values_to
exprs(DTYPE = 'LOCF')

```

## Simple Prompt
```text
Create R script to perform add indent using the tidytlg clinical task contract.

Input: df.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### df.tsv (36 bytes)
set_values_to
exprs(DTYPE = 'LOCF')

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
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(5, 3) vs llm=(1, 2) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(tidytlg))

suppressPackageStartupMessages(library(dplyr))

# 1. 读取输入数据 / Read input data
df_path <- file.path("inputs", "df.tsv")
if (!file.exists(df_path)) {
  stop("df.tsv is required input")
}
df <- read.delim(df_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("df")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
# set default list of variables to be removed
  remove_vars <- c("nested_level", "group_level", "value_add")

  # check if variables are already present in df, if not, add and set defaults
  if (!("nested_level" %in% names(df))) {
    df <- df %>%
      dplyr::mutate(nested_level = 0)
  }
  if (!("group_level" %in% names(df))) {
    df <- df %>%
      dplyr::mutate(group_level = 0)
  }

  # define amount to indent VALUE rows based on if a N row exists in the group
  # based on anbr
  if (!("value_add" %in% names(df))) {
    if ("anbr" %in% names(df)) {
      df <- df %>%
        group_by(anbr) %>%
        dplyr::mutate(value_add = 1 + max(as.numeric(row_type == "N")))
    } else {
      df <- df %>%
        dplyr::mutate(value_add = 1 + max(as.numeric(row_type == "N")))
    }
  }
  # if any table by headers, add one indentation to everything
  add_tableby_to_default <- any(df[["row_type"]] == "TABLE_BY_HEADER")

  result <- df %>%
    dplyr::mutate(indent = case_when(
          grepl("BY_HEADER[0-9]", row_type) ~ 0 + add_tableby_to_default + group_level,
          row_type == "HEADER" ~ 0 + add_tableby_to_default + group_level,
          row_type == "N" ~ 1 + add_tableby_to_default + group_level,
          row_type == "VALUE" ~ value_add + add_tableby_to_default + group_level,
          row_type == "NESTED" ~ nested_level + add_tableby_to_default + group_level,
          TRUE ~ 0
        )
    ) %>%
    select(-any_of(remove_vars))

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
  
```

## Current Solution
```r
library(tidytlg)

# Create directories if they don't exist
if (!dir.exists("inputs")) dir.create("inputs", recursive = TRUE)
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper: safe read of TSV
read_input_df <- function(path) {
  if (!file.exists(path)) {
    stop(sprintf("Input file not found: %s", path))
  }
  df <- tryCatch(
    {
      read.delim(path, header = TRUE, sep = "\t", quote = "", check.names = FALSE, stringsAsFactors = FALSE)
    },
    error = function(e) {
      stop(sprintf("Failed to read input file '%s': %s", path, conditionMessage(e)))
    }
  )
  if (!is.data.frame(df)) {
    stop("Input is not a data frame after reading.")
  }
  df
}

# Basic validation of required columns for add_indent
validate_df_for_add_indent <- function(df) {
  required_cols <- c("row_type", "label")
  missing_req <- setdiff(required_cols, names(df))
  if (length(missing_req) > 0) {
    stop(sprintf(
      "Data frame is missing required columns for add_indent: %s",
      paste(missing_req, collapse = ", ")
    ))
  }
  df
}

# Load input
input_path <- file.path("inputs", "df.tsv")
df_raw <- read_input_df(input_path)

# Ensure minimum structure required by add_indent
# If row_type or label are missing, attempt to construct them conservatively
if (!"row_type" %in% names(df_raw)) {
  df_raw$row_type <- "VALUE"
}
if (!"label" %in% names(df_raw)) {
  # Use first column as label if possible
  if (ncol(df_raw) > 0) {
    df_raw$label <- as.character(df_raw[[1]])
  } else {
    df_raw$label <- ""
  }
}

df <- validate_df_for_add_indent(df_raw)

# Call tidytlg::add_indent
df_indented <- tryCatch(
  {
    add_indent(df = df)
  },
  error = function(e) {
    stop(sprintf("add_indent failed: %s", conditionMessage(e)))
  }
)

# Validate output
if (!"indentme" %in% names(df_indented)) {
  stop("add_indent did not produce 'indentme' column in the output.")
}

if (!is.numeric(df_indented$indentme)) {
  stop("'indentme' column is not numeric as expected.")
}

# Basic sanity checks for unexpected patterns
if (any(is.na(df_indented$indentme))) {
  warning("NA values detected in 'indentme'. Check row_type / grouping variables for completeness.")
}

if (any(df_indented$indentme < 0, na.rm = TRUE)) {
  warning("Negative indentation values found in 'indentme'. This is unexpected.")
}

# Write outputs
csv_path <- file.path("outputs", "df_indented.csv")
rds_path <- file.path("outputs", "df_indented.rds")

write_ok_csv <- TRUE
write_ok_rds <- TRUE

tryCatch(
  {
    write.csv(df_indented, csv_path, row.names = FALSE)
  },
  error = function(e) {
    write_ok_csv <<- FALSE
    warning(sprintf("Failed to write CSV output '%s': %s", csv_path, conditionMessage(e)))
  }
)

tryCatch(
  {
    saveRDS(df_indented, rds_path)
  },
  error = function(e) {
    write_ok_rds <<- FALSE
    warning(sprintf("Failed to write RDS output '%s': %s", rds_path, conditionMessage(e)))
  }
)

# Confirm files written correctly
if (write_ok_csv && !file.exists(csv_path)) {
  warning(sprintf("CSV output file not found after writing: %s", csv_path))
}

if (write_ok_rds && !file.exists(rds_path)) {
  warning(sprintf("RDS output file not found after writing: %s", rds_path))
}

# Quick round-trip check for RDS (structure and basic alignment)
if (write_ok_rds && file.exists(rds_path)) {
  df_check <- tryCatch(
    {
      readRDS(rds_path)
    },
    error = function(e) {
      warning(sprintf("Failed to re-read RDS output '%s': %s", rds_path, conditionMessage(e)))
      NULL
    }
  )
  if (!is.null(df_check)) {
    if (!all(names(df_check) == names(df_indented))) {
      warning("Column names mismatch between in-memory and reloaded RDS data frame (possible misalignment).")
    }
    if (nrow(df_check) != nrow(df_indented)) {
      warning("Row count mismatch between in-memory and reloaded RDS data frame (possible truncation or corruption).")
    }
  }
}
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(tidytlg)
library(dplyr)
library(readr)
library(stringr)
library(purrr)

# Directories
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read clinical task contract instructions
df_path <- file.path(in_dir, "df.tsv")
instructions <- readr::read_tsv(
  df_path,
  col_types = cols(.default = "c"),
  comment = "#"
)

# Helper to safely parse expressions from the contract
parse_exprs <- function(x) {
  x <- str_trim(x)
  if (x == "" || is.na(x)) return(rlang::exprs())
  rlang::parse_exprs(x)
}

# Extract set_values_to and other components (if present)
# Expected: a column "set_values_to" containing something like:
# exprs(DTYPE = 'LOCF')
set_values_raw <- instructions$set_values_to %||% NA_character_
set_values_expr <- if (!is.na(set_values_raw)) {
  # strip leading "exprs(" and trailing ")"
  inner <- str_replace(set_values_raw, "^exprs\\((.*)\\)$", "\\1")
  parse_exprs(inner)
} else {
  rlang::exprs()
}

# For "add indent" we typically have a source data frame and we
# add variables defined in set_values_to; here we just materialize
# the set_values_to specification into a small result table.

# Build a tibble from set_values_to definitions
result <- purrr::map_dfr(set_values_expr, function(e) {
  # e is of the form `DTYPE = 'LOCF'`
  if (!rlang::is_call(e, "=") && !rlang::is_call(e, "==")) return(tibble())
  var_name <- rlang::as_name(rlang::f_lhs(e))
  value_expr <- rlang::f_rhs(e)

  # Evaluate right-hand side in empty environment
  value <- rlang::eval_tidy(value_expr)

  tibble(
    var = var_name,
    value = as.character(value)
  )
})

# Write result
out_path <- file.path(out_dir, "result.csv")
readr::write_csv(result, out_path)
```

## Current Candidate Prompt File
```text
Write R code to add indentation variable to the results dataframe using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/df.tsv. Add the `indentme` variable to your results data. This drives the number of indents for the row label text (e.g. 0, 1, 2, etc.). Additional details: The `group_level` variable, which is added to the results dataframe by `freq()` and `univar()` calls, is needed to define indentation when by variables are used for summary. The `nested_level` variable, which is added to the results dataframe by `nested_freq()`, is needed to define indentation for each level of nesting. Both of these are added to the default indentation which is driven by `row_type`. | row_type | default indentation | | ----------------- |:-------------------:| | TABLE_BY_HEADER | 0 | | BY_HEADER\[1-9\] | 0 | | HEADER | 0 | | N | 1 | | VALUE | 2 | | NESTED | 0 | Use tidytlg's add_indent function with the following parameters: df (dataframe of results that contains `row_type` and `label` and the optional `nested_level` and `group_level` variables.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: dataframe with the `indentme` variable added.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to add indentation variable to the results dataframe using tidytlg. At the beginning, load the required packages: library(tidytlg). The input data file is stored in inputs/df.tsv. Add the `indentme` variable to your results data. This drives the number of indents for the row label text (e.g. 0, 1, 2, etc.). Additional details: The `group_level` variable, which is added to the results dataframe by `freq()` and `univar()` calls, is needed to define indentation when by variables are used for summary. The `nested_level` variable, which is added to the results dataframe by `nested_freq()`, is needed to define indentation for each level of nesting. Both of these are added to the default indentation which is driven by `row_type`. | row_type | default indentation | | ----------------- |:-------------------:| | TABLE_BY_HEADER | 0 | | BY_HEADER\[1-9\] | 0 | | HEADER | 0 | | N | 1 | | VALUE | 2 | | NESTED | 0 | Use tidytlg's add_indent function with the following parameters: df (dataframe of results that contains `row_type` and `label` and the optional `nested_level` and `group_level` variables.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: dataframe with the `indentme` variable added.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```