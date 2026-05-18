# Case 070: pharmaverse/admiral/compute_scale

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_scale`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform compute scale using the admiral clinical task contract.

Input: flip_direction.tsv, source.tsv, source_range.tsv, target_range.tsv
Output: result.csv


Required columns for result.csv: source, source_min, source_max, target_min, target_max, flip_direction, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### flip_direction.tsv (21 bytes)
flip_direction
FALSE

### source.tsv (19 bytes)
source
0
25
50
100

### source_range.tsv (26 bytes)
bound	value
min	0
max	100

### target_range.tsv (24 bytes)
bound	value
min	0
max	1
```

## Input Data

### `flip_direction.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_scale/inputs/flip_direction.tsv`
- Size: 21 bytes

```text
flip_direction
FALSE
```

### `source.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_scale/inputs/source.tsv`
- Size: 19 bytes

```text
source
0
25
50
100
```

### `source_range.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_scale/inputs/source_range.tsv`
- Size: 26 bytes

```text
bound	value
min	0
max	100
```

### `target_range.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_scale/inputs/target_range.tsv`
- Size: 24 bytes

```text
bound	value
min	0
max	1
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_scale/solution.R`
- Size: 1288 bytes

```r
source <- as.numeric(read.delim(file.path("inputs", "source.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$source)
source_range <- read.delim(file.path("inputs", "source_range.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
target_range <- read.delim(file.path("inputs", "target_range.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
flip_direction <- as.logical(read.delim(file.path("inputs", "flip_direction.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$flip_direction[1])
get_bound <- function(tbl, name) as.numeric(tbl$value[tbl$bound == name][1])
source_min <- get_bound(source_range, "min")
source_max <- get_bound(source_range, "max")
target_min <- get_bound(target_range, "min")
target_max <- get_bound(target_range, "max")
if (flip_direction) {
  tmp <- target_min
  target_min <- target_max
  target_max <- tmp
}
result <- target_min + (source - source_min) / (source_max - source_min) * (target_max - target_min)
result_df <- data.frame(source = source, source_min = source_min, source_max = source_max, target_min = target_min, target_max = target_max, flip_direction = flip_direction, result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_scale/outputs/result.csv`
- Size: 176 bytes

```csv
"source","source_min","source_max","target_min","target_max","flip_direction","result"
0,0,100,0,1,FALSE,0
25,0,100,0,1,FALSE,0.25
50,0,100,0,1,FALSE,0.5
100,0,100,0,1,FALSE,1
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
flip_direction <- read_tsv(
  file = "inputs/flip_direction.tsv",
  col_types = cols(
    flip_direction = col_logical()
  )
) %>%
  pull(flip_direction) %>%
  .[1]

source_df <- read_tsv(
  file = "inputs/source.tsv",
  col_types = cols(
    source = col_double()
  )
)

source_range <- read_tsv(
  file = "inputs/source_range.tsv",
  col_types = cols(
    bound = col_character(),
    value = col_double()
  )
)

target_range <- read_tsv(
  file = "inputs/target_range.tsv",
  col_types = cols(
    bound = col_character(),
    value = col_double()
  )
)

source_min <- source_range %>% filter(bound == "min") %>% pull(value) %>% .[1]
source_max <- source_range %>% filter(bound == "max") %>% pull(value) %>% .[1]

target_min <- target_range %>% filter(bound == "min") %>% pull(value) %>% .[1]
target_max <- target_range %>% filter(bound == "max") %>% pull(value) %>% .[1]

# Compute scale
result_df <- source_df %>%
  mutate(
    source_min = source_min,
    source_max = source_max,
    target_min = target_min,
    target_max = target_max
  ) %>%
  mutate(
    result = if (!flip_direction) {
      # Standard scaling: map source_min->target_min, source_max->target_max
      target_min + (source - source_min) *
        (target_max - target_min) / (source_max - source_min)
    } else {
      # Flip scaling: map source_min->target_max, source_max->target_min
      target_max - (source - source_min) *
        (target_max - target_min) / (source_max - source_min)
    }
  ) %>%
  mutate(
    flip_direction = flip_direction
  ) %>%
  select(
    source,
    source_min,
    source_max,
    target_min,
    target_max,
    flip_direction,
    result
  )

# Write output
write_csv(result_df, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_scale/sample_00/case_01/llm_outputs/result.csv`
- Size: 162 bytes

```csv
source,source_min,source_max,target_min,target_max,flip_direction,result
0,0,100,0,1,FALSE,0
25,0,100,0,1,FALSE,0.25
50,0,100,0,1,FALSE,0.5
100,0,100,0,1,FALSE,1
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_scale/sample_00/case_01/stderr.txt`
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
