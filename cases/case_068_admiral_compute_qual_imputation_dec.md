# Case 068: pharmaverse/admiral/compute_qual_imputation_dec

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_qual_imputation_dec`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform compute qual imputation dec using the admiral clinical task contract.

Input: character_value_decimal.tsv
Output: result.csv


Required columns for result.csv: character_value_decimal, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### character_value_decimal.tsv (50 bytes)
character_value_decimal
5
5.0
5.25
<0.125
12.3000
```

## Input Data

### `character_value_decimal.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation_dec/inputs/character_value_decimal.tsv`
- Size: 50 bytes

```text
character_value_decimal
5
5.0
5.25
<0.125
12.3000
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation_dec/solution.R`
- Size: 544 bytes

```r
character_value_decimal <- as.character(read.delim(file.path("inputs", "character_value_decimal.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$character_value_decimal)
x <- trimws(character_value_decimal)
dot_pos <- regexpr("\\.", x)
result <- ifelse(dot_pos > 0, 1 / (10^(nchar(x) - dot_pos)), 1)
result_df <- data.frame(character_value_decimal = character_value_decimal, result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qual_imputation_dec/outputs/result.csv`
- Size: 94 bytes

```csv
"character_value_decimal","result"
"5",1
"5.0",0.1
"5.25",0.01
"<0.125",0.001
"12.3000",1e-04
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required package
suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
input_path <- file.path("inputs", "character_value_decimal.tsv")
df <- readr::read_tsv(input_path, col_types = cols(.default = "c"))

# Function to compute qualitative imputation (DEC) per admiral clinical task contract
compute_qual_imputation_dec <- function(x) {
  x_trim <- str_trim(x)

  # Missing or blank
  if (is.na(x_trim) || x_trim == "") {
    return(NA_character_)
  }

  # Detect inequality prefix
  prefix <- ""
  core <- x_trim

  if (str_starts(core, "<=")) {
    prefix <- "<="
    core <- str_sub(core, 3)
  } else if (str_starts(core, ">=")) {
    prefix <- ">="
    core <- str_sub(core, 3)
  } else if (str_starts(core, "<")) {
    prefix <- "<"
    core <- str_sub(core, 2)
  } else if (str_starts(core, ">")) {
    prefix <- ">"
    core <- str_sub(core, 2)
  }

  core <- str_trim(core)

  # If remaining is not numeric, return original
  suppressWarnings(num <- as.numeric(core))
  if (is.na(num)) {
    return(x_trim)
  }

  # Remove trailing zeros and decimal point if not needed
  core_std <- format(num, scientific = FALSE, trim = TRUE)
  core_std <- sub("\\.$", "", core_std)

  paste0(prefix, core_std)
}

# Apply computation
result_df <- df %>%
  mutate(
    result = vapply(
      character_value_decimal,
      compute_qual_imputation_dec,
      FUN.VALUE = character(1)
    )
  ) %>%
  select(character_value_decimal, result)

# Write output
output_path <- file.path("outputs", "result.csv")
readr::write_csv(result_df, output_path, na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_qual_imputation_dec/sample_00/case_01/llm_outputs/result.csv`
- Size: 78 bytes

```csv
character_value_decimal,result
5,5
5.0,5
5.25,5.25
<0.125,<0.125
12.3000,12.3
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_qual_imputation_dec/sample_00/case_01/stderr.txt`
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
