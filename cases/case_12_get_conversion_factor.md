# Case 12 - `pharmaverse/aNCA/get_conversion_factor`
**Package:** `aNCA`  **Function:** `get_conversion_factor`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_03`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to compute a **numeric conversion factor** between two unit strings. Load `library(units)` and optionally `library(aNCA)`.

**Inputs:** `inputs/initial_unit.tsv`, `inputs/target_unit.tsv` — read unit strings from the named columns.

**Computation:** The reference converts **1** from `initial_unit` to `target_unit` using **`units::set_units(..., mode='standard')`** and `as.numeric`, returning `1` when units match and `NA` when conversion is invalid. Do **not** require an exported `aNCA::get_conversion_factor`; match the reference numeric output.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
```

## Input Files

**`inputs/initial_unit.tsv`**

```tsv
initial_unit
"yes"
"no"
"true"
"false"
"active"
```

**`inputs/target_unit.tsv`**

```tsv
target_unit
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

## Reference Code

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
initial_unit_path <- file.path("inputs", "initial_unit.tsv")
if (!file.exists(initial_unit_path)) {
  stop("initial_unit.tsv is required input")
}
initial_unit_df <- read.delim(initial_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
initial_unit <- initial_unit_df$initial_unit
target_unit_path <- file.path("inputs", "target_unit.tsv")
if (!file.exists(target_unit_path)) {
  stop("target_unit.tsv is required input")
}
target_unit_df <- read.delim(target_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
target_unit <- target_unit_df$target_unit

# 2. 执行函数实现 / Execute function implementation
result <- tryCatch({
  conversion <- units::set_units(
    units::set_units(1, initial_unit, mode = "standard"),
    target_unit, mode = "standard"
  )
  unname(as.numeric(conversion))
}, error = function(e) {
  if (isTRUE(paste0(initial_unit) == paste0(target_unit))) {
    1
  } else {
    NA
  }
})

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    initial_unit = initial_unit, target_unit = target_unit,
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
"initial_unit","target_unit","result"
"yes","item_a",NA
"no","item_b",NA
"true","item_c",NA
"false","item_d",NA
"active","item_e",NA
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"initial_unit, target_unit, result"
```

## LLM Code

```r
library(units)
suppressWarnings({
  if (requireNamespace("aNCA", quietly = TRUE)) {
    library(aNCA)
  }
})

dir.create("outputs", showWarnings = FALSE)

initial <- read.delim("inputs/initial_unit.tsv", stringsAsFactors = FALSE, check.names = FALSE)
target  <- read.delim("inputs/target_unit.tsv",  stringsAsFactors = FALSE, check.names = FALSE)

# Assume there is a single column in each file with unit strings
init_col  <- initial[[1]]
targ_col  <- target[[1]]

get_conv_factor <- function(init_u, targ_u) {
  if (is.na(init_u) || is.na(targ_u)) return(NA_real_)
  init_u <- trimws(init_u)
  targ_u <- trimws(targ_u)
  if (init_u == "" || targ_u == "") return(NA_real_)
  if (identical(init_u, targ_u)) return(1)

  v <- tryCatch(
    set_units(1, init_u, mode = "standard"),
    error = function(e) NA
  )
  if (anyNA(v)) return(NA_real_)

  out <- tryCatch(
    as.numeric(set_units(v, targ_u, mode = "standard")),
    error = function(e) NA_real_
  )
  out
}

n <- max(length(init_col), length(targ_col))
init_vec <- rep(init_col, length.out = n)
targ_vec <- rep(targ_col, length.out = n)

result <- mapply(get_conv_factor, init_vec, targ_vec)

out_df <- data.frame(
  initial_unit = init_vec,
  target_unit  = targ_vec,
  conversion_factor = result,
  stringsAsFactors = FALSE
)

write.csv(out_df, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text
udunits database from /usr/share/xml/udunits/udunits2.xml
Registered S3 method overwritten by 'tern':
  method   from 
  tidy.glm broom
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"initial_unit","target_unit","conversion_factor"
"yes","item_a",NA
"no","item_b",NA
"true","item_c",NA
"false","item_d",NA
"active","item_e",NA
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/aNCA/get_conversion_factor",
  "package": "aNCA",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "analyze",
  "scoring_mode_id": "strict",
  "code_sha256": "2b10a96aab5327f35d212efb5cfb21f8768daa4557799d61c37737853c7182b2",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:09:11.769664",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/aNCA/get_conversion_factor",
  "sample_idx": 3,
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
          "reason": "Missing column: result"
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
