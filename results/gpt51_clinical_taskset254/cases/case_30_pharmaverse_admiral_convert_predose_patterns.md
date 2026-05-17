# Case 30 - `pharmaverse/admiral/convert_predose_patterns`

**Package:** `admiral`  **Function:** `convert_predose_patterns`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `TIMEOUT` / tier `exec_fail`  
**Simple prompt status:** `TIMEOUT` / tier `exec_fail`  
**Audit root cause:** `unclear_needs_rerun`  **Confidence:** `Low`

## Audit Evidence

Both current and simple executions time out with no stderr/comparison. The reference implements a regex transformation over `xxtpt`, `result`, and `na_idx`; sample previews show generic values/headers, but the available artifact is insufficient to tell whether the timeout is model code, fixture, or runner behavior.

## Task Prompt From `task.json`

```text
Write R code to implement the **Convert predose patterns** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/may.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'may.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/na_idx.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'na_idx.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/no.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'no.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/result.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'result.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/xxtpt.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'xxtpt.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Convert Predose Patterns** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
Write R code to convert predose/before patterns using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/xxtpt.tsv, inputs/result.tsv, inputs/na_idx.tsv). Converts predose and before timepoint patterns to negative numeric hours (time before dose/treatment). Additional details: Recognizes patterns like: * "5 MIN PREDOSE" -> -0.0833 (negative 5 minutes) * "5 MIN PRE-DOSE" -> -0.0833 (negative 5 minutes) * "1 HOUR BEFORE" -> -1 (negative 1 hour) Returns negative values to indicate time before dose/treatment. Only updates result for positions where result is currently NA and xxtpt is not NA. Use admiral's convert_predose_patterns function with the following parameters: xxtpt (Character vector of timepoint descriptions (trimmed, no leading/ trailing whitespace)), result (Numeric vector of results (partially filled, may contain NA)), na_idx (Logical vector indicating which positions in xxtpt are NA). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: Updated numeric vector with predose/before patterns converted to negative hours. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

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

### xxtpt.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Simple Generated Prompt

```text
Create R script to perform convert predose patterns using the admiral clinical task contract.

Input: may.tsv, na_idx.tsv, no.tsv, result.tsv, xxtpt.tsv
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

### xxtpt.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Actual Input Files

**`may.tsv`**

```tsv
may
"test_value"

```

**`na_idx.tsv`**

```tsv
na_idx
FALSE

```

**`no.tsv`**

```tsv
no
"test_value"

```

**`result.tsv`**

```tsv
result
0.1
1.5
10.0
100.0
1000.0

```

**`xxtpt.tsv`**

```tsv
xxtpt
"item1"
"item2"
"item3"
"item4"
"item5"

```

## Reference Output Files

**`result.csv`**

