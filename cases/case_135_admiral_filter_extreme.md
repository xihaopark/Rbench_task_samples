# Case 135: pharmaverse/admiral/filter_extreme

## Case Metadata

- Task ID: `pharmaverse/admiral/filter_extreme`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform filter extreme using the admiral clinical task contract.

Input: dataset.tsv, mode.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVISITN, AVAL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (89 bytes)
USUBJID	PARAMCD	AVISITN	AVAL
01	ALT	1	22
01	ALT	2	40
01	ALT	3	35
02	ALT	1	18
02	ALT	2	29

### mode.tsv (10 bytes)
mode
last
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_extreme/inputs/dataset.tsv`
- Size: 89 bytes

```text
USUBJID	PARAMCD	AVISITN	AVAL
01	ALT	1	22
01	ALT	2	40
01	ALT	3	35
02	ALT	1	18
02	ALT	2	29
```

### `mode.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_extreme/inputs/mode.tsv`
- Size: 10 bytes

```text
mode
last
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_extreme/solution.R`
- Size: 653 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
mode <- as.character(read.delim(file.path("inputs", "mode.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$mode[1])
dataset <- dataset[order(dataset$USUBJID, dataset$PARAMCD, dataset$AVISITN), , drop = FALSE]
groups <- interaction(dataset$USUBJID, dataset$PARAMCD, drop = TRUE)
idx <- if (mode == "first") {
  !duplicated(groups)
} else {
  !duplicated(groups, fromLast = TRUE)
}
result_df <- dataset[idx, , drop = FALSE]

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_extreme/outputs/result.csv`
- Size: 63 bytes

```csv
"USUBJID","PARAMCD","AVISITN","AVAL"
1,"ALT",3,35
2,"ALT",2,29
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    PARAMCD = col_character(),
    AVISITN = col_double(),
    AVAL = col_double()
  )
)

mode_df <- read_tsv(
  file = file.path("inputs", "mode.tsv"),
  col_types = cols(mode = col_character())
)

mode_val <- tolower(mode_df$mode[1])

# Filter extreme per admiral clinical task contract (mode: first/last)
result <- dataset %>%
  group_by(USUBJID, PARAMCD) %>%
  {
    if (mode_val == "first") {
      slice_min(., order_by = AVISITN, with_ties = FALSE)
    } else if (mode_val == "last") {
      slice_max(., order_by = AVISITN, with_ties = FALSE)
    } else {
      stop("Unsupported mode in mode.tsv. Expected 'first' or 'last'.")
    }
  } %>%
  ungroup() %>%
  select(USUBJID, PARAMCD, AVISITN, AVAL)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__filter_extreme/sample_00/case_01/llm_outputs/result.csv`
- Size: 53 bytes

```csv
USUBJID,PARAMCD,AVISITN,AVAL
01,ALT,3,35
02,ALT,2,29
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__filter_extreme/sample_00/case_01/stderr.txt`
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
