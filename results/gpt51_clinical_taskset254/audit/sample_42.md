# Sample 42: pharmaverse/admiral/assert_valid_queries

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiral/assert_valid_queries`
- package/function: `admiral` / `assert_valid_queries`
- expected_artifacts: `outputs/result.csv`
- current_status: `TIMEOUT` tier=`exec_fail`
- simple_status: `NO_OUTPUT` tier=`exec_fail`

## Reference Prompt
```text
Write R code to implement the **Assert valid queries** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/queries.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'queries.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/queries_name.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'queries_name.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Assert Valid Queries** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
Write R code to verify if a dataset has the required format as queries dataset. using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/queries.tsv, inputs/queries_name.tsv). Additional details: - `PREFIX`, e.g., SMQ01, CQ12 - `GRPNAME`, non NA, must be unique per each `PREFIX` - `GRPID`, could be NA, must be unique per each `PREFIX` - `SCOPE`, 'BROAD', 'NARROW', or NA - `SCOPEN`, 1, 2, or NA - `SRCVAR`, e.g., `"AEDECOD"`, `"AELLT"`, `"AELLTCD"`, ... - `TERMCHAR`, character, could be NA only at those observations where `TERMNUM` is non-NA - `TERMNUM`, integer, could be NA only at those observations where `TERMCHAR` is non-NA Use admiral's assert_valid_queries function with the following parameters: queries (A data.frame.), queries_name (Name of the queries dataset, a string.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error if any of the requirements not met.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### queries.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

### queries_name.tsv (34 bytes)
queries_name
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform assert valid queries using the admiral clinical task contract.

Input: queries.tsv, queries_name.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### queries.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

### queries_name.tsv (34 bytes)
queries_name
AVAL
AVISITN
USUBJID

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

suppressPackageStartupMessages(library(cli))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(rlang))
suppressPackageStartupMessages(library(stringr))

# 1. 读取输入数据 / Read input data
queries_path <- file.path("inputs", "queries.tsv")
if (!file.exists(queries_path)) {
  stop("queries.tsv is required input")
}
queries <- read.delim(queries_path, check.names = FALSE, stringsAsFactors = FALSE)
queries_name_path <- file.path("inputs", "queries_name.tsv")
if (!file.exists(queries_name_path)) {
  stop("queries_name.tsv is required input")
}
queries_name_df <- read.delim(queries_name_path, check.names = FALSE, stringsAsFactors = FALSE)
queries_name <- as.character(queries_name_df[[1]][1])

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
if (nrow(queries) == 0) stop("queries is empty")
if (ncol(queries) == 0) stop("queries has no columns")

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  if ("PREFIX" %in% names(queries)) {
    signal_duplicate_records(queries, by_vars = exprs(!!!syms(colnames(queries))))
  }
  queries
}, error = function(e) queries)

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    queries_name = queries_name,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# 5. 生成汇总统计 / Generate summary statistics
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

