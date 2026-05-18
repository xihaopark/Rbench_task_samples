# Case 171: pharmaverse/admiraldev/is_valid_dtc

## Case Metadata

- Task ID: `pharmaverse/admiraldev/is_valid_dtc`
- Package: `admiraldev`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform is valid dtc using the admiraldev clinical task contract.

Input: arg.tsv
Output: result.csv


Required columns for result.csv: arg, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### arg.tsv (60 bytes)
arg
2020
2020-05
2020-05-20
2020-05-20T12:30:45
20-MAY-2020
```

## Input Data

### `arg.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/is_valid_dtc/inputs/arg.tsv`
- Size: 60 bytes

```text
arg
2020
2020-05
2020-05-20
2020-05-20T12:30:45
20-MAY-2020
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/is_valid_dtc/solution.R`
- Size: 410 bytes

```r
arg <- as.character(read.delim(file.path("inputs", "arg.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$arg)
pattern <- "^[0-9]{4}(-[0-9]{2}(-[0-9]{2}(T[0-9]{2}(:[0-9]{2}(:[0-9]{2})?)?)?)?)?$"
result_df <- data.frame(arg = arg, result = grepl(pattern, arg), stringsAsFactors = FALSE)
dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldev/is_valid_dtc/outputs/result.csv`
- Size: 107 bytes

```csv
"arg","result"
"2020",TRUE
"2020-05",TRUE
"2020-05-20",TRUE
"2020-05-20T12:30:45",TRUE
"20-MAY-2020",FALSE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(admiraldev)
})

# Input / output paths
in_file  <- file.path("inputs", "arg.tsv")
out_dir  <- "outputs"
out_file <- file.path(out_dir, "result.csv")

if (!dir.exists(out_dir)) {
  dir.create(out_dir, recursive = TRUE)
}

# Read input
arg_df <- read_tsv(in_file, show_col_types = FALSE)

# Validate DTC using admiraldev clinical task contract
res_df <- arg_df %>%
  mutate(
    result = purrr::map_chr(
      arg,
      ~ {
        val <- tryCatch(
          {
            admiraldev::is_valid_dtc(.x)
          },
          error = function(e) NA
        )
        if (is.na(val)) {
          "ERROR"
        } else if (isTRUE(val)) {
          "TRUE"
        } else {
          "FALSE"
        }
      }
    )
  ) %>%
  select(arg, result)

# Write output
write_csv(res_df, out_file)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__is_valid_dtc/sample_00/case_01/llm_outputs/result.csv`
- Size: 93 bytes

```csv
arg,result
2020,TRUE
2020-05,TRUE
2020-05-20,TRUE
2020-05-20T12:30:45,TRUE
20-MAY-2020,FALSE
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldev__is_valid_dtc/sample_00/case_01/stderr.txt`
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
