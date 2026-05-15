# Case 14 - `pharmaverse/admiral/convert_simple_units`
**Package:** `admiral`  **Function:** `convert_simple_units`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to implement the **Convert simple units** workflow using the `admiral` package.
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

Implement the **Convert Simple Units** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Input Files

**`inputs/may.tsv`**

```tsv
may
"test_value"
```

**`inputs/na_idx.tsv`**

```tsv
na_idx
FALSE
```

**`inputs/no.tsv`**

```tsv
no
"test_value"
```

**`inputs/result.tsv`**

```tsv
result
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/xxtpt.tsv`**

```tsv
xxtpt
"item1"
"item2"
"item3"
"item4"
"item5"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(stringr))

# Read input data
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

# Execute function implementation
hours_pattern <- stringr::regex(
    paste0(
      "^(?<hours>\\d+(?:\\.\\d+)?)\\s*h(?:r|our)?s?",
      "(?:\\s+(?:post|after)(?:\\s*-?\\s*dose)?)?$"
    ),
    ignore_case = TRUE,
    comments = TRUE
  )
  hours_matches <- str_match(xxtpt, hours_pattern)
  hours_idx <- !is.na(hours_matches[, 1]) & is.na(result) & !na_idx
  if (any(hours_idx)) {
    result[hours_idx] <- as.numeric(hours_matches[hours_idx, "hours"])
  }

  minutes_pattern <- stringr::regex(
    paste0(
      "^(?<minutes>\\d+(?:\\.\\d+)?)\\s*m(?:in|inute)?s?",
      "(?:\\s+(?:post|after)(?:\\s*-?\\s*dose)?)?$"
    ),
    ignore_case = TRUE,
    comments = TRUE
  )
  minutes_matches <- str_match(xxtpt, minutes_pattern)
  minutes_idx <- !is.na(minutes_matches[, 1]) & is.na(result) & !na_idx
  if (any(minutes_idx)) {
    result[minutes_idx] <- as.numeric(
      minutes_matches[minutes_idx, "minutes"]
    ) / 60
  }

  result
result <- minutes_idx

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    xxtpt = xxtpt, result = result,
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
"xxtpt","result","result.1"
"item1",FALSE,FALSE
"item2",FALSE,FALSE
"item3",FALSE,FALSE
"item4",FALSE,FALSE
"item5",FALSE,FALSE
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"xxtpt, result, result.1"
```

## LLM Code

```r
library(admiral)

# Create outputs directory
dir.create("outputs", showWarnings = FALSE)

# Read inputs
may_df     <- read.delim(file.path("inputs", "may.tsv"),
                         check.names = FALSE, stringsAsFactors = FALSE)
na_idx_df  <- read.delim(file.path("inputs", "na_idx.tsv"),
                         check.names = FALSE, stringsAsFactors = FALSE)
no_df      <- read.delim(file.path("inputs", "no.tsv"),
                         check.names = FALSE, stringsAsFactors = FALSE)
result_df  <- read.delim(file.path("inputs", "result.tsv"),
                         check.names = FALSE, stringsAsFactors = FALSE)
xxtpt_df   <- read.delim(file.path("inputs", "xxtpt.tsv"),
                         check.names = FALSE, stringsAsFactors = FALSE)

# Map columns to arguments for convert_simple_units
# Assume common structure: one value column and one unit column.
# Prefer the canonical ADaM naming when present, otherwise fall back
# to generic names. Adjust as needed based on actual column names.

get_unit_cols <- function(df) {
  cols <- names(df)
  list(
    values = if ("AVAL" %in% cols) df[["AVAL"]] else if ("value" %in% cols) df[["value"]] else df[[1]],
    units  = if ("AVALU" %in% cols) df[["AVALU"]] else if ("unit" %in% cols) df[["unit"]] else df[[2]]
  )
}

may_cols    <- get_unit_cols(may_df)
na_idx_cols <- get_unit_cols(na_idx_df)
no_cols     <- get_unit_cols(no_df)
xxtpt_cols  <- get_unit_cols(xxtpt_df)

# Perform conversions with convert_simple_units
may_conv <- convert_simple_units(
  values = may_cols$values,
  units  = may_cols$units,
  int_units = "SI"
)

na_idx_conv <- convert_simple_units(
  values = na_idx_cols$values,
  units  = na_idx_cols$units,
  int_units = "SI"
)

no_conv <- convert_simple_units(
  values = no_cols$values,
  units  = no_cols$units,
  int_units = "SI"
)

xxtpt_conv <- convert_simple_units(
  values = xxtpt_cols$values,
  units  = xxtpt_cols$units,
  int_units = "SI"
)

# Assemble result table; keep any existing key columns from result_df
result_out <- result_df

# If result_df already has placeholder columns, overwrite them; otherwise append.
append_or_replace <- function(df, new_vec, nm) {
  if (nm %in% names(df)) {
    df[[nm]] <- new_vec
  } else {
    df[[nm]] <- new_vec
  }
  df
}

result_out <- append_or_replace(result_out, may_conv$values,    "may_values")
result_out <- append_or_replace(result_out, may_conv$units,     "may_units")
result_out <- append_or_replace(result_out, na_idx_conv$values, "na_idx_values")
result_out <- append_or_replace(result_out, na_idx_conv$units,  "na_idx_units")
result_out <- append_or_replace(result_out, no_conv$values,     "no_values")
result_out <- append_or_replace(result_out, no_conv$units,      "no_units")
result_out <- append_or_replace(result_out, xxtpt_conv$values,  "xxtpt_values")
result_out <- append_or_replace(result_out, xxtpt_conv$units,   "xxtpt_units")

# Write required output
write.csv(result_out, file.path("outputs", "result.csv"), row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error in .subset2(x, i, exact = exact) : subscript out of bounds
Calls: get_unit_cols -> [[ -> [[.data.frame -> <Anonymous>
Execution halted
```

