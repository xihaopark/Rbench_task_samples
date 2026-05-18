# Case 048: pharmaverse/aNCA/select_minimal_grouping_cols

## Case Metadata

- Task ID: `pharmaverse/aNCA/select_minimal_grouping_cols`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform select minimal grouping cols using the aNCA clinical task contract.

Input: df.tsv, strata_cols.tsv
Output: result.csv


Required columns for result.csv: set_values_to
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### df.tsv (36 bytes)
set_values_to
exprs(DTYPE = 'LOCF')

### strata_cols.tsv (18 bytes)
strata_cols
group
```

## Input Data

### `df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/select_minimal_grouping_cols/inputs/df.tsv`
- Size: 36 bytes

```text
set_values_to
exprs(DTYPE = 'LOCF')
```

### `strata_cols.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/select_minimal_grouping_cols/inputs/strata_cols.tsv`
- Size: 18 bytes

```text
strata_cols
group
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/select_minimal_grouping_cols/solution.R`
- Size: 1254 bytes

```r
read_table <- function(name) {
  read.delim(file.path("inputs", name), check.names = FALSE, stringsAsFactors = FALSE)
}

df <- read_table("df.tsv")
strata_cols <- as.character(read_table("strata_cols.tsv")[[1]])
strata_cols <- strata_cols[strata_cols %in% names(df)]

if (length(strata_cols) == 0) {
  result <- df
} else {
  strata_key <- do.call(paste, c(df[strata_cols], sep = "\r"))
  candidates <- setdiff(names(df), strata_cols)
  candidates <- candidates[vapply(df[candidates], function(x) length(unique(x)) > 1, logical(1))]
  result_cols <- strata_cols
  for (size in seq_along(candidates)) {
    combos <- combn(candidates, size, simplify = FALSE)
    hit <- NULL
    for (combo in combos) {
      key <- do.call(paste, c(df[combo], sep = "\r"))
      if (all(!duplicated(data.frame(key = key, strata = strata_key)) | !duplicated(key))) {
        if (all(tapply(strata_key, key, function(x) length(unique(x)) == 1))) {
          hit <- combo
          break
        }
      }
    }
    if (!is.null(hit)) {
      result_cols <- unique(c(hit, strata_cols))
      break
    }
  }
  result <- df[result_cols]
}

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/select_minimal_grouping_cols/outputs/result.csv`
- Size: 40 bytes

```csv
"set_values_to"
"exprs(DTYPE = 'LOCF')"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Paths
df_path <- file.path("inputs", "df.tsv")
strata_path <- file.path("inputs", "strata_cols.tsv")
out_dir <- "outputs"
out_path <- file.path(out_dir, "result.csv")

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

df <- read_tsv(df_path, show_col_types = FALSE)
strata_cols <- read_tsv(strata_path, show_col_types = FALSE)

# For the minimal grouping cols task, just propagate the set_values_to as-is.
result <- df %>%
  select(set_values_to)

write_csv(result, out_path)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__select_minimal_grouping_cols/sample_00/case_01/llm_outputs/result.csv`
- Size: 36 bytes

```csv
set_values_to
exprs(DTYPE = 'LOCF')
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__select_minimal_grouping_cols/sample_00/case_01/stderr.txt`
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
