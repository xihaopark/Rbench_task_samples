# Case 062: pharmaverse/admiral/compute_duration

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_duration`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform compute duration using the admiral clinical task contract.

Input: add_one.tsv, end_date.tsv, out_unit.tsv, start_date.tsv
Output: result.csv


Required columns for result.csv: start_date, end_date, add_one, out_unit, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### add_one.tsv (24 bytes)
add_one
TRUE
TRUE
FALSE

### end_date.tsv (42 bytes)
end_date
2020-01-10
2020-02-20
2020-03-01

### out_unit.tsv (24 bytes)
out_unit
days
days
days

### start_date.tsv (44 bytes)
start_date
2020-01-01
2020-02-10
2020-03-01
```

## Input Data

### `add_one.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_duration/inputs/add_one.tsv`
- Size: 24 bytes

```text
add_one
TRUE
TRUE
FALSE
```

### `end_date.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_duration/inputs/end_date.tsv`
- Size: 42 bytes

```text
end_date
2020-01-10
2020-02-20
2020-03-01
```

### `out_unit.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_duration/inputs/out_unit.tsv`
- Size: 24 bytes

```text
out_unit
days
days
days
```

### `start_date.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_duration/inputs/start_date.tsv`
- Size: 44 bytes

```text
start_date
2020-01-01
2020-02-10
2020-03-01
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_duration/solution.R`
- Size: 881 bytes

```r
start_date <- as.Date(read.delim(file.path("inputs", "start_date.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$start_date)
end_date <- as.Date(read.delim(file.path("inputs", "end_date.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$end_date)
add_one <- as.logical(read.delim(file.path("inputs", "add_one.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$add_one)
out_unit <- as.character(read.delim(file.path("inputs", "out_unit.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$out_unit)
result <- as.numeric(end_date - start_date) + ifelse(add_one, 1, 0)
result_df <- data.frame(start_date = as.character(start_date), end_date = as.character(end_date), add_one = add_one, out_unit = out_unit, result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_duration/outputs/result.csv`
- Size: 177 bytes

```csv
"start_date","end_date","add_one","out_unit","result"
"2020-01-01","2020-01-10",TRUE,"days",10
"2020-02-10","2020-02-20",TRUE,"days",11
"2020-03-01","2020-03-01",FALSE,"days",0
```

## LLM Generated Code

```r
# Load required packages
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(lubridate)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input files
add_one <- read_tsv(
  file = "inputs/add_one.tsv",
  col_types = cols(
    add_one = col_logical()
  )
)

end_date <- read_tsv(
  file = "inputs/end_date.tsv",
  col_types = cols(
    end_date = col_date(format = "%Y-%m-%d")
  )
)

out_unit <- read_tsv(
  file = "inputs/out_unit.tsv",
  col_types = cols(
    out_unit = col_character()
  )
)

start_date <- read_tsv(
  file = "inputs/start_date.tsv",
  col_types = cols(
    start_date = col_date(format = "%Y-%m-%d")
  )
)

# Combine inputs
dat <- bind_cols(start_date, end_date, add_one, out_unit)

# Compute duration following admiral clinical task contract logic
dat <- dat %>%
  mutate(
    result = case_when(
      out_unit == "days" ~ as.numeric(end_date - start_date),
      out_unit == "weeks" ~ as.numeric(end_date - start_date) / 7,
      out_unit == "months" ~ interval(start_date, end_date) / months(1),
      out_unit == "years" ~ interval(start_date, end_date) / years(1),
      TRUE ~ NA_real_
    ),
    result = if_else(add_one & !is.na(result), result + 1, result)
  )

# Keep required columns only
result <- dat %>%
  select(start_date, end_date, add_one, out_unit, result)

# Write output
write_csv(result, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_duration/sample_00/case_01/llm_outputs/result.csv`
- Size: 149 bytes

```csv
start_date,end_date,add_one,out_unit,result
2020-01-01,2020-01-10,TRUE,days,10
2020-02-10,2020-02-20,TRUE,days,11
2020-03-01,2020-03-01,FALSE,days,0
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_duration/sample_00/case_01/stderr.txt`
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
