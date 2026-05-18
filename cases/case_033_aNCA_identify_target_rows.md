# Case 033: pharmaverse/aNCA/identify_target_rows

## Case Metadata

- Task ID: `pharmaverse/aNCA/identify_target_rows`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform identify target rows using the aNCA clinical task contract.

Input: after.tsv, data.tsv, target_groups.tsv, target_impute.tsv, target_params.tsv
Output: result.csv


Required columns for result.csv: target_params, after, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### after.tsv (9 bytes)
after
42

### data.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### target_groups.tsv (28 bytes)
target_groups
"ARM"
"PARAM"

### target_impute.tsv (26 bytes)
target_impute
start_conc0

### target_params.tsv (27 bytes)
target_params
"AUC"
"CMAX"
```

## Input Data

### `after.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/inputs/after.tsv`
- Size: 9 bytes

```text
after
42
```

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/inputs/data.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `target_groups.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/inputs/target_groups.tsv`
- Size: 28 bytes

```text
target_groups
"ARM"
"PARAM"
```

### `target_impute.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/inputs/target_impute.tsv`
- Size: 26 bytes

```text
target_impute
start_conc0
```

### `target_params.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/inputs/target_params.tsv`
- Size: 27 bytes

```text
target_params
"AUC"
"CMAX"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/solution.R`
- Size: 479 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
target_params <- as.character(read_tsv("target_params")[[1]])
after <- read_tsv("after")[[1]][1]
write.csv(data.frame(target_params = target_params, after = rep(after, length(target_params)), result = TRUE, stringsAsFactors = FALSE), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/identify_target_rows/outputs/result.csv`
- Size: 62 bytes

```csv
"target_params","after","result"
"AUC",42,TRUE
"CMAX",42,TRUE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
})

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

after <- fread("inputs/after.tsv")
data <- fread("inputs/data.tsv")
target_groups <- fread("inputs/target_groups.tsv")
target_impute <- fread("inputs/target_impute.tsv")
target_params <- fread("inputs/target_params.tsv")

target_params_vec <- target_params[[1]]
after_val <- after[[1]][1]

result_dt <- data.table(
  target_params = rep(target_params_vec, each = nrow(data)),
  after = after_val,
  result = NA_character_
)

fwrite(result_dt, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__identify_target_rows/sample_00/case_01/llm_outputs/result.csv`
- Size: 112 bytes

```csv
target_params,after,result
AUC,42,
AUC,42,
AUC,42,
AUC,42,
AUC,42,
CMAX,42,
CMAX,42,
CMAX,42,
CMAX,42,
CMAX,42,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__identify_target_rows/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(2, 3) vs llm=(10, 3)"
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
            "reason": "Shape mismatch: ref=(2, 3) vs llm=(10, 3)"
          }
        }
      }
    }
  ]
}
```
