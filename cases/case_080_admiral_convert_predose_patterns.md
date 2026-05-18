# Case 080: pharmaverse/admiral/convert_predose_patterns

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_predose_patterns`
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
Write an R script to perform convert predose patterns using the admiral clinical task contract.

Input: na_idx.tsv, result.tsv, xxtpt.tsv
Output: result.csv


Required columns for result.csv: xxtpt, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### na_idx.tsv (30 bytes)
na_idx
FALSE
FALSE
FALSE
TRUE

### result.tsv (18 bytes)
result
NA
NA
1
NA

### xxtpt.tsv (61 bytes)
xxtpt
15 min predose
2 hr before
1 hour postdose
UNSCHEDULED
```

## Input Data

### `na_idx.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_predose_patterns/inputs/na_idx.tsv`
- Size: 30 bytes

```text
na_idx
FALSE
FALSE
FALSE
TRUE
```

### `result.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_predose_patterns/inputs/result.tsv`
- Size: 18 bytes

```text
result
NA
NA
1
NA
```

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_predose_patterns/inputs/xxtpt.tsv`
- Size: 61 bytes

```text
xxtpt
15 min predose
2 hr before
1 hour postdose
UNSCHEDULED
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_predose_patterns/solution.R`
- Size: 1008 bytes

```r
suppressPackageStartupMessages(library(stringr))

xxtpt <- read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$xxtpt
result <- read.delim(file.path("inputs", "result.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$result
result <- suppressWarnings(as.numeric(result))
na_idx <- read.delim(file.path("inputs", "na_idx.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$na_idx
na_idx <- as.logical(na_idx)

pattern <- regex("^(?<value>\\d+(?:\\.\\d+)?)\\s*(?<unit>m(?:in|inute)?|h(?:r|our)?)s?\\s+(?:pre-?dose|before)$", ignore_case = TRUE)
matches <- str_match(xxtpt, pattern)
idx <- !is.na(matches[, 1]) & is.na(result) & !na_idx
if (any(idx)) {
  value <- as.numeric(matches[idx, "value"])
  unit <- tolower(matches[idx, "unit"])
  result[idx] <- ifelse(substr(unit, 1, 1) == "m", -value / 60, -value)
}

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(xxtpt = xxtpt, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_predose_patterns/outputs/result.csv`
- Size: 94 bytes

```csv
"xxtpt","result"
"15 min predose",-0.25
"2 hr before",-2
"1 hour postdose",1
"UNSCHEDULED",NA
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
na_idx  <- read_tsv("inputs/na_idx.tsv", show_col_types = FALSE)
result  <- read_tsv("inputs/result.tsv", show_col_types = FALSE)
xxtpt   <- read_tsv("inputs/xxtpt.tsv", show_col_types = FALSE)

# Convert logical index if needed
na_logical <- na_idx[[1]]

# Apply NA index to result
result_vec <- result[[1]]
result_vec[na_logical] <- NA

# Prepare output
out <- tibble(
  xxtpt  = xxtpt[[1]],
  result = result_vec
)

# Write output
write_csv(out, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_predose_patterns/sample_00/case_01/llm_outputs/result.csv`
- Size: 79 bytes

```csv
xxtpt,result
15 min predose,NA
2 hr before,NA
1 hour postdose,1
UNSCHEDULED,NA
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_predose_patterns/sample_00/case_01/stderr.txt`
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
