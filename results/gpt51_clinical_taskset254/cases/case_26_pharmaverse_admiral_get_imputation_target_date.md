# Case 26 - `pharmaverse/admiral/get_imputation_target_date`

**Package:** `admiral`  **Function:** `get_imputation_target_date`  **Expected artifacts:** `outputs/result.csv, outputs/result.rds`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `High`

## Audit Evidence

Reference warns the helper is not exported and uses `get("get_imputation_target_date", envir=asNamespace("admiral"))`; current prompt says to use admiral's `get_imputation_target_date` directly, and current code calls `get_imputation_target_date(...)`, producing no outputs.

## Task Prompt From `task.json`

```text
Resolve **imputation target date** components. Load `library(admiral)`.

**Inputs:** `date_imputation.tsv`, `month.tsv`.

Some admiral helpers are **not exported**; the reference uses `get("<fn>", envir = asNamespace("admiral"))(...)`. Using the same call is fair game and avoids false failures from `admiral::<fn>` not existing.

**Computation:** **`get_imputation_target_date(date_imputation, month)`** via `asNamespace("admiral")`.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.

```

## Current Generated Prompt

```text
Write R code to get date imputation targets using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/date_imputation.tsv, inputs/month.tsv). Additional details: - For `date_imputation = "first"` `"0000"`, `"01"`, `"01"` are returned. - For `date_imputation = "mid"` `"xxxx"`, `"06"`, `"30"` if `month` is `NA`. otherwise `"15"` returned. - For `date_imputation = "last"` `"9999"`, `"12"`, `"28"` are returned. - For `date_imputation = "<mm>-<dd>"` `"xxxx"`, `"<mm>"`, `"<dd>"` are returned. `"xxxx"` indicates that the component is undefined. If an undefined component occurs in the imputed `--DTC` value, the imputed `--DTC` value is set to `NA_character_` in the imputation functions. Use admiral's get_imputation_target_date function with the following parameters: date_imputation (The value to impute the day/month when a datepart is missing.), month (Month component of the partial date). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: s A list of character vectors. The elements of the list are named "year", "month", "day".. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### date_imputation.tsv (21 bytes)
date_imputation
LAST

### month.tsv (27 bytes)
month
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform get imputation target date using the admiral clinical task contract.

Input: date_imputation.tsv, month.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### date_imputation.tsv (21 bytes)
date_imputation
LAST

### month.tsv (27 bytes)
month
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`date_imputation.tsv`**

```tsv
date_imputation
"test_value"

```

**`month.tsv`**

```tsv
month
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"year","month","day"
"xxxx","06","30"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))

