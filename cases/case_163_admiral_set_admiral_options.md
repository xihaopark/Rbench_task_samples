# Case 163: pharmaverse/admiral/set_admiral_options

## Case Metadata

- Task ID: `pharmaverse/admiral/set_admiral_options`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform set admiral options using the admiral clinical task contract.

Input: save_memory.tsv, signif_digits.tsv, subject_keys.tsv
Output: result.csv


Required columns for result.csv: option, value
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### save_memory.tsv (14 bytes)
save_memory
1

### signif_digits.tsv (16 bytes)
signif_digits
8

### subject_keys.tsv (33 bytes)
subject_keys
"STUDYID"
"USUBJID"
```

## Input Data

### `save_memory.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/set_admiral_options/inputs/save_memory.tsv`
- Size: 14 bytes

```text
save_memory
1
```

### `signif_digits.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/set_admiral_options/inputs/signif_digits.tsv`
- Size: 16 bytes

```text
signif_digits
8
```

### `subject_keys.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/set_admiral_options/inputs/subject_keys.tsv`
- Size: 33 bytes

```text
subject_keys
"STUDYID"
"USUBJID"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/set_admiral_options/solution.R`
- Size: 1674 bytes

```r
suppressPackageStartupMessages(library(admiral))

subject_keys_df <- read.delim(file.path("inputs", "subject_keys.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
subject_key_names <- as.character(subject_keys_df[[1]])
subject_key_names <- subject_key_names[nzchar(subject_key_names)]
if (!length(subject_key_names)) {
  stop("subject_keys.tsv must contain at least one subject key")
}
subject_keys <- rlang::exprs(!!!rlang::syms(subject_key_names))

signif_digits_df <- read.delim(file.path("inputs", "signif_digits.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
signif_digits <- suppressWarnings(as.integer(signif_digits_df[[1]][1]))
if (is.na(signif_digits) || signif_digits <= 0) {
  stop("signif_digits.tsv must contain a positive integer")
}

save_memory_df <- read.delim(file.path("inputs", "save_memory.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
save_memory_value <- tolower(as.character(save_memory_df[[1]][1]))
save_memory <- save_memory_value %in% c("true", "t", "1", "yes", "y")

admiral::set_admiral_options(subject_keys = subject_keys, signif_digits = signif_digits, save_memory = save_memory)

result_subject_keys <- vapply(admiral::get_admiral_option("subject_keys"), as.character, character(1))
result_df <- data.frame(
  option = c(rep("subject_keys", length(result_subject_keys)), "signif_digits", "save_memory"),
  value = c(
    result_subject_keys,
    as.character(admiral::get_admiral_option("signif_digits")),
    as.character(admiral::get_admiral_option("save_memory"))
  ),
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/set_admiral_options/outputs/result.csv`
- Size: 108 bytes

```csv
"option","value"
"subject_keys","STUDYID"
"subject_keys","USUBJID"
"signif_digits","8"
"save_memory","TRUE"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)
library(purrr)
library(fs)

# Ensure outputs directory exists
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read inputs
save_memory <- read_tsv(
  file = "inputs/save_memory.tsv",
  col_types = cols(.default = col_character())
) %>%
  slice(1) %>%
  pull(1)

signif_digits <- read_tsv(
  file = "inputs/signif_digits.tsv",
  col_types = cols(.default = col_character())
) %>%
  slice(1) %>%
  pull(1)

subject_keys <- read_tsv(
  file = "inputs/subject_keys.tsv",
  col_types = cols(.default = col_character())
) %>%
  pull(1) %>%
  # remove surrounding quotes if present
  str_replace_all('^"(.*)"$', "\\1") %>%
  paste(collapse = ",")

# Construct result
result <- tibble(
  option = c("save_memory", "signif_digits", "subject_keys"),
  value  = c(save_memory, signif_digits, subject_keys)
)

# Write output
write_csv(result, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__set_admiral_options/sample_00/case_01/llm_outputs/result.csv`
- Size: 74 bytes

```csv
option,value
save_memory,1
signif_digits,8
subject_keys,"STUDYID,USUBJID"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__set_admiral_options/sample_00/case_01/stderr.txt`
- Size: 1333 bytes

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
          "reason": "Shape mismatch: ref=(4, 2) vs llm=(3, 2)"
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
            "reason": "Shape mismatch: ref=(4, 2) vs llm=(3, 2)"
          }
        }
      }
    }
  ]
}
```
