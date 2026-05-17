# Sample 35: pharmaverse/ggsurvfit/scale_ggsurvfit

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/ggsurvfit/scale_ggsurvfit`
- package/function: `ggsurvfit` / `scale_ggsurvfit`
- expected_artifacts: `outputs/result.csv`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to build a `ggsurvfit::scale_ggsurvfit()` scale object using the `ggsurvfit` package.
At the beginning, load: library(ggsurvfit).

**Inputs:**
- `inputs/x_scales.tsv` and `inputs/y_scales.tsv`: each has a header row; the **first cell of the first data row** (column 1) must contain a valid R expression that evaluates to a **named list** of arguments for `ggplot2::scale_x_continuous()` / `scale_y_continuous()` (for example `list(expand = c(0.015, 0), n.breaks = 8)`). Read with read.delim(..., check.names=FALSE, stringsAsFactors=FALSE), take `txt <- trimws(as.character(df[[1]][1]))`, then `eval(parse(text = txt))` to obtain each list.

**Required output:**
- `outputs/result.csv`: a one-row summary table with at least one column describing the returned object (for example `scale_classes` = paste(class(result), collapse='|')) after calling `ggsurvfit::scale_ggsurvfit(x_scales = ..., y_scales = ...)`.

Create `outputs/` with dir.create('outputs', showWarnings=FALSE). Use write.csv(..., row.names=FALSE).
```

## Current Prompt
```text
Write R code to apply scales using ggsurvfit. At the beginning, load the required packages: library(ggsurvfit). The input data files are stored in inputs/ directory (inputs/x_scales.tsv, inputs/y_scales.tsv). The most common figure created with this package is a survival curve. This scale applies modifications often seen in these figures. - `scale_y_continuous(expand = c(0.025, 0), limits = c(0, 1), label = scales::label_percent())`. - `scale_x_continuous(expand = c(0.015, 0), n.breaks = 8)` *NOTE*: The y-axis limits are only set for survival curves. If you use this function, you **must** include **all** scale specifications that would appear in `scale_x_continuous()` or `scale_y_continuous()`. For example, it's common you'll need to specify the x-axis break points. `scale_ggsurvfit(x_scales=list(breaks=0:9))`. To reset any of the above settings to their ggplot2 default, set the value to `NULL`, e.g. `y_scales = list(limits = NULL)`. Additional details: Special case: in the risk table, large numbers (with more than 4 digits) may not be shown completely, with some digits truncated outside the plot region. To remedy this, consider adjusting the expand size: ```r scale_ggsurvfit(x_scales = list(expand = c(0.05, 0))) ``` This can modify the position of numbers in the risk table and make them all fit in the plot region. The scale of the `expand` argument differs by cases. Use ggsurvfit's scale_ggsurvfit function with the following parameters: x_scales (a named list of arguments that will be passed to `ggplot2::scale_x_continuous()`.), y_scales (a named list of arguments that will be passed to `ggplot2::scale_y_continuous()`.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: a ggplot2 figure. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### x_scales.tsv (46 bytes)
expr
list(expand = c(0.015, 0), n.breaks = 8)

### y_scales.tsv (50 bytes)
expr
list(expand = c(0.025, 0), limits = c(0, 1))

```

## Simple Prompt
```text
Create R script to perform scale ggsurvfit using the ggsurvfit clinical task contract.

Input: x_scales.tsv, y_scales.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### x_scales.tsv (46 bytes)
expr
list(expand = c(0.015, 0), n.breaks = 8)

### y_scales.tsv (50 bytes)
expr
list(expand = c(0.025, 0), limits = c(0, 1))

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
  "comparison": "result.csv: match=False reason=File not generated"
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 1) vs llm=(2, 2)"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(ggsurvfit))

parse_scale_list <- function(fname) {
  path <- file.path("inputs", fname)
  if (!file.exists(path)) {
    stop(fname, " is required input")
  }
  df <- read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
  txt <- trimws(as.character(df[[1]][1]))
  if (!nzchar(txt) || identical(txt, "NA")) {
    return(list())
  }
  ev <- eval(parse(text = txt))
  if (!is.list(ev)) {
    stop("First data cell in ", fname, " must evaluate to an R list of scale_* arguments.")
  }
  ev
}

x_scales <- parse_scale_list("x_scales.tsv")
y_scales <- parse_scale_list("y_scales.tsv")

result <- ggsurvfit::scale_ggsurvfit(x_scales = x_scales, y_scales = y_scales)

outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)

result_df <- data.frame(
  scale_classes = paste(class(result), collapse = "|"),
  stringsAsFactors = FALSE
)
write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)

```

