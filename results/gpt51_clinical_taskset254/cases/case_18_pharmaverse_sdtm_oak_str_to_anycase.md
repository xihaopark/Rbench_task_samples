# Case 18 - `pharmaverse/sdtm.oak/str_to_anycase`

**Package:** `sdtm.oak`  **Function:** `str_to_anycase`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `llm_wrong`  **Confidence:** `high`

## Audit Evidence

Prompt/reference/data align on `str_to_anycase`; current solution writes `outputs/x_anycase_regexps.csv` instead of `outputs/result.csv`, while simple computes a case conversion rather than reference regex strings.

## Task Prompt From `task.json`

```text
Write R code to implement the **Str to anycase** workflow using the `sdtm.oak` package.
At the beginning, load required packages: library(sdtm.oak).

**Inputs:**
- `inputs/x.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'x.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Str To Anycase** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
Write R code to generate case insensitive regexps using sdtm.oak. At the beginning, load the required packages: library(sdtm.oak). The input data file is stored in inputs/x.tsv. [str_to_anycase()] takes a character vector of word strings as input, and generates regular expressions that express that match in any case. Use sdtm.oak's str_to_anycase function with the following parameters: x (A character vector of strings consisting of word characters.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: s A character vector.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

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
Create R script to perform str to anycase using the sdtm.oak clinical task contract.

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
"item1"
"item2"
"item3"
"item4"
"item5"

```

## Reference Output Files

**`result.csv`**

```csv
"x","result.c..i....t....e....m....1..","result.c..i....t....e....m....2..","result.c..i....t....e....m....3..","result.c..i....t....e....m....4..","result.c..i....t....e....m....5.."
"item1","i","i","i","i","i"
"item2","t","t","t","t","t"
"item3","e","e","e","e","e"
"item4","m","m","m","m","m"
"item5","1","2","3","4","5"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,6,"x, result.c..i....t....e....m....1.., result.c..i....t....e....m....2.., result.c..i....t....e....m....3.., result.c..i....t....e....m....4.., result.c..i....t....e....m....5.."

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(sdtm.oak))
suppressPackageStartupMessages(library(purrr))


# 1. 读取输入数据 / Read input data
x_path <- file.path("inputs", "x.tsv")
if (!file.exists(x_path)) {
  stop("x.tsv is required input")
}
x_df <- read.delim(x_path, check.names = FALSE, stringsAsFactors = FALSE)
x <- x_df$x

# 2. 执行函数实现 / Execute function implementation
lst <- stringr::str_split(x, stringr::boundary("character"))
  purrr::map(lst, ~ stringr::str_c(stringr::str_to_upper(.x), stringr::str_to_lower(.x))) |>
    purrr::map(~ sprintf("[%s]", .x)) |>
    purrr::map(~ stringr::str_flatten(.x)) |>
    unlist()
result <- lst

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    x = x,
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
#!/usr/bin/env Rscript

## Load required packages
suppressPackageStartupMessages({
  library(sdtm.oak)
  library(readr)
  library(dplyr)
  library(stringr)
})

## Helper: safe stop with message
fail <- function(msg) {
  message("ERROR: ", msg)
  quit(status = 1, save = "no")
}

## Paths
in_file  <- "inputs/x.tsv"
out_file <- "outputs/x_anycase_regexps.csv"

## Validate input file existence
if (!file.exists(in_file)) {
  fail(paste0("Input file not found: ", in_file))
}

## Read input (TSV with a header 'x')
dat <- tryCatch(
  {
    read_tsv(
      in_file,
      col_types = cols(.default = col_character()),
      progress  = FALSE,
      trim_ws   = TRUE
    )
  },
  error = function(e) fail(paste("Failed to read input file:", conditionMessage(e)))
)

## Basic validation
if (!"x" %in% names(dat)) {
  fail("Input file must contain a column named 'x'.")
}

## Drop completely empty rows in x
dat <- dat %>%
  mutate(x = str_trim(x)) %>%
  filter(!is.na(x), x != "")

if (nrow(dat) == 0) {
  fail("No non-empty values found in column 'x'.")
}

