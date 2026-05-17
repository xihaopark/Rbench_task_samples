# Sample 26: pharmaverse/admiral/get_imputation_target_date

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiral/get_imputation_target_date`
- package/function: `admiral` / `get_imputation_target_date`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `NO_OUTPUT` tier=`exec_fail`

## Reference Prompt
```text
Resolve **imputation target date** components. Load `library(admiral)`.

**Inputs:** `date_imputation.tsv`, `month.tsv`.

Some admiral helpers are **not exported**; the reference uses `get("<fn>", envir = asNamespace("admiral"))(...)`. Using the same call is fair game and avoids false failures from `admiral::<fn>` not existing.

**Computation:** **`get_imputation_target_date(date_imputation, month)`** via `asNamespace("admiral")`.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.

```

## Current Prompt
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

## Simple Prompt
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

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "message": "No output files created",
  "returncode": 1,
  "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
  "comparison": ""
}
```

## Simple Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "message": "No output files created",
  "returncode": 1,
  "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
  "comparison": ""
}
```

## Reference Solution Head
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

## Current Solution
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
  
```

## Simple Solution
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

## Current Candidate Prompt File
```text
Write R code to get date imputation targets using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/date_imputation.tsv, inputs/month.tsv). Additional details: - For `date_imputation = "first"` `"0000"`, `"01"`, `"01"` are returned. - For `date_imputation = "mid"` `"xxxx"`, `"06"`, `"30"` if `month` is `NA`. otherwise `"15"` returned. - For `date_imputation = "last"` `"9999"`, `"12"`, `"28"` are returned. - For `date_imputation = "<mm>-<dd>"` `"xxxx"`, `"<mm>"`, `"<dd>"` are returned. `"xxxx"` indicates that the component is undefined. If an undefined component occurs in the imputed `--DTC` value, the imputed `--DTC` value is set to `NA_character_` in the imputation functions. Use admiral's get_imputation_target_date function with the following parameters: date_imputation (The value to impute the day/month when a datepart is missing.), month (Month component of the partial date). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: s A list of character vectors. The elements of the list are named "year", "month", "day".. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to get date imputation targets using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/date_imputation.tsv, inputs/month.tsv). Additional details: - For `date_imputation = "first"` `"0000"`, `"01"`, `"01"` are returned. - For `date_imputation = "mid"` `"xxxx"`, `"06"`, `"30"` if `month` is `NA`. otherwise `"15"` returned. - For `date_imputation = "last"` `"9999"`, `"12"`, `"28"` are returned. - For `date_imputation = "<mm>-<dd>"` `"xxxx"`, `"<mm>"`, `"<dd>"` are returned. `"xxxx"` indicates that the component is undefined. If an undefined component occurs in the imputed `--DTC` value, the imputed `--DTC` value is set to `NA_character_` in the imputation functions. Use admiral's get_imputation_target_date function with the following parameters: date_imputation (The value to impute the day/month when a datepart is missing.), month (Month component of the partial date). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: s A list of character vectors. The elements of the list are named "year", "month", "day".. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```