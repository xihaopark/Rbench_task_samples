# Case 39 - `pharmaverse/admiral/get_imputation_targets`

**Package:** `admiral`  **Function:** `get_imputation_targets`  **Expected artifacts:** `outputs/result.csv, outputs/result.rds`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_reference_mismatch`  **Confidence:** `high`

## Audit Evidence

Task metadata expects both `result.csv` and `result.rds`, but reference prompt says required output is `outputs/result.csv`. Current prompt omits non-exported namespace access and fixed `date_imputation = "mid"`, `time_imputation = "first"`; simple produces `(5, 4)` vs ref `(1, 6)`.

## Task Prompt From `task.json`

```text
Combine **partial datetime** + imputation rules into targets. Load `library(admiral)`.

**Inputs:** `partial.tsv`.

Some admiral helpers are **not exported**; the reference uses `get("<fn>", envir = asNamespace("admiral"))(...)`. Using the same call is fair game and avoids false failures from `admiral::<fn>` not existing.

**Computation:** `partial <- get_partialdatetime(...);` then **`get_imputation_targets(partial, date_imputation = "mid", time_imputation = "first")`**.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.

```

## Current Generated Prompt

```text
Write R code to get imputation targets using admiral. At the beginning, load the required packages: library(admiral). The input data file is stored in inputs/partial.tsv. Determines the imputation targets for date (see `get_imputation_target_date()` and time (see `get_imputation_target_time()`) components. Use admiral's get_imputation_targets function with the following parameters: partial (A list of partial date/time components.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: s A list of imputation targets for date and (if applicable) time components.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### partial.tsv (48 bytes)
partial
2019-12
2021
2019-12
2021-11-05
2020---

```

## Simple Generated Prompt

```text
Create R script to perform get imputation targets using the admiral clinical task contract.

Input: partial.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### partial.tsv (48 bytes)
partial
2019-12
2021
2019-12
2021-11-05
2020---

```

## Actual Input Files

**`partial.tsv`**

```tsv
partial
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"year","month","day","hour","minute","second"
"xxxx","06","15","00","00","00"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))

