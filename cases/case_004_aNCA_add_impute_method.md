# Case 004: pharmaverse/aNCA/add_impute_method

## Case Metadata

- Task ID: `pharmaverse/aNCA/add_impute_method`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform add impute method using the aNCA clinical task contract.

Input: after.tsv, impute_vals.tsv, target_impute.tsv
Output: result.csv


Required columns for result.csv: impute_vals, after, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### after.tsv (8 bytes)
after
1

### impute_vals.tsv (76 bytes)
impute_vals
start_predose
start_predose,end_obs
end_obs
start_conc0,end_obs

### target_impute.tsv (26 bytes)
target_impute
start_conc0
```

## Input Data

### `after.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/add_impute_method/inputs/after.tsv`
- Size: 8 bytes

```text
after
1
```

### `impute_vals.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/add_impute_method/inputs/impute_vals.tsv`
- Size: 76 bytes

```text
impute_vals
start_predose
start_predose,end_obs
end_obs
start_conc0,end_obs
```

### `target_impute.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/add_impute_method/inputs/target_impute.tsv`
- Size: 26 bytes

```text
target_impute
start_conc0
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/add_impute_method/solution.R`
- Size: 1116 bytes

```r
read_table <- function(name) {
  read.delim(file.path("inputs", name), check.names = FALSE, stringsAsFactors = FALSE)
}

first_value <- function(df, default = "") {
  if (nrow(df) == 0 || ncol(df) == 0 || is.na(df[[1]][[1]])) return(default)
  as.character(df[[1]][[1]])
}

insert_impute <- function(value, target, after) {
  parts <- unlist(strsplit(ifelse(is.na(value), "", as.character(value)), "[ ,]+"))
  parts <- parts[nzchar(parts) & parts != target]
  paste(append(parts, target, after = after), collapse = ",")
}

impute_vals <- read_table("impute_vals.tsv")[[1]]
target <- first_value(read_table("target_impute.tsv"))
after_raw <- suppressWarnings(as.integer(first_value(read_table("after.tsv"), "0")))
after <- ifelse(is.na(after_raw), 0L, max(0L, after_raw))
result_value <- vapply(impute_vals, insert_impute, character(1), target = target, after = after)
result <- data.frame(impute_vals = impute_vals, after = after, result = result_value, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/add_impute_method/outputs/result.csv`
- Size: 219 bytes

```csv
"impute_vals","after","result"
"start_predose",1,"start_predose,start_conc0"
"start_predose,end_obs",1,"start_predose,start_conc0,end_obs"
"end_obs",1,"end_obs,start_conc0"
"start_conc0,end_obs",1,"end_obs,start_conc0"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
after_df <- fread("inputs/after.tsv", sep = "\t", header = TRUE)
impute_df <- fread("inputs/impute_vals.tsv", sep = "\t", header = TRUE)
target_df <- fread("inputs/target_impute.tsv", sep = "\t", header = TRUE)

# Ensure required columns exist
if (!("after" %in% names(after_df))) stop("after.tsv must contain column 'after'")
if (!("impute_vals" %in% names(impute_df))) stop("impute_vals.tsv must contain column 'impute_vals'")
if (!("target_impute" %in% names(target_df))) stop("target_impute.tsv must contain column 'target_impute'")

# 'Add impute' method: select rows from impute_vals that contain the target_impute token
target_token <- target_df$target_impute[1]

contains_token <- function(x, token) {
  # split on comma and check if token is one of the elements
  sapply(strsplit(x, ","), function(v) token %in% v)
}

matches <- impute_df[contains_token(impute_df$impute_vals, target_token), ]

# If no matches, result is empty
if (nrow(matches) == 0) {
  result_df <- data.table(
    impute_vals = character(0),
    after       = numeric(0),
    result      = character(0)
  )
} else {
  # Repeat 'after' value for each matching impute_vals
  after_val <- after_df$after[1]
  result_df <- data.table(
    impute_vals = matches$impute_vals,
    after       = after_val,
    result      = matches$impute_vals
  )
}

# Write output
fwrite(result_df, file = "outputs/result.csv", sep = ",", quote = TRUE, row.names = FALSE)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__add_impute_method/sample_00/case_01/llm_outputs/result.csv`
- Size: 77 bytes

```csv
"impute_vals","after","result"
"start_conc0,end_obs",1,"start_conc0,end_obs"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__add_impute_method/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(4, 3) vs llm=(1, 3)"
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
            "reason": "Shape mismatch: ref=(4, 3) vs llm=(1, 3)"
          }
        }
      }
    }
  ]
}
```
