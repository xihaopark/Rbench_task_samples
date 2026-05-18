# Case 188: pharmaverse/metatools/remove_labels

## Case Metadata

- Task ID: `pharmaverse/metatools/remove_labels`
- Package: `metatools`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `mixed_needs_review`
- Attribution note: execution failure in object/helper task; may need more explicit contract

## Prompt

```text
Write an R script to perform remove labels using the metatools clinical task contract.

Input: data.tsv, labels.tsv
Output: result.csv


Required columns for result.csv: column, label_present
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/remove_labels/inputs/data.tsv`
- Size: 25 bytes

```text
USUBJID	AVAL
01	10
02	15
```

### `labels.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/remove_labels/inputs/labels.tsv`
- Size: 52 bytes

```text
column	label
USUBJID	Subject ID
AVAL	Analysis Value
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/remove_labels/solution.R`
- Size: 730 bytes

```r
suppressPackageStartupMessages(library(metatools))

data <- read.delim(file.path("inputs", "data.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
labels <- read.delim(file.path("inputs", "labels.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
args <- as.list(labels$label)
names(args) <- labels$column
labeled <- do.call(metatools::add_labels, c(list(data = data), args))
unlabeled <- metatools::remove_labels(labeled)
result <- data.frame(
  column = names(unlabeled),
  label_present = vapply(unlabeled, function(x) !is.null(attr(x, "label", exact = TRUE)), logical(1)),
  stringsAsFactors = FALSE
)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/metatools/remove_labels/outputs/result.csv`
- Size: 54 bytes

```csv
"column","label_present"
"USUBJID",FALSE
"AVAL",FALSE
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

# Read input files
data_path <- file.path("inputs", "data.tsv")
labels_path <- file.path("inputs", "labels.tsv")

dat <- read_tsv(data_path, col_types = cols(.default = "c"))
lbl <- read_tsv(labels_path, col_types = cols(.default = "c"))

# Prepare labels list named by column
label_list <- lbl$label
names(label_list) <- lbl$column

# Apply labels to data using metatools
dat_labeled <- add_labels(dat, labels = label_list)

# Remove labels: metatools uses attributes, so drop them
dat_unlabeled <- dat_labeled
for (nm in names(dat_unlabeled)) {
  attr(dat_unlabeled[[nm]], "label") <- NULL
}

# Prepare result: for each column whether label was present in labels.tsv
result <- tibble(
  column = names(dat),
  label_present = names(dat) %in% lbl$column
)

# Write result
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__metatools__remove_labels/sample_00/case_01/stderr.txt`
- Size: 1254 bytes

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
Error in add_labels(dat, labels = label_list) :
  All variable names supplied to label must be variables in data
Execution halted
```

## Evaluation Result

```json
{
  "status": "NO_OUTPUT",
  "failure_stage": "execution_failure",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "tier": "exec_fail",
      "failure_stage": "execution_failure",
      "message": "No output files created",
      "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
      "returncode": 1,
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [],
        "missing_artifacts": [
          "result.csv"
        ]
      }
    }
  ]
}
```
