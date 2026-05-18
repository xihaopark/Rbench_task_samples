# Case 193: pharmaverse/sdtmchecks/fail

## Case Metadata

- Task ID: `pharmaverse/sdtmchecks/fail`
- Package: `sdtmchecks`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: simple prompt dropped flattened boolean attributes contract

## Prompt

```text
Write an R script to perform fail using the sdtmchecks clinical task contract.

Input: data.tsv, msg.tsv
Output: result.csv


Required columns for result.csv: result, msg, data_rows, data_cols
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### msg.tsv (38 bytes)
msg
Required SDTM variable is missing
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtmchecks/fail/inputs/data.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `msg.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtmchecks/fail/inputs/msg.tsv`
- Size: 38 bytes

```text
msg
Required SDTM variable is missing
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtmchecks/fail/solution.R`
- Size: 950 bytes

```r
suppressPackageStartupMessages(library(sdtmchecks))

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

msg_df <- read.delim(
  file.path("inputs", "msg.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
data <- read.delim(
  file.path("inputs", "data.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

if (!"msg" %in% names(msg_df) || nrow(msg_df) < 1) {
  stop("inputs/msg.tsv must contain at least one row in a msg column")
}

msg <- as.character(msg_df$msg[[1]])
result <- sdtmchecks::fail(msg = msg, data = data)
result_data <- attr(result, "data", exact = TRUE)
if (!is.data.frame(result_data)) {
  result_data <- data
}

result_df <- data.frame(
  result = unname(as.logical(result)),
  msg = as.character(attr(result, "msg", exact = TRUE)),
  data_rows = nrow(result_data),
  data_cols = ncol(result_data),
  stringsAsFactors = FALSE
)

write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtmchecks/fail/outputs/result.csv`
- Size: 85 bytes

```csv
"result","msg","data_rows","data_cols"
FALSE,"Required SDTM variable is missing",5,4
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
data_path <- file.path("inputs", "data.tsv")
msg_path  <- file.path("inputs", "msg.tsv")

data_df <- read_tsv(data_path, col_types = cols(.default = col_character()))
msg_df  <- read_tsv(msg_path,  col_types = cols(.default = col_character()))

# Prepare result
result <- tibble(
  result    = "FAIL",
  msg       = msg_df$msg[1],
  data_rows = nrow(data_df),
  data_cols = ncol(data_df)
)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtmchecks__fail/sample_00/case_01/llm_outputs/result.csv`
- Size: 74 bytes

```csv
result,msg,data_rows,data_cols
FAIL,Required SDTM variable is missing,5,4
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtmchecks__fail/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric missingness mismatch in column: result"
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
            "reason": "Numeric missingness mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
