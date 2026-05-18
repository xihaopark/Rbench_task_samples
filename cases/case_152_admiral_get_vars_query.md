# Case 152: pharmaverse/admiral/get_vars_query

## Case Metadata

- Task ID: `pharmaverse/admiral/get_vars_query`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform get vars query using the admiral clinical task contract.

Input: dataset.tsv, dataset_queries.tsv
Output: result.csv


Required columns for result.csv: QUERY_ID, USUBJID, SRCVAR, SRCVAL, TERMCHAR
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (110 bytes)
USUBJID	AETERM	AEREL	AESEV
01	HEADACHE	RELATED	MILD
02	NAUSEA	NOT RELATED	MODERATE
03	HEADACHE	RELATED	SEVERE

### dataset_queries.tsv (61 bytes)
QUERY_ID	SRCVAR	TERMCHAR
Q1	AETERM	HEADACHE
Q2	AEREL	RELATED
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_vars_query/inputs/dataset.tsv`
- Size: 110 bytes

```text
USUBJID	AETERM	AEREL	AESEV
01	HEADACHE	RELATED	MILD
02	NAUSEA	NOT RELATED	MODERATE
03	HEADACHE	RELATED	SEVERE
```

### `dataset_queries.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_vars_query/inputs/dataset_queries.tsv`
- Size: 61 bytes

```text
QUERY_ID	SRCVAR	TERMCHAR
Q1	AETERM	HEADACHE
Q2	AEREL	RELATED
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_vars_query/solution.R`
- Size: 696 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
queries <- read.delim(file.path("inputs", "dataset_queries.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
pieces <- lapply(seq_len(nrow(queries)), function(i) {
  q <- queries[i, , drop = FALSE]
  src <- q$SRCVAR[1]
  hit <- dataset[[src]] == q$TERMCHAR[1]
  data.frame(QUERY_ID = q$QUERY_ID[1], USUBJID = dataset$USUBJID[hit], SRCVAR = src, SRCVAL = dataset[[src]][hit], TERMCHAR = q$TERMCHAR[1], stringsAsFactors = FALSE)
})
result_df <- do.call(rbind, pieces)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/get_vars_query/outputs/result.csv`
- Size: 196 bytes

```csv
"QUERY_ID","USUBJID","SRCVAR","SRCVAL","TERMCHAR"
"Q1",1,"AETERM","HEADACHE","HEADACHE"
"Q1",3,"AETERM","HEADACHE","HEADACHE"
"Q2",1,"AEREL","RELATED","RELATED"
"Q2",3,"AEREL","RELATED","RELATED"
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

# Read input datasets
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(.default = col_character())
)

queries <- read_tsv(
  file = file.path("inputs", "dataset_queries.tsv"),
  col_types = cols(.default = col_character())
)

# Perform get vars query
results_list <- lapply(seq_len(nrow(queries)), function(i) {
  q <- queries[i, ]
  var <- q$SRCVAR
  term <- q$TERMCHAR

  if (!var %in% names(dataset)) {
    return(NULL)
  }

  ds_sub <- dataset %>%
    filter(.data[[var]] == term) %>%
    mutate(
      QUERY_ID = q$QUERY_ID,
      SRCVAR   = var,
      SRCVAL   = .data[[var]],
      TERMCHAR = term,
      .keep = "all"
    ) %>%
    select(QUERY_ID, USUBJID, SRCVAR, SRCVAL, TERMCHAR)

  if (nrow(ds_sub) == 0) {
    return(NULL)
  }

  ds_sub
})

result <- bind_rows(results_list)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_vars_query/sample_00/case_01/llm_outputs/result.csv`
- Size: 158 bytes

```csv
QUERY_ID,USUBJID,SRCVAR,SRCVAL,TERMCHAR
Q1,01,AETERM,HEADACHE,HEADACHE
Q1,03,AETERM,HEADACHE,HEADACHE
Q2,01,AEREL,RELATED,RELATED
Q2,03,AEREL,RELATED,RELATED
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__get_vars_query/sample_00/case_01/stderr.txt`
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