## LLM Output Files

_No files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/convert_simple_units",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "c4957ecb57e1a72a43b3f9a5deae587deeb27465ab4d788f7bb040bf64789454",
  "raw_response": "```r\nlibrary(admiral)\n\n# Create outputs directory\ndir.create(\"outputs\", showWarnings = FALSE)\n\n# Read inputs\nmay_df     <- read.delim(file.path(\"inputs\", \"may.tsv\"),\n                         check.names = FALSE, stringsAsFactors = FALSE)\nna_idx_df  <- read.delim(file.path(\"inputs\", \"na_idx.tsv\"),\n                         check.names = FALSE, stringsAsFactors = FALSE)\nno_df      <- read.delim(file.path(\"inputs\", \"no.tsv\"),\n                         check.names = FALSE, stringsAsFactors = FALSE)\nresult_df  <- read.delim(file.path(\"inputs\", \"result.tsv\"),\n                         check.names = FALSE, stringsAsFactors = FALSE)\nxxtpt_df   <- read.delim(file.path(\"inputs\", \"xxtpt.tsv\"),\n                         check.names = FALSE, stringsAsFactors = FALSE)\n\n# Map columns to arguments for convert_simple_units\n# Assume common structure: one value column and one unit column.\n# Prefer the canonical ADaM naming when present, otherwise fall back\n# to generic names. Adjust as needed based on actual column names.\n\nget_unit_cols <- function(df) {\n  cols <- names(df)\n  list(\n    values = if (\"AVAL\" %in% cols) df[[\"AVAL\"]] else if (\"value\" %in% cols) df[[\"value\"]] else df[[1]],\n    units  = if (\"AVALU\" %in% cols) df[[\"AVALU\"]] else if (\"unit\" %in% cols) df[[\"unit\"]] else df[[2]]\n  )\n}\n\nmay_cols    <- get_unit_cols(may_df)\nna_idx_cols <- get_unit_cols(na_idx_df)\nno_cols     <- get_unit_cols(no_df)\nxxtpt_cols  <- get_unit_cols(xxtpt_df)\n\n# Perform conversions with convert_simple_units\nmay_conv <- convert_simple_units(\n  values = may_cols$values,\n  units  = may_cols$units,\n  int_units = \"SI\"\n)\n\nna_idx_conv <- convert_simple_units(\n  values = na_idx_cols$values,\n  units  = na_idx_cols$units,\n  int_units = \"SI\"\n)\n\nno_conv <- convert_simple_units(\n  values = no_cols$values,\n  units  = no_cols$units,\n  int_units = \"SI\"\n)\n\nxxtpt_conv <- convert_simple_units(\n  values = xxtpt_cols$values,\n  units  = xxtpt_cols$units,\n  int_units = \"SI\"\n)\n\n# Assemble result table; keep any existing key columns from result_df\nresult_out <- result_df\n\n# If result_df already has placeholder columns, overwrite them; otherwise append.\nappend_or_replace <- function(df, new_vec, nm) {\n  if (nm %in% names(df)) {\n    df[[nm]] <- new_vec\n  } else {\n    df[[nm]] <- new_vec\n  }\n  df\n}\n\nresult_out <- append_or_replace(result_out, may_conv$values,    \"may_values\")\nresult_out <- append_or_replace(result_out, may_conv$units,     \"may_units\")\nresult_out <- append_or_replace(result_out, na_idx_conv$values, \"na_idx_values\")\nresult_out <- append_or_replace(result_out, na_idx_conv$units,  \"na_idx_units\")\nresult_out <- append_or_replace(result_out, no_conv$values,     \"no_values\")\nresult_out <- append_or_replace(result_out, no_conv$units,      \"no_units\")\nresult_out <- append_or_replace(result_out, xxtpt_conv$values,  \"xxtpt_values\")\nresult_out <- append_or_replace(result_out, xxtpt_conv$units,   \"xxtpt_units\")\n\n# Write required output\nwrite.csv(result_out, file.path(\"outputs\", \"result.csv\"), row.names = FALSE)\n```",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:12:20.182550",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/convert_simple_units",
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
      "stderr": "Error in .subset2(x, i, exact = exact) : subscript out of bounds\nCalls: get_unit_cols -> [[ -> [[.data.frame -> <Anonymous>\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
