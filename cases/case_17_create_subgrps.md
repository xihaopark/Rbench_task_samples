# Case 17 - `pharmaverse/metatools/create_subgrps`
**Package:** `metatools`  **Function:** `create_subgrps`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Derive **subgroup labels** from numeric ranges and definitions. Load `library(metatools)`, `library(cli)`, `library(dplyr)`, `library(purrr)`, `library(stringr)`.

**Computation:** Reproduce **`dash_to_eq`**, `map2_chr`, `eval(parse(...))`**, and exclusivity checks as in `solution.R`.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.
```

## Input Files

**`inputs/grp_defs.tsv`**

```tsv
grp_defs
"item1"
"item2"
"item3"
"item4"
"item5"
```

**`inputs/grp_labs.tsv`**

```tsv
grp_labs
"option_a"
"option_b"
"option_c"
"option_d"
"option_e"
```

**`inputs/ref_vec.tsv`**

```tsv
ref_vec
0.1
1.5
10.0
100.0
1000.0
```

## Reference Code

```r
suppressPackageStartupMessages(library(metatools))

suppressPackageStartupMessages(library(cli))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(purrr))
suppressPackageStartupMessages(library(stringr))

# 1. 读取输入数据 / Read input data
ref_vec_path <- file.path("inputs", "ref_vec.tsv")
if (!file.exists(ref_vec_path)) {
  stop("ref_vec.tsv is required input")
}
ref_vec_df <- read.delim(ref_vec_path, check.names = FALSE, stringsAsFactors = FALSE)
ref_vec <- as.numeric(ref_vec_df$ref_vec)
grp_defs_path <- file.path("inputs", "grp_defs.tsv")
if (!file.exists(grp_defs_path)) {
  stop("grp_defs.tsv is required input")
}
grp_defs_df <- read.delim(grp_defs_path, check.names = FALSE, stringsAsFactors = FALSE)
grp_defs <- grp_defs_df$grp_defs
grp_labs_path <- file.path("inputs", "grp_labs.tsv")
if (!file.exists(grp_labs_path)) {
  stop("grp_labs.tsv is required input")
}
grp_labs_df <- read.delim(grp_labs_path, check.names = FALSE, stringsAsFactors = FALSE)
grp_labs <- grp_labs_df$grp_labs

# 2. 执行函数实现 / Execute function implementation
if (!is.numeric(ref_vec)) {
    cli_abort("ref_vec must be numeric")
}
if (is.null(grp_labs)) {
  grp_labs <- grp_defs
}

# Create equations used to derive the subgroups
# dash_to_eq 返回类似 "x>=Value_A & x<=Value_B" 的字符串
# 需要将其转换为可执行的函数
equations <- map2_chr(grp_defs, grp_labs, function(def, lab) {
  # 提取标量值
  def_val <- if(is.data.frame(def) || length(def) > 1) def[1] else def
  lab_val <- if(is.data.frame(lab) || length(lab) > 1) lab[1] else lab
  
  if (str_detect(def_val, "-")) {
    # 使用 dash_to_eq 转换
    eq_str <- dash_to_eq(def_val)
    # dash_to_eq 返回 "x>=Value_A & x<=Value_B"，需要包装成函数
    # 注意：eq_str 中的 x 会被函数参数 x 替换
    paste0("function(x){if_else(", eq_str, ", '", lab_val, "', '')}")
  } else {
    # 简单的条件 - 需要确保是有效的 R 表达式
    # 如果 def_val 是值（如 "Value_A"），需要转换为比较表达式
    paste0("function(x){if_else(x == '", def_val, "', '", lab_val, "', '')}")
  }
})

# Apply equations
if (all(!is.na(equations))) {
  out <- equations %>%
    map(~ eval(parse(text = .))) %>%
    map(~ .(ref_vec)) %>%
    reduce(str_c) %>%
    replace(. == "", NA)
  } else {
    na_index <- which(is.na(equations))
    bad_defs <- grp_defs[na_index]
    cli_abort(paste(
      "Unable to decipher the following group definition{?s}: {bad_defs}.",
      "Please check your controlled terminology."
    ))
  }
  # Find non-exclusive subgroups i.e., values that have been mapped to two groups
  non_excl <- out |>
    discard(is.na) |>
    map(~ grp_labs[str_detect(.x, grp_labs)]) |>
    keep(~ length(.) > 1) |>
    unique()

  # Throw error if groups are not exclusive
  if (length(non_excl) > 0) {
    msg <- map_chr(non_excl, ~ {
      items <- paste(.x, collapse = ", ")
    }) %>%
      paste0(seq_along(.), ". ", .)

    cli_abort(c(
      "Group definitions are not exclusive. Please check your controlled terminology",
      "The following group definitions overlap:",
      msg
    ))
  }
result <- out

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    ref_vec = ref_vec, grp_defs = grp_defs,
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
"ref_vec","grp_defs","result"
0.1,"item1",NA
1.5,"item2",NA
10,"item3",NA
100,"item4",NA
1000,"item5",NA
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"ref_vec, grp_defs, result"
```

## LLM Code

```r
library(metatools)
library(cli)
library(dplyr)
library(purrr)
library(stringr)

dir.create("outputs", showWarnings = FALSE)

