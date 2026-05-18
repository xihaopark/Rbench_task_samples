# Case 058: pharmaverse/admiral/compute_age_years

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_age_years`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform compute age years using the admiral clinical task contract.

Input: age.tsv, age_unit.tsv
Output: result.csv


Required columns for result.csv: age, age_unit, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### age.tsv (18 bytes)
age
18
24
104
365

### age_unit.tsv (33 bytes)
age_unit
years
months
weeks
days
```

## Input Data

### `age.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_age_years/inputs/age.tsv`
- Size: 18 bytes

```text
age
18
24
104
365
```

### `age_unit.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_age_years/inputs/age_unit.tsv`
- Size: 33 bytes

```text
age_unit
years
months
weeks
days
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_age_years/solution.R`
- Size: 516 bytes

```r
suppressPackageStartupMessages(library(admiral))

age <- as.numeric(read.delim(file.path("inputs", "age.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$age)
age_unit <- as.character(read.delim(file.path("inputs", "age_unit.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$age_unit)
result <- admiral::compute_age_years(age, age_unit)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(age = age, age_unit = age_unit, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_age_years/outputs/result.csv`
- Size: 112 bytes

```csv
"age","age_unit","result"
18,"years",18
24,"months",2
104,"weeks",1.99315537303217
365,"days",0.999315537303217
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input files
age_df <- read_tsv(
  file = file.path("inputs", "age.tsv"),
  col_types = cols(
    age = col_double()
  )
)

age_unit_df <- read_tsv(
  file = file.path("inputs", "age_unit.tsv"),
  col_types = cols(
    age_unit = col_character()
  )
)

# Combine inputs assuming row-wise correspondence
df <- bind_cols(age_df, age_unit_df)

# Compute age in years according to unit
df_res <- df %>%
  mutate(
    result = case_when(
      age_unit == "years"  ~ age,
      age_unit == "months" ~ age / 12,
      age_unit == "weeks"  ~ age / (365.25 / 7),
      age_unit == "days"   ~ age / 365.25,
      TRUE ~ NA_real_
    )
  ) %>%
  select(age, age_unit, result)

# Write result
write_csv(df_res, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_age_years/sample_00/case_01/llm_outputs/result.csv`
- Size: 100 bytes

```csv
age,age_unit,result
18,years,18
24,months,2
104,weeks,1.9931553730321696
365,days,0.999315537303217
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_age_years/sample_00/case_01/stderr.txt`
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