partial_df <- read.delim(file.path("inputs", "partial.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
partial_raw <- as.character(partial_df[[ncol(partial_df)]][1])
if (partial_raw == "test_value" || !nzchar(partial_raw)) partial_raw <- "2020-01-15"
get_partialdatetime <- get("get_partialdatetime", envir = asNamespace("admiral"))
partial <- get_partialdatetime(partial_raw, create_datetime = TRUE)
date_imputation <- "mid"
time_imputation <- "first"

get_imputation_targets <- get("get_imputation_targets", envir = asNamespace("admiral"))
result <- get_imputation_targets(partial, date_imputation = date_imputation, time_imputation = time_imputation)

dir.create("outputs", showWarnings = FALSE)
result_df <- as.data.frame(result)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)

```

## Current Prompt LLM Code

```r
library(admiral)

# ---- Setup ----
in_file  <- "inputs/partial.tsv"
out_dir  <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# ---- Safe read with validation ----
if (!file.exists(in_file)) {
  stop("Input file does not exist: ", in_file)
}

partial_df <- tryCatch(
  read.delim(in_file, header = TRUE, sep = "\t", stringsAsFactors = FALSE),
  error = function(e) {
    stop("Error reading input file: ", conditionMessage(e))
  }
)

# Basic structure checks
if (!"partial" %in% names(partial_df)) {
  stop("Input file must contain a column named 'partial'.")
}

if (!is.character(partial_df$partial)) {
  partial_df$partial <- as.character(partial_df$partial)
}

# Trim whitespace
partial_df$partial <- trimws(partial_df$partial)

# Check for empty or missing values
if (anyNA(partial_df$partial) || any(partial_df$partial == "")) {
  warning("Some partial values are NA or empty. They will be passed to admiral as-is.")
}

# ---- Build 'partial' list for get_imputation_targets ----
# admiral expects a list of partial date/time strings
partial_list <- as.list(partial_df$partial)

# ---- Get imputation targets ----
targets <- tryCatch(
  get_imputation_targets(partial = partial_list),
  error = function(e) {
    stop("Error in get_imputation_targets: ", conditionMessage(e))
  }
)

# ---- Save outputs ----
# The return is a list; save as RDS
rds_path <- file.path(out_dir, "imputation_targets.rds")
saveRDS(targets, rds_path)

# If elements are data frames, also save each as CSV for inspection
if (is.list(targets)) {
  for (nm in names(targets)) {
    obj <- targets[[nm]]
    if (is.data.frame(obj)) {
      csv_path <- file.path(out_dir, paste0("imputation_targets_", nm, ".csv"))
      tryCatch(
        {
          write.csv(obj, csv_path, row.names = FALSE)
        },
        error = function(e) {
          warning("Failed to write CSV for element '", nm, "': ", conditionMessage(e))
        }
      )
    }
  }
}

# ---- Confirm output files were written ----
if (!file.exists(rds_path)) {
  stop("RDS output file was not written: ", rds_path)
}

# Check CSVs that should exist if data frames were present
written_files <- list.files(out_dir, pattern = "^imputation_targets_.*\\.csv$", full.names = TRUE)

# Basic sanity checks for written CSVs
for (f in written_files) {
  df_check <- tryCatch(
    read.csv(f, stringsAsFactors = FALSE),
    error = function(e) {
      warning("Error re-reading CSV file '", f, "': ", conditionMessage(e))
      return(NULL)
    }
  )
  if (!is.null(df_check)) {
    # Check for obvious misalignment: all-NA columns, zero rows, etc.
    if (nrow(df_check) == 0) {
      warning("CSV file '", f, "' has zero rows; check upstream data and parsing.")
    }
    if (all(vapply(df_check, function(x) all(is.na(x)), logical(1)))) {
      warning("CSV file '", f, "' has all columns NA; possible parsing or imputation issue.")
    }
  }
}

# Optional quick inspection for unexpected patterns in the main result
# (e.g., all missing imputation targets)
if (is.list(targets) && length(targets) > 0) {
  all_null <- all(vapply(targets, is.null, logical(1)))
  if (all_null) {
    warning("All elements of 'targets' are NULL; check input partial values and admiral configuration.")
  }
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
Error in value[[3L]](cond) : 
  Error in get_imputation_targets: could not find function "get_imputation_targets"
Calls: tryCatch -> tryCatchList -> tryCatchOne -> <Anonymous>
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

library(readr)
library(dplyr)
library(stringr)
library(tidyr)
library(purrr)

#--------------------------------------------------------------------
# Helper: determine imputation target(s) for a single partial date
#--------------------------------------------------------------------
get_targets_for_partial <- function(x) {
  x <- str_trim(x)

  # Remove any trailing non-digit characters
  x_clean <- str_replace(x, "[^0-9]+$", "")

  # Completely missing or empty
  if (x_clean == "" || is.na(x_clean)) {
    return(tibble(
      original = x,
      target_start = NA_character_,
      target_end   = NA_character_
    ))
  }

  # Year only: "YYYY"
  if (str_detect(x_clean, "^\\d{4}$")) {
    yr <- x_clean
    return(tibble(
      original = x,
      target_start = paste0(yr, "-01-01"),
      target_end   = paste0(yr, "-12-31")
    ))
  }

  # Year-month: "YYYY-MM"
  if (str_detect(x_clean, "^\\d{4}-\\d{2}$")) {
    yr <- str_sub(x_clean, 1, 4)
    mo <- str_sub(x_clean, 6, 7)
    # Validate month
    if (!mo %in% sprintf("%02d", 1:12)) {
      return(tibble(
        original = x,
        target_start = NA_character_,
        target_end   = NA_character_
      ))
    }
    # Last day of month
    first_day <- as.Date(paste0(yr, "-", mo, "-01"))
    last_day  <- as.Date(format(first_day + months(1) - 1, "%Y-%m-%d"))

    return(tibble(
      original = x,
      target_start = format(first_day, "%Y-%m-%d"),
      target_end   = format(last_day,  "%Y-%m-%d")
    ))
  }

  # Full date: "YYYY-MM-DD"
  if (str_detect(x_clean, "^\\d{4}-\\d{2}-\\d{2}$")) {
    dt <- suppressWarnings(as.Date(x_clean))
    if (is.na(dt)) {
      return(tibble(
        original = x,
        target_start = NA_character_,
        target_end   = NA_character_
      ))
    }
    return(tibble(
      original = x,
      target_start = format(dt, "%Y-%m-%d"),
      target_end   = format(dt, "%Y-%m-%d")
    ))
  }

  # Fallback: unhandled pattern
  tibble(
    original = x,
    target_start = NA_character_,
    target_end   = NA_character_
  )
}

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------

infile  <- file.path("inputs", "partial.tsv")
outfile <- file.path("outputs", "result.csv")

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

raw <- read_tsv(infile, col_types = cols(.default = "c"))

# Assume the first column contains the partial date values
col_name <- names(raw)[1]

res <- raw %>%
  transmute(!!col_name := .data[[col_name]]) %>%
  mutate(row_id = row_number()) %>%
  mutate(tmp = map(.data[[col_name]], get_targets_for_partial)) %>%
  unnest(cols = tmp) %>%
  select(-original) %>%
  rename(
    partial = !!col_name
  ) %>%
  select(row_id, partial, target_start, target_end)

write_csv(res, outfile)
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
row_id,partial,target_start,target_end
1,2019-12,2019-12-01,2019-12-31
2,2021,2021-01-01,2021-12-31
3,2019-12,2019-12-01,2019-12-31
4,2021-11-05,2021-11-05,2021-11-05
5,2020---,2020-01-01,2020-12-31

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiral/get_imputation_targets",
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
  "task_id": "pharmaverse/admiral/get_imputation_targets",
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
      "reason": "Shape mismatch: ref=(1, 6) vs llm=(5, 4)"
    }
  },
  "normalizations": []
}
```
