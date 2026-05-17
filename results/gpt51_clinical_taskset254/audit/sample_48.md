# Sample 48: pharmaverse/admiral/dthcaus_source

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiral/dthcaus_source`
- package/function: `admiral` / `dthcaus_source`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `TIMEOUT` tier=`exec_fail`
- simple_status: `TIMEOUT` tier=`exec_fail`

## Reference Prompt
```text
Build a **death-cause** `tte_source` object for time-to-event. Load `library(admiral)`.

**Computation:** The reference uses a minimal **`ds`** data.frame and **`admiral::dthcaus_source(dataset_name = "ds", filter = DSDECOD == "DEATH", date = admiral::convert_dtc_to_dt(DSSTDTC), mode = "first", dthcaus = DSTERM)`**, then saves **`list(source = src, dataset = ds)`** to RDS plus CSV for the tabular part.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Prompt
```text
Write R code to create a `dthcaus_source` object using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset_name.tsv, inputs/filter.tsv, inputs/date.tsv, inputs/order.tsv, inputs/mode.tsv, inputs/dthcaus.tsv, inputs/set_values_to.tsv). `r lifecycle::badge("deprecated")` The `dthcaus_source()` function and `dthcaus_source()` have been deprecated in favor of `event()`. `exprs(ADT, desc(AVAL))` or `NULL` Use admiral's dthcaus_source function with the following parameters: dataset_name (The name of the dataset, i.e. a string, used to search for the death cause.), filter (An expression used for filtering `dataset`.), date (A date or datetime variable or an expression to be used for sorting `dataset`.), order (Sort order Additional variables/expressions to be used for sorting the `dataset`.), mode (One of `"first"` or `"last"`.), dthcaus (A variable name, an expression, or a string literal If a variable name is specified, e.g.), set_values_to (Variables to be set to trace the source dataset). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: An object of class "dthcaus_source".. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### dataset_name.tsv (18 bytes)
dataset_name
adsl

### date.tsv (20 bytes)
date_imputation
mid

### date_df.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

### dthcaus.tsv (69 bytes)
dt
2020-06-30
2020-01-10
2022-04-27
2019-07-22
2021-11-05
2019-03-15

### dthcaus_df.tsv (58 bytes)
dt
2020-01-10
2020-06-30
2020-01-10
2021-02-18
2020-06-30

### filter.tsv (16 bytes)
filter
AVAL > 0

### mode.tsv (10 bytes)
mode
last

### mode_df.tsv (11 bytes)
mode
first

### order.tsv (20 bytes)
order
AVISITN, AVAL

### order_df.tsv (20 bytes)
order
AVISITN, AVAL

### set_values_to.tsv (51 bytes)
set_values_to
exprs(AVAL = mean(AVAL, na.rm=TRUE))

```

## Simple Prompt
```text
Create R script to perform dthcaus source using the admiral clinical task contract.

Input: dataset_name.tsv, date.tsv, date_df.tsv, dthcaus.tsv, dthcaus_df.tsv, filter.tsv, mode.tsv, mode_df.tsv, order.tsv, order_df.tsv, set_values_to.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### dataset_name.tsv (18 bytes)
dataset_name
adsl

### date.tsv (20 bytes)
date_imputation
mid

### date_df.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

### dthcaus.tsv (69 bytes)
dt
2020-06-30
2020-01-10
2022-04-27
2019-07-22
2021-11-05
2019-03-15

### dthcaus_df.tsv (58 bytes)
dt
2020-01-10
2020-06-30
2020-01-10
2021-02-18
2020-06-30

### filter.tsv (16 bytes)
filter
AVAL > 0

### mode.tsv (10 bytes)
mode
last

### mode_df.tsv (11 bytes)
mode
first

### order.tsv (20 bytes)
order
AVISITN, AVAL

### order_df.tsv (20 bytes)
order
AVISITN, AVAL

### set_values_to.tsv (51 bytes)
set_values_to
exprs(AVAL = mean(AVAL, na.rm=TRUE))

```

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "message": "Timeout after 120s",
  "returncode": "",
  "stderr": "",
  "comparison": ""
}
```

## Simple Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "message": "Timeout after 120s",
  "returncode": "",
  "stderr": "",
  "comparison": ""
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(admiral))

# 1. 创建最小数据集用于 dthcaus_source
ds <- data.frame(
  USUBJID = c("1", "2"),
  DSDECOD = "DEATH",
  DSTERM = c("Unknown", "Unknown"),
  DSSTDTC = c("2022-02-01", "2022-03-03"),
  stringsAsFactors = FALSE
)

# 2. 创建 dthcaus_source 对象
src <- admiral::dthcaus_source(
  dataset_name = "ds",
  filter = DSDECOD == "DEATH",
  date = admiral::convert_dtc_to_dt(DSSTDTC),
  mode = "first",
  dthcaus = DSTERM
)

# 3. 保存为 RDS (dthcaus_source 返回的是 source 对象)
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
saveRDS(list(source = src, dataset = ds), file.path(outputs_dir, "result.rds"))
write.csv(ds, file.path(outputs_dir, "result.csv"), row.names = FALSE)

```

