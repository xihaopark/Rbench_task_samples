# Case 04 - `pharmaverse/admiral/compute_map`
**Package:** `admiral`  **Function:** `compute_map`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to compute **mean arterial pressure (MAP)**. Load `library(admiral)`.

**Inputs:** `inputs/sysbp.tsv`, `inputs/hr.tsv`, `inputs/diabp.tsv`, each with one numeric column.

**Computation:** Read numeric vectors from the first column of each file and call `admiral::compute_map(sysbp, hr, diabp)` using that argument order.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` with columns `diabp`, `sysbp`, `result`
- `outputs/summary.csv` with columns `n_rows`, `n_cols`, `col_names`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` and write CSV with `write.csv(..., row.names=FALSE)`.
```

## Prompt Repair Note

This display prompt lightly clarifies the output schema and includes `summary.csv`, because the reference output and evaluator compare both files. The computation and inputs are unchanged from the stable task.

## Input Files

**`inputs/diabp.tsv`**

```tsv
diabp
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/hr.tsv`**

```tsv
hr
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/sysbp.tsv`**

```tsv
sysbp
0.1
1.5
10.0
100.0
1000.0
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

suppressPackageStartupMessages(library(rlang))
# 1. 读取输入数据 / Read input data
diabp_path <- file.path("inputs", "diabp.tsv")
if (!file.exists(diabp_path)) {
  stop("diabp.tsv is required input")
}
diabp_df <- read.delim(diabp_path, check.names = FALSE, stringsAsFactors = FALSE)
diabp <- as.numeric(diabp_df$diabp)
sysbp_path <- file.path("inputs", "sysbp.tsv")
if (!file.exists(sysbp_path)) {
  stop("sysbp.tsv is required input")
}
sysbp_df <- read.delim(sysbp_path, check.names = FALSE, stringsAsFactors = FALSE)
sysbp <- as.numeric(sysbp_df$sysbp)
hr_path <- file.path("inputs", "hr.tsv")
if (!file.exists(hr_path)) {
  stop("hr.tsv is required input")
}
hr_df <- read.delim(hr_path, check.names = FALSE, stringsAsFactors = FALSE)
hr <- as.numeric(hr_df$hr)

# 3. 执行函数实现 / Execute function implementation
sysbp_path <- file.path("inputs", "sysbp.tsv")
if (!file.exists(sysbp_path)) {
  stop("sysbp.tsv is required input")
}
sysbp_df <- read.delim(sysbp_path, check.names = FALSE, stringsAsFactors = FALSE)
sysbp <- if(ncol(sysbp_df) > 0 && nrow(sysbp_df) > 0) sysbp_df[[1]] else sysbp_df
hr_path <- file.path("inputs", "hr.tsv")
if (!file.exists(hr_path)) {
  stop("hr.tsv is required input")
}
hr_df <- read.delim(hr_path, check.names = FALSE, stringsAsFactors = FALSE)
hr <- if(ncol(hr_df) > 0 && nrow(hr_df) > 0) hr_df[[1]] else hr_df
diabp_path <- file.path("inputs", "diabp.tsv")
if (!file.exists(diabp_path)) {
  stop("diabp.tsv is required input")
}
diabp_df <- read.delim(diabp_path, check.names = FALSE, stringsAsFactors = FALSE)
diabp <- if(ncol(diabp_df) > 0 && nrow(diabp_df) > 0) diabp_df[[1]] else diabp_df
result <- admiral::compute_map(sysbp, hr, diabp)

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    diabp = diabp, sysbp = sysbp,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
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
"diabp","sysbp","result"
0.1,0.1,0.1
1.5,1.5,1.5
10,10,10
100,100,100
1000,1000,1000
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"diabp, sysbp, result"
```

## LLM Code

```r
library(admiral)
library(rlang)

dir.create("outputs", showWarnings = FALSE)

sysbp <- read.delim("inputs/sysbp.tsv", header = TRUE, sep = "\t", check.names = FALSE)
hr    <- read.delim("inputs/hr.tsv",    header = TRUE, sep = "\t", check.names = FALSE)
diabp <- read.delim("inputs/diabp.tsv", header = TRUE, sep = "\t", check.names = FALSE)

# Assume the first column in each file contains the numeric values
sysbp_val <- sysbp[[1]]
hr_val    <- hr[[1]]
diabp_val <- diabp[[1]]

map_val <- admiral::compute_map(sysbp_val, hr_val, diabp_val)

result <- data.frame(
  SYSBP = sysbp_val,
  HR    = hr_val,
  DIABP = diabp_val,
  MAP   = map_val
)

write.csv(result, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"SYSBP","HR","DIABP","MAP"
0.1,0.1,0.1,0.1
1.5,1.5,1.5,1.5
10,10,10,10
100,100,100,100
1000,1000,1000,1000
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/compute_map",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "c6c2fdb0d330f47bf8d92f8d2c2dd9668eaa697a9b14c2a2d8016cf4c689a743",
  "raw_response": "```r\nlibrary(admiral)\nlibrary(rlang)\n\ndir.create(\"outputs\", showWarnings = FALSE)\n\nsysbp <- read.delim(\"inputs/sysbp.tsv\", header = TRUE, sep = \"\\t\", check.names = FALSE)\nhr    <- read.delim(\"inputs/hr.tsv\",    header = TRUE, sep = \"\\t\", check.names = FALSE)\ndiabp <- read.delim(\"inputs/diabp.tsv\", header = TRUE, sep = \"\\t\", check.names = FALSE)\n\n# Assume the first column in each file contains the numeric values\nsysbp_val <- sysbp[[1]]\nhr_val    <- hr[[1]]\ndiabp_val <- diabp[[1]]\n\nmap_val <- admiral::compute_map(sysbp_val, hr_val, diabp_val)\n\nresult <- data.frame(\n  SYSBP = sysbp_val,\n  HR    = hr_val,\n  DIABP = diabp_val,\n  MAP   = map_val\n)\n\nwrite.csv(result, \"outputs/result.csv\", row.names = FALSE)\n```",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:11:33.896276",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/compute_map",
  "sample_idx": 0,
  "model": "openai/gpt-5.1",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "comparison": {
        "result.csv": {
          "match": false,
          "reason": "Shape mismatch: ref=(5, 3) vs llm=(5, 4)"
        },
        "summary.csv": {
          "match": false,
          "reason": "File not generated"
        }
      },
      "returncode": 0,
      "normalizations": []
    }
  ]
}
```
