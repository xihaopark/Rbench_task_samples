# Case 18 - `pharmaverse/tidytlg/add_indent`
**Package:** `tidytlg`  **Function:** `add_indent`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_03`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Compute **indentation** for TLG rows. Load `library(tidytlg)`, `library(dplyr)`.

**Computation:** The reference uses **`dplyr::mutate` / `case_when`** on `row_type` (not necessarily the required functionality); reproduce that pipeline.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.
```

## Input Files

**`inputs/df.tsv`**

```tsv
row_type	label	nested_level	group_level
1	Item1	1	1
2	Item2	2	2
3	Item3	3	3
4	Item4	4	4
5	Item5	5	5
```

## Reference Code

```r
suppressPackageStartupMessages(library(tidytlg))

suppressPackageStartupMessages(library(dplyr))

# 1. 读取输入数据 / Read input data
df_path <- file.path("inputs", "df.tsv")
if (!file.exists(df_path)) {
  stop("df.tsv is required input")
}
df <- read.delim(df_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("df")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
# set default list of variables to be removed
  remove_vars <- c("nested_level", "group_level", "value_add")

  # check if variables are already present in df, if not, add and set defaults
  if (!("nested_level" %in% names(df))) {
    df <- df %>%
      dplyr::mutate(nested_level = 0)
  }
  if (!("group_level" %in% names(df))) {
    df <- df %>%
      dplyr::mutate(group_level = 0)
  }

  # define amount to indent VALUE rows based on if a N row exists in the group
  # based on anbr
  if (!("value_add" %in% names(df))) {
    if ("anbr" %in% names(df)) {
      df <- df %>%
        group_by(anbr) %>%
        dplyr::mutate(value_add = 1 + max(as.numeric(row_type == "N")))
    } else {
      df <- df %>%
        dplyr::mutate(value_add = 1 + max(as.numeric(row_type == "N")))
    }
  }
  # if any table by headers, add one indentation to everything
  add_tableby_to_default <- any(df[["row_type"]] == "TABLE_BY_HEADER")

  result <- df %>%
    dplyr::mutate(indent = case_when(
          grepl("BY_HEADER[0-9]", row_type) ~ 0 + add_tableby_to_default + group_level,
          row_type == "HEADER" ~ 0 + add_tableby_to_default + group_level,
          row_type == "N" ~ 1 + add_tableby_to_default + group_level,
          row_type == "VALUE" ~ value_add + add_tableby_to_default + group_level,
          row_type == "NESTED" ~ nested_level + add_tableby_to_default + group_level,
          TRUE ~ 0
        )
    ) %>%
    select(-any_of(remove_vars))

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
"row_type","label","indent"
1,"Item1",0
2,"Item2",0
3,"Item3",0
4,"Item4",0
5,"Item5",0
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"row_type, label, indent"
```

## LLM Code

```r
library(dplyr)
library(tidytlg)

dir.create("outputs", showWarnings = FALSE)

# assume input is in 'inputs/input.rds' or 'inputs/input.csv'
if (file.exists("inputs/input.rds")) {
  dat <- readRDS("inputs/input.rds")
} else if (file.exists("inputs/input.csv")) {
  dat <- read.csv("inputs/input.csv", stringsAsFactors = FALSE)
} else {
  stop("No input file found in inputs/input.rds or inputs/input.csv")
}

result <- dat %>%
  mutate(
    indent = case_when(
      row_type %in% c("HEADER1", "HEADER2") ~ 0L,
      row_type %in% c("ROW", "VALUE") ~ 1L,
      row_type %in% c("SUBROW", "SUBVAL") ~ 2L,
      TRUE ~ 0L
    )
  )

write.csv(result, "outputs/result.csv", row.names = FALSE)
saveRDS(result, "outputs/result.rds")
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error: No input file found in inputs/input.rds or inputs/input.csv
Execution halted
```

## LLM Output Files

_No output files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/tidytlg/add_indent",
  "package": "tidytlg",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "report",
  "scoring_mode_id": "strict",
  "code_sha256": "8351c5d9099e02c46ec2bb1af921dcb704be17aaaab69996eb504e30123a3b5f",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:16:14.056131",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/tidytlg/add_indent",
  "sample_idx": 3,
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
      "stderr": "\nAttaching package: ‘dplyr’\n\nThe following objects are masked from ‘package:stats’:\n\n    filter, lag\n\nThe following objects are masked from ‘package:base’:\n\n    intersect, setdiff, setequal, union\n\nError: No input file found in inputs/input.rds or inputs/input.csv\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
