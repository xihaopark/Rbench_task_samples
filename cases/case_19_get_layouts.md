# Case 19 - `pharmaverse/gridify/get_layouts`
**Package:** `gridify`  **Function:** `get_layouts`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
List **gridify** table layouts. Load `library(gridify)`.

**Computation:** **`gridify::get_layouts()`**.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.
```

## Input Files

**`inputs/gridify.tsv`**

```tsv
gridify
"yes"
"no"
"true"
"false"
"active"
```

## Reference Code

```r
suppressPackageStartupMessages(library(gridify))

# 1. 读取输入数据 / Read input data
# No input files required

# 3. 执行函数实现 / Execute function implementation
result <- gridify::get_layouts()

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    id = seq_along(result),
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
"id","result"
1,"complex_layout"
2,"simple_layout"
3,"pharma_layout_base"
4,"pharma_layout_A4"
5,"pharma_layout_letter"
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"id, result"
```

## LLM Code

```r
library(gridify)

dir.create("outputs", showWarnings = FALSE)

layouts <- gridify::get_layouts()

write.csv(layouts, "outputs/result.csv", row.names = FALSE)
saveRDS(layouts, "outputs/result.rds")
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
"x"
"complex_layout"
"simple_layout"
"pharma_layout_base"
"pharma_layout_A4"
"pharma_layout_letter"
```

**`outputs/result.rds`**

_RDS binary artifact generated; size: 107 bytes._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/gridify/get_layouts",
  "package": "gridify",
  "track_id": "clinical_pilot",
  "content_tag_id": "support",
  "flow_tag_id": "report",
  "scoring_mode_id": "strict",
  "code_sha256": "8e2e2e125a88378a7393fcbe44e67e3336a93184ea627321a145a10f4bb19c50",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:15:46.064647",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/gridify/get_layouts",
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
          "reason": "Shape mismatch: ref=(5, 2) vs llm=(5, 1)"
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
