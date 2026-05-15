# Case 13 - `pharmaverse/aNCA/parse_annotation`
**Package:** `aNCA`  **Function:** `parse_annotation`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_02`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to expand annotation strings with data-aware placeholders. Load `library(aNCA)`, `library(dplyr)`, and `library(glue)`.

**Inputs:** `inputs/data.tsv`, `inputs/text.tsv` — data frame and annotation text (`text` column).

**Computation:** Call **`aNCA:::parse_annotation(data=, text=)`** (internal). On failure, apply the string/`glue` fallback from the reference (e.g. newlines to `<br>`, `$` / `!` patterns). Do not assume `aNCA::parse_annotation` is exported.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
```

## Input Files

**`inputs/data.tsv`**

```tsv
data
"yes"
"no"
"true"
"false"
"active"
```

**`inputs/text.tsv`**

```tsv
text
"yes"
"no"
"true"
"false"
"active"
```

## Reference Code

```r
suppressPackageStartupMessages(library(aNCA))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(glue))

# 1. 读取输入数据 / Read input data
data_path <- file.path("inputs", "data.tsv")
if (!file.exists(data_path)) {
  stop("data.tsv is required input")
}
data <- read.delim(data_path, check.names = FALSE, stringsAsFactors = FALSE)
text_path <- file.path("inputs", "text.tsv")
if (!file.exists(text_path)) {
  stop("text.tsv is required input")
}
text_df <- read.delim(text_path, check.names = FALSE, stringsAsFactors = FALSE)
text <- text_df$text

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("data")) {
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
  aNCA:::parse_annotation(data = data, text = text)
}, error = function(e) {
  # 如果函数不存在，手动实现逻辑
  text_processed <- text %>%
    gsub("\n", "<br>", .) %>%
    gsub("\\$(\\w+)", "{unique(data[['\\1']])}", .) %>%
    gsub("!(\\w+)", "{attr(data[['\\1']], 'label')}", .)
  
  tryCatch({
    glue::glue(text_processed, .na = "ERR", .null = "ERR")
  }, error = function(e2) {
    text_processed
  })
})

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    text = text,
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
"text","result"
"yes","yes"
"no","no"
"true","true"
"false","false"
"active","active"
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"text, result"
```

## LLM Code

```r
library(aNCA)
library(dplyr)
library(glue)

dir.create("outputs", showWarnings = FALSE)

dat  <- read.delim("inputs/data.tsv", stringsAsFactors = FALSE, check.names = FALSE)
text <- read.delim("inputs/text.tsv", stringsAsFactors = FALSE, check.names = FALSE)

parse_safe <- function(data, txt) {
  res <- try(aNCA:::parse_annotation(data = data, text = txt), silent = TRUE)
  if (!inherits(res, "try-error")) return(res)

  # Fallback using glue
  # Convert newlines to <br>
  txt2 <- gsub("\r\n|\n|\r", "<br>", txt)

  # Replace $var and !var patterns with glue-style {var}
  # $var -> {var}
  txt2 <- gsub("\\$([A-Za-z0-9_.]+)", "{\\1}", txt2)
  # !var -> {var}
  txt2 <- gsub("!([A-Za-z0-9_.]+)", "{\\1}", txt2)

  # Evaluate with glue for each row of data
  out <- glue(txt2, .envir = as.environment(as.list(data)))
  as.character(out)
}

result <- text %>%
  mutate(
    expanded = parse_safe(dat, text)
  )

write.csv(result, "outputs/result.csv", row.names = FALSE)
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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error in `mutate()`:
ℹ In argument: `expanded = parse_safe(dat, text)`.
Caused by error:
! All unnamed arguments must be length 1
Backtrace:
     ▆
  1. ├─text %>% mutate(expanded = parse_safe(dat, text))
  2. ├─dplyr::mutate(., expanded = parse_safe(dat, text))
  3. ├─dplyr:::mutate.data.frame(., expanded = parse_safe(dat, text))
  4. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  5. │   ├─base::withCallingHandlers(...)
  6. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  7. │     └─mask$eval_all_mutate(quo)
  8. │       └─dplyr (local) eval()
  9. ├─global parse_safe(dat, text)
 10. │ └─glue::glue(txt2, .envir = as.environment(as.list(data)))
 11. │   └─glue::glue_data(...)
 12. │     └─base::stop("All unnamed arguments must be length 1", call. = FALSE)
 13. └─base::.handleSimpleError(...)
 14.   └─dplyr (local) h(simpleError(msg, call))
 15.     └─rlang::abort(message, class = error_class, parent = parent, call = error_call)
Execution halted
```

## LLM Output Files

_No output files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/aNCA/parse_annotation",
  "package": "aNCA",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "analyze",
  "scoring_mode_id": "strict",
  "code_sha256": "39d19adaf8b8d0ddc20a8e611d0fd1afb74907c8e9b7052db4cce4dab41e0540",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:10:11.482839",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/aNCA/parse_annotation",
  "sample_idx": 2,
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
      "stderr": "Registered S3 method overwritten by 'tern':\n  method   from \n  tidy.glm broom\n\nAttaching package: ‘dplyr’\n\nThe following objects are masked from ‘package:stats’:\n\n    filter, lag\n\nThe following objects are masked from ‘package:base’:\n\n    intersect, setdiff, setequal, union\n\nError in `mutate()`:\nℹ In argument: `expanded = parse_safe(dat, text)`.\nCaused by error:\n! All unnamed arguments must be length 1\nBacktrace:\n     ▆\n  1. ├─text %>% mutate(expanded = parse_safe(dat, text))\n  2. ├─dplyr::mutate(., expanded = parse_safe(dat, text))\n  3. ├─dplyr:::mutate.data.frame(., expanded = parse_safe(dat, text))\n  4. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)\n  5. │   ├─base::withCallingHandlers(...)\n  6. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)\n  7. │     └─mask$eval_all_mutate(quo)\n  8. │       └─dplyr (local) eval()\n  9. ├─global parse_safe(dat, text)\n 10. │ └─glue::glue(txt2, .envir = as.environment(as.list(data)))\n 11. │   └─glue::glue_data(...)\n 12. │     └─",
      "returncode": 1
    }
  ]
}
```
