# Case 25 - `pharmaverse/admiral/restrict_imputed_dtc_dtm`

**Package:** `admiral`  **Function:** `restrict_imputed_dtc_dtm`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `High`

## Audit Evidence

Reference first computes `imputed_dtc <- admiral::impute_dtc_dtm(dtc_raw)` then calls non-exported `restrict_imputed_dtc_dtm(dtc_raw, imputed_dtc, min_dates=NULL, max_dates=NULL)`; current prompt exposes only `imputed_dtc` and describes min/max behavior without the required call shape.

## Task Prompt From `task.json`

```text
Restrict an **imputed datetime** string. Load `library(admiral)`.

**Inputs:** `imputed_dtc.tsv`.

**Computation:** `imputed_dtc <- admiral::impute_dtc_dtm(dtc_raw)` then **`restrict_imputed_dtc_dtm(...)`** from namespace.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Generated Prompt

```text
Write R code to restrict imputed `--dtc` date to minimum/maximum dates using admiral. At the beginning, load the required packages: library(admiral). The input data file is stored in inputs/imputed_dtc.tsv. Use admiral's restrict_imputed_dtc_dtm function with the following parameters: imputed_dtc (The imputed `--DTC` date). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: s - The last of the minimum dates (`min_dates`) which are in the range of the partial `--DTC` date (`dtc`) - The first of the maximum dates (`max_dates`) which are in the range of the partial `--DTC` date (`dtc`) - `imputed_dtc` if the partial `--DTC` date (`dtc`) is not in range of any of the minimum or maximum dates.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### imputed_dtc.tsv (68 bytes)
dtc
---T08:00:00
2020
2022-09-14
2020
2021-11-05
2019-12
2021-11-05

```

## Simple Generated Prompt

```text
Create R script to perform restrict imputed dtc dtm using the admiral clinical task contract.

Input: imputed_dtc.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### imputed_dtc.tsv (68 bytes)
dtc
---T08:00:00
2020
2022-09-14
2020
2021-11-05
2019-12
2021-11-05

```

## Actual Input Files

**`imputed_dtc.tsv`**

```tsv
imputed_dtc
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"imputed_dtc","result"
"2020-01-15T12:00:00","2020-01-15T12:00:00"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"imputed_dtc, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))

# 1. 读取输入数据 / Read input data
imputed_dtc_path <- file.path("inputs", "imputed_dtc.tsv")
if (!file.exists(imputed_dtc_path)) {
  stop("imputed_dtc.tsv is required input")
}
imputed_dtc_df <- read.delim(imputed_dtc_path, check.names = FALSE, stringsAsFactors = FALSE)
dtc_raw <- as.character(imputed_dtc_df[[1]][1])
if (is.na(dtc_raw) || dtc_raw == "test_value" || !nzchar(dtc_raw)) dtc_raw <- "2020-01-15T12:00:00"
imputed_dtc <- admiral::impute_dtc_dtm(dtc_raw)
result <- get("restrict_imputed_dtc_dtm", envir = asNamespace("admiral"))(dtc_raw, imputed_dtc, min_dates = NULL, max_dates = NULL)

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    imputed_dtc = dtc_raw,
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
library(admiral)
library(readr)
library(dplyr)
library(stringr)
library(purrr)

#---- Helper functions ----

# Validate dtc format (very basic checks)
validate_dtc <- function(x) {
  # Allow "", NA, yyyy, yyyy-mm, yyyy-mm-dd, and with time parts
  ok <- is.na(x) |
    x == "" |
    str_detect(x,
      "^\\d{4}(-\\d{2}(-\\d{2})?)?(T\\d{2}:\\d{2}(:\\d{2})?)?$"
    )
  if (!all(ok)) {
    bad_vals <- unique(x[!ok])
    stop(
      "Invalid DTC values detected: ",
      paste(bad_vals, collapse = ", ")
    )
  }
  invisible(x)
}

# Safe writer that stops on error
safe_write <- function(expr) {
  tryCatch(
    expr,
    error = function(e) stop("File write failed: ", conditionMessage(e))
  )
}

#---- Load & validate input ----

inp_file <- "inputs/imputed_dtc.tsv"
if (!file.exists(inp_file)) {
  stop("Input file not found: ", inp_file)
}

