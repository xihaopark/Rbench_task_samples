# Case 036: pharmaverse/aNCA/keep_blq_timepoints

## Case Metadata

- Task ID: `pharmaverse/aNCA/keep_blq_timepoints`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform keep BLQ timepoints using the aNCA clinical task contract.

Input: mean_group_var.tsv, plot_data.tsv, xvar.tsv
Output: result.csv


Required columns for result.csv: ARM, TIME
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### mean_group_var.tsv (19 bytes)
mean_group_var
ARM

### plot_data.tsv (328 bytes)
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
... [3 more lines omitted]

### xvar.tsv (10 bytes)
xvar
TIME
```

## Input Data

### `mean_group_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/keep_blq_timepoints/inputs/mean_group_var.tsv`
- Size: 19 bytes

```text
mean_group_var
ARM
```

### `plot_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/keep_blq_timepoints/inputs/plot_data.tsv`
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

### `xvar.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/keep_blq_timepoints/inputs/xvar.tsv`
- Size: 10 bytes

```text
xvar
TIME
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/keep_blq_timepoints/solution.R`
- Size: 4032 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(rlang))

# 1. 读取输入数据 / Read input data
plot_data_path <- file.path("inputs", "plot_data.tsv")
if (!file.exists(plot_data_path)) {
  stop("plot_data.tsv is required input")
}
plot_data <- read.delim(plot_data_path, check.names = FALSE, stringsAsFactors = FALSE)
xvar_path <- file.path("inputs", "xvar.tsv")
if (!file.exists(xvar_path)) {
  stop("xvar.tsv is required input")
}
xvar_df <- read.delim(xvar_path, check.names = FALSE, stringsAsFactors = FALSE)
xvar <- xvar_df$xvar
mean_group_var_path <- file.path("inputs", "mean_group_var.tsv")
if (!file.exists(mean_group_var_path)) {
  stop("mean_group_var.tsv is required input")
}
mean_group_var_df <- read.delim(mean_group_var_path, check.names = FALSE, stringsAsFactors = FALSE)
mean_group_var <- mean_group_var_df$mean_group_var

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("plot_data")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 提取标量参数
if (is.data.frame(mean_group_var) && ncol(mean_group_var) > 0 && nrow(mean_group_var) > 0) {
  mean_group_var <- mean_group_var[[1]][1]
} else if (is.character(mean_group_var)) {
  mean_group_var <- mean_group_var[1]
}
if (is.data.frame(xvar) && ncol(xvar) > 0 && nrow(xvar) > 0) {
  xvar <- xvar[[1]][1]
} else if (is.character(xvar)) {
  xvar <- xvar[1]
}

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  if (!has_aNCA) stop("aNCA unavailable")
  aNCA:::keep_blq_timepoints(
    plot_data = plot_data,
    xvar = xvar,
    mean_group_var = mean_group_var
  )
}, error = function(e) {
  # 如果函数不存在，手动实现逻辑
  # identify valid BLQ column
  blq_col <- intersect(c("AVALC", "AVALCAT1"), names(plot_data))[1]

  if (!is.na(blq_col) && blq_col %in% names(plot_data)) {
    plot_data <- plot_data %>%
      mutate(is_blq = grepl("BLQ|LTR|<[1-9]|<PCLLOQ", .data[[blq_col]]))
  } else {
    plot_data$is_blq <- FALSE
  }

  if ("USUBJID" %in% names(plot_data)) {
    result_df <- plot_data %>%
      group_by(!!sym(mean_group_var), !!sym(xvar)) %>%
      summarise(
        n_samples = n_distinct(USUBJID),
        n_blq_ratio = sum(is_blq) / n_samples,
        .groups = "drop"
      ) %>%
      filter(n_blq_ratio <= 0.5, n_samples > 1) %>%
      select(all_of(c(mean_group_var, xvar)))
    result_df
  } else {
    data.frame()
  }
})

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    xvar = xvar, mean_group_var = mean_group_var,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}
# 6. 保存输出 / Save outputs
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/keep_blq_timepoints/outputs/result.csv`
- Size: 57 bytes

```csv
"ARM","TIME"
"100 mg",0
"100 mg",1
"100 mg",2
"100 mg",4
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input files
mean_group_var <- read.table(
  file = "inputs/mean_group_var.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE,
  check.names = FALSE
)

xvar <- read.table(
  file = "inputs/xvar.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE,
  check.names = FALSE
)

plot_data <- read.table(
  file = "inputs/plot_data.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE,
  check.names = FALSE
)

# Extract variable names
mgv <- mean_group_var$mean_group_var[1]
xv <- xvar$xvar[1]

# Ensure required columns exist
required_cols <- c("ARM", "TIME", "BLQFL")
missing_cols <- setdiff(required_cols, colnames(plot_data))
if (length(missing_cols) > 0) {
  stop(paste("Missing required columns in plot_data:", paste(missing_cols, collapse = ", ")))
}

# Filter to timepoints where all observations within ARM/TIME are BLQ (BLQFL == "Y")
library(dplyr)

result <- plot_data %>%
  group_by(.data[[mgv]], .data[[xv]]) %>%
  summarise(all_blq = all(BLQFL == "Y"), .groups = "drop") %>%
  filter(all_blq) %>%
  select(ARM = .data[[mgv]], TIME = .data[[xv]]) %>%
  distinct() %>%
  arrange(ARM, TIME)

# Write result
write.csv(result, file = "outputs/result.csv", row.names = FALSE, quote = TRUE)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__keep_blq_timepoints/sample_00/case_01/llm_outputs/result.csv`
- Size: 24 bytes

```csv
"ARM","TIME"
"100 mg",0
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__keep_blq_timepoints/sample_00/case_01/stderr.txt`
- Size: 1500 bytes

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

Warning message:
Use of .data in tidyselect expressions was deprecated in tidyselect 1.2.0.
ℹ Please use `all_of(var)` (or `any_of(var)`) instead of `.data[[var]]`
```

## Evaluation Result

```json
{
  "status": "FAIL",
  "failure_stage": "schema_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "schema_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "schema_mismatch",
          "reason": "Shape mismatch: ref=(4, 2) vs llm=(1, 2)"
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
            "stage": "schema_mismatch",
            "tier": "output_bad",
            "reason": "Shape mismatch: ref=(4, 2) vs llm=(1, 2)"
          }
        }
      }
    }
  ]
}
```