## Current Solution
```r
library(admiral)
library(dplyr)
library(rlang)
library(readr)
library(purrr)
library(stringr)

#-----------------------------
# Helper functions
#-----------------------------

read_single_value_tsv <- function(path, col_name) {
  df <- tryCatch(
    readr::read_tsv(path, show_col_types = FALSE),
    error = function(e) stop("Error reading ", path, ": ", conditionMessage(e), call. = FALSE)
  )
  if (!col_name %in% names(df)) {
    stop("Column '", col_name, "' not found in ", path, call. = FALSE)
  }
  if (nrow(df) != 1L) {
    stop("File ", path, " must contain exactly 1 row; found ", nrow(df), call. = FALSE)
  }
  df[[col_name]][[1]]
}

parse_expr_safely <- function(txt, label) {
  expr <- tryCatch(
    parse_expr(txt),
    error = function(e) stop("Failed to parse ", label, " expression '", txt, "': ", conditionMessage(e), call. = FALSE)
  )
  expr
}

check_file_exists <- function(path) {
  if (!file.exists(path)) {
    stop("Required file does not exist: ", path, call. = FALSE)
  }
}

#-----------------------------
# Read control inputs
#-----------------------------

dataset_name_path   <- file.path("inputs", "dataset_name.tsv")
filter_path         <- file.path("inputs", "filter.tsv")
date_path           <- file.path("inputs", "date.tsv")
order_path          <- file.path("inputs", "order.tsv")
mode_path           <- file.path("inputs", "mode.tsv")
dthcaus_path        <- file.path("inputs", "dthcaus.tsv")
set_values_to_path  <- file.path("inputs", "set_values_to.tsv")

walk(
  c(
    dataset_name_path,
    filter_path,
    date_path,
    order_path,
    mode_path,
    dthcaus_path,
    set_values_to_path
  ),
  check_file_exists
)

dataset_name <- read_single_value_tsv(dataset_name_path, "dataset_name")
filter_txt   <- read_single_value_tsv(filter_path, "filter")
mode_value   <- read_single_value_tsv(mode_path, "mode")
set_vals_txt <- read_single_value_tsv(set_values_to_path, "set_values_to")

# mode validation
if (!mode_value %in% c("first", "last")) {
  stop("Invalid mode value '", mode_value, "'. Must be 'first' or 'last'.", call. = FALSE)
}

# Filter expression
filter_expr <- parse_expr_safely(filter_txt, "filter")

# Order expression(s)
order_txt <- read_single_value_tsv(order_path, "order")
order_terms_chr <- str_split(order_txt, ",")[[1]] %>%
  trimws() %>%
  discard(~ .x == "")

if (length(order_terms_chr) == 0L) {
  order_expr <- NULL
} else {
  order_expr <- parse_expr_safely(paste(order_terms_chr, collapse = ", "), "order")
}

# Date expression or variable name
date_df_path <- file.path("inputs", "date_df.tsv")
check_file_exists(date_df_path)
date_df <- tryCatch(
  readr::read_tsv(date_df_path, show_col_types = FALSE),
  error = function(e) stop("Error reading ", date_df_path, ": ", conditionMessage(e), call. = FALSE)
)

# For illustration, assume date variable is ADT constructed from `id` or AVAL (user will adapt as needed)
# Here simply choose a placeholder symbol ADT, which should exist in the actual analysis dataset.
date_expr <- expr(ADT)

# dthcaus expression / variable / string
dthcaus_vec <- tryCatch(
  readr::read_tsv(dthcaus_path, show_col_types = FALSE),
  error = function(e) stop("Error reading ", dthcaus_path, ": ", conditionMessage(e), call. = FALSE)
)

if (!"dt" %in% names(dthcaus_vec)) {
  stop("Column 'dt' not found in ", dthcaus_path, call. = FALSE)
}

# Choose: treat as string literal column name "DTHCAUS" or direct values.
# Here: assume dataset has a variable DTHCAUS; dthcaus.tsv contains example values only.
dthcaus_expr <- expr(DTHCAUS)

# set_values_to expression
set_values_to_expr <- parse_expr_safely(set_vals_txt, "set_values_to")

#-----------------------------
# Load dataset referenced by dataset_name
#-----------------------------

dataset_path <- file.path("inputs", paste0(dataset_name, ".tsv"))
check_file_exists(dataset_path)

dataset <- tryCatch(
  readr::read_tsv(dataset_path, show_col_types = FALSE),
  error = function(e) stop("Error reading ", dataset_path, ": ", conditionMessage(e), call. = FALSE)
)

# Basic validation
if (!is.data.frame(dataset)) {
  stop("Dataset '", dataset_name, "' loaded from ", dataset_path, " is not a data frame.", call. = FALSE)
}

# Check referenced variables exist where possible
# Filter vars
filter_syms <- all.vars(filter_expr)
missing_filter_vars <- setdiff(filter_syms, names(dataset))
if (length(missing_filter_vars) > 0L) {
  stop("Variables missing in dataset '", dataset_name, "' but used in filter: ",
       paste(missing_filter_vars, collapse = ", "), call. = FALSE)
}

# Order vars
if (!is.null(order_expr)) {
  order_syms <- all.vars(order_expr)
  missing_order_vars <- setdiff(order_syms, names(dataset))
  if (length(missing_order_vars) > 0L) {
    stop("Variables missing in dataset '", dataset_name, "' but used in order: ",
         paste(missing_order_vars, collapse = ", "), call. = FALSE)
  }
}

# Date var
date_syms <- all.vars(date_expr)
missing_date_vars <- setdiff(date_syms, names(dataset))
if (length(missing_date_vars
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(stringr)
library(admiral)

# Helper to read single-cell TSVs (header + 1 value)
read_single_value <- function(path) {
  x <- read_tsv(path, show_col_types = FALSE)
  x[[1]][1]
}

# Inputs directory
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read control TSVs
dataset_name <- read_single_value(file.path(in_dir, "dataset_name.tsv"))
date_imp     <- read_single_value(file.path(in_dir, "date.tsv"))
filter_expr  <- read_single_value(file.path(in_dir, "filter.tsv"))
mode_main    <- read_single_value(file.path(in_dir, "mode.tsv"))
mode_df      <- read_single_value(file.path(in_dir, "mode_df.tsv"))
order_main   <- read_single_value(file.path(in_dir, "order.tsv"))
order_df     <- read_single_value(file.path(in_dir, "order_df.tsv"))
set_values   <- read_single_value(file.path(in_dir, "set_values_to.tsv"))

# Read date metadata: list of variable names
date_df <- read_tsv(file.path(in_dir, "date_df.tsv"), show_col_types = FALSE)
date_vars <- setdiff(names(date_df), "id")

# Read dthcaus & dthcaus_df: first column named "dt"
dthcaus    <- read_tsv(file.path(in_dir, "dthcaus.tsv"), show_col_types = FALSE)
dthcaus_df <- read_tsv(file.path(in_dir, "dthcaus_df.tsv"), show_col_types = FALSE)

# Read main dataset (dataset_name.tsv says "adsl")
main_path <- file.path(in_dir, paste0(dataset_name, ".tsv"))
adsl <- read_tsv(main_path, show_col_types = FALSE)

# Prepare order vectors
order_main_vars <- str_split(order_main, ",")[[1]] |> str_trim()
order_df_vars   <- str_split(order_df, ",")[[1]]   |> str_trim()

# Convert dt to Date in both dthcaus tables
dthcaus    <- dthcaus    %>% mutate(dt = as.Date(dt))
dthcaus_df <- dthcaus_df %>% mutate(dt = as.Date(dt))

# Attach row index to dthcaus_df for reproducible selection
dthcaus_df <- dthcaus_df %>% mutate(.row_id = row_number())

# Sort dthcaus_df according to order_df (if present in data)
for (v in order_df_vars) {
  if (v %in% names(dthcaus_df)) {
    dthcaus_df <- dthcaus_df %>% arrange(.data[[v]], .by_group = FALSE)
  }
}

# Select first/last per dt from dthcaus_df according to mode_df
if (mode_df == "first") {
  dthcaus_df_sel <- dthcaus_df %>%
    group_by(dt) %>%
    slice(1L) %>%
    ungroup()
} else if (mode_df == "last") {
  dthcaus_df_sel <- dthcaus_df %>%
    group_by(dt) %>%
    slice(n()) %>%
    ungroup()
} else {
  dthcaus_df_sel <- dthcaus_df
}

# Join dthcaus (unique dt) to selected dthcaus_df on dt
# If multiple rows in dthcaus_df_sel per dt, keep all matches
dth_join <- dthcaus %>%
  left_join(dthcaus_df_sel, by = "dt", suffix = c("", "_df"))

# Apply date imputation to dt (if partial dates existed; here assume complete)
# Using admiral::convert_blanks_to_na + derive_vars_dt if needed;
# in this example dt already Date, so just keep as is

# If AVAL present, filter and derive using set_values_to
if ("AVAL" %in% names(dth_join)) {
  dth_join <- dth_join %>%
    filter(eval(parse(text = filter_expr)))
  # Apply set_values_to expression within mutate
  # set_values is like 'exprs(AVAL = mean(AVAL, na.rm=TRUE))'
  dth_join <- dth_join %>%
    mutate(!!!eval(parse(text = set_values)))
}

# Order dth_join according to order_main
for (v in order_main_vars) {
  if (v %in% names(dth_join)) {
    dth_join <- dth_join %>% arrange(.data[[v]], .by_group = FALSE)
  }
}

# If mode_main is last/first on AVISITN + AVAL, apply row selection
group_vars <- intersect(order_main_vars, names(dth_join))
if (length(group_vars) > 0) {
  if (mode_main == "first") {
    dth_join <- dth_join %>%
      group_by(across(all_of(group_vars))) %>%
      slice(1L) %>%
      ungroup()
  } else if (mode_main == "last") {
    dth_join <- dth_join %>%
      group_by(across(all_of(group_vars))) %>%
      slice(n()) %>%
      ungroup()
  }
}

# Merge back with ADSL if there is a key overlap (e.g., USUBJID)
common_keys <- intersect(names(adsl), names(dth_join))
if (length(common_keys) > 0) {
  result <- adsl %>%
    left_join(dth_join, by = common_keys)
} else {
  result <- dplyr::bind_cols(adsl, dth_join)
}

# Write result
write_csv(result, file.path(out_dir, "result.csv"), na = "")
```

