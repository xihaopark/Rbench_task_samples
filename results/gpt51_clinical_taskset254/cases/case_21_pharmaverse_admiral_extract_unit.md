# Case 21 - `pharmaverse/admiral/extract_unit`

**Package:** `admiral`  **Function:** `extract_unit`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `TIMEOUT` / tier `exec_fail`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `llm_wrong`  **Confidence:** `Medium`

## Audit Evidence

Reference asks `admiral::extract_unit(x)` and `outputs/result.csv`; current code writes `outputs/x_unit.csv`, while simple code invents ADaM unit mappings and gets `Shape mismatch: ref=(1, 2) vs llm=(5, 2)`.

## Task Prompt From `task.json`

```text
Extract **unit text** from strings like `"10 (mg)"`. Load `library(admiral)`.

**Inputs:** `inputs/x.tsv`.

**Computation:** **`admiral::extract_unit(x)`** on the character vector.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.

```

## Current Generated Prompt

```text
Write R code to extract unit from parameter description using admiral. At the beginning, load the required packages: library(admiral). The input data file is stored in inputs/x.tsv. Extract the unit of a parameter from a description like "Param (unit)". Use admiral's extract_unit function with the following parameters: x (A parameter description). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: A string. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### x.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Simple Generated Prompt

```text
Create R script to perform extract unit using the admiral clinical task contract.

Input: x.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### x.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

```

## Actual Input Files

**`x.tsv`**

```tsv
x
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"x","result"
"test_value",NA

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(stringr))

x_df <- read.delim(file.path("inputs", "x.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
x <- as.character(x_df[[ncol(x_df)]])
if (length(x) == 0) x <- "10 (mg)"

result <- admiral::extract_unit(x)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(x = x, result = result), file.path("outputs", "result.csv"), row.names = FALSE)

```

## Current Prompt LLM Code

```r
library(admiral)

# Error handling helper
stop_if_not_file <- function(path) {
  if (!file.exists(path)) {
    stop(paste("Input file does not exist:", path))
  }
}

# Paths
in_path <- "inputs/x.tsv"
out_path <- "outputs/x_unit.csv"
log_path <- "outputs/x_unit_check.txt"

# Ensure input exists
stop_if_not_file(in_path)

# Read input
x_df <- tryCatch(
  read.delim(in_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) {
    stop("Error reading input file: ", conditionMessage(e))
  }
)

# Basic validation
if (!"x" %in% names(x_df)) {
  stop("Input data must contain a column named 'x'.")
}

if (anyNA(x_df$x)) {
  warning("Missing values detected in column 'x'.")
}

# Apply extract_unit to each parameter description
x_df$unit <- vapply(
  x_df$x,
  function(z) {
    # Ensure character input
    z_chr <- if (is.na(z)) "" else as.character(z)
    # Use admiral extract_unit
    out <- tryCatch(
      extract_unit(z_chr),
      error = function(e) {
        NA_character_
      }
    )
    out
  },
  character(1)
)

# Write output as CSV
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

tryCatch(
  {
    write.csv(x_df, out_path, row.names = FALSE, na = "")
  },
  error = function(e) {
    stop("Error writing CSV output: ", conditionMessage(e))
  }
)

# Basic post-write checks and pattern diagnostics
checks <- list()

checks$file_exists <- file.exists(out_path)
if (!checks$file_exists) {
  stop("Output file was not written: ", out_path)
}

# Reload written file to confirm integrity
x_df_out <- tryCatch(
  read.csv(out_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) {
    stop("Error re-reading output file: ", conditionMessage(e))
  }
)

# Check for data misalignment: same number of rows and key column equality
checks$nrow_match <- nrow(x_df_out) == nrow(x_df)
checks$x_identical <- identical(as.character(x_df_out$x), as.character(x_df$x))

# Check for unexpected patterns in units
checks$all_na_units <- all(is.na(x_df_out$unit) | x_df_out$unit == "")
checks$any_parentheses_in_x <- any(grepl("\\(", x_df_out$x))

summary_lines <- c(
  paste("Output file exists:", checks$file_exists),
  paste("Row count matches input:", checks$nrow_match),
  paste("Column 'x' identical to input:", checks$x_identical),
  paste("All units missing/empty:", checks$all_na_units),
  paste("Any '(' present in x (expected for 'Param (unit)' patterns):",
        checks$any_parentheses_in_x)
)

# Write diagnostics log
tryCatch(
  {
    writeLines(summary_lines, con = log_path)
  },
  error = function(e) {
    warning("Could not write diagnostics log: ", conditionMessage(e))
  }
)
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

```

## Current Prompt Output Files

**`x_unit.csv`**

```csv
"x","unit"
"SYSBP",
"DIABP",
"PULSE",
"WEIGHT",
"HEIGHT",

```

**`x_unit_check.txt`**

```text
Output file exists: TRUE
Row count matches input: TRUE
Column 'x' identical to input: TRUE
All units missing/empty: TRUE
Any '(' present in x (expected for 'Param (unit)' patterns): FALSE

```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(admiral)

# Input / output paths
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read input
x_path <- file.path(in_dir, "x.tsv")
vars <- read_tsv(x_path, show_col_types = FALSE)[[1]]

# Create units based on typical ADaM conventions (example mapping)
unit_map <- tibble::tribble(
  ~PARAMCD, ~UNIT,
  "SYSBP",  "mmHg",
  "DIABP",  "mmHg",
  "PULSE",  "beats/min",
  "WEIGHT", "kg",
  "HEIGHT", "cm"
)

result <- unit_map %>%
  filter(PARAMCD %in% vars) %>%
  arrange(PARAMCD)

# Write output
out_path <- file.path(out_dir, "result.csv")
write_csv(result, out_path)
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
PARAMCD,UNIT
DIABP,mmHg
HEIGHT,cm
PULSE,beats/min
SYSBP,mmHg
WEIGHT,kg

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiral/extract_unit",
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
  "task_id": "pharmaverse/admiral/extract_unit",
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
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(5, 2)"
    }
  },
  "normalizations": []
}
```
