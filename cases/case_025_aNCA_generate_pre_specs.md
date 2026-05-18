# Case 025: pharmaverse/aNCA/generate_pre_specs

## Case Metadata

- Task ID: `pharmaverse/aNCA/generate_pre_specs`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `comparison_error`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: datasets fixture/reference semantics mismatch

## Prompt

```text
Write an R script to perform generate pre specs using the aNCA clinical task contract.

Input: cdisc_data.tsv, datasets.tsv
Output: result.csv


Required columns for result.csv: source, variable, storage_type, n_nonmissing, n_unique
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### cdisc_data.tsv (62 bytes)
USUBJID	AVAL	PARAMCD
101	10.5	CMAX
102	20.3	AUC
103	30.7	CMAX

### datasets.tsv (19 bytes)
datasets
ADPC
ADPP
```

## Input Data

### `cdisc_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_pre_specs/inputs/cdisc_data.tsv`
- Size: 62 bytes

```text
USUBJID	AVAL	PARAMCD
101	10.5	CMAX
102	20.3	AUC
103	30.7	CMAX
```

### `datasets.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_pre_specs/inputs/datasets.tsv`
- Size: 19 bytes

```text
datasets
ADPC
ADPP
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_pre_specs/solution.R`
- Size: 1091 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

read_tsv <- function(name) {
  read.delim(file.path("inputs", name), check.names = FALSE, stringsAsFactors = FALSE)
}

summarize_specs <- function(df, source) {
  if (ncol(df) == 0) {
    return(data.frame(
      source = character(),
      variable = character(),
      storage_type = character(),
      n_nonmissing = integer(),
      n_unique = integer(),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    source = source,
    variable = names(df),
    storage_type = vapply(df, function(x) class(x)[1], character(1)),
    n_nonmissing = vapply(df, function(x) sum(!is.na(x) & nzchar(as.character(x))), integer(1)),
    n_unique = vapply(df, function(x) length(unique(x[!is.na(x) & nzchar(as.character(x))])), integer(1)),
    stringsAsFactors = FALSE
  )
}

cdisc_data <- read_tsv("cdisc_data.tsv")
datasets <- read_tsv("datasets.tsv")
result <- rbind(
  summarize_specs(cdisc_data, "cdisc_data"),
  summarize_specs(datasets, "datasets")
)

write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_pre_specs/outputs/result.csv`
- Size: 209 bytes

```csv
"source","variable","storage_type","n_nonmissing","n_unique"
"cdisc_data","USUBJID","integer",3,3
"cdisc_data","AVAL","numeric",3,3
"cdisc_data","PARAMCD","character",3,2
"datasets","datasets","character",2,2
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(purrr)
  library(fs)
})

# Paths
cdisc_path <- file.path("inputs", "cdisc_data.tsv")
datasets_path <- file.path("inputs", "datasets.tsv")
output_dir <- "outputs"
output_path <- file.path(output_dir, "result.csv")

# Read inputs
cdisc_data <- read_tsv(cdisc_path, col_types = cols(.default = col_character()))
datasets <- read_tsv(datasets_path, col_types = cols(.default = col_character()))$datasets

# Determine storage type
get_storage_type <- function(x) {
  suppressWarnings(num <- as.numeric(x))
  if (all(is.na(x) | !is.na(num))) {
    "numeric"
  } else {
    "character"
  }
}

# Generate result
result <- map_dfr(datasets, function(ds) {
  if (!("PARAMCD" %in% names(cdisc_data))) return(tibble())
  ds_rows <- cdisc_data %>% filter(PARAMCD == ds)
  if (nrow(ds_rows) == 0) return(tibble())
  ds_rows %>%
    select(-PARAMCD) %>%
    imap_dfr(function(col, nm) {
      nonmissing <- sum(!is.na(col) & col != "")
      uniq <- n_distinct(col[!is.na(col) & col != ""])
      tibble(
        source = ds,
        variable = nm,
        storage_type = get_storage_type(col),
        n_nonmissing = nonmissing,
        n_unique = uniq
      )
    })
})

# Ensure output directory
if (!dir_exists(output_dir)) dir_create(output_dir, recurse = TRUE)

# Write result
write_csv(result, output_path)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__generate_pre_specs/sample_00/case_01/llm_outputs/result.csv`
- Size: 0 bytes

```csv

```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__generate_pre_specs/sample_00/case_01/stderr.txt`
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
  "failure_stage": "comparison_error",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "comparison_error",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "comparison_error",
          "reason": "Comparison error: No columns to parse from file"
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
            "stage": "comparison_error",
            "tier": "output_bad",
            "reason": "Comparison error: No columns to parse from file"
          }
        }
      }
    }
  ]
}
```