## Current Candidate Prompt File
```text
Write R code to create a `dthcaus_source` object using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset_name.tsv, inputs/filter.tsv, inputs/date.tsv, inputs/order.tsv, inputs/mode.tsv, inputs/dthcaus.tsv, inputs/set_values_to.tsv). `r lifecycle::badge("deprecated")` The `dthcaus_source()` function and `dthcaus_source()` have been deprecated in favor of `event()`. `exprs(ADT, desc(AVAL))` or `NULL` Use admiral's dthcaus_source function with the following parameters: dataset_name (The name of the dataset, i.e. a string, used to search for the death cause.), filter (An expression used for filtering `dataset`.), date (A date or datetime variable or an expression to be used for sorting `dataset`.), order (Sort order Additional variables/expressions to be used for sorting the `dataset`.), mode (One of `"first"` or `"last"`.), dthcaus (A variable name, an expression, or a string literal If a variable name is specified, e.g.), set_values_to (Variables to be set to trace the source dataset). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: An object of class "dthcaus_source".. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to create a `dthcaus_source` object using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset_name.tsv, inputs/filter.tsv, inputs/date.tsv, inputs/order.tsv, inputs/mode.tsv, inputs/dthcaus.tsv, inputs/set_values_to.tsv). `r lifecycle::badge("deprecated")` The `dthcaus_source()` function and `dthcaus_source()` have been deprecated in favor of `event()`. `exprs(ADT, desc(AVAL))` or `NULL` Use admiral's dthcaus_source function with the following parameters: dataset_name (The name of the dataset, i.e. a string, used to search for the death cause.), filter (An expression used for filtering `dataset`.), date (A date or datetime variable or an expression to be used for sorting `dataset`.), order (Sort order Additional variables/expressions to be used for sorting the `dataset`.), mode (One of `"first"` or `"last"`.), dthcaus (A variable name, an expression, or a string literal If a variable name is specified, e.g.), set_values_to (Variables to be set to trace the source dataset). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: An object of class "dthcaus_source".. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```