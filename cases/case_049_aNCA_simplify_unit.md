# Case 049: pharmaverse/aNCA/simplify_unit

## Case Metadata

- Task ID: `pharmaverse/aNCA/simplify_unit`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform simplify unit using the aNCA clinical task contract.

Input: as_character.tsv, x.tsv
Output: result.csv


Required columns for result.csv: x, as_character, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### as_character.tsv (24 bytes)
as_character
TRUE
FALSE

### x.tsv (13 bytes)
x
mg/L
ng/mL
```

## Input Data

### `as_character.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/simplify_unit/inputs/as_character.tsv`
- Size: 24 bytes

```text
as_character
TRUE
FALSE
```

### `x.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/simplify_unit/inputs/x.tsv`
- Size: 13 bytes

```text
x
mg/L
ng/mL
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/simplify_unit/solution.R`
- Size: 517 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
x <- as.character(read_tsv("x")[[1]])
as_character <- as.character(read_tsv("as_character")[[1]])
n <- max(length(x), length(as_character))
write.csv(data.frame(x = rep_len(x, n), as_character = rep_len(as_character, n), result = rep_len(x, n), stringsAsFactors = FALSE), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/simplify_unit/outputs/result.csv`
- Size: 73 bytes

```csv
"x","as_character","result"
"mg/L","TRUE","mg/L"
"ng/mL","FALSE","ng/mL"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
as_character_df <- read_tsv("inputs/as_character.tsv", show_col_types = FALSE)
x_df            <- read_tsv("inputs/x.tsv", show_col_types = FALSE)

# Coerce as_character column to logical
as_character_logical <- as.logical(as_character_df$as_character)

# Simplify unit function (example behavior; adjust as per aNCA spec if needed)
simplify_unit <- function(unit, as_character) {
  u <- trimws(unit)
  if (as_character) {
    # Return simplified / canonical string
    return(u)
  } else {
    # Return numeric multiplier relative to the unit itself (identity)
    return(1)
  }
}

# Apply row-wise for all combinations (recycling like R would)
n <- max(nrow(x_df), length(as_character_logical))
x_vals  <- rep(x_df$x, length.out = n)
ac_vals <- rep(as_character_logical, length.out = n)

result_vals <- mapply(simplify_unit, x_vals, ac_vals, USE.NAMES = FALSE)

# Build result data frame
result_df <- tibble(
  x            = x_vals,
  as_character = ac_vals,
  result       = result_vals
)

# Write CSV
write_csv(result_df, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__simplify_unit/sample_00/case_01/llm_outputs/result.csv`
- Size: 51 bytes

```csv
x,as_character,result
mg/L,TRUE,mg/L
ng/mL,FALSE,1
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__simplify_unit/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result"
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
            "reason": "Value mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
