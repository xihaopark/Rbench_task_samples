# Case 172: pharmaverse/admiraldev/parse_code

## Case Metadata

- Task ID: `pharmaverse/admiraldev/parse_code`
- Package: `admiraldev`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform parse code using the admiraldev clinical task contract.

Input: code.tsv
Output: result.csv


Required columns for result.csv: item, expr, srcref, eval
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### code.tsv (27 bytes)
code
"x <- 1"
"y <- x + 2"
```

## Input Data

### `code.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/parse_code/inputs/code.tsv`
- Size: 27 bytes

```text
code
"x <- 1"
"y <- x + 2"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/parse_code/solution.R`
- Size: 884 bytes

```r
suppressPackageStartupMessages(library(admiraldev))

code <- read.delim(
  file.path("inputs", "code.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

code_text <- paste(code[[1]], collapse = "\n")
parsed <- admiraldev::parse_code(code_text)

result_df <- do.call(
  rbind,
  lapply(seq_along(parsed), function(i) {
    item <- parsed[[i]]
    data.frame(
      item = i,
      expr = if (is.null(item$expr)) NA_character_ else paste(deparse(item$expr), collapse = " "),
      srcref = paste(item$srcref, collapse = "\n"),
      eval = isTRUE(item$eval),
      stringsAsFactors = FALSE
    )
  })
)

if (length(parsed) == 0) {
  result_df <- data.frame(
    item = integer(),
    expr = character(),
    srcref = character(),
    eval = logical()
  )
}

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/parse_code/outputs/result.csv`
- Size: 88 bytes

```csv
"item","expr","srcref","eval"
1,"x <- 1","x <- 1",TRUE
2,"y <- x + 2","y <- x + 2",TRUE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(purrr)
  library(rlang)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
code_df <- readr::read_tsv(
  file = file.path("inputs", "code.tsv"),
  col_types = cols(.default = col_character())
)

# Ensure column name is 'code'
if (!"code" %in% names(code_df)) {
  stop("Input file must contain a 'code' column.")
}

# Helper to safely parse an expression and get srcref
parse_with_srcref <- function(code_str) {
  # Remove surrounding quotes if present
  code_clean <- str_replace_all(code_str, "^['\"]|['\"]$", "")

  con <- textConnection(code_clean)
  on.exit(close(con), add = TRUE)

  exprs <- tryCatch(
    parse(con, keep.source = TRUE),
    error = function(e) NULL
  )

  if (is.null(exprs) || length(exprs) == 0) {
    return(list(expr = NA_character_, srcref = NA_character_))
  }

  expr <- exprs[[1]]

  # Get srcref if available
  sr <- attr(expr, "srcref")
  sr_txt <- if (!is.null(sr)) {
    paste(as.character(sr), collapse = "")
  } else {
    NA_character_
  }

  list(
    expr   = rlang::expr_text(expr),
    srcref = sr_txt
  )
}

# Helper to safely evaluate an expression
eval_expr <- function(code_str, env) {
  code_clean <- str_replace_all(code_str, "^['\"]|['\"]$", "")

  exprs <- tryCatch(
    parse(text = code_clean),
    error = function(e) return(list(error = e))
  )

  if (is.list(exprs) && !is.null(exprs$error)) {
    return(paste0("ERROR: ", conditionMessage(exprs$error)))
  }

  if (length(exprs) == 0) {
    return(NA_character_)
  }

  expr <- exprs[[1]]

  val <- tryCatch(
    eval(expr, envir = env),
    error = function(e) paste0("ERROR: ", conditionMessage(e))
  )

  if (inherits(val, "error") || is.character(val) && str_starts(val, "ERROR: ")) {
    return(as.character(val))
  }

  # Capture evaluation result as deparsed text
  paste(deparse(val), collapse = " ")
}

# Environment for sequential evaluation
eval_env <- new.env(parent = baseenv())

# Process all rows
result_df <- code_df %>%
  mutate(
    item = row_number()
  ) %>%
  rowwise() %>%
  mutate(
    parsed = list(parse_with_srcref(code)),
    expr   = parsed$expr,
    srcref = parsed$srcref,
    eval   = eval_expr(code, eval_env)
  ) %>%
  ungroup() %>%
  select(item, expr, srcref, eval)

# Write output
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__parse_code/sample_00/case_01/llm_outputs/result.csv`
- Size: 50 bytes

```csv
item,expr,srcref,eval
1,x <- 1,,1
2,y <- x + 2,,3
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__parse_code/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: srcref"
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
            "reason": "Value mismatch in column: srcref"
          }
        }
      }
    }
  ]
}
```
