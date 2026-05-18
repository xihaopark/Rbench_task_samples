# Case 018: pharmaverse/aNCA/exploration_meanplot

## Case Metadata

- Task ID: `pharmaverse/aNCA/exploration_meanplot`
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
Write an R script to perform exploration meanplot using the aNCA clinical task contract.

Input: ci.tsv, pknca_data.tsv, sd_max.tsv, sd_min.tsv, tooltip_vars.tsv, x_limits.tsv, y_limits.tsv
Output: result.csv


Required columns for result.csv: operation, success, result_type
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### ci.tsv (8 bytes)
ci
TRUE

### pknca_data.tsv (98 bytes)
ARM	TIME	MEAN	SD	N
100 mg	0	0.0	0.0	2
100 mg	1	32.0	3.1	2
100 mg	2	58.4	4.3	2
100 mg	4	35.9	3.2	2

### sd_max.tsv (12 bytes)
sd_max
TRUE

### sd_min.tsv (12 bytes)
sd_min
TRUE

### tooltip_vars.tsv (27 bytes)
tooltip_vars
ARM
TIME
MEAN

### x_limits.tsv (13 bytes)
x_limits
0
4

### y_limits.tsv (14 bytes)
y_limits
0
70
```

## Input Data

### `ci.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/ci.tsv`
- Size: 8 bytes

```text
ci
TRUE
```

### `pknca_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/pknca_data.tsv`
- Size: 98 bytes

```text
ARM	TIME	MEAN	SD	N
100 mg	0	0.0	0.0	2
100 mg	1	32.0	3.1	2
100 mg	2	58.4	4.3	2
100 mg	4	35.9	3.2	2
```

### `sd_max.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/sd_max.tsv`
- Size: 12 bytes

```text
sd_max
TRUE
```

### `sd_min.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/sd_min.tsv`
- Size: 12 bytes

```text
sd_min
TRUE
```

### `tooltip_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/tooltip_vars.tsv`
- Size: 27 bytes

```text
tooltip_vars
ARM
TIME
MEAN
```

### `x_limits.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/x_limits.tsv`
- Size: 13 bytes

```text
x_limits
0
4
```

### `y_limits.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/inputs/y_limits.tsv`
- Size: 14 bytes

```text
y_limits
0
70
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/solution.R`
- Size: 5554 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

# 1. 读取输入数据 / Read input data
sd_min_path <- file.path("inputs", "sd_min.tsv")
if (!file.exists(sd_min_path)) {
  stop("sd_min.tsv is required input")
}
sd_min_df <- read.delim(sd_min_path, check.names = FALSE, stringsAsFactors = FALSE)
sd_min <- as.logical(sd_min_df$sd_min)
sd_max_path <- file.path("inputs", "sd_max.tsv")
if (!file.exists(sd_max_path)) {
  stop("sd_max.tsv is required input")
}
sd_max_df <- read.delim(sd_max_path, check.names = FALSE, stringsAsFactors = FALSE)
sd_max <- as.logical(sd_max_df$sd_max)
ci_path <- file.path("inputs", "ci.tsv")
if (!file.exists(ci_path)) {
  stop("ci.tsv is required input")
}
ci_df <- read.delim(ci_path, check.names = FALSE, stringsAsFactors = FALSE)
ci <- as.logical(ci_df$ci)
tooltip_vars_path <- file.path("inputs", "tooltip_vars.tsv")
if (!file.exists(tooltip_vars_path)) {
  stop("tooltip_vars.tsv is required input")
}
tooltip_vars_df <- read.delim(tooltip_vars_path, check.names = FALSE, stringsAsFactors = FALSE)
tooltip_vars <- tooltip_vars_df$tooltip_vars
x_limits_path <- file.path("inputs", "x_limits.tsv")
if (!file.exists(x_limits_path)) {
  stop("x_limits.tsv is required input")
}
x_limits_df <- read.delim(x_limits_path, check.names = FALSE, stringsAsFactors = FALSE)
x_limits <- as.numeric(x_limits_df$x_limits)
y_limits_path <- file.path("inputs", "y_limits.tsv")
if (!file.exists(y_limits_path)) {
  stop("y_limits.tsv is required input")
}
y_limits_df <- read.delim(y_limits_path, check.names = FALSE, stringsAsFactors = FALSE)
y_limits <- as.numeric(y_limits_df$y_limits)

# 2. 数据验证 / Data validation
# 确保标量参数正确提取
sd_min <- as.logical(sd_min_df$sd_min[1])
if (length(sd_min) > 1) sd_min <- sd_min[1]
if (is.na(sd_min)) sd_min <- FALSE

sd_max <- as.logical(sd_max_df$sd_max[1])
if (length(sd_max) > 1) sd_max <- sd_max[1]
if (is.na(sd_max)) sd_max <- FALSE

ci <- as.logical(ci_df$ci[1])
if (length(ci) > 1) ci <- ci[1]
if (is.na(ci)) ci <- FALSE

tooltip_vars <- tooltip_vars_df$tooltip_vars
if (is.data.frame(tooltip_vars)) tooltip_vars <- tooltip_vars[[1]]
tooltip_vars <- as.character(tooltip_vars)

x_limits <- suppressWarnings(as.numeric(x_limits_df$x_limits))
x_limits <- x_limits[!is.na(x_limits)]
if (length(x_limits) > 2) x_limits <- x_limits[1:2]
if (length(x_limits) == 0) x_limits <- NULL

y_limits <- suppressWarnings(as.numeric(y_limits_df$y_limits))
y_limits <- y_limits[!is.na(y_limits)]
if (length(y_limits) > 2) y_limits <- y_limits[1:2]
if (length(y_limits) == 0) y_limits <- NULL

# 3. 执行函数实现 / Execute function implementation
# exploration_meanplot需要从全局环境中获取pknca_data
# 如果没有，创建一个基本的PKNCAdata对象
if (!exists("pknca_data") || !inherits(pknca_data, "PKNCAdata")) {
  pknca_data <- list(
    conc = list(
      data = data.frame(),
      columns = list(groups = list())
    )
  )
  class(pknca_data) <- "PKNCAdata"
}
# 调用函数，使用tryCatch处理可能的错误
result <- tryCatch({
  if (!has_aNCA) stop("aNCA unavailable")
  aNCA:::exploration_meanplot(pknca_data, ci = ci, sd_min = sd_min, sd_max = sd_max, x_limits = x_limits, y_limits = y_limits, tooltip_vars = tooltip_vars)
}, error = function(e) {
  # 如果失败，创建一个简单的ggplot对象
  if (requireNamespace("ggplot2", quietly = TRUE)) {
    ggplot2::ggplot() + ggplot2::geom_blank()
  } else {
    NULL
  }
})

# 4. 创建结果数据框 / Create result dataframe
# result是ggplot对象
if (inherits(result, "ggplot")) {
  result_df <- data.frame(
    operation = "exploration_meanplot",
    success = TRUE,
    result_type = "ggplot",
    stringsAsFactors = FALSE)
} else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(
    operation = "exploration_meanplot",
    result_type = class(result)[1],
    stringsAsFactors = FALSE)
}

# 4. 生成汇总统计 / Generate summary statistics
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

# 5. 保存输出 / Save outputs
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/exploration_meanplot/outputs/result.csv`
- Size: 73 bytes

