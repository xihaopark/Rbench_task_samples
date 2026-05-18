# Case 187: pharmaverse/metatools/dash_to_eq

## Case Metadata

- Task ID: `pharmaverse/metatools/dash_to_eq`
- Package: `metatools`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform dash to eq using the metatools clinical task contract.

Input: id.tsv
Output: result.csv


Required columns for result.csv: id, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### id.tsv (22 bytes)
id
10-20
5-15
0.5-1.5
```

## Input Data

### `id.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/dash_to_eq/inputs/id.tsv`
- Size: 22 bytes

```text
id
10-20
5-15
0.5-1.5
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/dash_to_eq/solution.R`
- Size: 444 bytes

```r
id <- as.character(read.delim(file.path("inputs", "id.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$id)
parts <- strsplit(id, "-", fixed = TRUE)
result <- vapply(parts, function(x) paste0("x >= ", x[[1]], " & x <= ", x[[2]]), character(1))
result_df <- data.frame(id = id, result = result, stringsAsFactors = FALSE)
dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/dash_to_eq/outputs/result.csv`
- Size: 100 bytes

```csv
"id","result"
"10-20","x >= 10 & x <= 20"
"5-15","x >= 5 & x <= 15"
"0.5-1.5","x >= 0.5 & x <= 1.5"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
id_df <- read_tsv(
  file = file.path("inputs", "id.tsv"),
  col_types = cols(
    id = col_character()
  )
)

# Perform dash to eq
result_df <- id_df %>%
  mutate(
    result = str_replace_all(id, "-", "=")
  ) %>%
  select(id, result)

# Write output
write_csv(
  result_df,
  file.path("outputs", "result.csv"),
  na = ""
)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__dash_to_eq/sample_00/case_01/llm_outputs/result.csv`
- Size: 48 bytes

```csv
id,result
10-20,10=20
5-15,5=15
0.5-1.5,0.5=1.5
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__dash_to_eq/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result"
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
            "reason": "Value mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
