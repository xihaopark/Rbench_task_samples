# Case 129: pharmaverse/admiral/event_joined

## Case Metadata

- Task ID: `pharmaverse/admiral/event_joined`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform event joined using the admiral clinical task contract.

Input: condition.tsv, dataset_name.tsv, description.tsv, join_type.tsv, join_vars.tsv, order.tsv, set_values_to.tsv
Output: result.csv


Required columns for result.csv: class, description, dataset_name, condition, order, join_vars, join_type, first_cond_lower, first_cond_upper, set_values_to, keep_source_vars
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### condition.tsv (29 bytes)
condition
EXSTDTC <= AESTDTC

### dataset_name.tsv (18 bytes)
dataset_name
adae

### description.tsv (64 bytes)
description
Treatment-emergent adverse event joined to exposure

### join_type.tsv (14 bytes)
join_type
all

### join_vars.tsv (26 bytes)
join_vars
STUDYID;USUBJID

### order.tsv (20 bytes)
order
AESTDTC;AESEQ

### set_values_to.tsv (70 bytes)
variable	value
PARAMCD	TRTEMAE
PARAM	Treatment-emergent adverse event
```

## Input Data

### `condition.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/condition.tsv`
- Size: 29 bytes

```text
condition
EXSTDTC <= AESTDTC
```

### `dataset_name.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/dataset_name.tsv`
- Size: 18 bytes

```text
dataset_name
adae
```

### `description.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/description.tsv`
- Size: 64 bytes

```text
description
Treatment-emergent adverse event joined to exposure
```

### `join_type.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/join_type.tsv`
- Size: 14 bytes

```text
join_type
all
```

### `join_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/join_vars.tsv`
- Size: 26 bytes

```text
join_vars
STUDYID;USUBJID
```

### `order.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/order.tsv`
- Size: 20 bytes

```text
order
AESTDTC;AESEQ
```

### `set_values_to.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/inputs/set_values_to.tsv`
- Size: 70 bytes

```text
variable	value
PARAMCD	TRTEMAE
PARAM	Treatment-emergent adverse event
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/solution.R`
- Size: 2721 bytes

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
order <- parse_expr_list(read_scalar(file.path("inputs", "order.tsv"), "order"))
join_vars <- parse_expr_list(read_scalar(file.path("inputs", "join_vars.tsv"), "join_vars"))
join_type <- read_scalar(file.path("inputs", "join_type.tsv"), "join_type")
set_values <- read_key_values(file.path("inputs", "set_values_to.tsv"))
description <- read_scalar(file.path("inputs", "description.tsv"), "description")

event_def <- admiral::event_joined(
  dataset_name = dataset_name,
  condition = !!rlang::parse_expr(condition_text),
  order = order,
  join_vars = join_vars,
  join_type = join_type,
  set_values_to = rlang::exprs(!!!set_values),
  description = description
)

result <- data.frame(
  class = paste(class(event_def), collapse = "|"),
  description = event_def$description,
  dataset_name = event_def$dataset_name,
  condition = expr_label(event_def$condition),
  order = exprs_label(event_def$order),
  join_vars = exprs_label(event_def$join_vars),
  join_type = event_def$join_type,
  first_cond_lower = expr_label(event_def$first_cond_lower),
  first_cond_upper = expr_label(event_def$first_cond_upper),
  set_values_to = exprs_label(event_def$set_values_to),
  keep_source_vars = exprs_label(event_def$keep_source_vars),
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/event_joined/outputs/result.csv`
- Size: 387 bytes

```csv
"class","description","dataset_name","condition","order","join_vars","join_type","first_cond_lower","first_cond_upper","set_values_to","keep_source_vars"
"event_joined|event_def|source|list","Treatment-emergent adverse event joined to exposure","adae","EXSTDTC <= AESTDTC","AESTDTC;AESEQ","STUDYID;USUBJID","all","","","PARAMCD=""TRTEMAE"";PARAM=""Treatment-emergent adverse event""",""
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if not exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
condition_df   <- read_tsv("inputs/condition.tsv", show_col_types = FALSE)
dataset_df     <- read_tsv("inputs/dataset_name.tsv", show_col_types = FALSE)
description_df <- read_tsv("inputs/description.tsv", show_col_types = FALSE)
join_type_df   <- read_tsv("inputs/join_type.tsv", show_col_types = FALSE)
join_vars_df   <- read_tsv("inputs/join_vars.tsv", show_col_types = FALSE)
order_df       <- read_tsv("inputs/order.tsv", show_col_types = FALSE)
set_vals_df    <- read_tsv("inputs/set_values_to.tsv", show_col_types = FALSE)

# Extract scalar values
condition    <- condition_df$condition[1]
dataset_name <- dataset_df$dataset_name[1]
description  <- description_df$description[1]
join_type    <- join_type_df$join_type[1]
join_vars    <- join_vars_df$join_vars[1]
order        <- order_df$order[1]

# Split condition to lower and upper parts
# Assuming format "<expr1> <= <expr2>"
cond_split <- str_split_fixed(condition, "<=", 2)
first_cond_lower <- str_trim(cond_split[, 1])
first_cond_upper <- str_trim(cond_split[, 2])

# set_values_to as "VAR1=VAL1;VAR2=VAL2"
set_values_to <- set_vals_df %>%
  mutate(pair = paste0(variable, "=", value)) %>%
  pull(pair) %>%
  paste(collapse = ";")

# Build result
result <- tibble(
  class            = "event_joined",
  description      = description,
  dataset_name     = dataset_name,
  condition        = condition,
  order            = order,
  join_vars        = join_vars,
  join_type        = join_type,
  first_cond_lower = first_cond_lower,
  first_cond_upper = first_cond_upper,
  set_values_to    = set_values_to,
  keep_source_vars = "TRUE"
)

# Write output
write_csv(result, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__event_joined/sample_00/case_01/llm_outputs/result.csv`
- Size: 331 bytes

```csv
class,description,dataset_name,condition,order,join_vars,join_type,first_cond_lower,first_cond_upper,set_values_to,keep_source_vars
event_joined,Treatment-emergent adverse event joined to exposure,adae,EXSTDTC <= AESTDTC,AESTDTC;AESEQ,STUDYID;USUBJID,all,EXSTDTC,AESTDTC,PARAMCD=TRTEMAE;PARAM=Treatment-emergent adverse event,TRUE
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__event_joined/sample_00/case_01/stderr.txt`
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