## Ensure x consists only of word characters (\\w = [A-Za-z0-9_])
bad_rows <- which(!str_detect(dat$x, "^[[:alnum:]_]+$"))
if (length(bad_rows) > 0) {
  msg <- paste0(
    "Values in column 'x' must consist only of word characters ([A-Za-z0-9_]). ",
    "Invalid rows: ", paste(bad_rows, collapse = ", ")
  )
  fail(msg)
}

## Generate case-insensitive regexps using str_to_anycase()
regex_vec <- tryCatch(
  {
    str_to_anycase(dat$x)
  },
  error = function(e) fail(paste("str_to_anycase() failed:", conditionMessage(e)))
)

## Validate output from str_to_anycase()
if (!is.character(regex_vec)) {
  fail("Output from str_to_anycase() is not a character vector as expected.")
}
if (length(regex_vec) != nrow(dat)) {
  fail("Length of output from str_to_anycase() does not match number of input rows.")
}

## Combine with original data
out_dat <- dat %>%
  mutate(anycase_regexp = regex_vec)

## Create outputs directory if needed
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
}

## Write output as CSV
tryCatch(
  {
    write_csv(out_dat, out_file, na = "")
  },
  error = function(e) fail(paste("Failed to write output CSV:", conditionMessage(e)))
)

## Confirm the output was written
if (!file.exists(out_file)) {
  fail(paste0("Output file was not created: ", out_file))
}

## Re-read output to confirm integrity and check for obvious issues
check_dat <- tryCatch(
  {
    read_csv(out_file, col_types = cols(.default = col_character()), progress = FALSE)
  },
  error = function(e) fail(paste("Failed to re-read output CSV:", conditionMessage(e)))
)

## Basic consistency checks
if (!all(c("x", "anycase_regexp") %in% names(check_dat))) {
  fail("Output CSV is missing expected columns 'x' and/or 'anycase_regexp'.")
}

if (nrow(check_dat) != nrow(out_dat)) {
  fail("Row count mismatch between written and re-read output data.")
}

## Check for unexpected obvious parsing issues (e.g., NA in regex where not expected)
if (any(is.na(check_dat$anycase_regexp))) {
  fail("Detected NA values in 'anycase_regexp' after re-reading output, indicating possible parsing issues.")
}

## Optional lightweight sanity check: no empty regex
if (any(check_dat$anycase_regexp == "")) {
  fail("Detected empty strings in 'anycase_regexp', which may indicate a processing error.")
}

message("Output file written and verified: ", out_file)
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
ERROR: str_to_anycase() failed: could not find function "str_to_anycase"

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

_No files found._

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Paths
infile  <- file.path("inputs", "x.tsv")
outfile <- file.path("outputs", "result.csv")

# Read input
x_df <- read_tsv(infile, col_types = cols(.default = "c"))

# Detect and convert from any case to SDTM OAK-style case:
# - All upper or mixed → PascalCase
# - If contains underscore → lower_snake_case
to_anycase_sdtm_oak <- function(x) {
  x <- trimws(x)
  if (x == "") return(x)
  
  # If name has underscores, convert to lower_snake_case
  if (str_detect(x, "_")) {
    parts <- str_split(x, "_", simplify = TRUE)
    parts <- tolower(parts)
    return(paste(parts, collapse = "_"))
  }
  
  # Otherwise convert to PascalCase (UpperCamelCase)
  x_low <- tolower(x)
  # Split on transitions or non-letters
  parts <- str_split(x_low, "[^A-Za-z0-9]+", simplify = TRUE)
  parts <- parts[parts != ""]
  parts <- str_to_title(parts)
  paste(parts, collapse = "")
}

x_df$result <- vapply(x_df[[1]], to_anycase_sdtm_oak, character(1))

# Write output
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write_csv(x_df["result"], outfile)
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

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
result
Sysbp
Diabp
Pulse
Weight
Height

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/sdtm.oak/str_to_anycase",
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
  "task_id": "pharmaverse/sdtm.oak/str_to_anycase",
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
      "tier": "schema_ok",
      "reason": "Value mismatch in column: result"
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
