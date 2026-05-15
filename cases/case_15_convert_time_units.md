# Case 15 - `pharmaverse/admiral/convert_time_units`
**Package:** `admiral`  **Function:** `convert_time_units`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to implement the **Convert time units** workflow using the `admiral` package.
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

Implement the **Convert Time Units** functionality. Reproduce the same computational result as the reference using the given inputs.
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
suppressPackageStartupMessages(library(dplyr))

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
# Days - require at least one unit indicator to avoid ambiguity
  # Matches: "Day 1", "2D", "2 days", "30 DAYS AFTER LAST", "2 POST-DOSE"
  # Does NOT match: "2" (bare number - ambiguous, could be hours)
  days_pattern <- stringr::regex(
    paste0(
      "^(?:",
      "(?:day\\s+)(?<days1>\\d+(?:\\.\\d+)?)\\s*(?:d|day|days)?|",
      "(?<days2>\\d+(?:\\.\\d+)?)\\s*(?:d|day|days)(?!\\s*h(?:r|our)?)|",
      "(?<days3>\\d+(?:\\.\\d+)?)\\s+(?:days?\\s+)?",
      "(?:after\\s+last|post(?:\\s*-?\\s*dose)?)",
      ")",
      "$"
    ),
    ignore_case = TRUE,
    comments = TRUE
  )
  days_matches <- str_match(xxtpt, days_pattern)
  days_idx <- !is.na(days_matches[, 1]) & is.na(result) & !na_idx
  if (any(days_idx)) {
    # Extract whichever capture group matched
    days_value <- coalesce(
      as.numeric(days_matches[days_idx, "days1"]),
      as.numeric(days_matches[days_idx, "days2"]),
      as.numeric(days_matches[days_idx, "days3"])
    )
    result[days_idx] <- days_value * 24
  }

  # Hours+minutes combinations
  hm_pattern <- stringr::regex(
    paste0(
      "^(?<hours>\\d+(?:\\.\\d+)?)\\s*h(?:r|our)?s?\\s*",
      "(?<minutes>\\d+(?:\\.\\d+)?)\\s*m(?:in|inute)?s?",
      "(?:\\s+(?:post|after)(?:\\s*-?\\s*dose)?)?$"
    ),
    ignore_case = TRUE,
    comments = TRUE
  )
  hm_matches <- str_match(xxtpt, hm_pattern)
  hm_idx <- !is.na(hm_matches[, 1]) & is.na(result) & !na_idx
  if (any(hm_idx)) {
    hours <- as.numeric(hm_matches[hm_idx, "hours"])
    minutes <- as.numeric(hm_matches[hm_idx, "minutes"])
    result[hm_idx] <- hours + minutes / 60
  }

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    xxtpt = xxtpt, result = result,
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
"xxtpt","result"
"item1",0.1
"item2",1.5
"item3",10
"item4",100
"item5",1000
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"xxtpt, result"
```

## LLM Code

```r
library(admiral)

# Create outputs directory
dir.create("outputs", showWarnings = FALSE)

# Read inputs
may <- read.delim(file.path("inputs", "may.tsv"),
                  check.names = FALSE, stringsAsFactors = FALSE)
na_idx <- read.delim(file.path("inputs", "na_idx.tsv"),
                     check.names = FALSE, stringsAsFactors = FALSE)
no <- read.delim(file.path("inputs", "no.tsv"),
                 check.names = FALSE, stringsAsFactors = FALSE)
result_in <- read.delim(file.path("inputs", "result.tsv"),
                        check.names = FALSE, stringsAsFactors = FALSE)
xxtpt <- read.delim(file.path("inputs", "xxtpt.tsv"),
                    check.names = FALSE, stringsAsFactors = FALSE)

# Helper to map textual units to admiral-supported units
map_unit <- function(x) {
  recode(x,
    "secs"  = "seconds",
    "mins"  = "minutes",
    "hours" = "hours",
    "days"  = "days",
    "weeks" = "weeks",
    "months"= "months",
    "years" = "years",
    .default = x
  )
}

# Prepare arguments for convert_time_units from result.tsv
# Assumes columns: value, old_unit, new_unit
# and possibly id-like/group columns carried through
if (!all(c("value", "old_unit", "new_unit") %in% names(result_in))) {
  stop("result.tsv must contain columns: value, old_unit, new_unit")
}

values <- result_in[["value"]]
old_units <- map_unit(result_in[["old_unit"]])
new_units <- map_unit(result_in[["new_unit"]])

# Apply convert_time_units row-wise
converted <- mapply(
  function(val, ou, nu) {
    convert_time_units(
      input = val,
      input_unit = ou,
      target_unit = nu
    )
  },
  val = values,
  ou = old_units,
  nu = new_units
)

# Bind converted result back to original structure
result_out <- result_in
result_out[["converted"]] <- as.numeric(converted)

# Write required output
write.csv(result_out, file.path("outputs", "result.csv"), row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error: result.tsv must contain columns: value, old_unit, new_unit
Execution halted
```

## LLM Output Files

_No files generated._

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/convert_time_units",
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
      "stderr": "Error: result.tsv must contain columns: value, old_unit, new_unit\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
