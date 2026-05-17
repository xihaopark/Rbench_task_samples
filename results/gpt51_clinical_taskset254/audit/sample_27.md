# Sample 27: pharmaverse/admiraldiscovery/admiral_pkg_versions

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiraldiscovery/admiral_pkg_versions`
- package/function: `admiraldiscovery` / `admiral_pkg_versions`
- expected_artifacts: `outputs/result.csv, outputs/summary.csv`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Return installed **admiral** package versions. Load `library(admiraldiscovery)`.

**Computation:** **`admiraldiscovery::admiral_pkg_versions()`**; serialize like the long template in `solution.R`.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Prompt
```text
Write R code to report package versions using admiraldiscovery. At the beginning, load the required packages: library(admiraldiscovery). The input data files are stored in inputs/ directory. Function returns a string listing the packages and their versions. Use admiraldiscovery's admiral_pkg_versions function. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### admiraldiscovery.tsv (38 bytes)
admiraldiscovery
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform admiral pkg versions using the admiraldiscovery clinical task contract.

Input: admiraldiscovery.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### admiraldiscovery.tsv (38 bytes)
admiraldiscovery
AVAL
AVISITN
USUBJID

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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(3, 5) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(admiraldiscovery))

# 1. 读取输入数据 / Read input data
# No input files required

# 3. 执行函数实现 / Execute function implementation
result <- admiraldiscovery::admiral_pkg_versions()

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

## Current Solution
```r
#!/usr/bin/env Rscript

# Load required package(s)
suppressPackageStartupMessages({
  library(admiraldiscovery)
})

# Create I/O directories if needed
input_dir  <- "inputs"
output_dir <- "outputs"

if (!dir.exists(input_dir)) {
  stop("Input directory 'inputs/' does not exist.")
}
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
}

# Helper: safe write for data.frame -> CSV
safe_write_csv <- function(x, file) {
  tryCatch(
    {
      utils::write.csv(x, file = file, row.names = FALSE)
      TRUE
    },
    error = function(e) {
      message("Error writing CSV to ", file, ": ", conditionMessage(e))
      FALSE
    }
  )
}

# Helper: safe write for any R object -> RDS
safe_write_rds <- function(x, file) {
  tryCatch(
    {
      saveRDS(x, file = file)
      TRUE
    },
    error = function(e) {
      message("Error writing RDS to ", file, ": ", conditionMessage(e))
      FALSE
    }
  )
}

# Helper: basic validation / diagnostics for data.frames
validate_df <- function(df, name = "object") {
  if (!is.data.frame(df)) return(invisible(NULL))

  # Check for duplicated rows
  dup_rows <- any(duplicated(df))
  if (dup_rows) {
    warning("Data frame '", name, "' contains duplicated rows.")
  }

  # Check for all-NA columns
  na_cols <- vapply(df, function(col) all(is.na(col)), logical(1))
  if (any(na_cols)) {
    warning(
      "Data frame '", name, "' contains all-NA columns: ",
      paste(names(df)[na_cols], collapse = ", ")
    )
  }

  # Check for zero-row or zero-column
  if (nrow(df) == 0L) {
    warning("Data frame '", name, "' has 0 rows.")
  }
  if (ncol(df) == 0L) {
    warning("Data frame '", name, "' has 0 columns.")
  }

  invisible(NULL)
}

# Main wrapper with error handling
run_version_report <- function() {
  res <- tryCatch(
    {
      admiraldiscovery::admiral_pkg_versions()
    },
    error = function(e) {
      stop("Error calling admiral_pkg_versions(): ", conditionMessage(e))
    }
  )

  # Determine output format and path
  out_file <- NULL
  write_ok <- FALSE

  if (is.data.frame(res)) {
    out_file <- file.path(output_dir, "admiral_pkg_versions.csv")
    validate_df(res, name = "admiral_pkg_versions")
    write_ok <- safe_write_csv(res, out_file)
  } else {
    out_file <- file.path(output_dir, "admiral_pkg_versions.rds")
    write_ok <- safe_write_rds(res, out_file)
  }

  if (!write_ok) {
    stop("Failed to write package version output to disk.")
  }

  # Confirm file written & readable
  if (!file.exists(out_file)) {
    stop("Output file not found after write attempt: ", out_file)
  }

  reloaded <- tryCatch(
    {
      if (is.data.frame(res)) {
        utils::read.csv(out_file, stringsAsFactors = FALSE)
      } else {
        readRDS(out_file)
      }
    },
    error = function(e) {
      stop("Error re-reading output file: ", conditionMessage(e))
    }
  )

  # Basic cross-check for unexpected patterns / misalignment
  if (is.data.frame(res) && is.data.frame(reloaded)) {
    if (!identical(names(res), names(reloaded))) {
      warning(
        "Column names changed after round-trip I/O. ",
        "Original: ", paste(names(res), collapse = ", "),
        " | Reloaded: ", paste(names(reloaded), collapse = ", ")
      )
    }
  }

  # Construct and return string listing packages and versions
  pkg_str <- tryCatch(
    {
      if (is.data.frame(res)) {
        required_cols <- c("package", "version")
        if (!all(required_cols %in% names(res))) {
          warning(
            "Expected columns 'package' and 'version' not both present; ",
            "returning deparsed object instead."
          )
          paste(capture.output(str(res)), collapse = "\n")
        } else {
          paste(sprintf("%s: %s", res$package, res$version), collapse = "; ")
        }
      } else {
        # Fallback for non-data.frame objects
        paste(capture.output(str(res)), collapse = "\n")
      }
    },
    error = function(e) {
      warning("Error constructing package/version string: ", conditionMessage(e))
      paste(capture.output(str(res)), collapse = "\n")
    }
  )

  pkg_str
}

# Execute and (optionally) print the returned string
pkg_version_string <- run_version_report()
pkg_version_string
```