dt_raw <- tryCatch(
  read_tsv(
    inp_file,
    col_types = cols(.default = col_character())
  ),
  error = function(e) stop("Failed to read input file: ", conditionMessage(e))
)

if (!"dtc" %in% names(dt_raw)) {
  stop("Input data must contain a 'dtc' column.")
}

# Basic structural checks
if (nrow(dt_raw) == 0L) {
  stop("Input data has zero rows.")
}

validate_dtc(dt_raw$dtc)

#---- Construct min_dates / max_dates for restriction ----
# Example rule:
# - For partial year "2020", min_dates = "2020-01-01", max_dates = "2020-12-31"
# - For year-month "2019-12", min_dates = "2019-12-01", max_dates = "2019-12-31"
# - For fully specified dates, use the exact date as min and max
# - For missing/invalid patterns (like leading dashes), leave as NA so restriction
#   will return imputed_dtc unchanged.

# Convert partial dtc to a concrete "imputed_dtc" assuming:
#   - Unknown month -> January
#   - Unknown day -> first of month
# Keep time if present.
impute_dtc_simple <- function(dtc) {
  if (is.na(dtc) || dtc == "") return(NA_character_)

  # Split date and time
  parts <- str_split_fixed(dtc, "T", 2)
  dpart <- parts[, 1]
  tpart <- ifelse(parts[, 2] == "", NA_character_, parts[, 2])

  # Year only
  if (str_detect(dpart, "^\\d{4}$")) {
    d_res <- paste0(dpart, "-01-01")
  } else if (str_detect(dpart, "^\\d{4}-\\d{2}$")) {
    # Year-month
    d_res <- paste0(dpart, "-01")
  } else if (str_detect(dpart, "^\\d{4}-\\d{2}-\\d{2}$")) {
    d_res <- dpart
  } else {
    # Any other pattern -> leave as-is
    return(dtc)
  }

  if (!is.na(tpart)) {
    paste0(d_res, "T", tpart)
  } else {
    d_res
  }
}

# Compute min/max date (date part only)
get_min_date <- function(dtc) {
  if (is.na(dtc) || dtc == "") return(NA_character_)

  dpart <- str_split_fixed(dtc, "T", 2)[, 1]

  if (str_detect(dpart, "^\\d{4}$")) {
    paste0(dpart, "-01-01")
  } else if (str_detect(dpart, "^\\d{4}-\\d{2}$")) {
    paste0(dpart, "-01")
  } else if (str_detect(dpart, "^\\d{4}-\\d{2}-\\d{2}$")) {
    dpart
  } else {
    NA_character_
  }
}

get_max_date <- function(dtc) {
  if (is.na(dtc) || dtc == "") return(NA_character_)

  dpart <- str_split_fixed(dtc, "T", 2)[, 1]

  if (str_detect(dpart, "^\\d{4}$")) {
    paste0(dpart, "-12-31")
  } else if (str_detect(dpart, "^\\d{4}-\\d{2}$")) {
    # last day of month
    y <- as.integer(substr(dpart, 1, 4))
    m <- as.integer(substr(dpart, 6, 7))
    first_next <- as.Date(sprintf("%04d-%02d-01", ifelse(m == 12, y + 1, y),
                                  ifelse(m == 12, 1, m + 1)))
    last_this <- first_next - 1
    as.character(last_this)
  } else if (str_detect(dpart, "^\\d{4}-\\d{2}-\\d{2}$")) {
    dpart
  } else {
    NA_character_
  }
}

dt_pre <- dt_raw %>%
  mutate(
    imputed_dtc = map_chr(dtc, impute_dtc_simple),
    min_dates   = map_chr(dtc, get_min_date),
    max_dates   = map_chr(dtc, get_max_date)
  )

#---- Apply restrict_imputed_dtc_dtm rowwise ----

restrict_safe <- function(dtc, imputed_dtc, min_date, max_date) {
  # Handle rows with no usable min/max: return imputed_dtc
  if (is.na(min_date) && is.na(max_date)) return(imputed_dtc)

  # Build vectors of min/max for API (single-element vectors here)
  min_vec <- if (!is.na(min_date)) min_date else NULL
  max_vec <- if (!is.na(max_date)) max_date else NULL

  out <- tryCatch(
    restrict_imputed_dtc_dtm(
      dtc         = dtc,
      imputed_dtc = imputed_dtc,
      min_dates   = min_vec,
      max_dates   = max_vec
    ),
    error = function(e) {
      warning("restrict_imputed_dtc_dtm failed for dtc=",
              dtc, " imputed_dtc=", imputed_dtc,
              " : ", conditionMessage(e))
      imputed_dtc
    }
  )
  out
}

