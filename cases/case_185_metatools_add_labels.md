# Case 185: pharmaverse/metatools/add_labels

## Case Metadata

- Task ID: `pharmaverse/metatools/add_labels`
- Package: `metatools`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform add labels using the metatools clinical task contract.

Input: data.tsv, labels.tsv
Output: result.csv


Required columns for result.csv: column, label
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (25 bytes)
USUBJID	AVAL
01	10
02	15

### labels.tsv (52 bytes)
column	label
USUBJID	Subject ID
AVAL	Analysis Value
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/add_labels/inputs/data.tsv`
- Size: 25 bytes

```text
USUBJID	AVAL
01	10
02	15
```

### `labels.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/add_labels/inputs/labels.tsv`
- Size: 52 bytes

```text
column	label
USUBJID	Subject ID
AVAL	Analysis Value
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/add_labels/solution.R`
- Size: 745 bytes

```r
suppressPackageStartupMessages(library(metatools))

data <- read.delim(file.path("inputs", "data.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
labels <- read.delim(file.path("inputs", "labels.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
args <- as.list(labels$label)
names(args) <- labels$column
labeled <- do.call(metatools::add_labels, c(list(data = data), args))
result <- data.frame(
  column = names(labeled),
  label = vapply(labeled, function(x) {
    value <- attr(x, "label", exact = TRUE)
    if (is.null(value)) NA_character_ else as.character(value)
  }, character(1)),
  stringsAsFactors = FALSE
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/add_labels/outputs/result.csv`
- Size: 64 bytes

```csv
"column","label"
"USUBJID","Subject ID"
"AVAL","Analysis Value"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(metatools)
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input data
data_path   <- file.path("inputs", "data.tsv")
labels_path <- file.path("inputs", "labels.tsv")

dat <- read_tsv(data_path, show_col_types = FALSE)
lbl <- read_tsv(labels_path, show_col_types = FALSE)

# Ensure required columns
lbl <- lbl %>% select(column, label)

# Apply labels using metatools clinical task contract
# (Assumes 'column' in labels.tsv matches column names in dat)
for (i in seq_len(nrow(lbl))) {
  col_name  <- lbl$column[i]
  col_label <- lbl$label[i]
  if (col_name %in% names(dat)) {
    attr(dat[[col_name]], "label") <- col_label
  }
}

# Prepare result according to required columns
result <- lbl %>% select(column, label)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__add_labels/sample_00/case_01/llm_outputs/result.csv`
- Size: 52 bytes

```csv
column,label
USUBJID,Subject ID
AVAL,Analysis Value
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__add_labels/sample_00/case_01/stderr.txt`
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
