# Case 181: pharmaverse/logrx/log_config

## Case Metadata

- Task ID: `pharmaverse/logrx/log_config`
- Package: `logrx`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: logging side effect graded by CSV summary

## Prompt

```text
Write an R script to perform log config using the logrx clinical task contract.

Input: extra_info.tsv, file.tsv, log_name.tsv, log_path.tsv
Output: result.csv


Required columns for result.csv: key, value
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### extra_info.tsv (52 bytes)
key	value
project	clinical_pilot
run_type	reference

### file.tsv (16 bytes)
file
analysis.R

### log_name.tsv (22 bytes)
log_name
analysis_run

### log_path.tsv (22 bytes)
log_path
outputs/logs
```

## Input Data

### `extra_info.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/logrx/log_config/inputs/extra_info.tsv`
- Size: 52 bytes

```text
key	value
project	clinical_pilot
run_type	reference
```

### `file.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/logrx/log_config/inputs/file.tsv`
- Size: 16 bytes

```text
file
analysis.R
```

### `log_name.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/logrx/log_config/inputs/log_name.tsv`
- Size: 22 bytes

```text
log_name
analysis_run
```

### `log_path.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/logrx/log_config/inputs/log_path.tsv`
- Size: 22 bytes

```text
log_path
outputs/logs
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/logrx/log_config/solution.R`
- Size: 800 bytes

```r
file <- read.delim(file.path("inputs", "file.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$file[1]
log_name <- read.delim(file.path("inputs", "log_name.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$log_name[1]
log_path <- read.delim(file.path("inputs", "log_path.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$log_path[1]
extra <- read.delim(file.path("inputs", "extra_info.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result <- rbind(
  data.frame(key = c("file", "log_name", "log_path"), value = c(file, log_name, log_path), stringsAsFactors = FALSE),
  data.frame(key = paste0("extra.", extra$key), value = extra$value, stringsAsFactors = FALSE)
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/logrx/log_config/outputs/result.csv`
- Size: 148 bytes

```csv
"key","value"
"file","analysis.R"
"log_name","analysis_run"
"log_path","outputs/logs"
"extra.project","clinical_pilot"
"extra.run_type","reference"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

extra_info <- read_tsv(
  file = file.path("inputs", "extra_info.tsv"),
  col_types = cols(.default = col_character())
)

file_df <- read_tsv(
  file = file.path("inputs", "file.tsv"),
  col_types = cols(.default = col_character())
)

log_name_df <- read_tsv(
  file = file.path("inputs", "log_name.tsv"),
  col_types = cols(.default = col_character())
)

log_path_df <- read_tsv(
  file = file.path("inputs", "log_path.tsv"),
  col_types = cols(.default = col_character())
)

project <- extra_info %>% filter(key == "project") %>% pull(value)
run_type <- extra_info %>% filter(key == "run_type") %>% pull(value)
script_file <- file_df$file[1]
log_name <- log_name_df$log_name[1]
log_path <- log_path_df$log_path[1]

log_file_full <- file.path(log_path, paste0(log_name, ".log"))

result <- tibble(
  key = c(
    "project",
    "run_type",
    "script_file",
    "log_name",
    "log_path",
    "log_file"
  ),
  value = c(
    project,
    run_type,
    script_file,
    log_name,
    log_path,
    log_file_full
  )
)

write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__logrx__log_config/sample_00/case_01/llm_outputs/result.csv`
- Size: 158 bytes

```csv
key,value
project,clinical_pilot
run_type,reference
script_file,analysis.R
log_name,analysis_run
log_path,outputs/logs
log_file,outputs/logs/analysis_run.log
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__logrx__log_config/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(5, 2) vs llm=(6, 2)"
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
            "reason": "Shape mismatch: ref=(5, 2) vs llm=(6, 2)"
          }
        }
      }
    }
  ]
}
```
