# Case 042: pharmaverse/aNCA/prepare_plot_data

## Case Metadata

- Task ID: `pharmaverse/aNCA/prepare_plot_data`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform prepare plot data using the aNCA clinical task contract.

Input: colour_var.tsv, data_conc.tsv, data_dose.tsv, grouping_vars.tsv, labels_df.tsv, plot_conc_data.tsv, shape_var.tsv, tooltip_vars.tsv
Output: result.csv


Required columns for result.csv: USUBJID, ARM, TIME, CONC, DOSE, PARAM, ROUTE, TSLD, BLQFL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### colour_var.tsv (15 bytes)
colour_var
ARM

### data_conc.tsv (328 bytes)
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
... [3 more lines omitted]

### data_dose.tsv (84 bytes)
USUBJID	TIME	DOSE	DOSEU	ROUTE	ARM
101	0	100	mg	oral	100 mg
102	0	100	mg	oral	100 mg

### grouping_vars.tsv (26 bytes)
grouping_vars
USUBJID
ARM

### labels_df.tsv (144 bytes)
variable	label
USUBJID	Subject identifier
ARM	Treatment arm
TIME	Nominal time after dose
CONC	Concentration
DOSE	Dose amount
... [1 more lines omitted]

### plot_conc_data.tsv (20 bytes)
plot_conc_data
TRUE

### shape_var.tsv (16 bytes)
shape_var
PARAM

### tooltip_vars.tsv (31 bytes)
tooltip_vars
USUBJID
TIME
CONC
```

## Input Data

### `colour_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/colour_var.tsv`
- Size: 15 bytes

```text
colour_var
ARM
```

### `data_conc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/data_conc.tsv`
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

### `data_dose.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/data_dose.tsv`
- Size: 84 bytes

```text
USUBJID	TIME	DOSE	DOSEU	ROUTE	ARM
101	0	100	mg	oral	100 mg
102	0	100	mg	oral	100 mg
```

### `grouping_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/grouping_vars.tsv`
- Size: 26 bytes

```text
grouping_vars
USUBJID
ARM
```

### `labels_df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/labels_df.tsv`
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

### `plot_conc_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/plot_conc_data.tsv`
- Size: 20 bytes

```text
plot_conc_data
TRUE
```

### `shape_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/shape_var.tsv`
- Size: 16 bytes

```text
shape_var
PARAM
```

### `tooltip_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/inputs/tooltip_vars.tsv`
- Size: 31 bytes

```text
tooltip_vars
USUBJID
TIME
CONC
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/solution.R`
- Size: 5218 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

# 1. 读取输入数据 / Read input data
data_conc_path <- file.path("inputs", "data_conc.tsv")
if (!file.exists(data_conc_path)) {
  stop("data_conc.tsv is required input")
}
data_conc <- read.delim(data_conc_path, check.names = FALSE, stringsAsFactors = FALSE)
data_dose_path <- file.path("inputs", "data_dose.tsv")
if (!file.exists(data_dose_path)) {
  stop("data_dose.tsv is required input")
}
data_dose <- read.delim(data_dose_path, check.names = FALSE, stringsAsFactors = FALSE)
shape_var_path <- file.path("inputs", "shape_var.tsv")
if (!file.exists(shape_var_path)) {
  stop("shape_var.tsv is required input")
}
shape_var_df <- read.delim(shape_var_path, check.names = FALSE, stringsAsFactors = FALSE)
shape_var <- shape_var_df$shape_var
colour_var_path <- file.path("inputs", "colour_var.tsv")
if (!file.exists(colour_var_path)) {
  stop("colour_var.tsv is required input")
}
colour_var_df <- read.delim(colour_var_path, check.names = FALSE, stringsAsFactors = FALSE)
colour_var <- colour_var_df$colour_var
grouping_vars_path <- file.path("inputs", "grouping_vars.tsv")
if (!file.exists(grouping_vars_path)) {
  stop("grouping_vars.tsv is required input")
}
grouping_vars_df <- read.delim(grouping_vars_path, check.names = FALSE, stringsAsFactors = FALSE)
grouping_vars <- grouping_vars_df$grouping_vars
labels_df_path <- file.path("inputs", "labels_df.tsv")
if (!file.exists(labels_df_path)) {
  stop("labels_df.tsv is required input")
}
labels_df <- read.delim(labels_df_path, check.names = FALSE, stringsAsFactors = FALSE)
tooltip_vars_path <- file.path("inputs", "tooltip_vars.tsv")
if (!file.exists(tooltip_vars_path)) {
  stop("tooltip_vars.tsv is required input")
}
tooltip_vars_df <- read.delim(tooltip_vars_path, check.names = FALSE, stringsAsFactors = FALSE)
tooltip_vars <- tooltip_vars_df$tooltip_vars
plot_conc_data_path <- file.path("inputs", "plot_conc_data.tsv")
if (!file.exists(plot_conc_data_path)) {
  stop("plot_conc_data.tsv is required input")
}
plot_conc_data_df <- read.delim(plot_conc_data_path, check.names = FALSE, stringsAsFactors = FALSE)
plot_conc_data <- as.logical(plot_conc_data_df[[1]][1])


# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证
if (nrow(data_conc) == 0 || nrow(data_dose) == 0) stop("data_conc or data_dose is empty")

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  if (!has_aNCA) stop("aNCA unavailable")
  aNCA::prepare_plot_data(
    data_conc = data_conc,
    data_dose = data_dose,
    shape_var = if (nrow(shape_var_df) > 0) shape_var_df$shape_var[1] else NULL,
    colour_var = if (nrow(colour_var_df) > 0) colour_var_df$colour_var[1] else NULL,
    grouping_vars = if (nrow(grouping_vars_df) > 0) grouping_vars_df$grouping_vars else NULL,
    labels_df = labels_df,
    tooltip_vars = if (nrow(tooltip_vars_df) > 0) tooltip_vars_df$tooltip_vars else NULL,
    plot_conc_data = plot_conc_data
  )
}, error = function(e) data_conc)
if (is.null(result) || (is.list(result) && !is.data.frame(result))) result <- data_conc


# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    shape_var = shape_var, colour_var = colour_var,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# 5. 生成汇总统计 / Generate summary statistics
if (is.data.frame(result_df)) {
  summary_stats <- data.frame(
    n_rows = nrow(result_df),
    n_cols = ncol(result_df),
    col_names = paste(colnames(result_df), collapse = ", "),
    stringsAsFactors = FALSE)
  } else if (is.vector(result) || is.numeric(result)) {
  summary_stats <- data.frame(
    n_values = length(result),
    mean_value = mean(result, na.rm = TRUE),
    min_value = min(result, na.rm = TRUE),
    max_value = max(result, na.rm = TRUE),
    median_value = median(result, na.rm = TRUE),
    stringsAsFactors = FALSE)
  } else {
  summary_stats <- data.frame(
    result_type = class(result)[1],
    stringsAsFactors = FALSE
  )
}

# 7. 保存输出 / Save outputs
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
unlink(file.path(outputs_dir, c("result.rds", "summary.csv")))
if (exists("result_df") && is.data.frame(result_df)) {
  write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (exists("result")) {
  if (is.data.frame(result)) {
    write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (is.list(result)) {
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  } else if (is.vector(result) || is.numeric(result) || is.character(result)) {
    result_df <- data.frame(result = result, stringsAsFactors = FALSE)
    write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else {
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  }
} else {
  stop("No result variable found. Function implementation may not have returned a value.")
}
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/prepare_plot_data/outputs/result.csv`
- Size: 406 bytes