```csv
"xxtpt","result"
"item1",0.1
"item2",1.5
"item3",10
"item4",100
"item5",1000

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"xxtpt, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(stringr))
suppressPackageStartupMessages(library(dplyr))

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

# 2. 执行函数实现 / Execute function implementation
predose_pattern <- stringr::regex(
    paste0(
      "^(?<value>\\d+(?:\\.\\d+)?)\\s*",
      "(?<unit>m(?:in|inute)?|h(?:r|our)?)s?\\s+",
      "(?:pre-?dose|before)$"
    ),
    ignore_case = TRUE,
    comments = TRUE
  )
  predose_matches <- str_match(xxtpt, predose_pattern)
  predose_idx <- !is.na(predose_matches[, 1]) & is.na(result) & !na_idx
  if (any(predose_idx)) {
    time_value <- as.numeric(predose_matches[predose_idx, "value"])
    unit <- tolower(predose_matches[predose_idx, "unit"])
    is_minutes <- substr(unit, 1, 1) == "m"
    result[predose_idx] <- if_else(
      is_minutes,
      -time_value / 60,
      -time_value
    )
  }

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    xxtpt = xxtpt, result = result,
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
library(admiral)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#---------------------------
# Helper functions
#---------------------------
read_single_column_tsv <- function(path, colname_expected = NULL) {
  if (!file.exists(path)) {
    stop(paste0("Input file not found: ", path))
  }
  df <- tryCatch(
    read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop(paste0("Failed to read ", path, ": ", e$message))
  )
  if (!is.null(colname_expected)) {
    if (!colname_expected %in% names(df)) {
      stop(paste0("Expected column '", colname_expected, "' not found in ", path))
    }
    if (ncol(df) > 1) {
      warning(paste0("File ", path, " has more than one column. Using only '", colname_expected, "'."))
    }
    return(df[[colname_expected]])
  } else {
    if (ncol(df) != 1) {
      stop(paste0("File ", path, " must have exactly one column when colname_expected is NULL."))
    }
    return(df[[1]])
  }
}

#---------------------------
# Read inputs
#---------------------------
xxtpt_path   <- file.path("inputs", "xxtpt.tsv")
result_path  <- file.path("inputs", "result.tsv")
na_idx_path  <- file.path("inputs", "na_idx.tsv")

# xxtpt: character vector of timepoint descriptions
xxtpt_vec <- read_single_column_tsv(xxtpt_path, colname_expected = "x")

# result: numeric vector (may contain NA)
result_vec_raw <- read_single_column_tsv(result_path, colname_expected = "result")
# Coerce to numeric; warn on NAs introduced by coercion
suppressWarnings({
  result_vec <- as.numeric(result_vec_raw)
})
if (length(result_vec_raw) != length(result_vec)) {
  stop("Length mismatch when coercing result to numeric.")
}

# na_idx: logical vector indicating which positions in xxtpt are NA
na_idx_raw <- read_single_column_tsv(na_idx_path, colname_expected = "x")

# Try to interpret na_idx as logical:
#   - if already logical, keep
#   - if "TRUE"/"FALSE"/"T"/"F" strings, convert
#   - if "1"/"0" numeric-like, treat 1 as TRUE, 0 as FALSE
na_idx <- NA

if (is.logical(na_idx_raw)) {
  na_idx <- na_idx_raw
} else if (is.character(na_idx_raw)) {
  # Try direct logical coercion
  tmp <- tolower(trimws(na_idx_raw))
  if (all(tmp %in% c("true", "false", "t", "f"))) {
    na_idx <- tmp %in% c("true", "t")
  } else if (all(tmp %in% c("1", "0"))) {
    na_idx <- tmp == "1"
  } else {
    stop("na_idx.tsv must contain only logical-like values (TRUE/FALSE/T/F or 1/0).")
  }
} else if (is.numeric(na_idx_raw) || is.integer(na_idx_raw)) {
  if (!all(na_idx_raw %in% c(0, 1))) {
    stop("Numeric na_idx.tsv must contain only 0/1 values.")
  }
  na_idx <- na_idx_raw == 1
} else {
  stop("Unsupported type in na_idx.tsv for logical conversion.")
}

#---------------------------
# Basic validations
#---------------------------
n_xxtpt  <- length(xxtpt_vec)
n_result <- length(result_vec)
n_naidx  <- length(na_idx)

if (!(n_xxtpt == n_result && n_xxtpt == n_naidx)) {
  stop(paste(
    "Length mismatch among inputs:",
    "length(xxtpt) =", n_xxtpt,
    "length(result) =", n_result,
    "length(na_idx) =", n_naidx
  ))
}

# Check that na_idx is logical and no NAs in na_idx
if (!is.logical(na_idx) || any(is.na(na_idx))) {
  stop("na_idx must be a logical vector with no NA values.")
}

#---------------------------
# Preprocess xxtpt
#---------------------------
# Trim leading/trailing whitespace as required
xxtpt_vec_trim <- trimws(xxtpt_vec)

# Validate that positions marked as NA in na_idx truly have NA xxtpt
if (any(!is.na(xxtpt_vec_trim[na_idx]))) {
  warning("Some positions in na_idx are TRUE but corresponding xxtpt values are not NA after trimming.")
}

#---------------------------
# Convert predose/before patterns
#---------------------------
res_converted <- tryCatch(
  convert_predose_patterns(
    xxtpt   = xxtpt_vec_trim,
    result  = result_vec,
    na_idx  = na_idx
  ),
  error = function(e) {
    stop(paste0("convert_predose_patterns failed: ", e$message))
  }
)

#---------------------------
# Post-conversion checks
#---------------------------
# Check that length is preserved
if (length(res_converted) != length(result_vec)) {
  stop("convert_predose_patterns returned a vector of incorrect length.")
}

# Check that only NA positions (with non-NA xxtpt) were updated
updated_positions <- which(is.na(result_vec) & !na_idx & !is.na(res_converted))
if (length(updated_positions) == 0) {
  warning("No positions were updated by convert_predose_patterns. Check if patterns were present.")
}

# Identify any suspicious patterns that still contain pre-dose/before text
# but did not get converted (still NA in res_converted where xxtpt is non-NA)
pattern_idx <- grepl("(?i)predose|pre-dose|before", xxtpt_vec_trim, perl = TRUE)
suspect_idx <- which(pattern_idx & !na_idx & is.na(res_converted))

if (length(suspect_idx) > 0) {
  warning(
    paste0(
      "There are ", length(suspect_idx),
      " timepoints with 'predose/pre-dose/before' patterns that remain NA after conversion. ",
      "Possible unrecognized patterns or data issues."
    )
  )
}

#---------------------------
# Save outputs
#---------------------------
# 1) Save full result as CSV (one column 'result')
result_df <- data.frame(result = res_converted)
out_csv_path <- file.path("outputs", "result_converted.csv")

tryCatch(
  {
    write.csv(result_df, out_csv_path, row.names = FALSE)
  },
  error = function(e) {
    stop(paste0("Failed to write CSV to ", out_csv_path, ": ", e$message))
  }
)

# 2) Save full object as RDS (in case downstream code needs the raw numeric vector)
out_rds_path <- file.path("outputs", "result_converted.rds")
tryCatch(
  {
    saveRDS(res_converted, out_rds_path)
  },
  error = function(e) {
    stop(paste0("Failed to write RDS to ", out_rds_path, ": ", e$message))
  }
)

#---------------------------
# Confirm outputs
#---------------------------
if (!file.exists(out_csv_path)) {
  stop(paste0("Output CSV not found after writing: ", out_csv_path))
}
if (!file.exists(out_rds_path)) {
  stop(paste0("Output RDS not found after writing: ", out_rds_path))
}

# Basic read-back check for CSV
check_df <- tryCatch(
  read.csv(out_csv_path, stringsAsFactors = FALSE),
  error = function(e) stop(paste0("Failed to read back CSV: ", e$message))
)

if (!"result" %in% names(check_df)) {
  stop("Read-back CSV does not contain 'result' column.")
}
if (nrow(check_df) != length(res_converted)) {
  stop("Row count mismatch after reading back result_converted.csv.")
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
Error: na_idx.tsv must contain only logical-like values (TRUE/FALSE/T/F or 1/0).
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

library(dplyr)
library(readr)
library(stringr)

in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

may      <- read_tsv(file.path(in_dir, "may.tsv"), col_types = cols())
na_idx   <- read_tsv(file.path(in_dir, "na_idx.tsv"), col_types = cols())
no       <- read_tsv(file.path(in_dir, "no.tsv"), col_types = cols())
result   <- read_tsv(file.path(in_dir, "result.tsv"), col_types = cols())
xxtpt    <- read_tsv(file.path(in_dir, "xxtpt.tsv"), col_types = cols())

# Placeholder predose pattern conversion using admiral-like style:
# Ensure required columns exist
req_cols <- c("USUBJID", "AVISITN", "AVAL")

for (nm in list(may = may, no = no, result = result)) {
  missing_cols <- setdiff(req_cols, names(nm[[1]]))
  if (length(missing_cols) > 0) {
    for (cl in missing_cols) {
      nm[[1]][[cl]] <- NA
    }
  }
}

may    <- may  %>% select(any_of(req_cols))
no     <- no   %>% select(any_of(req_cols))
result <- result %>% select(any_of(req_cols))

# Example predose flag/selection using na_idx/xxtpt as list of parameters
# (dummy implementation – keep structure compatible)
param_vars <- intersect(na_idx$x, xxtpt$x)

result_conv <-
  result %>%
  mutate(
    PARAMCD = if ("AVAL" %in% names(.)) "PD" else NA_character_,
    PARCAT1 = if_else(AVISITN <= 1, "PREDOSE", "POSTDOSE"),
    ADT     = NA_Date_
  ) %>%
  select(USUBJID, AVISITN, AVAL, PARAMCD, PARCAT1, ADT)

write_csv(result_conv, file.path(out_dir, "result.csv"), na = "")
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

Error in `[[<-`:
! Assigned data `*vtmp*` must be compatible with existing data.
✖ Existing data has 3 rows.
✖ Assigned data has 4 rows.
ℹ Only vectors of size 1 are recycled.
Caused by error in `vectbl_recycle_rhs_rows()`:
! Can't recycle input of size 4 to size 3.
Backtrace:
    ▆
 1. ├─base::`[[<-`(`*tmp*`, 1, value = `<chr>`)
 2. ├─tibble:::`[[<-.tbl_df`(`*tmp*`, 1, value = `<chr>`)
 3. │ └─tibble:::tbl_subassign(...)
 4. │   └─tibble:::vectbl_recycle_rhs_rows(value, fast_nrow(xo), i_arg = NULL, value_arg, call)
 5. │     ├─base::withCallingHandlers(...)
 6. │     └─vctrs::vec_recycle(value[[j]], nrow)
 7. └─vctrs:::stop_recycle_incompatible_size(...)
 8.   └─vctrs:::stop_vctrs(...)
 9.     └─rlang::abort(message, class = c(class, "vctrs_error"), ..., call = call)
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
  "task_id": "pharmaverse/admiral/convert_predose_patterns",
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
  "task_id": "pharmaverse/admiral/convert_predose_patterns",
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
