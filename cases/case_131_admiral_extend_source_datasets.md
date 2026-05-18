# Case 131: pharmaverse/admiral/extend_source_datasets

## Case Metadata

- Task ID: `pharmaverse/admiral/extend_source_datasets`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform extend source datasets using the admiral clinical task contract.

Input: adlb.tsv, adsl.tsv, by_vars.tsv
Output: result.csv


Required columns for result.csv: dataset, n_rows, n_cols, columns
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### adlb.tsv (41 bytes)
USUBJID	PARAMCD	AVAL
01	ALT	35
02	ALT	28

### adsl.tsv (36 bytes)
USUBJID	TRT01P
01	Drug A
02	Placebo

### by_vars.tsv (12 bytes)
var
USUBJID
```

## Input Data

### `adlb.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extend_source_datasets/inputs/adlb.tsv`
- Size: 41 bytes

```text
USUBJID	PARAMCD	AVAL
01	ALT	35
02	ALT	28
```

### `adsl.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extend_source_datasets/inputs/adsl.tsv`
- Size: 36 bytes

```text
USUBJID	TRT01P
01	Drug A
02	Placebo
```

### `by_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extend_source_datasets/inputs/by_vars.tsv`
- Size: 12 bytes

```text
var
USUBJID
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extend_source_datasets/solution.R`
- Size: 950 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

adsl <- read.delim(file.path("inputs", "adsl.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
adlb <- read.delim(file.path("inputs", "adlb.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
vars <- read.delim(file.path("inputs", "by_vars.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$var
by_vars <- as.list(lapply(vars, sym))
source_datasets <- list(adsl = adsl, adlb = adlb)
extended <- admiral:::extend_source_datasets(source_datasets, by_vars = by_vars)
result <- data.frame(
  dataset = names(extended),
  n_rows = vapply(extended, nrow, integer(1)),
  n_cols = vapply(extended, ncol, integer(1)),
  columns = vapply(extended, function(x) paste(names(x), collapse = ","), character(1)),
  stringsAsFactors = FALSE
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/extend_source_datasets/outputs/result.csv`
- Size: 100 bytes

```csv
"dataset","n_rows","n_cols","columns"
"adsl",2,2,"USUBJID,TRT01P"
"adlb",2,3,"USUBJID,PARAMCD,AVAL"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(purrr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
adlb <- read_tsv(
  file = file.path("inputs", "adlb.tsv"),
  col_types = cols(.default = col_character())
)

adsl <- read_tsv(
  file = file.path("inputs", "adsl.tsv"),
  col_types = cols(.default = col_character())
)

by_vars <- read_tsv(
  file = file.path("inputs", "by_vars.tsv"),
  col_types = cols(.default = col_character())
)

by_vec <- by_vars$var

# Function to summarize a dataset
summarize_dataset <- function(df, name) {
  tibble(
    dataset = name,
    n_rows = nrow(df),
    n_cols = ncol(df),
    columns = paste(names(df), collapse = ",")
  )
}

# For this task, "extend source datasets using the admiral clinical task contract"
# is interpreted as: ensure that BY variables exist in source datasets by
# performing left joins where appropriate (a common ADaM extension step).

# Ensure BY vars present: join ADLB with ADSL on BY vars (if all BY vars exist)
if (all(by_vec %in% names(adlb)) && all(by_vec %in% names(adsl))) {
  adlb_extended <- adlb %>%
    left_join(adsl, by = by_vec)
} else {
  adlb_extended <- adlb
}

# Summarize datasets (original and extended)
result <- bind_rows(
  summarize_dataset(adlb, "ADLB"),
  summarize_dataset(adsl, "ADSL"),
  summarize_dataset(adlb_extended, "ADLB_EXTENDED")
)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__extend_source_datasets/sample_00/case_01/llm_outputs/result.csv`
- Size: 136 bytes

```csv
dataset,n_rows,n_cols,columns
ADLB,2,3,"USUBJID,PARAMCD,AVAL"
ADSL,2,2,"USUBJID,TRT01P"
ADLB_EXTENDED,2,4,"USUBJID,PARAMCD,AVAL,TRT01P"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__extend_source_datasets/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(2, 4) vs llm=(3, 4)"
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
            "reason": "Shape mismatch: ref=(2, 4) vs llm=(3, 4)"
          }
        }
      }
    }
  ]
}
```