```csv
"USUBJID","ARM","TIME","CONC","DOSE","PARAM","ROUTE","TSLD","BLQFL"
101,"100 mg",0,0,100,"AUC","oral",0,"Y"
101,"100 mg",1,34.2,100,"AUC","oral",1,"N"
101,"100 mg",2,61.5,100,"AUC","oral",2,"N"
101,"100 mg",4,38.1,100,"AUC","oral",4,"N"
102,"100 mg",0,0,100,"AUC","oral",0,"Y"
102,"100 mg",1,29.8,100,"AUC","oral",1,"N"
102,"100 mg",2,55.4,100,"AUC","oral",2,"N"
102,"100 mg",4,33.6,100,"AUC","oral",4,"N"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input concentration data
data_conc <- read_tsv(
  file = file.path("inputs", "data_conc.tsv"),
  col_types = cols()
)

# Ensure required columns exist
required_cols <- c("USUBJID", "ARM", "TIME", "CONC", "DOSE", "PARAM", "ROUTE", "TSLD", "BLQFL")
missing_cols <- setdiff(required_cols, names(data_conc))
if (length(missing_cols) > 0) {
  stop("Missing required columns in data_conc.tsv: ", paste(missing_cols, collapse = ", "))
}

# Select and order required columns
result <- data_conc %>%
  select(all_of(required_cols))

# Write result
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__prepare_plot_data/sample_00/case_01/llm_outputs/result.csv`
- Size: 324 bytes

```csv
USUBJID,ARM,TIME,CONC,DOSE,PARAM,ROUTE,TSLD,BLQFL
101,100 mg,0,0,100,AUC,oral,0,Y
101,100 mg,1,34.2,100,AUC,oral,1,N
101,100 mg,2,61.5,100,AUC,oral,2,N
101,100 mg,4,38.1,100,AUC,oral,4,N
102,100 mg,0,0,100,AUC,oral,0,Y
102,100 mg,1,29.8,100,AUC,oral,1,N
102,100 mg,2,55.4,100,AUC,oral,2,N
102,100 mg,4,33.6,100,AUC,oral,4,N
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__prepare_plot_data/sample_00/case_01/stderr.txt`
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
