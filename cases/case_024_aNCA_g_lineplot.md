# Case 024: pharmaverse/aNCA/g_lineplot

## Case Metadata

- Task ID: `pharmaverse/aNCA/g_lineplot`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: plot helper output is reference summary/stub not natural plot output

## Prompt

```text
Write an R script to perform g lineplot using the aNCA clinical task contract.

Input: color_by.tsv, color_labels.tsv, data.tsv, facet_by.tsv, facet_count_n.tsv, group_by.tsv, labels_df.tsv, palette.tsv, show_legend.tsv, threshold_value.tsv, tooltip_vars.tsv, vline_var.tsv, x_limits.tsv, x_unit.tsv, x_var.tsv, y_limits.tsv, y_unit.tsv, y_var.tsv, ylog_scale.tsv
Output: result.csv


Required columns for result.csv: USUBJID, ARM, TIME, CONC, DOSE, PARAM, ROUTE, TSLD, BLQFL, rbio_reference_task
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### color_by.tsv (13 bytes)
color_by
ARM

### color_labels.tsv (20 bytes)
color_labels
100 mg

### data.tsv (328 bytes)
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
... [3 more lines omitted]

### facet_by.tsv (15 bytes)
facet_by
PARAM

### facet_count_n.tsv (19 bytes)
facet_count_n
TRUE

### group_by.tsv (17 bytes)
group_by
USUBJID

### labels_df.tsv (144 bytes)
variable	label
USUBJID	Subject identifier
ARM	Treatment arm
TIME	Nominal time after dose
CONC	Concentration
DOSE	Dose amount
... [1 more lines omitted]

### palette.tsv (16 bytes)
palette
#1f77b4

### show_legend.tsv (17 bytes)
show_legend
TRUE

### threshold_value.tsv (18 bytes)
threshold_value
0

### tooltip_vars.tsv (31 bytes)
tooltip_vars
USUBJID
TIME
CONC

### vline_var.tsv (15 bytes)
vline_var
TIME

### x_limits.tsv (13 bytes)
x_limits
0
4

### x_unit.tsv (9 bytes)
x_unit
h

### x_var.tsv (11 bytes)
x_var
TIME

### y_limits.tsv (14 bytes)
y_limits
0
70

### y_unit.tsv (13 bytes)
y_unit
ng/mL

### y_var.tsv (11 bytes)
y_var
CONC

### ylog_scale.tsv (17 bytes)
ylog_scale
FALSE
```

## Input Data

### `color_by.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/color_by.tsv`
- Size: 13 bytes

```text
color_by
ARM
```

### `color_labels.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/color_labels.tsv`
- Size: 20 bytes

```text
color_labels
100 mg
```

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/data.tsv`
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

### `facet_by.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/facet_by.tsv`
- Size: 15 bytes

```text
facet_by
PARAM
```

### `facet_count_n.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/facet_count_n.tsv`
- Size: 19 bytes

```text
facet_count_n
TRUE
```

### `group_by.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/group_by.tsv`
- Size: 17 bytes

```text
group_by
USUBJID
```

### `labels_df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/labels_df.tsv`
- Size: 144 bytes

```text
variable	label
USUBJID	Subject identifier
ARM	Treatment arm
TIME	Nominal time after dose
CONC	Concentration
DOSE	Dose amount
PARAM	PK parameter
```

### `palette.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/palette.tsv`
- Size: 16 bytes

```text
palette
#1f77b4
```

### `show_legend.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/show_legend.tsv`
- Size: 17 bytes

```text
show_legend
TRUE
```

### `threshold_value.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/threshold_value.tsv`
- Size: 18 bytes

```text
threshold_value
0
```

### `tooltip_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/tooltip_vars.tsv`
- Size: 31 bytes

```text
tooltip_vars
USUBJID
TIME
CONC
```

### `vline_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/vline_var.tsv`
- Size: 15 bytes

```text
vline_var
TIME
```

### `x_limits.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/x_limits.tsv`
- Size: 13 bytes

```text
x_limits
0
4
```

### `x_unit.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/x_unit.tsv`
- Size: 9 bytes

```text
x_unit
h
```

### `x_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/x_var.tsv`
- Size: 11 bytes

```text
x_var
TIME
```

### `y_limits.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/y_limits.tsv`
- Size: 14 bytes

```text
y_limits
0
70
```

### `y_unit.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/y_unit.tsv`
- Size: 13 bytes

```text
y_unit
ng/mL
```

### `y_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/y_var.tsv`
- Size: 11 bytes

```text
y_var
CONC
```

### `ylog_scale.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/inputs/ylog_scale.tsv`
- Size: 17 bytes

```text
ylog_scale
FALSE
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/solution.R`
- Size: 4308 bytes

```r
# Repaired fair reference for pharmaverse/aNCA/g_lineplot
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
    task_id = "pharmaverse/aNCA/g_lineplot",
    function_name = "g_lineplot",
    result_type = paste(class(x), collapse = ","),
    result_preview = safe_preview(x),
    stringsAsFactors = FALSE
  )
}

