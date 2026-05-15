# Case 06 - `pharmaverse/admiral/compute_age_years`
**Package:** `admiral`  **Function:** `compute_age_years`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to convert age to **years** for ADaM. Load `library(admiral)`.

**Inputs:** `inputs/age.tsv`, `inputs/age_unit.tsv` — numeric age and a unit string (`years`, `months`, `weeks`, `days`, `hours`, `minutes`, `seconds`); invalid units fall back to `years` in the reference.

**Computation:** **`admiral::compute_age_years(age, age_unit)`** — public API.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
```

## Input Files

**`inputs/age.tsv`**

```tsv
age
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/age_unit.tsv`**

```tsv
age_unit
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

# Read input data
age_path <- file.path("inputs", "age.tsv")
if (!file.exists(age_path)) {
  stop("age.tsv is required input")
}
age_df <- read.delim(age_path, check.names = FALSE, stringsAsFactors = FALSE)
age_col <- if ("age" %in% names(age_df)) age_df$age else age_df[[1]]
age <- suppressWarnings(as.numeric(as.character(age_col)))
age_unit_path <- file.path("inputs", "age_unit.tsv")
if (!file.exists(age_unit_path)) {
  stop("age_unit.tsv is required input")
}
age_unit_df <- read.delim(age_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
age_unit <- tolower(as.character(age_unit_df[[1]][1]))
valid_units <- c("years", "months", "weeks", "days", "hours", "minutes", "seconds")
if (!age_unit %in% valid_units) age_unit <- "years"

# Execute function implementation
result <- admiral::compute_age_years(age, age_unit)

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    age = age, age_unit = age_unit,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# Generate summary statistics
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

# Save outputs
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

## Reference Output

**`outputs/result.csv`**

```csv
"age","age_unit","result"
0.1,"years",0.1
1.5,"years",1.5
10,"years",10
100,"years",100
1000,"years",1000
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"age, age_unit, result"
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

age_df <- read.table("inputs/age.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
age_unit_df <- read.table("inputs/age_unit.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)

df <- cbind(age_df, age_unit_df)

df$AGE_Y <- compute_age_years(df[[1]], df[[2]])

write.csv(df, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error in `compute_age_years()`:
! Argument `unique(tolower(age_unit))` must be <character> with values
  NA, "years", "months", "weeks", "days", "hours", "minutes", and "seconds".
Backtrace:
    ▆
 1. └─admiral::compute_age_years(df[[1]], df[[2]])
 2.   └─admiraldev::assert_character_vector(...)
 3.     └─cli::cli_abort(...)
 4.       └─rlang::abort(...)
Execution halted
```

## LLM Output Files

_No files generated._

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/compute_age_years",
  "sample_idx": 0,
  "model": "openai/gpt-5.1",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "message": "No output files created",
      "stderr": "Error in `compute_age_years()`:\n! Argument `unique(tolower(age_unit))` must be <character> with values\n  NA, \"years\", \"months\", \"weeks\", \"days\", \"hours\", \"minutes\", and \"seconds\".\nBacktrace:\n    ▆\n 1. └─admiral::compute_age_years(df[[1]], df[[2]])\n 2.   └─admiraldev::assert_character_vector(...)\n 3.     └─cli::cli_abort(...)\n 4.       └─rlang::abort(...)\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
