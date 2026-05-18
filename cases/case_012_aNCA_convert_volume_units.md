# Case 012: pharmaverse/aNCA/convert_volume_units

## Case Metadata

- Task ID: `pharmaverse/aNCA/convert_volume_units`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform convert volume units using the aNCA clinical task contract.

Input: avalu.tsv, df.tsv, volume.tsv, volumeu.tsv
Output: result.csv


Required columns for result.csv: id, avalu, volume, volumeu
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### avalu.tsv (12 bytes)
avalu
avalu

### df.tsv (67 bytes)
id	avalu	volume	volumeu
1	10.5	1.0	L
2	20.3	500.0	mL
3	30.7	0.75	L

### volume.tsv (14 bytes)
volume
volume

### volumeu.tsv (16 bytes)
volumeu
volumeu
```

## Input Data

### `avalu.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/convert_volume_units/inputs/avalu.tsv`
- Size: 12 bytes

```text
avalu
avalu
```

### `df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/convert_volume_units/inputs/df.tsv`
- Size: 67 bytes

```text
id	avalu	volume	volumeu
1	10.5	1.0	L
2	20.3	500.0	mL
3	30.7	0.75	L
```

### `volume.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/convert_volume_units/inputs/volume.tsv`
- Size: 14 bytes

```text
volume
volume
```

### `volumeu.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/convert_volume_units/inputs/volumeu.tsv`
- Size: 16 bytes

```text
volumeu
volumeu
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/convert_volume_units/solution.R`
- Size: 280 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
df <- read_tsv("df")
write.csv(df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/convert_volume_units/outputs/result.csv`
- Size: 77 bytes

```csv
"id","avalu","volume","volumeu"
1,10.5,1,"L"
2,20.3,500,"mL"
3,30.7,0.75,"L"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required package
suppressPackageStartupMessages({
  if (!requireNamespace("readr", quietly = TRUE)) {
    stop("Package 'readr' is required.")
  }
  if (!requireNamespace("dplyr", quietly = TRUE)) {
    stop("Package 'dplyr' is required.")
  }
})

library(readr)
library(dplyr)

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input files
df      <- read_tsv("inputs/df.tsv", show_col_types = FALSE)
avalu   <- read_tsv("inputs/avalu.tsv", show_col_types = FALSE)
volume  <- read_tsv("inputs/volume.tsv", show_col_types = FALSE)
volumeu <- read_tsv("inputs/volumeu.tsv", show_col_types = FALSE)

# aNCA clinical task contract: normalize volume units to liters (L)
# Assume 'volume' column is numeric and 'volumeu' has units like 'L', 'mL'
convert_to_L <- function(vol, unit) {
  factor <- dplyr::case_when(
    unit == "L"  ~ 1,
    unit == "mL" ~ 1 / 1000,
    TRUE         ~ NA_real_
  )
  vol * factor
}

df_converted <- df %>%
  mutate(
    volume = convert_to_L(volume, volumeu),
    volumeu = "L"
  ) %>%
  select(id, avalu, volume, volumeu)

# Write output
write_csv(df_converted, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__convert_volume_units/sample_00/case_01/llm_outputs/result.csv`
- Size: 62 bytes

```csv
id,avalu,volume,volumeu
1,10.5,1,L
2,20.3,0.5,L
3,30.7,0.75,L
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__convert_volume_units/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric mismatch in column: volume"
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
            "reason": "Numeric mismatch in column: volume"
          }
        }
      }
    }
  ]
}
```
