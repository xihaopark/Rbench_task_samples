# Case 126: pharmaverse/admiral/dthcaus_source

## Case Metadata

- Task ID: `pharmaverse/admiral/dthcaus_source`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform dthcaus source using the admiral clinical task contract.

Input: ds.tsv
Output: result.csv


Required columns for result.csv: dataset_name, mode, filter_expr, date_expr, dthcaus_expr, USUBJID, DSSTDTC, DSTERM
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### ds.tsv (145 bytes)
USUBJID	DSDECOD	DSTERM	DSSTDTC
01	DEATH	Disease progression	2022-02-01
02	COMPLETED	Completed study	2022-01-15
03	DEATH	Adverse event	2022-03-03
```

## Input Data

### `ds.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/dthcaus_source/inputs/ds.tsv`
- Size: 145 bytes

```text
USUBJID	DSDECOD	DSTERM	DSSTDTC
01	DEATH	Disease progression	2022-02-01
02	COMPLETED	Completed study	2022-01-15
03	DEATH	Adverse event	2022-03-03
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/dthcaus_source/solution.R`
- Size: 886 bytes

```r
suppressPackageStartupMessages(library(admiral))

ds <- read.delim(file.path("inputs", "ds.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
src <- suppressWarnings(admiral::dthcaus_source(
  dataset_name = "ds",
  filter = DSDECOD == "DEATH",
  date = admiral::convert_dtc_to_dt(DSSTDTC),
  mode = "first",
  dthcaus = DSTERM
))

death_rows <- ds[ds$DSDECOD == "DEATH", , drop = FALSE]
result <- data.frame(
  dataset_name = src$dataset_name,
  mode = src$mode,
  filter_expr = paste(deparse(src$filter), collapse = " "),
  date_expr = paste(deparse(src$date), collapse = " "),
  dthcaus_expr = paste(deparse(src$dthcaus), collapse = " "),
  USUBJID = death_rows$USUBJID,
  DSSTDTC = death_rows$DSSTDTC,
  DSTERM = death_rows$DSTERM,
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/dthcaus_source/outputs/result.csv`
- Size: 326 bytes

```csv
"dataset_name","mode","filter_expr","date_expr","dthcaus_expr","USUBJID","DSSTDTC","DSTERM"
"ds","first","DSDECOD == ""DEATH""","admiral::convert_dtc_to_dt(DSSTDTC)","DSTERM",1,"2022-02-01","Disease progression"
"ds","first","DSDECOD == ""DEATH""","admiral::convert_dtc_to_dt(DSSTDTC)","DSTERM",3,"2022-03-03","Adverse event"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
ds <- read_tsv(
  file = file.path("inputs", "ds.tsv"),
  col_types = cols(.default = col_character())
)

# Prepare result
result <- ds %>%
  transmute(
    dataset_name = "DS",
    mode         = "source",
    filter_expr  = "DSDECOD == 'DEATH'",
    date_expr    = "DSSTDTC",
    dthcaus_expr = "DSTERM",
    USUBJID,
    DSSTDTC,
    DSTERM
  )

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__dthcaus_source/sample_00/case_01/llm_outputs/result.csv`
- Size: 300 bytes

```csv
dataset_name,mode,filter_expr,date_expr,dthcaus_expr,USUBJID,DSSTDTC,DSTERM
DS,source,DSDECOD == 'DEATH',DSSTDTC,DSTERM,01,2022-02-01,Disease progression
DS,source,DSDECOD == 'DEATH',DSSTDTC,DSTERM,02,2022-01-15,Completed study
DS,source,DSDECOD == 'DEATH',DSSTDTC,DSTERM,03,2022-03-03,Adverse event
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__dthcaus_source/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(2, 8) vs llm=(3, 8)"
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
            "reason": "Shape mismatch: ref=(2, 8) vs llm=(3, 8)"
          }
        }
      }
    }
  ]
}
```
