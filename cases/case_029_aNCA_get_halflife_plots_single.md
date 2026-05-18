# Case 029: pharmaverse/aNCA/get_halflife_plots_single

## Case Metadata

- Task ID: `pharmaverse/aNCA/get_halflife_plots_single`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: plot helper output is reference summary/stub not natural plot output

## Prompt

```text
Write an R script to perform get halflife plots single using the aNCA clinical task contract.

Input: add_annotations.tsv, color.tsv, conc_col.tsv, fit_line_data.tsv, group_vars.tsv, plot_data.tsv, subtitle.tsv, symbol.tsv, text.tsv, time_col.tsv, title.tsv, xlab.tsv, ylab.tsv
Output: result.csv


Required columns for result.csv: USUBJID, TIME, LOG_CONC, rbio_reference_task
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### add_annotations.tsv (22 bytes)
add_annotations
FALSE

### color.tsv (10 bytes)
color
ARM

### conc_col.tsv (14 bytes)
conc_col
CONC

### fit_line_data.tsv (55 bytes)
USUBJID	TIME	LOG_CONC
101	1	3.53
101	2	4.12
101	4	3.64

### group_vars.tsv (15 bytes)
group_vars
ARM

### plot_data.tsv (328 bytes)
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
... [3 more lines omitted]

### subtitle.tsv (26 bytes)
subtitle
100 mg oral dose

### symbol.tsv (15 bytes)
symbol
USUBJID

### text.tsv (28 bytes)
text
Terminal half-life fit

### time_col.tsv (14 bytes)
time_col
TIME

### title.tsv (32 bytes)
title
Half-life diagnostic plot

### xlab.tsv (25 bytes)
xlab
Time after dose (h)

### ylab.tsv (27 bytes)
ylab
Concentration (ng/mL)
```

## Input Data

### `add_annotations.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/add_annotations.tsv`
- Size: 22 bytes

```text
add_annotations
FALSE
```

### `color.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/color.tsv`
- Size: 10 bytes

```text
color
ARM
```

### `conc_col.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/conc_col.tsv`
- Size: 14 bytes

```text
conc_col
CONC
```

### `fit_line_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/fit_line_data.tsv`
- Size: 55 bytes

```text
USUBJID	TIME	LOG_CONC
101	1	3.53
101	2	4.12
101	4	3.64
```

### `group_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/group_vars.tsv`
- Size: 15 bytes

```text
group_vars
ARM
```

### `plot_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/plot_data.tsv`
- Size: 328 bytes

```text
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
102	100 mg	1	29.8	100	AUC	oral	1	N
102	100 mg	2	55.4	100	AUC	oral	2	N
102	100 mg	4	33.6	100	AUC	oral	4	N
```

### `subtitle.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/subtitle.tsv`
- Size: 26 bytes

```text
subtitle
100 mg oral dose
```

### `symbol.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/symbol.tsv`
- Size: 15 bytes

```text
symbol
USUBJID
```

### `text.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/text.tsv`
- Size: 28 bytes

```text
text
Terminal half-life fit
```

### `time_col.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/time_col.tsv`
- Size: 14 bytes

```text
time_col
TIME
```

### `title.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/title.tsv`
- Size: 32 bytes

```text
title
Half-life diagnostic plot
```

### `xlab.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/xlab.tsv`
- Size: 25 bytes

```text
xlab
Time after dose (h)
```

### `ylab.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/inputs/ylab.tsv`
- Size: 27 bytes

```text
ylab
Concentration (ng/mL)
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/solution.R`
- Size: 4270 bytes

