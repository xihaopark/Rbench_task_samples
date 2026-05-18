# Case 174: pharmaverse/admiraldev/replace_values_by_names

## Case Metadata

- Task ID: `pharmaverse/admiraldev/replace_values_by_names`
- Package: `admiraldev`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform replace values by names using the admiraldev clinical task contract.

Input: expressions.tsv
Output: result.csv


Required columns for result.csv: name, expression
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### expressions.tsv (54 bytes)
name	expression
AVAL	MEAN
PARAMCD	CODE
TRTSDT	STARTDT
```

## Input Data

### `expressions.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/replace_values_by_names/inputs/expressions.tsv`
- Size: 54 bytes

```text
name	expression
AVAL	MEAN
PARAMCD	CODE
TRTSDT	STARTDT
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/replace_values_by_names/solution.R`
- Size: 653 bytes

```r
suppressPackageStartupMessages(library(admiraldev))
suppressPackageStartupMessages(library(rlang))

expr_df <- read.delim(file.path("inputs", "expressions.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
exprs_list <- lapply(expr_df$expression, parse_expr)
names(exprs_list) <- expr_df$name
result_list <- admiraldev::replace_values_by_names(exprs_list)
result <- data.frame(
  name = names(result_list),
  expression = vapply(result_list, function(x) paste(deparse(x), collapse = " "), character(1)),
  stringsAsFactors = FALSE
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/replace_values_by_names/outputs/result.csv`
- Size: 72 bytes

```csv
"name","expression"
"AVAL","AVAL"
"PARAMCD","PARAMCD"
"TRTSDT","TRTSDT"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load necessary package
suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input expressions
expr_path <- file.path("inputs", "expressions.tsv")
expressions <- readr::read_tsv(expr_path, show_col_types = FALSE)

# Example mapping for clinical task contract (extend as needed)
# This assumes replacing expression values by canonical names
# based on typical ADaM clinical variable usage.
mapping <- tribble(
  ~from,     ~to,
  "MEAN",    "AVAL",
  "CODE",    "PARAMCD",
  "STARTDT", "TRTSDT"
)

# Replace expression values by names using the mapping
result <- expressions %>%
  left_join(mapping, by = c("expression" = "from")) %>%
  mutate(expression = if_else(!is.na(to), to, expression)) %>%
  select(name, expression)

# Write result
out_path <- file.path("outputs", "result.csv")
readr::write_csv(result, out_path)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__replace_values_by_names/sample_00/case_01/llm_outputs/result.csv`
- Size: 56 bytes

```csv
name,expression
AVAL,AVAL
PARAMCD,PARAMCD
TRTSDT,TRTSDT
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__replace_values_by_names/sample_00/case_01/stderr.txt`
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