## Current Solution
```r
library(ggsurvfit)
library(survival)
library(readr)

#--------------------------------------------------------------------
# Helper: safe reader for single-expression TSV
#--------------------------------------------------------------------
read_scale_expr <- function(path) {
  if (!file.exists(path)) {
    stop("File not found: ", path)
  }
  df <- tryCatch(
    readr::read_tsv(path, show_col_types = FALSE),
    error = function(e) stop("Failed to read TSV file: ", path, " - ", e$message)
  )
  if (!"expr" %in% names(df)) {
    stop("File ", path, " must contain a column named 'expr'.")
  }
  expr_chr <- df$expr[1]
  if (is.na(expr_chr) || !nzchar(expr_chr)) {
    stop("Empty 'expr' value in ", path)
  }
  parsed <- tryCatch(
    eval(parse(text = expr_chr)),
    error = function(e) stop("Failed to parse expression from ", path, ": ", e$message)
  )
  if (!is.list(parsed)) {
    stop("Parsed expression from ", path, " is not a list as required.")
  }
  parsed
}

#--------------------------------------------------------------------
# Load scale parameters from inputs/
#--------------------------------------------------------------------
x_scale_file <- file.path("inputs", "x_scales.tsv")
y_scale_file <- file.path("inputs", "y_scales.tsv")

x_scales <- read_scale_expr(x_scale_file)
y_scales <- read_scale_expr(y_scale_file)

# Validate keys for scale lists (must be valid args to scale_*_continuous)
valid_x_args <- c("name", "breaks", "limits", "expand", "labels", "n.breaks",
                  "position", "trans", "guide", "oob", "sec.axis")
valid_y_args <- valid_x_args

invalid_x <- setdiff(names(x_scales), valid_x_args)
invalid_y <- setdiff(names(y_scales), valid_y_args)

if (length(invalid_x) > 0) {
  stop("Invalid x_scales argument names: ", paste(invalid_x, collapse = ", "))
}
if (length(invalid_y) > 0) {
  stop("Invalid y_scales argument names: ", paste(invalid_y, collapse = ", "))
}

#--------------------------------------------------------------------
# Generate example survival data (lung dataset from survival)
#--------------------------------------------------------------------
data("lung", package = "survival")

if (!all(c("time", "status") %in% names(lung))) {
  stop("Required columns 'time' and 'status' not found in lung dataset.")
}

# Basic data validation
if (any(is.na(lung$time))) {
  stop("Missing values in lung$time; cannot fit survival model.")
}
if (any(is.na(lung$status))) {
  stop("Missing values in lung$status; cannot fit survival model.")
}

surv_obj <- Surv(time = lung$time, event = lung$status == 2)

# Fit survival curve by sex for example
fit <- survfit2(surv_obj ~ sex, data = lung)

#--------------------------------------------------------------------
# Build survival curve with ggsurvfit and apply scales
#--------------------------------------------------------------------
p <- tryCatch(
  {
    ggsurvfit(fit) +
      scale_ggsurvfit(
        x_scales = x_scales,
        y_scales = y_scales
      )
  },
  error = function(e) stop("Failed to build survival plot: ", e$message)
)

#--------------------------------------------------------------------
# Prepare outputs directory
#--------------------------------------------------------------------
out_dir <- "outputs"
if (!dir.exists(out_dir)) {
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
}
if (!dir.exists(out_dir)) {
  stop("Failed to create outputs directory: ", out_dir)
}

#--------------------------------------------------------------------
# Save complex object (ggplot) as RDS
#--------------------------------------------------------------------
plot_rds_path <- file.path(out_dir, "survival_plot.rds")
tryCatch(
  saveRDS(p, plot_rds_path),
  error = function(e) stop("Failed to save RDS file: ", e$message)
)

# Confirm RDS can be read back
p_check <- tryCatch(
  readRDS(plot_rds_path),
  error = function(e) stop("Failed to re-read saved RDS file: ", e$message)
)
if (!inherits(p_check, "ggplot")) {
  stop("Re-read object from RDS is not a ggplot object; output may be corrupted.")
}

#--------------------------------------------------------------------
# Extract underlying data from survfit object and save as CSV
#--------------------------------------------------------------------
df_fit <- tryCatch(
  broom::tidy(fit),
  error = function(e) {
    stop("Failed to tidy survfit object: ", e$message)
  }
)

# Basic validation for data frame
if (!is.data.frame(df_fit) || nrow(df_fit) == 0L) {
  stop("Tidied survfit data frame is empty or invalid.")
}

# Check for unexpected patterns: non-finite time or estimate
if (any(!is.finite(df_fit$time))) {
  stop("Non-finite values detected in 'time' column of survival data.")
}
if (any(!is.finite(df_fit$estimate))) {
  stop("Non-finite values detected in 'estimate' column of survival data.")
}

csv_path <- file.path(out_dir, "survival_data.csv")
tryCatch(
  readr::write_csv(df_fit, csv_path),
  error = function(e) stop("Failed to write CSV file: ", e$message)
)

# Confirm CSV 
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(purrr)
})

# Directories
in_dir  <- "inputs"
out_dir <- "outputs"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

# Read scale expressions
x_df <- read_tsv(file.path(in_dir, "x_scales.tsv"), show_col_types = FALSE)
y_df <- read_tsv(file.path(in_dir, "y_scales.tsv"), show_col_types = FALSE)

# Extract expression strings
x_expr_chr <- x_df$expr[[1]]
y_expr_chr <- y_df$expr[[1]]

# Parse safely
parse_safe <- function(expr_chr) {
  res <- try(parse(text = expr_chr)[[1]], silent = TRUE)
  if (inherits(res, "try-error")) NA_character_ else expr_chr
}

x_valid <- parse_safe(x_expr_chr)
y_valid <- parse_safe(y_expr_chr)

# Build result table
result <- tibble::tibble(
  aesthetic = c("x", "y"),
  scale_expr = c(x_valid, y_valid)
)

# Write output
write_csv(result, file.path(out_dir, "result.csv"))
```

