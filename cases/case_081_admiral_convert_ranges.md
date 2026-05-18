# Case 081: pharmaverse/admiral/convert_ranges

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_ranges`
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
Write an R script to perform convert ranges using the admiral clinical task contract.

Input: na_idx.tsv, range_method.tsv, result.tsv, xxtpt.tsv
Output: result.csv


Required columns for result.csv: xxtpt, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### na_idx.tsv (31 bytes)
na_idx
FALSE
FALSE
FALSE
FALSE

### range_method.tsv (22 bytes)
range_method
midpoint

### result.tsv (18 bytes)
result
NA
NA
NA
5

### xxtpt.tsv (73 bytes)
xxtpt
1-3 h prior start
2-4 hours after start
6-8 hr post dose
unmatched
```

## Input Data

### `na_idx.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_ranges/inputs/na_idx.tsv`
- Size: 31 bytes

```text
na_idx
FALSE
FALSE
FALSE
FALSE
```

### `range_method.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_ranges/inputs/range_method.tsv`
- Size: 22 bytes

```text
range_method
midpoint
```

### `result.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_ranges/inputs/result.tsv`
- Size: 18 bytes

```text
result
NA
NA
NA
5
```

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_ranges/inputs/xxtpt.tsv`
- Size: 73 bytes

```text
xxtpt
1-3 h prior start
2-4 hours after start
6-8 hr post dose
unmatched
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_ranges/solution.R`
- Size: 1440 bytes

```r
suppressPackageStartupMessages(library(stringr))

xxtpt <- read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$xxtpt
result <- read.delim(file.path("inputs", "result.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$result
result <- suppressWarnings(as.numeric(result))
na_idx <- read.delim(file.path("inputs", "na_idx.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$na_idx
na_idx <- as.logical(na_idx)
range_method <- read.delim(file.path("inputs", "range_method.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]][1]

range_value <- function(start, end, method) {
  if (tolower(method) %in% c("midpoint", "mean", "average")) (start + end) / 2 else end
}
pattern <- regex("^(?<start>\\d+(?:\\.\\d+)?)\\s*-\\s*(?<end>\\d+(?:\\.\\d+)?)\\s*h(?:r|our)?s?(?:\\s+(?<direction>prior|before|post|after)(?:\\s+(?:start|end|dose))?)?$", ignore_case = TRUE)
matches <- str_match(xxtpt, pattern)
idx <- !is.na(matches[, 1]) & is.na(result) & !na_idx
if (any(idx)) {
  value <- range_value(as.numeric(matches[idx, "start"]), as.numeric(matches[idx, "end"]), range_method)
  direction <- tolower(matches[idx, "direction"])
  direction[is.na(direction)] <- "after"
  result[idx] <- ifelse(direction %in% c("prior", "before"), -value, value)
}

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(xxtpt = xxtpt, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_ranges/outputs/result.csv`
- Size: 101 bytes

```csv
"xxtpt","result"
"1-3 h prior start",-2
"2-4 hours after start",3
"6-8 hr post dose",7
"unmatched",5
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
na_idx <- read_tsv(
  file = file.path("inputs", "na_idx.tsv"),
  show_col_types = FALSE
) %>%
  mutate(row = row_number())

range_method <- read_tsv(
  file = file.path("inputs", "range_method.tsv"),
  show_col_types = FALSE
)

result <- read_tsv(
  file = file.path("inputs", "result.tsv"),
  show_col_types = FALSE
) %>%
  mutate(row = row_number())

xxtpt <- read_tsv(
  file = file.path("inputs", "xxtpt.tsv"),
  show_col_types = FALSE
) %>%
  mutate(row = row_number())

# Helper: get midpoint from a label containing a numeric range
get_midpoint <- function(label) {
  # Extract all numbers (integer or decimal, including possible leading minus)
  nums <- str_extract_all(label, "-?\\d*\\.?\\d+")[[1]]
  # Keep only first two numeric values as range bounds
  if (length(nums) < 2) return(NA_real_)
  vals <- as.numeric(nums[1:2])
  mean(vals)
}

# Apply range conversion only where:
# - result is NA
# - na_idx is FALSE
# - range_method is "midpoint"
res <- result %>%
  left_join(na_idx, by = "row", suffix = c("", "_naidx")) %>%
  left_join(xxtpt, by = "row", suffix = c("", "_xxtpt")) %>%
  mutate(
    result = case_when(
      is.na(result) &
        !na_idx &
        range_method$range_method[1] == "midpoint" ~
          vapply(xxtpt, get_midpoint, numeric(1)),
      TRUE ~ result
    )
  ) %>%
  select(xxtpt, result)

# Write output
write_csv(res, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_ranges/sample_00/case_01/llm_outputs/result.csv`
- Size: 91 bytes

```csv
xxtpt,result
1-3 h prior start,-1
2-4 hours after start,-1
6-8 hr post dose,-1
unmatched,5
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_ranges/sample_00/case_01/stderr.txt`
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
            "reason": "Numeric mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
