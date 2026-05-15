# Case 11 - `pharmaverse/aNCA/generate_tooltip_text`
**Package:** `aNCA`  **Function:** `generate_tooltip_text`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_02`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to implement the **Generate tooltip text** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/data.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'data.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::generate_tooltip_text` (numeric vectors are often stored in a column named like the parameter).
- `inputs/labels_df.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'labels_df.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::generate_tooltip_text` (numeric vectors are often stored in a column named like the parameter).
- `inputs/tooltip_vars.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'tooltip_vars.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::generate_tooltip_text` (numeric vectors are often stored in a column named like the parameter).
- `inputs/type.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'type.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::generate_tooltip_text` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::generate_tooltip_text` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Input Files

**`inputs/data.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/labels_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/tooltip_vars.tsv`**

```tsv
tooltip_vars
"item1"
"item2"
"item3"
"item4"
"item5"
```

**`inputs/type.tsv`**

```tsv
type
"yes"
"no"
"true"
"false"
"active"
```

## Reference Code

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
data_path <- file.path("inputs", "data.tsv")
if (!file.exists(data_path)) {
  stop("data.tsv is required input")
}
data <- read.delim(data_path, check.names = FALSE, stringsAsFactors = FALSE)
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
type_path <- file.path("inputs", "type.tsv")
if (!file.exists(type_path)) {
  stop("type.tsv is required input")
}
type_df <- read.delim(type_path, check.names = FALSE, stringsAsFactors = FALSE)
type <- type_df$type

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("data", "labels_df")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  aNCA:::generate_tooltip_text(data = data, labels_df = labels_df, tooltip_vars = tooltip_vars, type = type)
}, error = function(e) {
  # 如果函数不存在或失败，手动实现逻辑
  if (nrow(data) == 0) {
    return(character())
  }
  
  tooltip_vars <- tooltip_vars[tooltip_vars %in% names(data)]
  
  if (length(tooltip_vars) == 0) {
    return(character())
  }
  
  # Get all labels
  tooltip_components <- lapply(tooltip_vars, function(var_name) {
    label <- if (var_name %in% names(labels_df)) labels_df[[var_name]][1] else var_name
    paste0("<b>", label, "</b>: ", data[[var_name]])
  })
  
  # Combine the components for each row
  do.call(paste, c(tooltip_components, sep = "<br>"))
})

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    tooltip_vars = tooltip_vars, type = type,
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

# 6. 保存输出 / Save outputs
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
"tooltip_vars","type","result"
"item1","yes",""
"item2","no",""
"item3","true",""
"item4","false",""
"item5","active",""
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"tooltip_vars, type, result"
```

## LLM Code

```r
library(aNCA)

# Create outputs directory
dir.create("outputs", showWarnings = FALSE)

# Read inputs
data_df        <- read.delim(file.path("inputs", "data.tsv"),
                             check.names = FALSE, stringsAsFactors = FALSE)
labels_df      <- read.delim(file.path("inputs", "labels_df.tsv"),
                             check.names = FALSE, stringsAsFactors = FALSE)
tooltip_vars   <- read.delim(file.path("inputs", "tooltip_vars.tsv"),
                             check.names = FALSE, stringsAsFactors = FALSE)
type_df        <- read.delim(file.path("inputs", "type.tsv"),
                             check.names = FALSE, stringsAsFactors = FALSE)

## Map columns from helper TSVs to arguments expected by generate_tooltip_text
## Assumes:
##  - tooltip_vars has a column 'tooltip_vars'
##  - type_df has a column 'type'
##  - labels_df is already in the correct structure

if (!"tooltip_vars" %in% colnames(tooltip_vars)) {
  stop("Expected a column named 'tooltip_vars' in inputs/tooltip_vars.tsv")
}
if (!"type" %in% colnames(type_df)) {
  stop("Expected a column named 'type' in inputs/type.tsv")
}

tooltip_vars_vec <- tooltip_vars[["tooltip_vars"]]
type_vec         <- type_df[["type"]]

# Generate tooltip text
result <- aNCA::generate_tooltip_text(
  data         = data_df,
  labels_df    = labels_df,
  tooltip_vars = tooltip_vars_vec,
  type         = type_vec
)

# Write result
write.csv(result, file = file.path("outputs", "result.csv"), row.names = FALSE)
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
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"x"
""
""
""
""
""
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/aNCA/generate_tooltip_text",
  "package": "aNCA",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "analyze",
  "scoring_mode_id": "strict",
  "code_sha256": "e62771e4ac7c377fe0b619e3e56cd019de2f948179527e22186cf3722d337013",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:08:58.995693",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/aNCA/generate_tooltip_text",
  "sample_idx": 2,
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
          "reason": "Shape mismatch: ref=(5, 3) vs llm=(5, 1)"
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
