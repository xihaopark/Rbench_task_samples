# Case 16 - `pharmaverse/admiraldev/process_set_values_to`
**Package:** `admiraldev`  **Function:** `process_set_values_to`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_01`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Process **`set_values_to`** expressions for admiral derivations. Load `library(admiraldev)`, `library(cli)`, `library(dplyr)`, `library(purrr)`.

Follow `solution.R` for `tryCatch` and outputs.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.
```

## Input Files

**`inputs/dataset.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/expected_type.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/expected_types.tsv`**

```tsv
expected_types
"test_value"
```

**`inputs/set_values_to.tsv`**

```tsv
set_values_to
"x + y"
"a * b"
"sum(z)"
"mean(values)"
"max(data)"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiraldev))

suppressPackageStartupMessages(library(cli))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(purrr))

# 1. 读取输入数据 / Read input data
dataset_path <- file.path("inputs", "dataset.tsv")
if (!file.exists(dataset_path)) {
  stop("dataset.tsv is required input")
}
dataset <- read.delim(dataset_path, check.names = FALSE, stringsAsFactors = FALSE)
set_values_to_path <- file.path("inputs", "set_values_to.tsv")
if (!file.exists(set_values_to_path)) {
  stop("set_values_to.tsv is required input")
}
set_values_to_df <- read.delim(set_values_to_path, check.names = FALSE, stringsAsFactors = FALSE)
set_values_to <- set_values_to_df$set_values_to
expected_type_path <- file.path("inputs", "expected_type.tsv")
if (!file.exists(expected_type_path)) {
  stop("expected_type.tsv is required input")
}
expected_type <- read.delim(expected_type_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("dataset", "expected_type")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
# 处理 set_values_to 参数
# 将 set_values_to 转换为命名列表（exprs 格式）
if (is.vector(set_values_to) || is.character(set_values_to)) {
  # 如果是向量，转换为命名列表
  set_values_to_list <- rlang::exprs(!!!setNames(set_values_to, set_values_to))
} else {
  set_values_to_list <- set_values_to
}

# 处理 expected_type
if (exists("expected_type") && !is.null(expected_type)) {
  expected_types <- if(is.data.frame(expected_type) && ncol(expected_type) > 0) {
    if (nrow(expected_type) > 0) {
      setNames(expected_type[[1]], names(expected_type))
    } else {
      NULL
    }
  } else {
    expected_type
  }
} else {
  expected_types <- NULL
}

# 调用函数
result <- tryCatch({
  admiraldev::process_set_values_to(
    dataset = dataset,
    set_values_to = set_values_to_list,
    expected_types = expected_types
  )
}, error = function(e) {
  # 如果出错，返回错误信息
  error_msg <- paste("Error:", conditionMessage(e))
  error_msg
})

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    set_values_to = set_values_to,
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
"set_values_to","result"
"x + y","Error: Argument `expected_types` must be <character> with values ""numeric"" and
""character""."
"a * b","Error: Argument `expected_types` must be <character> with values ""numeric"" and
""character""."
"sum(z)","Error: Argument `expected_types` must be <character> with values ""numeric"" and
""character""."
"mean(values)","Error: Argument `expected_types` must be <character> with values ""numeric"" and
""character""."
"max(data)","Error: Argument `expected_types` must be <character> with values ""numeric"" and
""character""."
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"set_values_to, result"
```

## LLM Code

```r
library(admiraldev)
library(cli)
library(dplyr)
library(purrr)

dir.create("outputs", showWarnings = FALSE)

result <- tryCatch(
  {
    # Read input ----
    adsl <- readRDS("inputs/adsl.rds")
    param <- readRDS("inputs/params.rds")

    # Process set_values_to expressions for admiral derivations ----
    # Expecting a column `set_values_to` in param with expression lists
    out <- param %>%
      mutate(
        set_values_to = map(
          .data$set_values_to,
          ~ {
            expr <- .
            if (is.null(expr)) {
              NULL
            } else {
              admiraldev::exprs(!!!expr)
            }
          }
        )
      )

    # Save outputs ----
    write.csv(out, "outputs/result.csv", row.names = FALSE)
    saveRDS(out, "outputs/result.rds")

    out
  },
  error = function(e) {
    cli::cli_alert_danger("Error in processing: {conditionMessage(e)}")
    write.csv(
      data.frame(error = conditionMessage(e)),
      "outputs/result.csv",
      row.names = FALSE
    )
    saveRDS(
      list(error = conditionMessage(e)),
      "outputs/result.rds"
    )
    NULL
  }
)
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text

Attaching package: ‘dplyr’

The following object is masked from ‘package:admiraldev’:

    filter_if

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

✖ Error in processing: cannot open the connection
Warning message:
In gzfile(file, "rb") :
  cannot open compressed file 'inputs/adsl.rds', probable reason 'No such file or directory'
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"error"
"cannot open the connection"
```

**`outputs/result.rds`**

_RDS binary artifact generated; size: 107 bytes._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiraldev/process_set_values_to",
  "package": "admiraldev",
  "track_id": "clinical_pilot",
  "content_tag_id": "support",
  "flow_tag_id": "read",
  "scoring_mode_id": "strict",
  "code_sha256": "8782c33392dd2ceb9ec51c5816045d7dd7a33c342b5965de8c10d40e6a98c46b",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:15:37.202642",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiraldev/process_set_values_to",
  "sample_idx": 1,
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
          "reason": "Shape mismatch: ref=(5, 2) vs llm=(1, 1)"
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
