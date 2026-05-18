# Case 067: pharmaverse/admiral/compute_qual_imputation

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_qual_imputation`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform compute qual imputation using the admiral clinical task contract.

Input: character_value.tsv, factor.tsv, imputation_type.tsv
Output: result.csv


Required columns for result.csv: character_value, factor, imputation_type, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### character_value.tsv (41 bytes)
character_value
<5.0
>10.0
=7.5
12.0
BLQ

### factor.tsv (11 bytes)
factor
0.5

### imputation_type.tsv (25 bytes)
imputation_type
half_min
```

## Input Data

### `character_value.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation/inputs/character_value.tsv`
- Size: 41 bytes

```text
character_value
<5.0
>10.0
=7.5
12.0
BLQ
```

### `factor.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation/inputs/factor.tsv`
- Size: 11 bytes

```text
factor
0.5
```

### `imputation_type.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation/inputs/imputation_type.tsv`
- Size: 25 bytes

```text
imputation_type
half_min
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation/solution.R`
- Size: 966 bytes

```r
character_value <- as.character(read.delim(file.path("inputs", "character_value.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$character_value)
factor <- as.numeric(read.delim(file.path("inputs", "factor.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$factor[1])
imputation_type <- as.character(read.delim(file.path("inputs", "imputation_type.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$imputation_type[1])
clean <- gsub("^[<>=]", "", character_value)
numeric_value <- suppressWarnings(as.numeric(clean))
result <- numeric_value
below <- grepl("^<", character_value)
result[below] <- numeric_value[below] * factor
result[toupper(character_value) == "BLQ"] <- NA_real_
result_df <- data.frame(character_value = character_value, factor = factor, imputation_type = imputation_type, result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation/outputs/result.csv`
- Size: 181 bytes

```csv
"character_value","factor","imputation_type","result"
"<5.0",0.5,"half_min",2.5
">10.0",0.5,"half_min",10
"=7.5",0.5,"half_min",7.5
"12.0",0.5,"half_min",12
"BLQ",0.5,"half_min",NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
character_df <- read_tsv(
  file = file.path("inputs", "character_value.tsv"),
  col_types = cols(.default = col_character())
)

factor_df <- read_tsv(
  file = file.path("inputs", "factor.tsv"),
  col_types = cols(.default = col_double())
)

imputation_df <- read_tsv(
  file = file.path("inputs", "imputation_type.tsv"),
  col_types = cols(.default = col_character())
)

char_vals <- character_df$character_value
factor_val <- factor_df$factor[1]
imputation_type <- imputation_df$imputation_type[1]

# Helper to extract numeric part
extract_numeric <- function(x) {
  x_clean <- str_trim(x)
  x_num <- str_replace_all(x_clean, "^[<>=]+", "")
  suppressWarnings(as.numeric(x_num))
}

# Compute result based on imputation_type
compute_imputation <- function(value, imp_type, factor_val) {
  v_trim <- str_trim(value)
  num_val <- extract_numeric(v_trim)

  if (is.na(num_val)) {
    return(NA_real_)
  }

  if (imp_type == "half_min") {
    if (str_detect(v_trim, "^<")) {
      return(num_val * factor_val)
    } else {
      return(num_val)
    }
  } else {
    return(NA_real_)
  }
}

results <- vapply(char_vals, compute_imputation, numeric(1), imp_type = imputation_type, factor_val = factor_val)

output_df <- tibble(
  character_value = char_vals,
  factor = factor_val,
  imputation_type = imputation_type,
  result = results
)

write_csv(output_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_qual_imputation/sample_00/case_01/llm_outputs/result.csv`
- Size: 151 bytes

```csv
character_value,factor,imputation_type,result
<5.0,0.5,half_min,2.5
>10.0,0.5,half_min,10
=7.5,0.5,half_min,7.5
12.0,0.5,half_min,12
BLQ,0.5,half_min,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_qual_imputation/sample_00/case_01/stderr.txt`
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
