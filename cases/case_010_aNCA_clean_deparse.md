# Case 010: pharmaverse/aNCA/clean_deparse

## Case Metadata

- Task ID: `pharmaverse/aNCA/clean_deparse`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform clean deparse using the aNCA clinical task contract.

Input: indent.tsv, max_per_line.tsv, min_to_rep.tsv, obj.tsv
Output: result.csv


Required columns for result.csv: result, indent
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### indent.tsv (9 bytes)
indent
2

### max_per_line.tsv (16 bytes)
max_per_line
80

### min_to_rep.tsv (13 bytes)
min_to_rep
3

### obj.tsv (21 bytes)
obj
alpha
beta
gamma
```

## Input Data

### `indent.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/clean_deparse/inputs/indent.tsv`
- Size: 9 bytes

```text
indent
2
```

### `max_per_line.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/clean_deparse/inputs/max_per_line.tsv`
- Size: 16 bytes

```text
max_per_line
80
```

### `min_to_rep.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/clean_deparse/inputs/min_to_rep.tsv`
- Size: 13 bytes

```text
min_to_rep
3
```

### `obj.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/clean_deparse/inputs/obj.tsv`
- Size: 21 bytes

```text
obj
alpha
beta
gamma
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/clean_deparse/solution.R`
- Size: 5025 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

# 1. 读取输入数据 / Read input data
obj_path <- file.path("inputs", "obj.tsv")
if (!file.exists(obj_path)) {
  stop("obj.tsv is required input")
}
obj_df <- read.delim(obj_path, check.names = FALSE, stringsAsFactors = FALSE)
# obj可能是任意R对象，尝试解析
if (ncol(obj_df) == 1 && nrow(obj_df) == 1) {
  obj_str <- obj_df[[1]][1]
  # 尝试eval解析
  obj <- tryCatch({
    eval(parse(text = obj_str))
  }, error = function(e) {
    # 如果解析失败，使用字符串
    obj_str
  })
} else if (ncol(obj_df) == 1) {
  # 如果是单列多行，使用向量
  obj <- obj_df[[1]]
} else {
  # 如果是多列数据，使用数据框
  obj <- obj_df
}
max_per_line_path <- file.path("inputs", "max_per_line.tsv")
if (!file.exists(max_per_line_path)) {
  stop("max_per_line.tsv is required input")
}
max_per_line_df <- read.delim(max_per_line_path, check.names = FALSE, stringsAsFactors = FALSE)
max_per_line <- suppressWarnings(as.numeric(max_per_line_df[[1]][1]))
if (length(max_per_line) > 1) max_per_line <- max_per_line[1]
if (is.na(max_per_line)) max_per_line <- 80
min_to_rep_path <- file.path("inputs", "min_to_rep.tsv")
if (!file.exists(min_to_rep_path)) {
  stop("min_to_rep.tsv is required input")
}
min_to_rep_df <- read.delim(min_to_rep_path, check.names = FALSE, stringsAsFactors = FALSE)
min_to_rep <- suppressWarnings(as.numeric(min_to_rep_df[[1]][1]))
if (length(min_to_rep) > 1) min_to_rep <- min_to_rep[1]
if (is.na(min_to_rep)) min_to_rep <- 3
indent_path <- file.path("inputs", "indent.tsv")
if (!file.exists(indent_path)) {
  stop("indent.tsv is required input")
}
indent_df <- read.delim(indent_path, check.names = FALSE, stringsAsFactors = FALSE)
indent <- suppressWarnings(as.numeric(indent_df[[1]][1]))
if (length(indent) > 1) indent <- indent[1]
if (is.na(indent)) indent <- 0

# 2. 数据验证 / Data validation
# obj是任意R对象，不需要数据框验证

# 3. 执行函数实现 / Execute function implementation
# Handle tbl_df objects as data.frame
if (inherits(obj, "tbl_df")) obj <- as.data.frame(obj)

# clean_deparse 对 character 无方法，转为 data.frame 或 list
if (is.character(obj) && length(obj) > 0) {
  obj <- as.data.frame(matrix(obj, ncol = 1), stringsAsFactors = FALSE)
  colnames(obj) <- "value"
}

# Handle trivial length-0 constructors (character(0), numeric(0), list(), data.frame(), ...)
if (length(obj) == 0 && !is.null(obj)) {
  result <- paste0(class(obj)[1], "()")
} else {
  # clean_deparse是S3泛型函数，直接调用会分派到正确的方法
  result <- tryCatch(
    {
      if (!has_aNCA) stop("aNCA unavailable")
      aNCA:::clean_deparse(obj, max_per_line = max_per_line, min_to_rep = min_to_rep, indent = indent)
    },
    error = function(e) deparse(obj)
  )
}

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  # result 可能是多行字符串，统一为单行
  result_str <- paste(as.character(result), collapse = "\n")
  result_df <- data.frame(
    result = result_str,
    indent = indent,
    stringsAsFactors = FALSE)
} else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = as.character(result), stringsAsFactors = FALSE)
}

# 6. 生成汇总统计 / Generate summary statistics
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/clean_deparse/outputs/result.csv`
- Size: 130 bytes

