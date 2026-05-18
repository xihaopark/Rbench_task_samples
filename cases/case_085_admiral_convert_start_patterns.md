# Case 085: pharmaverse/admiral/convert_start_patterns

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_start_patterns`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform convert start patterns using the admiral clinical task contract.

Input: na_idx.tsv, result.tsv, xxtpt.tsv
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

### result.tsv (18 bytes)
result
NA
NA
NA
4

### xxtpt.tsv (100 bytes)
xxtpt
2h prior start of infusion
1h after start of treatment
3h post start of infusion
random label
```

## Input Data

### `na_idx.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_start_patterns/inputs/na_idx.tsv`
- Size: 31 bytes

```text
na_idx
FALSE
FALSE
FALSE
FALSE
```

### `result.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_start_patterns/inputs/result.tsv`
- Size: 18 bytes

```text
result
NA
NA
NA
4
```

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_start_patterns/inputs/xxtpt.tsv`
- Size: 100 bytes

```text
xxtpt
2h prior start of infusion
1h after start of treatment
3h post start of infusion
random label
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_start_patterns/solution.R`
- Size: 1040 bytes

```r
suppressPackageStartupMessages(library(stringr))

xxtpt <- read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$xxtpt
result <- read.delim(file.path("inputs", "result.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$result
result <- suppressWarnings(as.numeric(result))
na_idx <- read.delim(file.path("inputs", "na_idx.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$na_idx
na_idx <- as.logical(na_idx)

pattern <- regex("^(?<value>\\d+(?:\\.\\d+)?)h\\s+(?<direction>prior|before|post|after)\\s+start\\s+of\\s+(?:infusion|treatment)$", ignore_case = TRUE)
matches <- str_match(xxtpt, pattern)
idx <- !is.na(matches[, 1]) & is.na(result) & !na_idx
if (any(idx)) {
  value <- as.numeric(matches[idx, "value"])
  direction <- tolower(matches[idx, "direction"])
  result[idx] <- ifelse(direction %in% c("prior", "before"), -value, value)
}

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(xxtpt = xxtpt, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_start_patterns/outputs/result.csv`
- Size: 128 bytes

```csv
"xxtpt","result"
"2h prior start of infusion",-2
"1h after start of treatment",1
"3h post start of infusion",3
"random label",4
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(stringr)
library(fs)

# Create outputs directory if it does not exist
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read inputs
na_idx   <- read_tsv("inputs/na_idx.tsv", show_col_types = FALSE)
result   <- read_tsv("inputs/result.tsv", show_col_types = FALSE)
xxtpt    <- read_tsv("inputs/xxtpt.tsv", show_col_types = FALSE)

# Ensure logical na_idx
na_idx <- na_idx %>%
  mutate(na_idx = as.logical(na_idx))

# Apply admiral-like clinical task contract:
# - For rows where na_idx is TRUE, result stays NA
# - For rows where na_idx is FALSE, convert start patterns in xxtpt into numeric
#   keeping any pre-existing non-NA result values
#
# Pattern examples to convert:
#   "2h prior start of infusion"  -> -2
#   "1h after start of treatment" ->  1
#   "3h post start of infusion"   ->  3
#
# Any text containing:
#   "prior start" => negative sign
#   "after start" or "post start" => positive sign
# Extract leading hours before 'h'.

derive_time_from_xxtpt <- function(text) {
  if (is.na(text)) return(NA_real_)
  hrs <- str_match(text, "^(\\d+)h")[, 2]
  if (is.na(hrs)) return(NA_real_)
  hrs_num <- as.numeric(hrs)
  if (str_detect(text, "prior start")) {
    return(-hrs_num)
  } else if (str_detect(text, "after start|post start")) {
    return(hrs_num)
  } else {
    return(NA_real_)
  }
}

converted <- tibble(
  xxtpt = xxtpt$xxtpt,
  na_idx = na_idx$na_idx,
  result = result$result
) %>%
  mutate(
    conv = vapply(xxtpt, derive_time_from_xxtpt, numeric(1)),
    result = case_when(
      na_idx ~ NA_real_,
      !is.na(result) ~ result,
      TRUE ~ conv
    )
  ) %>%
  select(xxtpt, result)

# Write output
write_csv(converted, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_start_patterns/sample_00/case_01/llm_outputs/result.csv`
- Size: 116 bytes

```csv
xxtpt,result
2h prior start of infusion,-2
1h after start of treatment,1
3h post start of infusion,3
random label,4
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_start_patterns/sample_00/case_01/stderr.txt`
- Size: 1333 bytes

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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union
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
