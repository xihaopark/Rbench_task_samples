# Case 10 - `pharmaverse/aNCA/format_pkncadata_intervals`
**Package:** `aNCA`  **Function:** `format_pkncadata_intervals`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to format PKNCA interval data for downstream analysis. Load `library(aNCA)`, `library(PKNCA)`, and `library(purrr)` as needed.

**Inputs:** Read with `read.delim(file.path('inputs', ...), check.names=FALSE, stringsAsFactors=FALSE)`:
- `inputs/pknca_conc.tsv`, `inputs/pknca_dose.tsv` — tables used to build **`PKNCAdata`** objects (`PKNCA::PKNCAdata(conc=, dose=)`), matching the reference.
- `inputs/start_from_last_dose.tsv` — logical scalar `start_from_last_dose`.
- `inputs/keep_interval_cols.tsv` — character vector of interval column names to keep (`keep_interval_cols`).

**Computation:** Call **`aNCA:::format_pkncadata_intervals`** with arguments `pknca_conc`, `pknca_dose`, `start_from_last_dose`, and `keep_interval_cols` (PKNCAdata objects and vectors as in the reference). This helper is **not** exported; do not use `aNCA::format_pkncadata_intervals`.

**Outputs:** Write `outputs/result.csv` for the main result; the reference also writes `outputs/summary.csv` with basic shape statistics.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
```

## Input Files

**`inputs/keep_interval_cols.tsv`**

```tsv
keep_interval_cols
"item1"
"item2"
"item3"
"item4"
"item5"
```

**`inputs/pknca_conc.tsv`**

```tsv
pknca_conc
"test_value"
```

**`inputs/pknca_dose.tsv`**

```tsv
pknca_dose
"test_value"
```

**`inputs/start_from_last_dose.tsv`**

```tsv
start_from_last_dose
FALSE
```

## Reference Code

```r
suppressPackageStartupMessages(library(aNCA))
suppressPackageStartupMessages(library(purrr))


# 1. 读取输入数据 / Read input data
pknca_conc_path <- file.path("inputs", "pknca_conc.tsv")
if (!file.exists(pknca_conc_path)) {
  stop("pknca_conc.tsv is required input")
}
pknca_conc <- read.delim(pknca_conc_path, check.names = FALSE, stringsAsFactors = FALSE)
pknca_dose_path <- file.path("inputs", "pknca_dose.tsv")
if (!file.exists(pknca_dose_path)) {
  stop("pknca_dose.tsv is required input")
}
pknca_dose <- read.delim(pknca_dose_path, check.names = FALSE, stringsAsFactors = FALSE)
start_from_last_dose_path <- file.path("inputs", "start_from_last_dose.tsv")
if (!file.exists(start_from_last_dose_path)) {
  stop("start_from_last_dose.tsv is required input")
}
start_from_last_dose_df <- read.delim(start_from_last_dose_path, check.names = FALSE, stringsAsFactors = FALSE)
start_from_last_dose <- as.logical(start_from_last_dose_df$start_from_last_dose)
keep_interval_cols_path <- file.path("inputs", "keep_interval_cols.tsv")
if (!file.exists(keep_interval_cols_path)) {
  stop("keep_interval_cols.tsv is required input")
}
keep_interval_cols_df <- read.delim(keep_interval_cols_path, check.names = FALSE, stringsAsFactors = FALSE)
keep_interval_cols <- keep_interval_cols_df$keep_interval_cols

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("pknca_conc", "pknca_dose")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
# 提取keep_interval_cols参数
if (is.data.frame(keep_interval_cols_df) && ncol(keep_interval_cols_df) > 0 && nrow(keep_interval_cols_df) > 0) {
  keep_interval_cols <- keep_interval_cols_df[[1]]
} else {
  keep_interval_cols <- NULL
}

# 创建PKNCAdata对象（简化版本）
suppressPackageStartupMessages(library(PKNCA))
pknca_conc_obj <- tryCatch({
  PKNCAdata(conc = pknca_conc, dose = pknca_dose)
}, error = function(e) {
  # 如果创建失败，使用NULL
  NULL
})