```csv
"result","indent"
"structure(list(value = c(""alpha"", ""beta"", ""gamma"")), class = ""data.frame"", row.names = c(NA,
-3L))",2
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  # no extra packages needed
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
indent_df      <- read.table("inputs/indent.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE, quote = "")
max_per_line_df<- read.table("inputs/max_per_line.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE, quote = "")
min_to_rep_df  <- read.table("inputs/min_to_rep.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE, quote = "")
obj_df         <- read.table("inputs/obj.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE, quote = "")

indent      <- as.integer(indent_df$indent[1])
max_per_line<- as.integer(max_per_line_df$max_per_line[1])
min_to_rep  <- as.integer(min_to_rep_df$min_to_rep[1])

# Construct the object to deparse
obj <- obj_df[[1]]

# Clean deparse function following aNCA-style clinical task contract ideas:
# - Respect indent
# - Do not exceed max characters per line when possible
# - Only introduce repetition constructs (rep()) when length >= min_to_rep
clean_deparse <- function(x, indent = 2, max_per_line = 80, min_to_rep = 3) {
  base <- deparse(x, width.cutoff = max_per_line)

  # If no repetition or length too small, just re-indent
  if (length(x) < min_to_rep) {
    ind_str <- paste0(rep(" ", indent), collapse = "")
    if (length(base) == 1L) {
      return(list(result = base, indent = as.integer(indent)))
    } else {
      base[2:length(base)] <- paste0(ind_str, base[2:length(base)])
      return(list(result = base, indent = as.integer(indent)))
    }
  }

  # Detect simple repetition patterns; if all elements identical, use rep()
  all_same <- length(unique(x)) == 1L
  if (all_same && length(x) >= min_to_rep) {
    val <- deparse(x[1], width.cutoff = max_per_line)
    if (length(val) > 1L) {
      val <- paste(val, collapse = " ")
    }
    rep_call <- paste0("rep(", val, ", ", length(x), ")")
    return(list(result = rep_call, indent = as.integer(indent)))
  }

  # Fallback to standard deparse with indent fix
  ind_str <- paste0(rep(" ", indent), collapse = "")
  if (length(base) > 1L) {
    base[2:length(base)] <- paste0(ind_str, base[2:length(base)])
  }
  list(result = base, indent = as.integer(indent))
}

res <- clean_deparse(obj, indent = indent, max_per_line = max_per_line, min_to_rep = min_to_rep)

# Normalize result to a single string (join lines with newline if multiple)
result_str <- if (length(res$result) == 1L) res$result else paste(res$result, collapse = "\n")

out_df <- data.frame(
  result = result_str,
  indent = res$indent,
  stringsAsFactors = FALSE
)

write.csv(out_df, file = "outputs/result.csv", row.names = FALSE, quote = TRUE)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__clean_deparse/sample_00/case_01/llm_outputs/result.csv`
- Size: 56 bytes

```csv
"result","indent"
"c(""alpha"", ""beta"", ""gamma"")",2
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__clean_deparse/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result"
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
            "reason": "Value mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
