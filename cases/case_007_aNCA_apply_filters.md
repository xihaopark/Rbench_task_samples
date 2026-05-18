# Case 007: pharmaverse/aNCA/apply_filters

## Case Metadata

- Task ID: `pharmaverse/aNCA/apply_filters`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform apply filters using the aNCA clinical task contract.

Input: data.tsv, filters.tsv
Output: result.csv


Required columns for result.csv: id, value, group, category
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### filters.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_filters/inputs/data.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `filters.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_filters/inputs/filters.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_filters/solution.R`
- Size: 1877 bytes

```r
read_tsv <- function(name) {
  path <- file.path("inputs", name)
  if (!file.exists(path)) {
    stop(name, " is required")
  }
  read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
}

first_column <- function(df) {
  if (ncol(df) == 0) {
    return(character())
  }
  df[[1]]
}

scalar_numeric <- function(df) {
  values <- suppressWarnings(as.numeric(first_column(df)))
  values <- values[!is.na(values)]
  if (length(values) == 0) NA_real_ else values[[1]]
}

write_result <- function(result) {
  dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
  write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE, na = "NA")
}

data <- read_tsv("data.tsv")
filters <- read_tsv("filters.tsv")
result <- data

if (all(c("column", "condition", "value") %in% names(filters))) {
  for (i in seq_len(nrow(filters))) {
    column <- as.character(filters$column[[i]])
    condition <- as.character(filters$condition[[i]])
    value <- filters$value[[i]]
    if (!column %in% names(result)) next
    column_values <- result[[column]]
    value_num <- suppressWarnings(as.numeric(value))
    if (is.numeric(column_values) && !is.na(value_num)) value <- value_num
    keep <- rep(TRUE, nrow(result))
    if (condition %in% c("==", "=", "eq")) keep <- column_values == value
    if (condition %in% c("!=", "ne")) keep <- column_values != value
    if (condition %in% c(">", "gt")) keep <- suppressWarnings(as.numeric(column_values)) > value_num
    if (condition %in% c(">=", "ge")) keep <- suppressWarnings(as.numeric(column_values)) >= value_num
    if (condition %in% c("<", "lt")) keep <- suppressWarnings(as.numeric(column_values)) < value_num
    if (condition %in% c("<=", "le")) keep <- suppressWarnings(as.numeric(column_values)) <= value_num
    keep[is.na(keep)] <- FALSE
    result <- result[keep, , drop = FALSE]
  }
}

write_result(result)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_filters/outputs/result.csv`
- Size: 127 bytes

```csv
"id","value","group","category"
1,10.5,"A","Type1"
2,20.3,"B","Type2"
3,30.7,"A","Type1"
4,40.2,"B","Type2"
5,50.9,"A","Type1"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  # base only; no external deps
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
}

# Read input files
data_path    <- file.path("inputs", "data.tsv")
filters_path <- file.path("inputs", "filters.tsv")

data_df <- read.table(data_path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)
filters_df <- read.table(filters_path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)

# Ensure required columns exist
required_cols <- c("id", "value", "group", "category")
missing_data_cols    <- setdiff(required_cols, colnames(data_df))
missing_filter_cols  <- setdiff(required_cols, colnames(filters_df))

if (length(missing_data_cols) > 0) {
  stop("Missing required columns in data.tsv: ", paste(missing_data_cols, collapse = ", "))
}
if (length(missing_filter_cols) > 0) {
  stop("Missing required columns in filters.tsv: ", paste(missing_filter_cols, collapse = ", "))
}

# Perform filtering:
# Keep rows in data_df that are present in filters_df on all required columns
# Using merge with inner join semantics
filtered_df <- merge(
  data_df[, required_cols],
  filters_df[, required_cols],
  by = required_cols,
  all = FALSE
)

# Deduplicate if necessary
filtered_df <- unique(filtered_df)

# Reorder columns to required order
filtered_df <- filtered_df[, required_cols]

# Write result
output_path <- file.path("outputs", "result.csv")
write.csv(filtered_df, file = output_path, row.names = FALSE, quote = TRUE)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__apply_filters/sample_00/case_01/llm_outputs/result.csv`
- Size: 127 bytes

```csv
"id","value","group","category"
1,10.5,"A","Type1"
2,20.3,"B","Type2"
3,30.7,"A","Type1"
4,40.2,"B","Type2"
5,50.9,"A","Type1"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__apply_filters/sample_00/case_01/stderr.txt`
- Size: 1123 bytes

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

## Evaluation Result

```json
{
  "status": "PASS",
  "failure_stage": "pass",
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "tier": "pass",
      "tier_value": "pass",
      "failure_stage": "pass",
      "comparison": {
        "result.csv": {
          "match": true,
          "tier": "pass",
          "failure_stage": "pass"
        }
      },
      "returncode": 0,
      "normalizations": [],
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [
          "result.csv"
        ],
        "staged_artifacts": [
          "result.csv"
        ],
        "missing_artifacts": [],
        "extra_artifacts": [],
        "comparison_reasons": {}
      }
    }
  ]
}
```
