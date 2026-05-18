# Case 128: pharmaverse/admiral/event

## Case Metadata

- Task ID: `pharmaverse/admiral/event`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform event using the admiral clinical task contract.

Input: condition.tsv, dataset_name.tsv, description.tsv, keep_source_vars.tsv, mode.tsv, order.tsv, set_values_to.tsv
Output: result.csv


Required columns for result.csv: class, description, dataset_name, condition, mode, order, set_values_to, keep_source_vars
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### condition.tsv (23 bytes)
condition
AETOXGR >= 2

### dataset_name.tsv (18 bytes)
dataset_name
adae

### description.tsv (50 bytes)
description
First grade 2 or higher adverse event

### keep_source_vars.tsv (36 bytes)
keep_source_vars
ADT;AETERM;AETOXGR

### mode.tsv (11 bytes)
mode
first

### order.tsv (16 bytes)
order
ADT;AESEQ

### set_values_to.tsv (72 bytes)
variable	value
PARAMCD	G2AE
PARAM	First grade 2 or higher adverse event
```

## Input Data

### `condition.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/condition.tsv`
- Size: 23 bytes

```text
condition
AETOXGR >= 2
```

### `dataset_name.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/dataset_name.tsv`
- Size: 18 bytes

```text
dataset_name
adae
```

### `description.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/description.tsv`
- Size: 50 bytes

```text
description
First grade 2 or higher adverse event
```

### `keep_source_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/keep_source_vars.tsv`
- Size: 36 bytes

```text
keep_source_vars
ADT;AETERM;AETOXGR
```

### `mode.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/mode.tsv`
- Size: 11 bytes

```text
mode
first
```

### `order.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/order.tsv`
- Size: 16 bytes

```text
order
ADT;AESEQ
```

### `set_values_to.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/inputs/set_values_to.tsv`
- Size: 72 bytes

```text
variable	value
PARAMCD	G2AE
PARAM	First grade 2 or higher adverse event
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/solution.R`
- Size: 2544 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

read_scalar <- function(path, column, default = "") {
  if (!file.exists(path)) return(default)
  data <- read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
  if (!nrow(data)) return(default)
  if (column %in% names(data)) return(as.character(data[[column]][1]))
  as.character(data[[1]][1])
}

read_key_values <- function(path) {
  data <- read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
  values <- as.list(as.character(data$value))
  names(values) <- as.character(data$variable)
  values
}

parse_expr_list <- function(text) {
  parts <- trimws(strsplit(text, ";", fixed = TRUE)[[1]])
  parts <- parts[nzchar(parts)]
  rlang::parse_exprs(parts)
}

expr_label <- function(x) {
  if (is.null(x)) return("")
  rlang::as_label(x)
}

exprs_label <- function(x) {
  if (is.null(x) || length(x) == 0) return("")
  labels <- vapply(x, rlang::as_label, character(1))
  names_x <- names(x)
  if (is.null(names_x)) names_x <- rep("", length(labels))
  labels <- ifelse(nzchar(names_x), paste0(names_x, "=", labels), labels)
  paste(labels, collapse = ";")
}

dataset_name <- read_scalar(file.path("inputs", "dataset_name.tsv"), "dataset_name")
condition_text <- read_scalar(file.path("inputs", "condition.tsv"), "condition")
mode <- read_scalar(file.path("inputs", "mode.tsv"), "mode")
order <- parse_expr_list(read_scalar(file.path("inputs", "order.tsv"), "order"))
set_values <- read_key_values(file.path("inputs", "set_values_to.tsv"))
keep_source_vars <- parse_expr_list(read_scalar(file.path("inputs", "keep_source_vars.tsv"), "keep_source_vars"))
description <- read_scalar(file.path("inputs", "description.tsv"), "description")

event_def <- admiral::event(
  dataset_name = dataset_name,
  condition = !!rlang::parse_expr(condition_text),
  mode = mode,
  order = order,
  set_values_to = rlang::exprs(!!!set_values),
  keep_source_vars = keep_source_vars,
  description = description
)

result <- data.frame(
  class = paste(class(event_def), collapse = "|"),
  description = event_def$description,
  dataset_name = event_def$dataset_name,
  condition = expr_label(event_def$condition),
  mode = event_def$mode,
  order = exprs_label(event_def$order),
  set_values_to = exprs_label(event_def$set_values_to),
  keep_source_vars = exprs_label(event_def$keep_source_vars),
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event/outputs/result.csv`
- Size: 299 bytes

```csv
"class","description","dataset_name","condition","mode","order","set_values_to","keep_source_vars"
"event|event_def|source|list","First grade 2 or higher adverse event","adae","AETOXGR >= 2","first","ADT;AESEQ","PARAMCD=""G2AE"";PARAM=""First grade 2 or higher adverse event""","ADT;AETERM;AETOXGR"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(tidyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Helper to read simple single-column TSVs
read_single_col_tsv <- function(path) {
  read_tsv(
    path,
    col_types = cols(.default = col_character())
  )
}

# Read inputs
condition_df      <- read_single_col_tsv("inputs/condition.tsv")
dataset_name_df   <- read_single_col_tsv("inputs/dataset_name.tsv")
description_df    <- read_single_col_tsv("inputs/description.tsv")
keep_source_df    <- read_single_col_tsv("inputs/keep_source_vars.tsv")
mode_df           <- read_single_col_tsv("inputs/mode.tsv")
order_df          <- read_single_col_tsv("inputs/order.tsv")
set_values_to_df  <- read_tsv("inputs/set_values_to.tsv",
                              col_types = cols(.default = col_character()))

# Extract scalar values
condition      <- condition_df$condition[1]
dataset_name   <- dataset_name_df$dataset_name[1]
description    <- description_df$description[1]
mode_val       <- mode_df$mode[1]
order_val      <- order_df$order[1]
keep_source    <- keep_source_df$keep_source_vars[1]

# Collapse set_values_to key/value pairs into a single string "VAR1=VAL1;VAR2=VAL2"
set_values_to <- set_values_to_df %>%
  mutate(pair = paste0(variable, "=", value)) %>%
  pull(pair) %>%
  paste(collapse = ";")

# Build result row
result <- tibble(
  class           = "event",
  description     = description,
  dataset_name    = dataset_name,
  condition       = condition,
  mode            = mode_val,
  order           = order_val,
  set_values_to   = set_values_to,
  keep_source_vars = keep_source
)

# Write output
write_csv(result, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__event/sample_00/case_01/llm_outputs/result.csv`
- Size: 237 bytes

```csv
class,description,dataset_name,condition,mode,order,set_values_to,keep_source_vars
event,First grade 2 or higher adverse event,adae,AETOXGR >= 2,first,ADT;AESEQ,PARAMCD=G2AE;PARAM=First grade 2 or higher adverse event,ADT;AETERM;AETOXGR
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__event/sample_00/case_01/stderr.txt`
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
  "failure_stage": "value_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "schema_ok",
      "tier_value": "schema_ok",
      "failure_stage": "value_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "schema_ok",
          "failure_stage": "value_mismatch",
          "reason": "Value mismatch in column: class"
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
            "stage": "value_mismatch",
            "tier": "schema_ok",
            "reason": "Value mismatch in column: class"
          }
        }
      }
    }
  ]
}
```
