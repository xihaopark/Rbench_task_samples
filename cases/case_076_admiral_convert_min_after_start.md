# Case 076: pharmaverse/admiral/convert_min_after_start

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_min_after_start`
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
Write an R script to perform convert min after start using the admiral clinical task contract.

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
2
NA

### xxtpt.tsv (90 bytes)
xxtpt
5 min after start inf
30 minutes after start inf
2 hours after start
not applicable
```

## Input Data

### `na_idx.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_after_start/inputs/na_idx.tsv`
- Size: 30 bytes

```text
na_idx
FALSE
FALSE
FALSE
TRUE
```

### `result.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_after_start/inputs/result.tsv`
- Size: 18 bytes

```text
result
NA
NA
2
NA
```

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_after_start/inputs/xxtpt.tsv`
- Size: 90 bytes

```text
xxtpt
5 min after start inf
30 minutes after start inf
2 hours after start
not applicable
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_after_start/solution.R`
- Size: 867 bytes

```r
suppressPackageStartupMessages(library(stringr))

xxtpt <- read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$xxtpt
result <- read.delim(file.path("inputs", "result.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$result
result <- suppressWarnings(as.numeric(result))
na_idx <- read.delim(file.path("inputs", "na_idx.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$na_idx
na_idx <- as.logical(na_idx)

pattern <- regex("^(?<value>\\d+(?:\\.\\d+)?)\\s*m(?:in|inute)?s?\\s+after\\s+start\\s+inf$", ignore_case = TRUE)
matches <- str_match(xxtpt, pattern)
idx <- !is.na(matches[, 1]) & is.na(result) & !na_idx
result[idx] <- as.numeric(matches[idx, "value"]) / 60

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(xxtpt = xxtpt, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_min_after_start/outputs/result.csv`
- Size: 137 bytes

```csv
"xxtpt","result"
"5 min after start inf",0.0833333333333333
"30 minutes after start inf",0.5
"2 hours after start",2
"not applicable",NA
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
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
na_idx  <- read_tsv("inputs/na_idx.tsv", show_col_types = FALSE)
result  <- read_tsv("inputs/result.tsv", show_col_types = FALSE)
xxtpt   <- read_tsv("inputs/xxtpt.tsv", show_col_types = FALSE)

# Ensure logical na_idx
na_idx <- na_idx %>%
  mutate(na_idx = as.logical(na_idx))

# Apply ADMIRAL clinical task contract:
# - For rows where na_idx is TRUE, derive result from xxtpt as minutes after start
# - Else keep existing result
derive_mins_after_start <- function(txt) {
  txt <- tolower(txt)

  # pattern components
  num <- "([0-9]+(?:\\.[0-9]+)?)"
  unit <- "(min|mins|minute|minutes|hour|hours|hr|hrs)"
  after_start_pattern <- paste0("^\\s*", num, "\\s*", unit, "s?\\s+after\\s+start")

  out <- rep(NA_real_, length(txt))

  is_match <- str_detect(txt, after_start_pattern)
  matched_txt <- txt[is_match]

  n <- as.numeric(str_match(matched_txt, num)[, 2])
  u <- str_match(matched_txt, unit)[, 2]

  factor_min <- ifelse(str_detect(u, "hour|hr"), 60, 1)
  out[is_match] <- n * factor_min

  out
}

derived_result <- derive_mins_after_start(xxtpt$xxtpt)

final_result <- result %>%
  mutate(
    result = if_else(na_idx$na_idx, derived_result, as.numeric(result))
  ) %>%
  select(result = result) %>%
  bind_cols(xxtpt %>% select(xxtpt)) %>%
  select(xxtpt, result)

# Write output
write_csv(final_result, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_min_after_start/sample_00/case_01/llm_outputs/result.csv`
- Size: 102 bytes

```csv
xxtpt,result
5 min after start inf,
30 minutes after start inf,
2 hours after start,2
not applicable,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_min_after_start/sample_00/case_01/stderr.txt`
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
