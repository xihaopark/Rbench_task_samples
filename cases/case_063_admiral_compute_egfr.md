# Case 063: pharmaverse/admiral/compute_egfr

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_egfr`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: formula not specified; CKD-EPI vs MDRD

## Prompt

```text
Write an R script to perform compute egfr using the admiral clinical task contract.

Input: age.tsv, creat.tsv, race.tsv, sex.tsv
Output: result.csv, summary.csv


Required columns for result.csv: creat, age, sex, race, result
Required columns for summary.csv: n_rows, n_cols, col_names
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### age.tsv (13 bytes)
age
45
60
72

### creat.tsv (18 bytes)
creat
0.8
1.1
1.4

### race.tsv (43 bytes)
race
OTHER
BLACK OR AFRICAN AMERICAN
OTHER

### sex.tsv (10 bytes)
sex
F
M
F
```

## Input Data

### `age.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/inputs/age.tsv`
- Size: 13 bytes

```text
age
45
60
72
```

### `creat.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/inputs/creat.tsv`
- Size: 18 bytes

```text
creat
0.8
1.1
1.4
```

### `race.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/inputs/race.tsv`
- Size: 43 bytes

```text
race
OTHER
BLACK OR AFRICAN AMERICAN
OTHER
```

### `sex.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/inputs/sex.tsv`
- Size: 10 bytes

```text
sex
F
M
F
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/solution.R`
- Size: 1141 bytes

```r
creat <- as.numeric(read.delim(file.path("inputs", "creat.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$creat)
age <- as.numeric(read.delim(file.path("inputs", "age.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$age)
sex <- as.character(read.delim(file.path("inputs", "sex.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$sex)
race <- as.character(read.delim(file.path("inputs", "race.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$race)
sex_factor <- ifelse(toupper(sex) == "F", 0.742, 1)
race_factor <- ifelse(toupper(race) == "BLACK OR AFRICAN AMERICAN", 1.212, 1)
result <- 175 * creat^(-1.154) * age^(-0.203) * sex_factor * race_factor
result_df <- data.frame(creat = creat, age = age, sex = sex, race = race, result = result, stringsAsFactors = FALSE)
summary_df <- data.frame(n_rows = nrow(result_df), n_cols = ncol(result_df), col_names = paste(names(result_df), collapse = ", "), stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
write.csv(summary_df, file.path("outputs", "summary.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/outputs/result.csv`
- Size: 163 bytes

```csv
"creat","age","sex","race","result"
0.8,45,"F","OTHER",77.566459506687
1.1,60,"M","BLACK OR AFRICAN AMERICAN",82.7577750329383
1.4,72,"F","OTHER",36.9633822946498
```

### `summary.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_egfr/outputs/summary.csv`
- Size: 66 bytes

```csv
"n_rows","n_cols","col_names"
3,5,"creat, age, sex, race, result"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
age_df   <- read_tsv("inputs/age.tsv",   show_col_types = FALSE)
creat_df <- read_tsv("inputs/creat.tsv", show_col_types = FALSE)
race_df  <- read_tsv("inputs/race.tsv",  show_col_types = FALSE)
sex_df   <- read_tsv("inputs/sex.tsv",   show_col_types = FALSE)

# Combine into one data frame
df <- bind_cols(creat_df, age_df, sex_df, race_df)

# Normalize race and sex
df <- df %>%
  mutate(
    race_std = case_when(
      str_to_upper(race) == "BLACK OR AFRICAN AMERICAN" ~ "BLACK",
      TRUE ~ "OTHER"
    ),
    sex_std = case_when(
      str_to_upper(sex) == "F" ~ "F",
      str_to_upper(sex) == "M" ~ "M",
      TRUE ~ NA_character_
    )
  )

# CKD-EPI 2009 creatinine equation (mL/min/1.73m^2)
df <- df %>%
  mutate(
    scr = creat,
    k   = if_else(sex_std == "F", 0.7, 0.9),
    a   = if_else(sex_std == "F", -0.329, -0.411),
    alpha = pmin(scr / k, 1),
    beta  = pmax(scr / k, 1),
    sex_factor  = if_else(sex_std == "F", 1.018, 1.0),
    race_factor = if_else(race_std == "BLACK", 1.159, 1.0),
    result = 141 * (alpha ^ a) * (beta ^ (-1.209)) * (0.993 ^ age) *
      sex_factor * race_factor
  ) %>%
  select(creat, age, sex, race, result)

# Write result.csv
write_csv(df, "outputs/result.csv")

# Prepare and write summary.csv
summary_df <- tibble(
  n_rows   = nrow(df),
  n_cols   = ncol(df),
  col_names = paste(colnames(df), collapse = ",")
)

write_csv(summary_df, "outputs/summary.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_egfr/sample_00/case_01/llm_outputs/result.csv`
- Size: 145 bytes

```csv
creat,age,sex,race,result
0.8,45,F,OTHER,89.03705956423661
1.1,60,M,BLACK OR AFRICAN AMERICAN,84.11876654652023
1.4,72,F,OTHER,37.44273097839041
```

### `summary.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_egfr/sample_00/case_01/llm_outputs/summary.csv`
- Size: 56 bytes

```csv
n_rows,n_cols,col_names
3,5,"creat,age,sex,race,result"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_egfr/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric mismatch in column: result"
        },
        "summary.csv": {
          "match": false,
          "tier": "schema_ok",
          "failure_stage": "value_mismatch",
          "reason": "Value mismatch in column: col_names"
        }
      },
      "returncode": 0,
      "normalizations": [],
      "diagnostics": {
        "expected_artifacts": [
          "result.csv",
          "summary.csv"
        ],
        "produced_artifacts": [
          "result.csv",
          "summary.csv"
        ],
        "staged_artifacts": [
          "result.csv",
          "summary.csv"
        ],
        "missing_artifacts": [],
        "extra_artifacts": [],
        "comparison_reasons": {
          "result.csv": {
            "stage": "value_mismatch",
            "tier": "schema_ok",
            "reason": "Numeric mismatch in column: result"
          },
          "summary.csv": {
            "stage": "value_mismatch",
            "tier": "schema_ok",
            "reason": "Value mismatch in column: col_names"
          }
        }
      }
    }
  ]
}
```
