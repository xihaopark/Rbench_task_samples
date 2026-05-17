# Sample 03: pharmaverse/admiral/convert_special_cases

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiral/convert_special_cases`
- package/function: `admiral` / `convert_special_cases`
- expected_artifacts: `outputs/result.csv`
- current_status: `TIMEOUT` tier=`exec_fail`
- simple_status: `TIMEOUT` tier=`exec_fail`

## Reference Prompt
```text
Write R code to implement the **Convert special cases** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/may.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'may.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/na_idx.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'na_idx.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/no.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'no.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/result.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'result.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/same.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'same.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/treatment_duration.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'treatment_duration.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/xxtpt.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'xxtpt.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Convert Special Cases** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
Write R code to convert special case patterns using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/xxtpt.tsv, inputs/result.tsv, inputs/na_idx.tsv, inputs/treatment_duration.tsv). Converts special case timepoint patterns to numeric hours including screening, pre-dose, pre-treatment, before, and end of treatment markers. Additional details: Recognizes and converts the following patterns: * "Screening" -> 0 * "Pre-dose", "Predose", "Pre-treatment", "Pre-infusion", "Pre-inf", "Before", "Infusion", "0H" -> 0 * "EOI", "EOT", "End of Infusion", "End of Treatment", "After End of Infusion", "After End of Treatment" -> treatment_duration Only updates result for positions where result is currently NA and xxtpt is not NA. Use admiral's convert_special_cases function with the following parameters: xxtpt (Character vector of timepoint descriptions (trimmed, no leading/ trailing whitespace)), result (Numeric vector of results (partially filled, may contain NA)), na_idx (Logical vector indicating which positions in xxtpt are NA), treatment_duration (Duration of treatment in hours (non-negative numeric vector, same length as xxtpt)). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: Updated numeric vector with special case patterns converted to hours. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### may.tsv (25 bytes)
may
AVAL
AVISITN
USUBJID

### na_idx.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### no.tsv (24 bytes)
no
AVAL
AVISITN
USUBJID

### result.tsv (28 bytes)
result
AVAL
AVISITN
USUBJID

### same.tsv (26 bytes)
same
AVAL
AVISITN
USUBJID

### treatment_duration.tsv (40 bytes)
treatment_duration
AVAL
AVISITN
USUBJID

### xxtpt.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Simple Prompt
```text
Create R script to perform convert special cases using the admiral clinical task contract.

Input: may.tsv, na_idx.tsv, no.tsv, result.tsv, same.tsv, treatment_duration.tsv, xxtpt.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### may.tsv (25 bytes)
may
AVAL
AVISITN
USUBJID

### na_idx.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### no.tsv (24 bytes)
no
AVAL
AVISITN
USUBJID

### result.tsv (28 bytes)
result
AVAL
AVISITN
USUBJID

### same.tsv (26 bytes)
same
AVAL
AVISITN
USUBJID

### treatment_duration.tsv (40 bytes)
treatment_duration
AVAL
AVISITN
USUBJID

### xxtpt.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

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

suppressPackageStartupMessages(library(stringr))

# 1. 读取输入数据 / Read input data
xxtpt_path <- file.path("inputs", "xxtpt.tsv")
if (!file.exists(xxtpt_path)) {
  stop("xxtpt.tsv is required input")
}
xxtpt_df <- read.delim(xxtpt_path, check.names = FALSE, stringsAsFactors = FALSE)
xxtpt <- xxtpt_df$xxtpt
result_path <- file.path("inputs", "result.tsv")
if (!file.exists(result_path)) {
  stop("result.tsv is required input")
}
result_df <- read.delim(result_path, check.names = FALSE, stringsAsFactors = FALSE)
result <- as.numeric(result_df$result)
na_idx_path <- file.path("inputs", "na_idx.tsv")
if (!file.exists(na_idx_path)) {
  stop("na_idx.tsv is required input")
}
na_idx_df <- read.delim(na_idx_path, check.names = FALSE, stringsAsFactors = FALSE)
na_idx <- as.logical(na_idx_df$na_idx)
treatment_duration_path <- file.path("inputs", "treatment_duration.tsv")
if (!file.exists(treatment_duration_path)) {
  stop("treatment_duration.tsv is required input")
}
treatment_duration_df <- read.delim(treatment_duration_path, check.names = FALSE, stringsAsFactors = FALSE)
treatment_duration <- as.numeric(treatment_duration_df$treatment_duration)

# 2. 执行函数实现 / Execute function implementation
zero_pattern <- regex(
    paste0(
      "^(screening|pre-?(?:dose|treatment|inf(?:usion)?)|",
      "before|infusion|0\\s*h(?:r|our)?s?)$"
    ),
    ignore_case = TRUE
  )
  zero_idx <- str_detect(xxtpt, zero_pattern) & !na_idx
  result[zero_idx] <- 0

  eot_pattern <- regex(
    paste0(
      "^(eo[it]|end\\s+of\\s+(?:infusion|treatment)|",
      "after\\s+end\\s+of\\s+(?:infusion|treatment))$"
    ),
    ignore_case = TRUE
  )
  eot_idx <- str_detect(xxtpt, eot_pattern) & is.na(result) & !na_idx
  result[eot_idx] <- treatment_duration[eot_idx]

  result
result <- eot_idx

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    xxtpt = xxtpt, result = result,
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
dir.create(outputs_dir, showWarning
```