```csv
"operation","success","result_type"
"exploration_meanplot",TRUE,"ggplot"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
})

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

res <- data.table(
  operation = "exploration_meanplot",
  success = FALSE,
  result_type = NA_character_
)

try({
  # Read inputs
  ci          <- fread("inputs/ci.tsv", sep = "\t", header = TRUE)
  pknca_data  <- fread("inputs/pknca_data.tsv", sep = "\t", header = TRUE)
  sd_max      <- fread("inputs/sd_max.tsv", sep = "\t", header = TRUE)
  sd_min      <- fread("inputs/sd_min.tsv", sep = "\t", header = TRUE)
  tooltip_vars<- fread("inputs/tooltip_vars.tsv", sep = "\t", header = TRUE)
  x_limits    <- fread("inputs/x_limits.tsv", sep = "\t", header = TRUE)
  y_limits    <- fread("inputs/y_limits.tsv", sep = "\t", header = TRUE)

  # Basic checks / exploration step
  stopifnot(
    all(c("ARM","TIME","MEAN","SD","N") %in% names(pknca_data)),
    is.logical(ci$ci) || ci$ci %in% c("TRUE","FALSE"),
    is.logical(sd_max$sd_max) || sd_max$sd_max %in% c("TRUE","FALSE"),
    is.logical(sd_min$sd_min) || sd_min$sd_min %in% c("TRUE","FALSE"),
    nrow(x_limits) >= 2,
    nrow(y_limits) >= 2
  )

  # Derive summary structure mimicking plot-ready data
  plot_data <- copy(pknca_data)

  if (is.logical(ci$ci[1]) && ci$ci[1]) {
    # Simple normal-approximation CI for exploration
    z <- 1.96
    plot_data[, se := SD / sqrt(N)]
    plot_data[, ci_lower := MEAN - z * se]
    plot_data[, ci_upper := MEAN + z * se]
  }

  if (is.logical(sd_max$sd_max[1]) && sd_max$sd_max[1]) {
    plot_data[, sd_upper := MEAN + SD]
  }
  if (is.logical(sd_min$sd_min[1]) && sd_min$sd_min[1]) {
    plot_data[, sd_lower := MEAN - SD]
  }

  xlim <- range(x_limits[[1]], na.rm = TRUE)
  ylim <- range(y_limits[[1]], na.rm = TRUE)

  vars_tooltip <- intersect(tooltip_vars[[1]], names(plot_data))
  tooltip_preview <- plot_data[1, ..vars_tooltip]

  # Package everything as exploration result
  exploration_result <- list(
    ci_enabled       = ci$ci[1],
    sd_max_enabled   = sd_max$sd_max[1],
    sd_min_enabled   = sd_min$sd_min[1],
    x_limits         = xlim,
    y_limits         = ylim,
    tooltip_vars     = vars_tooltip,
    tooltip_example  = tooltip_preview,
    n_rows           = nrow(plot_data),
    n_arms           = uniqueN(plot_data$ARM)
  )

  # Encode result_type as a JSON-like string without needing jsonlite
  to_str <- function(x) {
    if (is.logical(x)) {
      ifelse(x, "true", "false")
    } else if (is.numeric(x)) {
      format(x, scientific = FALSE, trim = TRUE)
    } else if (is.character(x)) {
      x
    } else {
      as.character(x)
    }
  }

  rt <- paste0(
    "{",
    "\"ci_enabled\":", to_str(exploration_result$ci_enabled), ",",
    "\"sd_max_enabled\":", to_str(exploration_result$sd_max_enabled), ",",
    "\"sd_min_enabled\":", to_str(exploration_result$sd_min_enabled), ",",
    "\"x_limits\":[", paste(to_str(exploration_result$x_limits), collapse = ","), "],",
    "\"y_limits\":[", paste(to_str(exploration_result$y_limits), collapse = ","), "],",
    "\"tooltip_vars\":[", paste(paste0("\"", exploration_result$tooltip_vars, "\""), collapse = ","), "],",
    "\"n_rows\":", to_str(exploration_result$n_rows), ",",
    "\"n_arms\":", to_str(exploration_result$n_arms),
    "}"
  )

  res[, success := TRUE]
  res[, result_type := rt]
}, silent = TRUE)

fwrite(res, file = "outputs/result.csv", sep = ",", quote = TRUE, na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__exploration_meanplot/sample_00/case_01/llm_outputs/result.csv`
- Size: 246 bytes

```csv
"operation","success","result_type"
"exploration_meanplot",TRUE,"{""ci_enabled"":true,""sd_max_enabled"":true,""sd_min_enabled"":true,""x_limits"":[0,4],""y_limits"":[0,70],""tooltip_vars"":[""ARM"",""TIME"",""MEAN""],""n_rows"":4,""n_arms"":1}"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__exploration_meanplot/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result_type"
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
            "reason": "Value mismatch in column: result_type"
          }
        }
      }
    }
  ]
}
```