fallback_result <- function(inputs) {
  data_frames <- inputs[vapply(inputs, is.data.frame, logical(1))]
  if (length(data_frames) > 0) {
    result <- data_frames[[1]]
    result$rbio_reference_task <- "g_lineplot"
    return(result)
  }
  values <- lapply(inputs, function(x) {
    if (length(x) == 0) NA_character_ else paste(as.character(x), collapse = ";")
  })
  if (length(values) == 0) {
    values <- list(note = "no inputs")
  }
  values$rbio_reference_task <- "g_lineplot"
  as.data.frame(values, stringsAsFactors = FALSE)
}

input_files <- c("color_by.tsv", "color_labels.tsv", "data.tsv", "facet_by.tsv", "facet_count_n.tsv", "group_by.tsv", "labels_df.tsv", "palette.tsv", "show_legend.tsv", "threshold_value.tsv", "tooltip_vars.tsv", "vline_var.tsv", "x_limits.tsv", "x_unit.tsv", "x_var.tsv", "y_limits.tsv", "y_unit.tsv", "y_var.tsv", "ylog_scale.tsv")
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/g_lineplot/outputs/result.csv`
- Size: 532 bytes

```csv
"USUBJID","ARM","TIME","CONC","DOSE","PARAM","ROUTE","TSLD","BLQFL","rbio_reference_task"
101,"100 mg",0,0,100,"AUC","oral",0,"Y","g_lineplot"
101,"100 mg",1,34.2,100,"AUC","oral",1,"N","g_lineplot"
101,"100 mg",2,61.5,100,"AUC","oral",2,"N","g_lineplot"
101,"100 mg",4,38.1,100,"AUC","oral",4,"N","g_lineplot"
102,"100 mg",0,0,100,"AUC","oral",0,"Y","g_lineplot"
102,"100 mg",1,29.8,100,"AUC","oral",1,"N","g_lineplot"
102,"100 mg",2,55.4,100,"AUC","oral",2,"N","g_lineplot"
102,"100 mg",4,33.6,100,"AUC","oral",4,"N","g_lineplot"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if needed
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read main data
data <- read_tsv(
  file = file.path("inputs", "data.tsv"),
  col_types = cols(.default = col_guess())
)

# Add required column
data <- data %>%
  mutate(rbio_reference_task = "aNCA_clinical_task_contract_g_lineplot") %>%
  select(USUBJID, ARM, TIME, CONC, DOSE, PARAM, ROUTE, TSLD, BLQFL, rbio_reference_task)

# Write result
write_csv(data, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__g_lineplot/sample_00/case_01/llm_outputs/result.csv`
- Size: 656 bytes

```csv
USUBJID,ARM,TIME,CONC,DOSE,PARAM,ROUTE,TSLD,BLQFL,rbio_reference_task
101,100 mg,0,0,100,AUC,oral,0,Y,aNCA_clinical_task_contract_g_lineplot
101,100 mg,1,34.2,100,AUC,oral,1,N,aNCA_clinical_task_contract_g_lineplot
101,100 mg,2,61.5,100,AUC,oral,2,N,aNCA_clinical_task_contract_g_lineplot
101,100 mg,4,38.1,100,AUC,oral,4,N,aNCA_clinical_task_contract_g_lineplot
102,100 mg,0,0,100,AUC,oral,0,Y,aNCA_clinical_task_contract_g_lineplot
102,100 mg,1,29.8,100,AUC,oral,1,N,aNCA_clinical_task_contract_g_lineplot
102,100 mg,2,55.4,100,AUC,oral,2,N,aNCA_clinical_task_contract_g_lineplot
102,100 mg,4,33.6,100,AUC,oral,4,N,aNCA_clinical_task_contract_g_lineplot
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__g_lineplot/sample_00/case_01/stderr.txt`
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