## Current Solution
```r
library(admiral)

# Create output directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#------------------------------
# Helper functions
#------------------------------

read_single_column_tsv <- function(path, colname) {
  if (!file.exists(path)) {
    stop(sprintf("File not found: %s", path))
  }
  df <- tryCatch(
    read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop(sprintf("Failed to read %s: %s", path, e$message))
  )
  if (!colname %in% names(df)) {
    stop(sprintf("Expected column '%s' not found in %s", colname, path))
  }
  vec <- df[[colname]]
  if (length(vec) == 0L) {
    stop(sprintf("Column '%s' in %s is empty", colname, path))
  }
  vec
}

validate_lengths <- function(...) {
  args <- list(...)
  lens <- vapply(args, length, integer(1))
  if (length(unique(lens)) != 1L) {
    stop(sprintf(
      "Length mismatch among inputs: %s",
      paste(sprintf("%s=%d", names(args), lens), collapse = ", ")
    ))
  }
  invisible(TRUE)
}

#------------------------------
# Read inputs
#------------------------------

xxtpt <- read_single_column_tsv("inputs/xxtpt.tsv", "x")
result_raw <- read_single_column_tsv("inputs/result.tsv", "result")
na_idx_raw <- read_single_column_tsv("inputs/na_idx.tsv", "x")
treatment_duration_raw <- read_single_column_tsv("inputs/treatment_duration.tsv", "treatment_duration")

#------------------------------
# Preprocess / coerce types
#------------------------------

# Trim xxtpt, keep as character, allow NA
xxtpt <- trimws(as.character(xxtpt))

# Result: numeric, may contain NA; coerce non-numeric to NA with warning
suppressWarnings({
  result <- as.numeric(result_raw)
})
if (any(is.na(result) & !is.na(result_raw))) {
  warning("Some values in 'result' could not be coerced to numeric and were set to NA.")
}

# na_idx: logical vector indicating which positions in xxtpt are NA
# Input preview suggests it is not pre-logical; coerce safely
na_idx_chr <- as.character(na_idx_raw)
na_idx <- tolower(na_idx_chr) %in% c("true", "t", "1", "yes", "y")

# If all FALSE and xxtpt actually has NA, reconstruct from xxtpt
if (!any(na_idx) && any(is.na(xxtpt))) {
  warning("Recomputing na_idx from xxtpt because no TRUE values were found.")
  na_idx <- is.na(xxtpt)
}

# treatment_duration: numeric, non-negative
suppressWarnings({
  treatment_duration <- as.numeric(treatment_duration_raw)
})
if (any(is.na(treatment_duration) & !is.na(treatment_duration_raw))) {
  warning("Some values in 'treatment_duration' could not be coerced to numeric and were set to NA.")
}
if (any(treatment_duration < 0, na.rm = TRUE)) {
  stop("Negative values found in treatment_duration; expected non-negative hours.")
}

#------------------------------
# Validate alignment
#------------------------------

validate_lengths(
  xxtpt = xxtpt,
  result = result,
  na_idx = na_idx,
  treatment_duration = treatment_duration
)

# Sanity check: positions marked as NA in na_idx should correspond to NA in xxtpt
mismatch_na <- which(na_idx & !is.na(xxtpt))
if (length(mismatch_na) > 0L) {
  warning(sprintf(
    "na_idx indicates NA at positions %s, but xxtpt is not NA there.",
    paste(head(mismatch_na, 20), collapse = ", ")
  ))
}

#------------------------------
# Convert special case patterns
#------------------------------

# admiral::convert_special_cases expects:
# - xxtpt (character)
# - result (numeric)
# - na_idx (logical)
# - treatment_duration (numeric)

result_converted <- convert_special_cases(
  xxtpt = xxtpt,
  result = result,
  na_idx = na_idx,
  treatment_duration = treatment_duration
)

#------------------------------
# Post-conversion checks
#------------------------------

# Check for unexpected patterns: positions where result is still NA while xxtpt is non-NA
still_na_idx <- which(is.na(result_converted) & !is.na(xxtpt))
if (length(still_na_idx) > 0L) {
  warning(sprintf(
    "There are %d positions where result remains NA although xxtpt is not NA. Examples indices: %s",
    length(still_na_idx),
    paste(head(still_na_idx, 20), collapse = ", ")
  ))
}

# Simple consistency check: length and type
if (length(result_converted) != length(result)) {
  stop("Length of converted result does not match original result.")
}
if (!is.numeric(result_converted)) {
  stop("Converted result is not numeric.")
}

#------------------------------
# Save outputs
#------------------------------

# Combine into a data frame for CSV output
out_df <- data.frame(
  xxtpt = xxtpt,
  result_original = result,
  result_converted = result_converted,
  na_idx = na_idx,
  treatment_duration = treatment_duration,
  stringsAsFactors = FALSE
)

csv_path <- file.path("outputs", "converted_timepoints.csv")
rds_path <- file.path("outputs", "converted_timepoints.rds")

write.csv(out_df, file = csv_path, row.names = FALSE)
saveRDS(result_converted, file = rds_path)

#------------------------------
# Verify that files were written

```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)

