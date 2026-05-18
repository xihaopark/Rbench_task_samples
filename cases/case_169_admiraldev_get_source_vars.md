# Case 169: pharmaverse/admiraldev/get_source_vars

## Case Metadata

- Task ID: `pharmaverse/admiraldev/get_source_vars`
- Package: `admiraldev`
- Model: `openai/gpt-5.1`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform get source vars using the admiraldev clinical task contract.

Input: expressions.tsv
Output: result.csv


Required columns for result.csv: target, source_var
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### expressions.tsv (85 bytes)
target	expression
baseline	AVAL
change	CHG
percent_change	PCHG
analysis_flag	ANL01FL
```

## Input Data

### `expressions.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/get_source_vars/inputs/expressions.tsv`
- Size: 85 bytes

```text
target	expression
baseline	AVAL
change	CHG
percent_change	PCHG
analysis_flag	ANL01FL
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/get_source_vars/solution.R`
- Size: 775 bytes

```r
suppressPackageStartupMessages(library(admiraldev))
suppressPackageStartupMessages(library(rlang))

expressions <- read.delim(
  file.path("inputs", "expressions.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

expr_list <- setNames(
  lapply(expressions$expression, rlang::parse_expr),
  expressions$target
)
result <- admiraldev::get_source_vars(expr_list)

if (is.null(result) || length(result) == 0) {
  result_df <- data.frame(target = character(), source_var = character())
} else {
  result_df <- data.frame(
    target = names(result),
    source_var = vapply(result, rlang::as_label, character(1)),
    stringsAsFactors = FALSE
  )
}

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/get_source_vars/outputs/result.csv`
- Size: 105 bytes

```csv
"target","source_var"
"baseline","AVAL"
"change","CHG"
"percent_change","PCHG"
"analysis_flag","ANL01FL"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(stringr)
library(purrr)
library(fs)

# Create outputs directory if it doesn't exist
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read input
expr_df <- read_tsv(
  file = "inputs/expressions.tsv",
  col_types = cols(
    target = col_character(),
    expression = col_character()
  )
)

# Extract source vars from expressions using admiraldev-style logic:
# - Valid source vars are uppercase A-Z, 0-9 and underscore
# - Variables must start with a letter, and are taken as standalone tokens
get_source_vars <- function(expr) {
  if (is.na(expr) || expr == "") return(character(0))
  tokens <- str_extract_all(expr, "\\b[A-Z][A-Z0-9_]*\\b")[[1]]
  unique(tokens)
}

result_df <- expr_df %>%
  mutate(source_var = map(expression, get_source_vars)) %>%
  select(target, source_var) %>%
  unnest_longer(source_var, values_to = "source_var") %>%
  filter(!is.na(source_var) & source_var != "") %>%
  distinct(target, source_var) %>%
  arrange(target, source_var)

# Write output
write_csv(result_df, "outputs/result.csv")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__get_source_vars/sample_00/case_01/stderr.txt`
- Size: 1503 bytes

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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error in unnest_longer(., source_var, values_to = "source_var") :
  could not find function "unnest_longer"
Calls: %>% -> arrange -> distinct -> filter
Execution halted
```

## Evaluation Result

```json
{
  "status": "NO_OUTPUT",
  "failure_stage": "execution_failure",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "tier": "exec_fail",
      "failure_stage": "execution_failure",
      "message": "No output files created",
      "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
      "returncode": 1,
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [],
        "missing_artifacts": [
          "result.csv"
        ]
      }
    }
  ]
}
```
