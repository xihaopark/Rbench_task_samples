# Case 015: pharmaverse/aNCA/derive_last_dose_time

## Case Metadata

- Task ID: `pharmaverse/aNCA/derive_last_dose_time`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive last dose time using the aNCA clinical task contract.

Input: conc_time_col.tsv, pknca_data.tsv
Output: result.csv


Required columns for result.csv: subject, time, conc
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### conc_time_col.tsv (19 bytes)
conc_time_col
time

### pknca_data.tsv (70 bytes)
subject	time	conc
101	0	0.0
101	1	10.5
101	2	8.2
102	0	0.0
102	1	12.1
```

## Input Data

### `conc_time_col.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/derive_last_dose_time/inputs/conc_time_col.tsv`
- Size: 19 bytes

```text
conc_time_col
time
```

### `pknca_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/derive_last_dose_time/inputs/pknca_data.tsv`
- Size: 70 bytes

```text
subject	time	conc
101	0	0.0
101	1	10.5
101	2	8.2
102	0	0.0
102	1	12.1
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/derive_last_dose_time/solution.R`
- Size: 729 bytes

```r
read_tsv <- function(name) {
  path <- file.path("inputs", name)
  if (!file.exists(path)) {
    stop(name, " is required")
  }
  read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
}

first_column <- function(df) {
  if (ncol(df) == 0) {
    return(character())
  }
  df[[1]]
}

scalar_numeric <- function(df) {
  values <- suppressWarnings(as.numeric(first_column(df)))
  values <- values[!is.na(values)]
  if (length(values) == 0) NA_real_ else values[[1]]
}

write_result <- function(result) {
  dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
  write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE, na = "NA")
}

pknca_data <- read_tsv("pknca_data.tsv")
write_result(pknca_data)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/derive_last_dose_time/outputs/result.csv`
- Size: 72 bytes

```csv
"subject","time","conc"
101,0,0
101,1,10.5
101,2,8.2
102,0,0
102,1,12.1
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
conc_time_col <- read_tsv(
  file = file.path("inputs", "conc_time_col.tsv"),
  col_types = cols()
)

pknca_data <- read_tsv(
  file = file.path("inputs", "pknca_data.tsv"),
  col_types = cols()
)

# Identify concentration time column name
time_col <- conc_time_col$conc_time_col[1]

# Rename columns in pknca_data to required output names
# subject, time, conc
result <- pknca_data %>%
  rename(
    subject = !!sym("subject"),
    time    = !!sym(time_col),
    conc    = !!sym("conc")
  ) %>%
  select(subject, time, conc)

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__derive_last_dose_time/sample_00/case_01/llm_outputs/result.csv`
- Size: 66 bytes

```csv
subject,time,conc
101,0,0
101,1,10.5
101,2,8.2
102,0,0
102,1,12.1
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__derive_last_dose_time/sample_00/case_01/stderr.txt`
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