date_imputation_df <- read.delim(file.path("inputs", "date_imputation.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
date_imputation <- as.character(date_imputation_df[[ncol(date_imputation_df)]][1])
if (!date_imputation %in% c("first", "mid", "last", " - ")) date_imputation <- "mid"
month_df <- read.delim(file.path("inputs", "month.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
month_raw <- as.character(month_df[[ncol(month_df)]][1])
if (month_raw == "test_value" || !grepl("^[0-9]{4}-", month_raw)) month_raw <- NA_character_
month <- as.Date(month_raw, tryFormats = c("%Y-%m-%d", "%Y/%m/%d"))

get_imputation_target_date <- get("get_imputation_target_date", envir = asNamespace("admiral"))
result <- get_imputation_target_date(date_imputation, month)

dir.create("outputs", showWarnings = FALSE)
result_df <- as.data.frame(result)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)

```

## Current Prompt LLM Code

```r
library(admiral)
library(readr)
library(dplyr)
library(purrr)
library(stringr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

#-----------------------------
# Read and validate inputs
#-----------------------------

# Read date_imputation
date_imp_path <- file.path("inputs", "date_imputation.tsv")
if (!file.exists(date_imp_path)) {
  stop("Input file not found: ", date_imp_path)
}

date_imp_df <- tryCatch(
  read_tsv(date_imp_path, show_col_types = FALSE),
  error = function(e) stop("Failed to read date_imputation.tsv: ", conditionMessage(e))
)

if (!"date_imputation" %in% names(date_imp_df)) {
  stop("Column 'date_imputation' not found in date_imputation.tsv")
}

if (nrow(date_imp_df) != 1L) {
  stop("date_imputation.tsv must contain exactly one row")
}

date_imputation_val <- as.character(date_imp_df$date_imputation[1])

# Normalize common textual values if necessary
date_imputation_val <- toupper(trimws(date_imputation_val))

# Map from textual value to function-compatible value if needed
date_imputation_val <- dplyr::case_when(
  date_imputation_val %in% c("FIRST") ~ "first",
  date_imputation_val %in% c("MID", "MIDDLE") ~ "mid",
  date_imputation_val %in% c("LAST") ~ "last",
  TRUE ~ date_imputation_val
)

# Read month input
month_path <- file.path("inputs", "month.tsv")
if (!file.exists(month_path)) {
  stop("Input file not found: ", month_path)
}

month_df <- tryCatch(
  read_tsv(month_path, show_col_types = FALSE),
  error = function(e) stop("Failed to read month.tsv: ", conditionMessage(e))
)

if (!"month" %in% names(month_df)) {
  stop("Column 'month' not found in month.tsv")
}

# Attempt to parse month as numeric; non-numeric become NA
month_vec <- suppressWarnings(as.integer(month_df$month))
month_vec[month_vec < 1 | month_vec > 12] <- NA_integer_

#-----------------------------
# Compute imputation targets
#-----------------------------

# Wrapper around get_imputation_target_date to handle vectorization and errors
safe_get_target <- safely(function(di, mo) {
  get_imputation_target_date(
    date_imputation = di,
    month = mo
  )
})

results_list <- map(month_vec, ~ safe_get_target(date_imputation_val, .x))

# Check for errors from safely
errors_idx <- which(map_lgl(results_list, ~ !is.null(.x$error)))
if (length(errors_idx) > 0L) {
  stop(
    "Error(s) occurred in get_imputation_target_date for row(s): ",
    paste(errors_idx, collapse = ", "),
    "; First error: ", conditionMessage(results_list[[errors_idx[1]]]$error)
  )
}

# Extract successful results
targets <- map(results_list, "result")

# Validate result structure
valid_structure <- function(x) {
  is.list(x) &&
    all(c("year", "month", "day") %in% names(x)) &&
    all(vapply(x, function(v) is.character(v) && length(v) == 1L, logical(1)))
}

if (!all(map_lgl(targets, valid_structure))) {
  stop("Unexpected structure in get_imputation_target_date results")
}

# Convert to data frame
targets_df <- tibble(
  input_row = seq_along(targets),
  imputed_year  = map_chr(targets, ~ .x$year),
  imputed_month = map_chr(targets, ~ .x$month),
  imputed_day   = map_chr(targets, ~ .x$day)
)

# Combine with original month data (for traceability)
output_df <- bind_cols(
  tibble(row = seq_len(nrow(month_df))),
  month_df,
  targets_df %>% select(-input_row)
)

#-----------------------------
# Basic pattern checks
#-----------------------------

# Check for unexpected "xxxx"/"0000"/"9999" patterns vs. date_imputation setting
# Note: these are logical diagnostics; they do not stop execution
diag_msgs <- c()

if (date_imputation_val == "first") {
  if (any(output_df$imputed_year != "0000")) {
    diag_msgs <- c(diag_msgs, "FIRST: some imputed_year values are not '0000'.")
  }
  if (any(output_df$imputed_month != "01")) {
    diag_msgs <- c(diag_msgs, "FIRST: some imputed_month values are not '01'.")
  }
  if (any(output_df$imputed_day != "01")) {
    diag_msgs <- c(diag_msgs, "FIRST: some imputed_day values are not '01'.")
  }
} else if (date_imputation_val == "mid") {
  # Month NA -> xxxx-06-30; Month not NA -> xxxx-<mm>-15 (day=15)
  na_idx <- which(is.na(month_vec))
  if (length(na_idx) > 0L) {
    if (any(output_df$imputed_year[na_idx] != "xxxx")) {
      diag_msgs <- c(diag_msgs, "MID: NA month rows: imputed_year not 'xxxx'.")
    }
    if (any(output_df$imputed_month[na_idx] != "06")) {
      diag_msgs <- c(diag_msgs, "MID: NA month rows: imputed_month not '06'.")
    }
    if (any(output_df$imputed_day[na_idx] != "30")) {
      diag_msgs <- c(diag_msgs, "MID: NA month rows: imputed_day not '30'.")
    }
  }
  non_na_idx <- which(!is.na(month_vec))
  if (length(non_na_idx) > 0L) {
    if (any(output_df$imputed_year[non_na_idx] != "xxxx")) {
      diag_msgs <- c(diag_msgs, "MID: non-NA month rows: imputed_year not 'xxxx'.")
    }
    if (any(output_df$imputed_day[non_na_idx] != "15")) {
      diag_msgs <- c(diag_msgs, "MID: non-NA month rows: imputed_day not '15'.")
    }
  }
} else if (date_imputation_val == "last") {
  if (any(output_df$imputed_year != "9999")) {
    diag_msgs <- c(diag_msgs, "LAST: some imputed_year values are not '9999'.")
  }
  if (any(output_df$imputed_month != "12")) {
    diag_msgs <- c(diag_msgs, "LAST: some imputed_month values are not '12'.")
  }
  if (any(output_df$imputed_day != "28")) {
    diag_msgs <- c(diag_msgs, "LAST: some imputed_day values are not '28'.")
  }
} else if (str_detect(date_imputation_val, "^[0-9]{2}-[0-9]{2}$")) {
  # <mm>-<dd>
  parts <- str_split_fixed(date_imputation_val, "-", 2)
  exp_mm <- parts[1]
  exp_dd <- parts[2]
  if (any(output_df$imputed_year != "xxxx")) {
    diag_msgs <- c(diag_msgs, "<mm>-<dd>: some imputed_year values are not 'xxxx'.")
  }
  if (any(output_df$imputed_month != exp_mm)) {
    diag_msgs <- c(diag_msgs, "<mm>-<dd>: some imputed_month values differ from requested mm.")
  }
  if (any(output_df$imputed_day != exp_dd)) {
    diag_msgs <- c(diag_msgs, "<mm>-<dd>: some imputed_day values differ from requested dd.")
  }
}

if (length(diag_msgs) > 0L) {
  warning(paste(diag_msgs, collapse = " | "))
}

#-----------------------------
# Save outputs
#-----------------------------

# 1) Save full table as CSV
csv_out_path <- file.path("outputs", "date_imputation_targets.csv")
write_csv(output_df, csv_out_path)

# 2) Save raw list of targets as RDS (complex object)
rds_out_path <- file.path("outputs", "date_imputation_targets_list.rds")
saveRDS(targets, rds_out_path)

#-----------------------------
# Verify outputs written
#-----------------------------

verify_file <- function(path) {
  if (!file.exists(path)) {
    stop("Expected output file was not created: ", path)
  }
  info <- file.info(path)
  if (is.na(info$size) || info$size <= 0) {
    stop("Output file appears empty or invalid: ", path)
  }
  invisible(TRUE)
}

verify_file(csv_out_path)
verify_file(rds_out_path)

# Basic sanity check: re-read CSV and check row count
reloaded_df <- read_csv(csv_out_path, show_col_types = FALSE)
if (nrow(reloaded_df) != nrow(output_df)) {
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

Error: Error(s) occurred in get_imputation_target_date for row(s): 1, 2, 3; First error: could not find function "get_imputation_target_date"
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
library(lubridate)

# Directories
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read inputs
date_imp_cfg <- read_tsv(
  file.path(in_dir, "date_imputation.tsv"),
  show_col_types = FALSE
)

month <- read_tsv(
  file.path(in_dir, "month.tsv"),
  show_col_types = FALSE
)

# Expecting admiral date imputation type in first row / column `date_imputation`
imp_type <- date_imp_cfg$date_imputation[[1]]

# Helper to impute a date from a partial ISO string and type
impute_date <- function(x, type) {
  # x is character vector of dates like "2020-02-  ", "2020-  -  ", etc.
  # type is one of "FIRST", "MIDDLE", "LAST"
  x_chr <- as.character(x)

  # Extract components when present
  yr  <- str_sub(x_chr, 1, 4)
  mo  <- str_sub(x_chr, 6, 7)
  dy  <- str_sub(x_chr, 9, 10)

  # If missing, set according to type
  mo_imp <- ifelse(
    str_trim(mo) == "" | is.na(mo),
    if (toupper(type) == "FIRST") "01" else if (toupper(type) == "MIDDLE") "06" else "12",
    mo
  )

  # For day, we need max day in month for LAST, mid for MIDDLE
  # First construct a temporary date with day 01 for LAST/MIDDLE to get month length
  base_date <- suppressWarnings(
    ymd(paste0(yr, "-", mo_imp, "-01"))
  )

  max_day <- ifelse(
    is.na(base_date),
    NA_integer_,
    day(ceiling_date(base_date, "month") - days(1))
  )

  dy_imp <- case_when(
    str_trim(dy) != "" & !is.na(dy) ~ dy,
    toupper(type) == "FIRST" ~ "01",
    toupper(type) == "MIDDLE" ~ sprintf("%02d", ceiling(max_day / 2)),
    toupper(type) == "LAST"   ~ sprintf("%02d", max_day),
    TRUE ~ NA_character_
  )

  res <- suppressWarnings(
    ymd(paste0(yr, "-", mo_imp, "-", dy_imp))
  )

  res
}

# Assume AVAL is a partial date character suitable for imputation
result <- month %>%
  mutate(
    AVALC = as.character(AVAL),
    AVAL_DT = impute_date(AVALC, imp_type)
  )

# Write output
write_csv(result, file.path(out_dir, "result.csv"), na = "")
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

Error in `mutate()`:
ℹ In argument: `AVALC = as.character(AVAL)`.
Caused by error:
! object 'AVAL' not found
Backtrace:
     ▆
  1. ├─month %>% ...
  2. ├─dplyr::mutate(...)
  3. ├─dplyr:::mutate.data.frame(...)
  4. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  5. │   ├─base::withCallingHandlers(...)
  6. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  7. │     └─mask$eval_all_mutate(quo)
  8. │       └─dplyr (local) eval()
  9. └─base::.handleSimpleError(`<fn>`, "object 'AVAL' not found", base::quote(NULL))
 10.   └─dplyr (local) h(simpleError(msg, call))
 11.     └─rlang::abort(message, class = error_class, parent = parent, call = error_call)
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
  "task_id": "pharmaverse/admiral/get_imputation_target_date",
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
  "task_id": "pharmaverse/admiral/get_imputation_target_date",
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
