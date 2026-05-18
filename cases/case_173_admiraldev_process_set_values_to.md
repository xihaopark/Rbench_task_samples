# Case 173: pharmaverse/admiraldev/process_set_values_to

## Case Metadata

- Task ID: `pharmaverse/admiraldev/process_set_values_to`
- Package: `admiraldev`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform process set values to using the admiraldev clinical task contract.

Input: dataset.tsv, expected_type.tsv, expected_types.tsv, set_values_to.tsv
Output: result.csv


Required columns for result.csv: USUBJID, AVAL, BASE, AVISIT, CHG, DTYPE
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (117 bytes)
USUBJID	AVAL	BASE	AVISIT
01-701-1015	104.5	102.0	Week 4
01-701-1023	98.0	100.0	Week 4
01-701-1033	112.2	108.2	Week 8

### expected_type.tsv (42 bytes)
variable	type
CHG	numeric
DTYPE	character

### expected_types.tsv (42 bytes)
variable	type
CHG	numeric
DTYPE	character

### set_values_to.tsv (90 bytes)
variable	expression
CHG	AVAL - BASE
DTYPE	if_else(AVAL >= BASE, "INCREASED", "DECREASED")
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/process_set_values_to/inputs/dataset.tsv`
- Size: 117 bytes

```text
USUBJID	AVAL	BASE	AVISIT
01-701-1015	104.5	102.0	Week 4
01-701-1023	98.0	100.0	Week 4
01-701-1033	112.2	108.2	Week 8
```

### `expected_type.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/process_set_values_to/inputs/expected_type.tsv`
- Size: 42 bytes

```text
variable	type
CHG	numeric
DTYPE	character
```

### `expected_types.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/process_set_values_to/inputs/expected_types.tsv`
- Size: 42 bytes

```text
variable	type
CHG	numeric
DTYPE	character
```

### `set_values_to.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/process_set_values_to/inputs/set_values_to.tsv`
- Size: 90 bytes

```text
variable	expression
CHG	AVAL - BASE
DTYPE	if_else(AVAL >= BASE, "INCREASED", "DECREASED")
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/process_set_values_to/solution.R`
- Size: 981 bytes

```r
suppressPackageStartupMessages(library(admiraldev))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(rlang))

dataset <- read.delim(
  file.path("inputs", "dataset.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
set_values_to_df <- read.delim(
  file.path("inputs", "set_values_to.tsv"),
  check.names = FALSE,
  quote = "",
  stringsAsFactors = FALSE
)
expected_types_df <- read.delim(
  file.path("inputs", "expected_types.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

set_values_to <- setNames(
  lapply(set_values_to_df$expression, rlang::parse_expr),
  set_values_to_df$variable
)
expected_types <- setNames(expected_types_df$type, expected_types_df$variable)

result <- admiraldev::process_set_values_to(
  dataset = dataset,
  set_values_to = set_values_to,
  expected_types = expected_types
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/process_set_values_to/outputs/result.csv`
- Size: 190 bytes

```csv
"USUBJID","AVAL","BASE","AVISIT","CHG","DTYPE"
"01-701-1015",104.5,102,"Week 4",2.5,"INCREASED"
"01-701-1023",98,100,"Week 4",-2,"DECREASED"
"01-701-1033",112.2,108.2,"Week 8",4,"INCREASED"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(rlang)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input datasets
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(.default = col_character())
) %>%
  mutate(
    AVAL = as.numeric(AVAL),
    BASE = as.numeric(BASE)
  )

set_values_to <- read_tsv(
  file = file.path("inputs", "set_values_to.tsv"),
  col_types = cols(
    variable = col_character(),
    expression = col_character()
  )
)

expected_types <- read_tsv(
  file = file.path("inputs", "expected_types.tsv"),
  col_types = cols(
    variable = col_character(),
    type = col_character()
  )
)

# Apply set_values_to expressions
res <- dataset

for (i in seq_len(nrow(set_values_to))) {
  var_name <- set_values_to$variable[i]
  expr_txt <- set_values_to$expression[i]

  # Parse and evaluate expression in the context of res
  expr_parsed <- parse_expr(expr_txt)

  res <- res %>%
    mutate(!!sym(var_name) := !!expr_parsed)
}

# Enforce expected types
for (i in seq_len(nrow(expected_types))) {
  var_name <- expected_types$variable[i]
  var_type <- expected_types$type[i]

  if (!var_name %in% names(res)) next

  if (identical(var_type, "numeric")) {
    res[[var_name]] <- as.numeric(res[[var_name]])
  } else if (identical(var_type, "character")) {
    res[[var_name]] <- as.character(res[[var_name]])
  }
}

# Keep only required columns in specified order
result <- res %>%
  select(USUBJID, AVAL, BASE, AVISIT, CHG, DTYPE)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__process_set_values_to/sample_00/case_01/llm_outputs/result.csv`
- Size: 160 bytes

```csv
USUBJID,AVAL,BASE,AVISIT,CHG,DTYPE
01-701-1015,104.5,102,Week 4,2.5,INCREASED
01-701-1023,98,100,Week 4,-2,DECREASED
01-701-1033,112.2,108.2,Week 8,4,INCREASED
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__process_set_values_to/sample_00/case_01/stderr.txt`
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