## Current Candidate Prompt File
```text
Write R code to apply scales using ggsurvfit. At the beginning, load the required packages: library(ggsurvfit). The input data files are stored in inputs/ directory (inputs/x_scales.tsv, inputs/y_scales.tsv). The most common figure created with this package is a survival curve. This scale applies modifications often seen in these figures. - `scale_y_continuous(expand = c(0.025, 0), limits = c(0, 1), label = scales::label_percent())`. - `scale_x_continuous(expand = c(0.015, 0), n.breaks = 8)` *NOTE*: The y-axis limits are only set for survival curves. If you use this function, you **must** include **all** scale specifications that would appear in `scale_x_continuous()` or `scale_y_continuous()`. For example, it's common you'll need to specify the x-axis break points. `scale_ggsurvfit(x_scales=list(breaks=0:9))`. To reset any of the above settings to their ggplot2 default, set the value to `NULL`, e.g. `y_scales = list(limits = NULL)`. Additional details: Special case: in the risk table, large numbers (with more than 4 digits) may not be shown completely, with some digits truncated outside the plot region. To remedy this, consider adjusting the expand size: ```r scale_ggsurvfit(x_scales = list(expand = c(0.05, 0))) ``` This can modify the position of numbers in the risk table and make them all fit in the plot region. The scale of the `expand` argument differs by cases. Use ggsurvfit's scale_ggsurvfit function with the following parameters: x_scales (a named list of arguments that will be passed to `ggplot2::scale_x_continuous()`.), y_scales (a named list of arguments that will be passed to `ggplot2::scale_y_continuous()`.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: a ggplot2 figure. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to apply scales using ggsurvfit. At the beginning, load the required packages: library(ggsurvfit). The input data files are stored in inputs/ directory (inputs/x_scales.tsv, inputs/y_scales.tsv). The most common figure created with this package is a survival curve. This scale applies modifications often seen in these figures. - `scale_y_continuous(expand = c(0.025, 0), limits = c(0, 1), label = scales::label_percent())`. - `scale_x_continuous(expand = c(0.015, 0), n.breaks = 8)` *NOTE*: The y-axis limits are only set for survival curves. If you use this function, you **must** include **all** scale specifications that would appear in `scale_x_continuous()` or `scale_y_continuous()`. For example, it's common you'll need to specify the x-axis break points. `scale_ggsurvfit(x_scales=list(breaks=0:9))`. To reset any of the above settings to their ggplot2 default, set the value to `NULL`, e.g. `y_scales = list(limits = NULL)`. Additional details: Special case: in the risk table, large numbers (with more than 4 digits) may not be shown completely, with some digits truncated outside the plot region. To remedy this, consider adjusting the expand size: ```r scale_ggsurvfit(x_scales = list(expand = c(0.05, 0))) ``` This can modify the position of numbers in the risk table and make them all fit in the plot region. The scale of the `expand` argument differs by cases. Use ggsurvfit's scale_ggsurvfit function with the following parameters: x_scales (a named list of arguments that will be passed to `ggplot2::scale_x_continuous()`.), y_scales (a named list of arguments that will be passed to `ggplot2::scale_y_continuous()`.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: a ggplot2 figure. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```