dt_res <- dt_pre %>%
  rowwise() %>%
  mutate(
    restricted_imputed_dtc = restrict_safe(
      dtc         = dtc,
      imputed_dtc = imputed_dtc,
      min_date    = min_dates,
      max_date    = max_dates
    )
  ) %>%
  ungroup()

#---- Basic sanity checks on result ----

# Check for any NA where input imputed_dtc was non-NA
na_mismatch <- dt_res %>%
  filter(!is.na(imputed_dtc) & is.na(restricted_imputed_dtc))

if (nrow(na_mismatch) > 0L) {
  warning("Unexpected NAs introduced in restricted_imputed_dtc.")
}

# Quick pattern checks that could indicate parsing issues
if (any(str_detect(dt_res$restricted_imputed_dtc, "---"))) {
  warning("Found '---' in restricted_imputed_dtc; possible parsing/misalignment.")
}

#---- Write outputs ----

if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

out_csv  <- "outputs/restricted_imputed_dtc.csv"
out_rds  <- "outputs/restricted_imputed_dtc.rds"

safe_write(
  write_csv(dt_res, out_csv, na = "")
)
safe_write(
  saveRDS(dt_res, out_rds)
)

# Confirm that files exist and are readable
if (!file.exists(out_csv))  stop("CSV output file not found after writing.")
if (!file.exists(out_rds))  stop("RDS output file not found after writing.")

# Lightweight reload check
dt_check_csv <- tryCatch(
  read_csv(out_csv, col_types = cols(.default = col_character())),
  error = function(e) stop("Failed to re-read CSV output: ", conditionMessage(e))
)

dt_check_rds <- tryCatch(
  readRDS(out_rds),
  error = function(e) stop("Failed to re-read RDS output: ", conditionMessage(e))
)

if (!identical(nrow(dt_res), nrow(dt_check_csv)) ||
    !identical(nrow(dt_res), nrow(dt_check_rds))) {
  stop("Row count mismatch between in-memory and written outputs.")
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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error in validate_dtc(dt_raw$dtc) : 
  Invalid DTC values detected: ---T08:00:00
Execution halted

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

_No files found._

## Simple Prompt LLM Code

```r
# scripts/restrict_imputed_dtc.R

library(dplyr)
library(readr)
library(stringr)
library(lubridate)

#-----------------------------
# Helper: identify imputed dtc
#-----------------------------
# Assumptions based on ADaM/ADSL-like imputation rules:
# - DTC containing only a year       (e.g., "2020")                    -> missing month/day
# - DTC containing year-month       (e.g., "2019-12")                  -> missing day
# - DTC containing full date        (e.g., "2022-09-14")               -> no imputation
# - DTC containing only time        (e.g., "---T08:00:00")             -> missing date
# The "restrict imputed dtc dtm" task keeps only fully specified
# non-imputed dates (i.e., complete YYYY-MM-DD).

is_full_date <- function(x) {
  # Full ISO date pattern: YYYY-MM-DD
  str_detect(x, "^\\d{4}-\\d{2}-\\d{2}$")
}

#-----------------------------
# IO
#-----------------------------
in_file  <- file.path("inputs", "imputed_dtc.tsv")
out_file <- file.path("outputs", "result.csv")

dt <- read_tsv(
  in_file,
  col_types = cols(
    dtc = col_character()
  )
)

#-----------------------------
# Restrict to non-imputed DTC
#-----------------------------
result <- dt %>%
  filter(is_full_date(dtc)) %>%
  mutate(
    # Optionally, convert to Date if desired by downstream tasks
    dt = ymd(dtc)
  )

#-----------------------------
# Write output
#-----------------------------
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


Attaching package: ‘lubridate’

The following objects are masked from ‘package:base’:

    date, intersect, setdiff, union


```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
dtc,dt
2022-09-14,2022-09-14
2021-11-05,2021-11-05
2021-11-05,2021-11-05

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiral/restrict_imputed_dtc_dtm",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "returncode": 1,
  "comparison": null,
  "normalizations": null
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/admiral/restrict_imputed_dtc_dtm",
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
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(3, 2)"
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
