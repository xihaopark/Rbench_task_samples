# Case 159: pharmaverse/admiral/print_named_list

## Case Metadata

- Task ID: `pharmaverse/admiral/print_named_list`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform print named list using the admiral clinical task contract.

Input: indent.tsv, items.tsv
Output: result.csv


Required columns for result.csv: line_number, line
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### indent.tsv (9 bytes)
indent
2

### items.tsv (39 bytes)
name	value
alpha	1,2
beta	x
gamma	TRUE
```

## Input Data

### `indent.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/print_named_list/inputs/indent.tsv`
- Size: 9 bytes

```text
indent
2
```

### `items.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/print_named_list/inputs/items.tsv`
- Size: 39 bytes

```text
name	value
alpha	1,2
beta	x
gamma	TRUE
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/print_named_list/solution.R`
- Size: 729 bytes

```r
suppressPackageStartupMessages(library(admiral))

items <- read.delim(file.path("inputs", "items.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
indent <- as.integer(read.delim(file.path("inputs", "indent.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$indent[1])
values <- strsplit(items$value, ",", fixed = TRUE)
values <- lapply(values, function(x) if (length(x) == 1) x[[1]] else x)
named <- stats::setNames(values, items$name)
lines <- capture.output(admiral::print_named_list(named, indent = indent))
result <- data.frame(line_number = seq_along(lines), line = lines, stringsAsFactors = FALSE)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/print_named_list/outputs/result.csv`
- Size: 90 bytes

```csv
"line_number","line"
1,"  alpha: ""1"""
2,"""2"""
3,"  beta: ""x"""
4,"  gamma: ""TRUE"""
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(purrr)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
indent_df <- read_tsv(
  file = file.path("inputs", "indent.tsv"),
  col_types = cols(
    indent = col_integer()
  )
)

items_df <- read_tsv(
  file = file.path("inputs", "items.tsv"),
  col_types = cols(
    name = col_character(),
    value = col_character()
  )
)

indent_size <- indent_df$indent[1]

# Helper function to infer R type and format value
format_value <- function(x) {
  x_trim <- str_trim(x)

  # Check for logical
  if (x_trim %in% c("TRUE", "FALSE")) {
    return(x_trim)
  }

  # Check for numeric (single value, no comma)
  if (!str_detect(x_trim, ",") && !is.na(suppressWarnings(as.numeric(x_trim)))) {
    return(x_trim)
  }

  # Otherwise, character; escape internal quotes
  escaped <- str_replace_all(x_trim, "\"", "\\\\\"")
  paste0("\"", escaped, "\"")
}

# Build R code lines for named list
lines <- character(0)

# Opening line
lines <- c(lines, "list(")

n_items <- nrow(items_df)

for (i in seq_len(n_items)) {
  nm <- items_df$name[i]
  val_raw <- items_df$value[i]

  # Detect vector via comma separation
  parts <- str_split(val_raw, ",", n = Inf, simplify = FALSE)[[1]]
  parts <- str_trim(parts)
  parts <- parts[parts != ""]

  if (length(parts) == 1) {
    # Single value
    val_formatted <- format_value(parts[1])
  } else {
    # Vector
    formatted_parts <- map_chr(parts, format_value)
    val_formatted <- paste0("c(", paste(formatted_parts, collapse = ", "), ")")
  }

  indent_spaces <- str_dup(" ", indent_size)
  comma <- if (i < n_items) "," else ""
  line <- paste0(indent_spaces, nm, " = ", val_formatted, comma)
  lines <- c(lines, line)
}

# Closing parenthesis
lines <- c(lines, ")")

result_df <- tibble(
  line_number = seq_along(lines),
  line = lines
)

write_csv(
  result_df,
  file = file.path("outputs", "result.csv"),
  na = ""
)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__print_named_list/sample_00/case_01/llm_outputs/result.csv`
- Size: 89 bytes

```csv
line_number,line
1,list(
2,"  alpha = c(1, 2),"
3,"  beta = ""x"","
4,  gamma = TRUE
5,)
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__print_named_list/sample_00/case_01/stderr.txt`
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
  "status": "FAIL",
  "failure_stage": "schema_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "schema_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "schema_mismatch",
          "reason": "Shape mismatch: ref=(4, 2) vs llm=(5, 2)"
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
        "comparison_reasons": {
          "result.csv": {
            "stage": "schema_mismatch",
            "tier": "output_bad",
            "reason": "Shape mismatch: ref=(4, 2) vs llm=(5, 2)"
          }
        }
      }
    }
  ]
}
```