## Simple Solution
```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(purrr)
})

# Paths
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read task contract (list of variable names)
contract_path <- file.path(in_dir, "admiraldiscovery.tsv")
vars <- read_tsv(
  contract_path,
  col_names = FALSE,
  show_col_types = FALSE
) %>% 
  pull(X1)

# Identify core dataset type from contract
core_vars <- toupper(vars)
is_adae <- any(core_vars %in% c("AEDECOD", "AETERM", "AESTDTC", "AESTDY"))
is_adsl <- any(core_vars %in% c("USUBJID", "TRT01A", "TRT01P", "AGE"))
is_adrs <- any(core_vars %in% c("PARAMCD", "AVALC", "AVAL", "AVISITN"))
is_adqs <- any(core_vars %in% c("QSTESTCD", "QSTEST", "AVAL", "AVISITN"))

dataset_type <- dplyr::case_when(
  is_adae ~ "ADAE",
  is_adrs ~ "ADRS",
  is_adqs ~ "ADQS",
  is_adsl ~ "ADSL",
  TRUE    ~ "UNKNOWN"
)

# Map dataset type to admiral/admiralxxx minimal version expectations
# (versions here are examples and can be adjusted to current recommendations)
admiral_core <- tibble::tribble(
  ~pkg,             ~min_version,
  "admiral",        "0.14.0",
  "admiraldev",     "0.3.0"
)

type_specific <- switch(
  dataset_type,
  "ADAE" = tibble::tribble(
    ~pkg,               ~min_version,
    "admiral",          "0.14.0",
    "admiraldev",       "0.3.0"
  ),
  "ADRS" = tibble::tribble(
    ~pkg,               ~min_version,
    "admiral",          "0.14.0",
    "admiralonco",      "0.5.0",
    "admiraldev",       "0.3.0"
  ),
  "ADQS" = tibble::tribble(
    ~pkg,               ~min_version,
    "admiral",          "0.14.0",
    "admiralophtha",    "0.2.0",
    "admiraldev",       "0.3.0"
  ),
  "ADSL" = tibble::tribble(
    ~pkg,               ~min_version,
    "admiral",          "0.14.0",
    "admiraldev",       "0.3.0"
  ),
  tibble::tribble(
    ~pkg,               ~min_version,
    "admiral",          "0.14.0",
    "admiraldev",       "0.3.0"
  )
)

required_pkgs <- bind_rows(admiral_core, type_specific) %>%
  distinct(pkg, .keep_all = TRUE)

# Helper: get installed version or NA
get_installed_version <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) return(NA_character_)
  as.character(utils::packageVersion(pkg))
}

installed <- required_pkgs %>%
  mutate(installed_version = map_chr(pkg, get_installed_version))

# Compare installed vs required
compare_version_safe <- function(installed, required) {
  if (is.na(installed)) return("NOT INSTALLED")
  if (utils::compareVersion(installed, required) < 0) return("OUTDATED")
  "OK"
}

result <- installed %>%
  mutate(
    status = purrr::map2_chr(installed_version, min_version, compare_version_safe),
    dataset_type = dataset_type
  ) %>%
  select(dataset_type, package = pkg, required_version = min_version,
         installed_version, status)

# Write result
out_path <- file.path(out_dir, "result.csv")
write_csv(result, out_path, na = "")

```

## Current Candidate Prompt File
```text
Write R code to report package versions using admiraldiscovery. At the beginning, load the required packages: library(admiraldiscovery). The input data files are stored in inputs/ directory. Function returns a string listing the packages and their versions. Use admiraldiscovery's admiral_pkg_versions function. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to report package versions using admiraldiscovery. At the beginning, load the required packages: library(admiraldiscovery). The input data files are stored in inputs/ directory. Function returns a string listing the packages and their versions. Use admiraldiscovery's admiral_pkg_versions function. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```