# 6. 保存输出 / Save outputs
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
    saveRDS(result, file.path(outputs_dir, "result.rd
```

## Current Solution
```r
library(admiral)

# Create output directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#---------------------------
# Helper: safe read TSV
#---------------------------
safe_read_tsv <- function(path) {
  if (!file.exists(path)) {
    stop(sprintf("Input file not found: %s", path))
  }
  df <- tryCatch(
    read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE),
    error = function(e) stop(sprintf("Failed to read %s: %s", path, e$message))
  )
  if (nrow(df) == 0L) {
    warning(sprintf("Input file %s has 0 rows.", path))
  }
  df
}

#---------------------------
# Read inputs
#---------------------------
queries_raw       <- safe_read_tsv("inputs/queries.tsv")
queries_name_raw  <- safe_read_tsv("inputs/queries_name.tsv")

#---------------------------
# Derive queries_name
#---------------------------
# Expect a single-column, single-row dataset, or first non-header cell as name
# Fallback: use first non-NA value excluding the column header
qn_vals <- unlist(queries_name_raw, use.names = FALSE)
qn_vals <- qn_vals[!is.na(qn_vals)]
if (length(qn_vals) < 2L) {
  stop("queries_name.tsv does not contain enough data to derive a queries_name string.")
}
# First element is assumed to be the column header; use the second
queries_name <- as.character(qn_vals[2L])

if (!nzchar(queries_name)) {
  stop("Derived queries_name is empty. Check inputs/queries_name.tsv.")
}

#---------------------------
# Coerce and validate columns in queries
#---------------------------

# Ensure required columns exist
required_cols <- c(
  "PREFIX", "GRPNAME", "GRPID", "SCOPE", "SCOPEN",
  "SRCVAR", "TERMCHAR", "TERMNUM"
)
missing_cols <- setdiff(required_cols, names(queries_raw))
if (length(missing_cols) > 0L) {
  stop(sprintf(
    "Missing required columns in queries dataset: %s",
    paste(missing_cols, collapse = ", ")
  ))
}

queries <- queries_raw

# Basic type coercions
queries$PREFIX   <- as.character(queries$PREFIX)
queries$GRPNAME  <- as.character(queries$GRPNAME)
queries$GRPID    <- as.character(queries$GRPID)
queries$SCOPE    <- ifelse(is.na(queries$SCOPE), NA_character_, toupper(as.character(queries$SCOPE)))
queries$SCOPEN   <- ifelse(is.na(queries$SCOPEN), NA_integer_, as.integer(queries$SCOPEN))
queries$SRCVAR   <- as.character(queries$SRCVAR)
queries$TERMCHAR <- as.character(queries$TERMCHAR)
queries$TERMNUM  <- ifelse(is.na(queries$TERMNUM), NA_integer_, as.integer(queries$TERMNUM))

#---------------------------
# Custom checks per spec
#---------------------------

# 1) PREFIX not NA
if (any(is.na(queries$PREFIX))) {
  stop("PREFIX contains NA values.")
}

# 2) GRPNAME: non-NA, unique per PREFIX
if (any(is.na(queries$GRPNAME))) {
  stop("GRPNAME contains NA values.")
}
dup_grpname <- queries[duplicated(queries[c("PREFIX", "GRPNAME")]), c("PREFIX", "GRPNAME")]
if (nrow(dup_grpname) > 0L) {
  stop("GRPNAME is not unique within PREFIX. Examples:\n",
       paste(utils::capture.output(print(head(unique(dup_grpname), 10))), collapse = "\n"))
}

# 3) GRPID: could be NA, but if not NA must be unique per PREFIX
non_na_grpid <- queries[!is.na(queries$GRPID), ]
dup_grpid <- non_na_grpid[duplicated(non_na_grpid[c("PREFIX", "GRPID")]), c("PREFIX", "GRPID")]
if (nrow(dup_grpid) > 0L) {
  stop("Non-NA GRPID is not unique within PREFIX. Examples:\n",
       paste(utils::capture.output(print(head(unique(dup_grpid), 10))), collapse = "\n"))
}

# 4) SCOPE: 'BROAD', 'NARROW', or NA
allowed_scope <- c("BROAD", "NARROW")
bad_scope <- !is.na(queries$SCOPE) & !(queries$SCOPE %in% allowed_scope)
if (any(bad_scope)) {
  stop("SCOPE contains invalid values. Allowed: 'BROAD', 'NARROW', or NA.")
}

# 5) SCOPEN: 1, 2, or NA
allowed_scopen <- c(1L, 2L)
bad_scopen <- !is.na(queries$SCOPEN) & !(queries$SCOPEN %in% allowed_scopen)
if (any(bad_scopen)) {
  stop("SCOPEN contains invalid values. Allowed: 1, 2, or NA.")
}

# 6) TERMCHAR / TERMNUM mutual-NA rule:
# TERMCHAR may be NA only where TERMNUM is non-NA
# TERMNUM may be NA only where TERMCHAR is non-NA
viol_char <- is.na(queries$TERMCHAR) & is.na(queries$TERMNUM)
viol_num  <- !is.na(queries$TERMCHAR) & !is.na(queries$TERMNUM)
if (any(viol_char) || any(viol_num)) {
  stop("TERMCHAR and TERMNUM must be mutually exclusive NAs: exactly one of them should be NA in each row.")
}

#---------------------------
# Use admiral::assert_valid_queries
#---------------------------
res <- tryCatch(
  {
    admiral::assert_valid_queries(
      queries      = queries,
      queries_name = queries_name
    )
  },
  error = function(e) {
    stop(sprintf("assert_valid_queries failed: %s", e$message))
  }
)

#---------------------------
# Save outputs
#---------------------------

# Save queries (data frame) as CSV
queries_out_path <- file.path("outputs", paste0(queries_name, "_queries.csv"))
tryCatch(
  {
    utils::write.csv(queries, file = queries_out_path, row.names = FALSE, na = "")
  },
  error = function(e) {
    stop(sprintf("Faile
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(admiral)

# Inputs
queries_path      <- file.path("inputs", "queries.tsv")
queries_name_path <- file.path("inputs", "queries_name.tsv")

# Outputs
output_path <- file.path("outputs", "result.csv")

# Read input files
queries <- read_tsv(queries_path, show_col_types = FALSE)
queries_name <- read_tsv(queries_name_path, show_col_types = FALSE)

# Perform assert-valid-queries using admiral clinical task contract
# Map queries and queries_name to the contract input structure
# (contract expects named lists of vectors or data frames)
input_list <- list(
  queries      = queries,
  queries_name = queries_name
)

# Run contract (assuming exported function `run_clinical_task_contract`
# and contract id "assert_valid_queries")
result <- admiral::run_clinical_task_contract(
  contract_id = "assert_valid_queries",
  input       = input_list
)

# Ensure result is a data frame for writing
if (!is.data.frame(result)) {
  result <- as.data.frame(result)
}

# Create outputs dir if needed
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Write result
write_csv(result, output_path)
```

## Current Candidate Prompt File
```text
Write R code to verify if a dataset has the required format as queries dataset. using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/queries.tsv, inputs/queries_name.tsv). Additional details: - `PREFIX`, e.g., SMQ01, CQ12 - `GRPNAME`, non NA, must be unique per each `PREFIX` - `GRPID`, could be NA, must be unique per each `PREFIX` - `SCOPE`, 'BROAD', 'NARROW', or NA - `SCOPEN`, 1, 2, or NA - `SRCVAR`, e.g., `"AEDECOD"`, `"AELLT"`, `"AELLTCD"`, ... - `TERMCHAR`, character, could be NA only at those observations where `TERMNUM` is non-NA - `TERMNUM`, integer, could be NA only at those observations where `TERMCHAR` is non-NA Use admiral's assert_valid_queries function with the following parameters: queries (A data.frame.), queries_name (Name of the queries dataset, a string.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error if any of the requirements not met.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to verify if a dataset has the required format as queries dataset. using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/queries.tsv, inputs/queries_name.tsv). Additional details: - `PREFIX`, e.g., SMQ01, CQ12 - `GRPNAME`, non NA, must be unique per each `PREFIX` - `GRPID`, could be NA, must be unique per each `PREFIX` - `SCOPE`, 'BROAD', 'NARROW', or NA - `SCOPEN`, 1, 2, or NA - `SRCVAR`, e.g., `"AEDECOD"`, `"AELLT"`, `"AELLTCD"`, ... - `TERMCHAR`, character, could be NA only at those observations where `TERMNUM` is non-NA - `TERMNUM`, integer, could be NA only at those observations where `TERMCHAR` is non-NA Use admiral's assert_valid_queries function with the following parameters: queries (A data.frame.), queries_name (Name of the queries dataset, a string.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error if any of the requirements not met.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```