in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Helper to read simple single-column TSV as character vector
read_var_list <- function(fname) {
  path <- file.path(in_dir, fname)
  if (!file.exists(path)) return(character(0))
  x <- read_tsv(path, col_names = FALSE, show_col_types = FALSE)[[1]]
  x[!is.na(x) & x != ""]
}

may              <- read_var_list("may.tsv")
na_idx           <- read_var_list("na_idx.tsv")
no               <- read_var_list("no.tsv")
result           <- read_var_list("result.tsv")
same             <- read_var_list("same.tsv")
treatment_dur    <- read_var_list("treatment_duration.tsv")
xxtpt            <- read_var_list("xxtpt.tsv")

# Placeholder example: construct a data frame that reflects
# "convert special cases" by classifying variables into the
# different categories based on the input lists, then merging
# according to the "result" list as desired output variables.

all_vars <- unique(c(may, no, same, treatment_dur, xxtpt, na_idx, result))
all_vars <- all_vars[all_vars != ""]

df <- tibble(
  VAR = all_vars,
  MAY_FLAG      = VAR %in% may,
  NO_FLAG       = VAR %in% no,
  SAME_FLAG     = VAR %in% same,
  TRTDUR_FLAG   = VAR %in% treatment_dur,
  XXTPT_FLAG    = VAR %in% xxtpt,
  NA_IDX_FLAG   = VAR %in% na_idx,
  IN_RESULT     = VAR %in% result
)

write_csv(df, file.path(out_dir, "result.csv"), na = "")
```

## Current Candidate Prompt File
```text
Write R code to convert special case patterns using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/xxtpt.tsv, inputs/result.tsv, inputs/na_idx.tsv, inputs/treatment_duration.tsv). Converts special case timepoint patterns to numeric hours including screening, pre-dose, pre-treatment, before, and end of treatment markers. Additional details: Recognizes and converts the following patterns: * "Screening" -> 0 * "Pre-dose", "Predose", "Pre-treatment", "Pre-infusion", "Pre-inf", "Before", "Infusion", "0H" -> 0 * "EOI", "EOT", "End of Infusion", "End of Treatment", "After End of Infusion", "After End of Treatment" -> treatment_duration Only updates result for positions where result is currently NA and xxtpt is not NA. Use admiral's convert_special_cases function with the following parameters: xxtpt (Character vector of timepoint descriptions (trimmed, no leading/ trailing whitespace)), result (Numeric vector of results (partially filled, may contain NA)), na_idx (Logical vector indicating which positions in xxtpt are NA), treatment_duration (Duration of treatment in hours (non-negative numeric vector, same length as xxtpt)). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: Updated numeric vector with special case patterns converted to hours. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to convert special case patterns using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/xxtpt.tsv, inputs/result.tsv, inputs/na_idx.tsv, inputs/treatment_duration.tsv). Converts special case timepoint patterns to numeric hours including screening, pre-dose, pre-treatment, before, and end of treatment markers. Additional details: Recognizes and converts the following patterns: * "Screening" -> 0 * "Pre-dose", "Predose", "Pre-treatment", "Pre-infusion", "Pre-inf", "Before", "Infusion", "0H" -> 0 * "EOI", "EOT", "End of Infusion", "End of Treatment", "After End of Infusion", "After End of Treatment" -> treatment_duration Only updates result for positions where result is currently NA and xxtpt is not NA. Use admiral's convert_special_cases function with the following parameters: xxtpt (Character vector of timepoint descriptions (trimmed, no leading/ trailing whitespace)), result (Numeric vector of results (partially filled, may contain NA)), na_idx (Logical vector indicating which positions in xxtpt are NA), treatment_duration (Duration of treatment in hours (non-negative numeric vector, same length as xxtpt)). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: Updated numeric vector with special case patterns converted to hours. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```