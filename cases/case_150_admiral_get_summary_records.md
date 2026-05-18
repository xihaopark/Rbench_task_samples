# Case 150: pharmaverse/admiral/get_summary_records

## Case Metadata

- Task ID: `pharmaverse/admiral/get_summary_records`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform get summary records using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, N, MEAN, MIN, MAX
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (71 bytes)
USUBJID	PARAMCD	AVAL
01	ALT	20
01	ALT	30
01	AST	18
02	ALT	40
02	ALT	50
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_summary_records/inputs/dataset.tsv`
- Size: 71 bytes

```text
USUBJID	PARAMCD	AVAL
01	ALT	20
01	ALT	30
01	AST	18
02	ALT	40
02	ALT	50
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_summary_records/solution.R`
- Size: 649 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
keys <- unique(dataset[c("USUBJID", "PARAMCD")])
pieces <- lapply(seq_len(nrow(keys)), function(i) {
  hit <- dataset$USUBJID == keys$USUBJID[i] & dataset$PARAMCD == keys$PARAMCD[i]
  values <- dataset$AVAL[hit]
  data.frame(USUBJID = keys$USUBJID[i], PARAMCD = keys$PARAMCD[i], N = length(values), MEAN = mean(values), MIN = min(values), MAX = max(values), stringsAsFactors = FALSE)
})
result_df <- do.call(rbind, pieces)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_summary_records/outputs/result.csv`
- Size: 100 bytes

```csv
"USUBJID","PARAMCD","N","MEAN","MIN","MAX"
1,"ALT",2,25,20,30
1,"AST",1,18,18,18
2,"ALT",2,45,40,50
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
adsl <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    PARAMCD = col_character(),
    AVAL = col_double()
  )
)

# Derive summary records
result <- adsl %>%
  group_by(USUBJID, PARAMCD) %>%
  summarise(
    N    = n(),
    MEAN = mean(AVAL, na.rm = TRUE),
    MIN  = min(AVAL, na.rm = TRUE),
    MAX  = max(AVAL, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(USUBJID, PARAMCD)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_summary_records/sample_00/case_01/llm_outputs/result.csv`
- Size: 85 bytes

```csv
USUBJID,PARAMCD,N,MEAN,MIN,MAX
01,ALT,2,25,20,30
01,AST,1,18,18,18
02,ALT,2,45,40,50
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_summary_records/sample_00/case_01/stderr.txt`
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