dash_to_eq <- function(x) {
  x %>%
    str_replace_all("–", "-") %>%
    str_replace_all("—", "-") %>%
    str_replace_all("−", "-") %>%
    str_replace_all(":", "-") %>%
    str_replace_all("\\s+", "") %>%
    str_replace_all("^(\\d+)-(\\d+)$", "x>=\\1 & x<=\\2") %>%
    str_replace_all("^<(\\d+\\.*\\d*)$", "x<\\1") %>%
    str_replace_all("^<=(\\d+\\.*\\d*)$", "x<=\\1") %>%
    str_replace_all("^>(\\d+\\.*\\d*)$", "x>\\1") %>%
    str_replace_all("^>=(\\d+\\.*\\d*)$", "x>=\\1")
}

# Example template for ranges and labels; adjust to actual incoming data structure if different
# Expecting a data.frame 'ranges_df' with columns:
#   var   (variable name to cut)
#   label (subgroup label)
#   range (range definition as text, e.g. "0-10", "<5", ">=20")
#
# If the input is from a CSV, read it here, e.g.:
# ranges_df <- read.csv("inputs/ranges.csv", stringsAsFactors = FALSE)

# Placeholder for user-provided or upstream-created 'ranges_df'
# Remove or replace with actual data loading in real use
ranges_df <- tibble::tibble(
  var   = c("x", "x", "x"),
  label = c("low", "mid", "high"),
  range = c("<10", "10-20", ">20")
)

ranges_parsed <- ranges_df %>%
  mutate(
    expr_txt = dash_to_eq(range),
    expr     = map(expr_txt, ~ parse(text = .x)[[1]])
  )

# Example numeric data; replace with actual analysis data frame:
#   analysis_df contains at least the variable named in 'var'
analysis_df <- tibble::tibble(
  x = seq(0, 30, by = 1)
)

assign_subgroup <- function(data, rules_df, var_name) {
  x_vals <- data[[var_name]]

  cond_matrix <- map_lgl(
    seq_len(nrow(rules_df)),
    function(i) {
      expr_i <- rules_df$expr[[i]]
      eval(expr_i, envir = list(x = x_vals))
    }
  )

  cond_matrix <- matrix(
    cond_matrix,
    nrow = length(x_vals),
    ncol = nrow(rules_df),
    byrow = FALSE
  )

  overlaps <- rowSums(cond_matrix) > 1
  if (any(overlaps, na.rm = TRUE)) {
    cli::cli_abort("Overlapping subgroup definitions detected for variable {.val {var_name}}.")
  }

  no_match <- rowSums(cond_matrix, na.rm = TRUE) == 0
  subgroup <- rep(NA_character_, length(x_vals))
  idx <- max.col(cond_matrix, ties.method = "first")
  subgroup[!no_match] <- rules_df$label[idx[!no_match]]

  subgroup
}

result_df <- analysis_df

vars <- unique(ranges_parsed$var)

for (v in vars) {
  rules_v <- ranges_parsed %>% filter(var == v)
  subgroup_col <- assign_subgroup(analysis_df, rules_v, v)
  result_df[[paste0(v, "_subgroup")]] <- subgroup_col
}

write.csv(result_df, file = "outputs/result.csv", row.names = FALSE)
saveRDS(result_df, file = "outputs/result.rds")
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

Error in `map_lgl()`:
ℹ In index: 1.
Caused by error:
! Result must be length 1, not 31.
Backtrace:
     ▆
  1. ├─global assign_subgroup(analysis_df, rules_v, v)
  2. │ └─purrr::map_lgl(...)
  3. │   └─purrr:::map_("logical", .x, .f, ..., .progress = .progress)
  4. │     ├─purrr:::with_indexed_errors(...)
  5. │     │ └─base::withCallingHandlers(...)
  6. │     └─purrr:::call_with_cleanup(...)
  7. └─base::.handleSimpleError(...)
  8.   └─purrr (local) h(simpleError(msg, call))
  9.     └─cli::cli_abort(...)
 10.       └─rlang::abort(...)
Execution halted
```

## LLM Output Files

_No output files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/metatools/create_subgrps",
  "package": "metatools",
  "track_id": "clinical_pilot",
  "content_tag_id": "support",
  "flow_tag_id": "read",
  "scoring_mode_id": "strict",
  "code_sha256": "4a929316cba87b2ea1bf497b6f18e8ca08e76f4130e3e815eaaef6c05caa9c65",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:16:02.630461",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/metatools/create_subgrps",
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
      "stderr": "\nAttaching package: ‘dplyr’\n\nThe following objects are masked from ‘package:stats’:\n\n    filter, lag\n\nThe following objects are masked from ‘package:base’:\n\n    intersect, setdiff, setequal, union\n\nError in `map_lgl()`:\nℹ In index: 1.\nCaused by error:\n! Result must be length 1, not 31.\nBacktrace:\n     ▆\n  1. ├─global assign_subgroup(analysis_df, rules_v, v)\n  2. │ └─purrr::map_lgl(...)\n  3. │   └─purrr:::map_(\"logical\", .x, .f, ..., .progress = .progress)\n  4. │     ├─purrr:::with_indexed_errors(...)\n  5. │     │ └─base::withCallingHandlers(...)\n  6. │     └─purrr:::call_with_cleanup(...)\n  7. └─base::.handleSimpleError(...)\n  8.   └─purrr (local) h(simpleError(msg, call))\n  9.     └─cli::cli_abort(...)\n 10.       └─rlang::abort(...)\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