```r
# Repaired fair reference for pharmaverse/aNCA/get_halflife_plots_single
# Generated by scripts/tools/repair_anca_references.py
# Function class in aNCA 0.1.0 Docker image: missing

has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

read_input_value <- function(path) {
  df <- read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
  if (nrow(df) == 1 && ncol(df) == 1) {
    value <- df[[1]][[1]]
    lower <- tolower(as.character(value))
    if (lower %in% c("true", "false")) {
      return(lower == "true")
    }
    numeric_value <- suppressWarnings(as.numeric(value))
    if (!is.na(numeric_value) && grepl("^-?[0-9]+(\\.[0-9]+)?$", as.character(value))) {
      return(numeric_value)
    }
    return(value)
  }
  df
}

safe_preview <- function(x) {
  text <- paste(capture.output(str(x, max.level = 1, give.attr = FALSE)), collapse = " | ")
  substr(text, 1, 500)
}

as_result_df <- function(x, inputs) {
  if (is.data.frame(x)) {
    return(x)
  }
  if (is.atomic(x) && !is.null(x)) {
    return(data.frame(result = as.character(x), stringsAsFactors = FALSE))
  }
  if (is.list(x) && length(x) > 0 && all(vapply(x, function(item) length(item) <= 1, logical(1)))) {
    out <- as.data.frame(lapply(x, function(item) {
      if (length(item) == 0) NA_character_ else as.character(item[[1]])
    }), stringsAsFactors = FALSE)
    return(out)
  }
  data_frames <- inputs[vapply(inputs, is.data.frame, logical(1))]
  if (length(data_frames) > 0) {
    first <- data_frames[[1]]
    if (nrow(first) > 0 && ncol(first) > 0) {
      return(first)
    }
  }
  data.frame(
    task_id = "pharmaverse/aNCA/get_halflife_plots_single",
    function_name = "get_halflife_plots_single",
    result_type = paste(class(x), collapse = ","),
    result_preview = safe_preview(x),
    stringsAsFactors = FALSE
  )
}

fallback_result <- function(inputs) {
  data_frames <- inputs[vapply(inputs, is.data.frame, logical(1))]
  if (length(data_frames) > 0) {
    result <- data_frames[[1]]
    result$rbio_reference_task <- "get_halflife_plots_single"
    return(result)
  }
  values <- lapply(inputs, function(x) {
    if (length(x) == 0) NA_character_ else paste(as.character(x), collapse = ";")
  })
  if (length(values) == 0) {
    values <- list(note = "no inputs")
  }
  values$rbio_reference_task <- "get_halflife_plots_single"
  as.data.frame(values, stringsAsFactors = FALSE)
}

input_files <- c("add_annotations.tsv", "color.tsv", "conc_col.tsv", "fit_line_data.tsv", "group_vars.tsv", "plot_data.tsv", "subtitle.tsv", "symbol.tsv", "text.tsv", "time_col.tsv", "title.tsv", "xlab.tsv", "ylab.tsv")
inputs <- list()
for (file_name in input_files) {
  stem <- sub("\\.tsv$", "", basename(file_name))
  inputs[[stem]] <- read_input_value(file.path("inputs", file_name))
}

result <- NULL
call_error <- NA_character_
if (FALSE) {
  result <- tryCatch({
    target_fn <- NULL
    do.call(target_fn, inputs)
  }, error = function(err) {
    call_error <<- conditionMessage(err)
    NULL
  })
  if (is.null(result)) {
    result <- tryCatch({
      target_fn <- NULL
      do.call(target_fn, unname(inputs))
    }, error = function(err) {
      call_error <<- paste(na.omit(c(call_error, conditionMessage(err))), collapse = " | ")
      NULL
    })
  }
}

if (is.null(result)) {
  result <- fallback_result(inputs)
}

write_csv_artifact <- function(x, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  result_df <- as_result_df(x, inputs)
  write.csv(result_df, path, row.names = FALSE)
}

write_rds_artifact <- function(x, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  saveRDS(x, path)
}

write_text_artifact <- function(x, path) {
  dir.create(dirname(path), showWarnings = FALSE, recursive = TRUE)
  writeLines(safe_preview(x), path)
}

expected_artifacts <- c("outputs/result.csv")
unlink(file.path("outputs", c("result.rds", "summary.csv")))
for (artifact in expected_artifacts) {
  if (grepl("\\.csv$", artifact, ignore.case = TRUE)) {
    write_csv_artifact(result, artifact)
  } else if (grepl("\\.rds$", artifact, ignore.case = TRUE)) {
    write_rds_artifact(result, artifact)
  } else {
    write_text_artifact(result, artifact)
  }
}
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single/outputs/result.csv`
- Size: 167 bytes

```csv
"USUBJID","TIME","LOG_CONC","rbio_reference_task"
101,1,3.53,"get_halflife_plots_single"
101,2,4.12,"get_halflife_plots_single"
101,4,3.64,"get_halflife_plots_single"
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

# Read required input files
fit_line_data <- read_tsv(
  file = file.path("inputs", "fit_line_data.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    TIME = col_double(),
    LOG_CONC = col_double()
  )
)

# Add rbio_reference_task column
result <- fit_line_data %>%
  mutate(rbio_reference_task = "aNCA_clinical_halflife_plots_single")

# Select and order required columns
result <- result %>%
  select(USUBJID, TIME, LOG_CONC, rbio_reference_task)

# Write result
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__get_halflife_plots_single/sample_00/case_01/llm_outputs/result.csv`
- Size: 183 bytes

```csv
USUBJID,TIME,LOG_CONC,rbio_reference_task
101,1,3.53,aNCA_clinical_halflife_plots_single
101,2,4.12,aNCA_clinical_halflife_plots_single
101,4,3.64,aNCA_clinical_halflife_plots_single
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__get_halflife_plots_single/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: rbio_reference_task"
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
            "reason": "Value mismatch in column: rbio_reference_task"
          }
        }
      }
    }
  ]
}
```
