# Case 027: pharmaverse/aNCA/get_code

## Case Metadata

- Task ID: `pharmaverse/aNCA/get_code`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform get code using the aNCA clinical task contract.

Input: output_path.tsv, setts_obj.tsv, template_path.tsv
Output: result.csv


Required columns for result.csv: id, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### output_path.tsv (28 bytes)
output_path
"temp_file.txt"

### setts_obj.tsv (35 bytes)
setts_obj
clinical_report_settings

### template_path.tsv (35 bytes)
template_path
"temp_template.pptx"
```

## Input Data

### `output_path.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_code/inputs/output_path.tsv`
- Size: 28 bytes

```text
output_path
"temp_file.txt"
```

### `setts_obj.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_code/inputs/setts_obj.tsv`
- Size: 35 bytes

```text
setts_obj
clinical_report_settings
```

### `template_path.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_code/inputs/template_path.tsv`
- Size: 35 bytes

```text
template_path
"temp_template.pptx"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_code/solution.R`
- Size: 460 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
scalar <- function(x) if (nrow(x) && ncol(x)) as.character(x[[1]][1]) else NA_character_
output_path <- scalar(read_tsv("output_path"))
write.csv(data.frame(id = 1L, result = output_path, stringsAsFactors = FALSE), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_code/outputs/result.csv`
- Size: 32 bytes

```csv
"id","result"
1,"temp_file.txt"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
output_path_df <- read_tsv(
  file = file.path("inputs", "output_path.tsv"),
  col_types = cols(.default = col_character())
)

setts_obj_df <- read_tsv(
  file = file.path("inputs", "setts_obj.tsv"),
  col_types = cols(.default = col_character())
)

template_path_df <- read_tsv(
  file = file.path("inputs", "template_path.tsv"),
  col_types = cols(.default = col_character())
)

# Extract values
output_path <- gsub('"', "", output_path_df$output_path[1])
setts_obj <- setts_obj_df$setts_obj[1]
template_path <- gsub('"', "", template_path_df$template_path[1])

# Placeholder "get code using the aNCA clinical task contract"
# In absence of specification, just combine inputs into a single result row
result_df <- tibble(
  id = "aNCA_clinical_task",
  result = paste(
    "output_path:", output_path,
    "| setts_obj:", setts_obj,
    "| template_path:", template_path
  )
)

# Write result
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__get_code/sample_00/case_01/llm_outputs/result.csv`
- Size: 130 bytes

```csv
id,result
aNCA_clinical_task,output_path: temp_file.txt | setts_obj: clinical_report_settings | template_path: temp_template.pptx
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__get_code/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric missingness mismatch in column: id"
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
            "reason": "Numeric missingness mismatch in column: id"
          }
        }
      }
    }
  ]
}
```