pknca_dose_obj <- tryCatch({
  PKNCAdata(conc = pknca_conc, dose = pknca_dose)
}, error = function(e) {
  NULL
})

result <- tryCatch({
  aNCA:::format_pkncadata_intervals(
    pknca_conc = pknca_conc_obj,
    pknca_dose = pknca_dose_obj,
    start_from_last_dose = start_from_last_dose,
    keep_interval_cols = keep_interval_cols
  )
}, error = function(e) {
  # 如果函数调用失败，返回一个默认的数据框
  data.frame(
    start = 0,
    end = Inf,
    stringsAsFactors = FALSE
  )
})


# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    start_from_last_dose = start_from_last_dose, keep_interval_cols = keep_interval_cols,
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
if (exists("summary_stats")) {
  write.csv(summary_stats, file.path(outputs_dir, "summary.csv"), row.names = FALSE)
}
```

## Reference Output

**`outputs/result.csv`**

```csv
"start","end"
0,Inf
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"start, end"
```

## LLM Code

```r
library(aNCA)
library(PKNCA)
library(purrr)

dir.create("outputs", showWarnings = FALSE)

## Read inputs
pknca_conc <- read.delim(
  file.path("inputs", "pknca_conc.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

pknca_dose <- read.delim(
  file.path("inputs", "pknca_dose.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

start_from_last_dose_df <- read.delim(
  file.path("inputs", "start_from_last_dose.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

keep_interval_cols_df <- read.delim(
  file.path("inputs", "keep_interval_cols.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

## Coerce scalar logical and character vector
start_from_last_dose <- as.logical(start_from_last_dose_df[[1]][1])

keep_interval_cols <- as.character(keep_interval_cols_df[[1]])
keep_interval_cols <- keep_interval_cols[!is.na(keep_interval_cols) & keep_interval_cols != ""]

## Build PKNCAdata objects
conc_obj <- PKNCAconc(pknca_conc)
dose_obj <- PKNCAdose(pknca_dose)
pkncadata <- PKNCAdata(conc = conc_obj, dose = dose_obj)

## Format intervals using internal helper
res <- aNCA:::format_pkncadata_intervals(
  pknca_conc = conc_obj,
  pknca_dose = dose_obj,
  start_from_last_dose = start_from_last_dose,
  keep_interval_cols = keep_interval_cols
)

## Write main result
write.csv(res, file = file.path("outputs", "result.csv"), row.names = FALSE)

## Also write basic summary (shape stats)
summary_df <- data.frame(
  nrow = nrow(res),
  ncol = ncol(res),
  colnames = I(list(colnames(res)))
)

write.csv(summary_df, file = file.path("outputs", "summary.csv"), row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text
Registered S3 method overwritten by 'tern':
  method   from 
  tidy.glm broom

Attaching package: ‘PKNCA’

The following object is masked from ‘package:stats’:

    filter

Error in PKNCAconc.data.frame(pknca_conc) : 
  argument "formula" is missing, with no default
Calls: PKNCAconc -> PKNCAconc.data.frame -> setdiff -> all.vars
Execution halted
```

## LLM Output Files

_No output files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/aNCA/format_pkncadata_intervals",
  "package": "aNCA",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "analyze",
  "scoring_mode_id": "strict",
  "code_sha256": "d805513ed470948ce09f66ea561b28cd2637fd26be7beb993398e81bff2ee9b3",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:08:03.166646",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/aNCA/format_pkncadata_intervals",
  "sample_idx": 0,
  "model": "openai/gpt-5.1",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "message": "No output files created",
      "stderr": "Registered S3 method overwritten by 'tern':\n  method   from \n  tidy.glm broom\n\nAttaching package: ‘PKNCA’\n\nThe following object is masked from ‘package:stats’:\n\n    filter\n\nError in PKNCAconc.data.frame(pknca_conc) : \n  argument \"formula\" is missing, with no default\nCalls: PKNCAconc -> PKNCAconc.data.frame -> setdiff -> all.vars\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
