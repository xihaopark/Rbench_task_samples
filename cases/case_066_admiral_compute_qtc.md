# Case 066: pharmaverse/admiral/compute_qtc

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_qtc`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform compute qtc using the admiral clinical task contract.

Input: method.tsv, qt.tsv, rr.tsv
Output: result.csv


Required columns for result.csv: qt, rr, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### method.tsv (14 bytes)
method
bazett

### qt.tsv (15 bytes)
qt
380
410
450

### rr.tsv (17 bytes)
rr
800
1000
1200
```

## Input Data

### `method.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qtc/inputs/method.tsv`
- Size: 14 bytes

```text
method
bazett
```

### `qt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qtc/inputs/qt.tsv`
- Size: 15 bytes

```text
qt
380
410
450
```

### `rr.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qtc/inputs/rr.tsv`
- Size: 17 bytes

```text
rr
800
1000
1200
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qtc/solution.R`
- Size: 786 bytes

```r
suppressPackageStartupMessages(library(admiral))

qt <- as.numeric(read.delim(file.path("inputs", "qt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
rr <- as.numeric(read.delim(file.path("inputs", "rr.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]])
method <- tolower(as.character(read.delim(file.path("inputs", "method.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]][1]))
if (!method %in% c("bazett", "fridericia", "sagie")) method <- "bazett"
result <- switch(method, bazett = qt / sqrt(rr / 1000), fridericia = qt / (rr / 1000)^(1 / 3), sagie = 1000 * (qt / 1000 + 0.154 * (1 - rr / 1000)))

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(qt = qt, rr = rr, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_qtc/outputs/result.csv`
- Size: 82 bytes

```csv
"qt","rr","result"
380,800,424.85291572496
410,1000,410
450,1200,410.791918128875
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
method_df <- read_tsv(
  file = file.path("inputs", "method.tsv"),
  col_types = cols(
    method = col_character()
  )
)

qt_df <- read_tsv(
  file = file.path("inputs", "qt.tsv"),
  col_types = cols(
    qt = col_double()
  )
)

rr_df <- read_tsv(
  file = file.path("inputs", "rr.tsv"),
  col_types = cols(
    rr = col_double()
  )
)

# Determine method (first non-NA value)
method <- method_df$method[1]

# Align qt and rr by position (recycle shorter vector if needed)
n <- max(nrow(qt_df), nrow(rr_df))
qt_vec <- rep(qt_df$qt, length.out = n)
rr_vec <- rep(rr_df$rr, length.out = n)

# Compute corrected QT (qtc)
if (tolower(method) == "bazett") {
  result_vec <- qt_vec / sqrt(rr_vec / 1000)
} else {
  stop("Unsupported method: ", method)
}

# Prepare result
result_df <- tibble(
  qt = qt_vec,
  rr = rr_vec,
  result = result_vec
)

# Write output
write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_qtc/sample_00/case_01/llm_outputs/result.csv`
- Size: 80 bytes

```csv
qt,rr,result
380,800,424.85291572496004
410,1000,410
450,1200,410.7919181288746
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_qtc/sample_00/case_01/stderr.txt`
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
