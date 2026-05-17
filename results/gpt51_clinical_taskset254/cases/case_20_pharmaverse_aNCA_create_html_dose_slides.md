# Case 20 - `pharmaverse/aNCA/create_html_dose_slides`

**Package:** `aNCA`  **Function:** `create_html_dose_slides`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `medium`

## Audit Evidence

Reference creates QMD dose slides via `aNCA:::create_qmd_dose_slides` and returns scalar `path`; current/simple prompts are generic enough that both generated solutions produce multi-row HTML/table summaries instead of the 1-row path result.

## Task Prompt From `task.json`

```text
Write R code to implement the **Create html dose slides** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/path.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'path.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/res_dose_slides.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'res_dose_slides.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/title.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'title.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Create Html Dose Slides** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for create HTML dose slides. The available input files are `inputs/path.tsv`, `inputs/res_dose_slides.tsv`, `inputs/title.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### path.tsv (26 bytes)
path
AVAL
AVISITN
USUBJID

### res_dose_slides.tsv (37 bytes)
res_dose_slides
AVAL
AVISITN
USUBJID

### title.tsv (27 bytes)
title
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform create HTML dose slides using the aNCA clinical task contract.

Input: path.tsv, res_dose_slides.tsv, title.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### path.tsv (26 bytes)
path
AVAL
AVISITN
USUBJID

### res_dose_slides.tsv (37 bytes)
res_dose_slides
AVAL
AVISITN
USUBJID

### title.tsv (27 bytes)
title
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`path.tsv`**

```tsv
path
"temp_file.txt"

```

**`res_dose_slides.tsv`**

```tsv
res_dose_slides
"yes"
"no"
"true"
"false"
"active"

```

**`title.tsv`**

```tsv
title
"yes"
"no"
"true"
"false"
"active"

```

## Reference Output Files

**`result.csv`**

```csv
"id","result"
1,"temp_file.txt"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"id, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
res_dose_slides_path <- file.path("inputs", "res_dose_slides.tsv")
if (!file.exists(res_dose_slides_path)) {
  stop("res_dose_slides.tsv is required input")
}
res_dose_slides <- read.delim(res_dose_slides_path, check.names = FALSE, stringsAsFactors = FALSE)
path_path <- file.path("inputs", "path.tsv")
if (!file.exists(path_path)) {
  stop("path.tsv is required input")
}
path_df <- read.delim(path_path, check.names = FALSE, stringsAsFactors = FALSE)
path <- path_df[[1]][1]
if (length(path) > 1) path <- path[1]
if (is.na(path)) path <- "temp_output.html"
title_path <- file.path("inputs", "title.tsv")
if (!file.exists(title_path)) {
  stop("title.tsv is required input")
}
title_df <- read.delim(title_path, check.names = FALSE, stringsAsFactors = FALSE)
title <- title_df[[1]][1]
if (length(title) > 1) title <- title[1]
if (is.na(title)) title <- "Dose Slides"

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("res_dose_slides")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}
# path和title是标量字符串，不需要数据框验证
# res_dose_slides需要是列表
if (!is.list(res_dose_slides) || (is.list(res_dose_slides) && length(res_dose_slides) > 0 && !is.list(res_dose_slides[[1]]))) {
  # 如果只是数据框或原子向量，转换为列表格式
  if (is.data.frame(res_dose_slides)) {
    res_dose_slides <- list(list(
      info = res_dose_slides,
      group = "Group1",
      ind_params = list(),
      ind_plots = list(),
      statistics = res_dose_slides,
      meanplot = NULL,
      linplot = NULL,
      boxplot = NULL
    ))
  } else {
    # 如果是原子向量，创建空列表
    res_dose_slides <- list()
  }
}
# 确保res_dose_slides是命名列表
if (is.null(names(res_dose_slides)) && length(res_dose_slides) > 0) {
  names(res_dose_slides) <- paste0("group", seq_along(res_dose_slides))
}

# 3. 执行函数实现 / Execute function implementation
output_format <- tools::file_ext(path)
quarto_path <- gsub(paste0("\\.", output_format, "$"), ".qmd", path)
use_plotly <- if (output_format == "html") TRUE else FALSE
output_format <- if (output_format == "html") "all" else output_format

aNCA:::create_qmd_dose_slides(
  res_dose_slides,
  quarto_path = quarto_path,
  title = title,
  use_plotly = use_plotly
)
# 检查quarto是否可用，如果不可用则跳过渲染
if (requireNamespace("quarto", quietly = TRUE)) {
  tryCatch({
    quarto::quarto_render(input = quarto_path, output_format = output_format)
  }, error = function(e) {
    # 如果quarto渲染失败，只记录警告但不停止
    warning("Quarto rendering failed: ", e$message)
  }, warning = function(w) {
    # 忽略警告
    NULL
  })
} else {
  warning("Quarto package not available, skipping rendering")
}
result <- path

# 5. 创建结果数据框 / Create result dataframe
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

## Current Prompt LLM Code

```r
#!/usr/bin/env Rscript

# Load required packages (base only; no external dependencies)
# Create outputs directory
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Helper: read TSV preserving header, strings, and types simply
read_tsv <- function(path) {
  read.table(
    path,
    header = TRUE,
    sep = "\t",
    quote = "",
    comment.char = "",
    check.names = FALSE,
    stringsAsFactors = FALSE
  )
}

# Read inputs
path_tbl  <- read_tsv("inputs/path.tsv")
res_tbl   <- read_tsv("inputs/res_dose_slides.tsv")
title_tbl <- read_tsv("inputs/title.tsv")

# Helper: for aNCA-like scalar handling:
# if a table has exactly one row and one column, treat as scalar;
# otherwise keep full vector/table for row-wise alignment.
scalar_or_vec <- function(tbl) {
  if (nrow(tbl) == 1L && ncol(tbl) == 1L) {
    as.vector(tbl[[1L]])
  } else {
    tbl
  }
}

path_val  <- scalar_or_vec(path_tbl)
res_val   <- scalar_or_vec(res_tbl)
title_val <- scalar_or_vec(title_tbl)

# Build a compact, inspectable result:
# Put each input either as scalar or as column(s), preserving alignment if vectors.
# If any input is a data.frame with >1 row, align by row index.
inputs_list <- list(
  path  = path_val,
  res_dose_slides = res_val,
  title = title_val
)

# Normalize all inputs to a data.frame with compatible row counts.
# Strategy:
# - Determine max number of rows across all non-scalar inputs.
# - Scalars are repeated to match that length if needed.
# - If there are no non-scalar inputs, create a single-row result.
get_nrow <- function(x) {
  if (is.data.frame(x)) nrow(x) else length(x)
}

n_rows <- max(
  1L,
  unlist(lapply(inputs_list, get_nrow), use.names = FALSE)
)

expand_to_n <- function(x, n) {
  if (is.data.frame(x)) {
    if (nrow(x) == n) {
      x
    } else if (nrow(x) == 1L && n > 1L) {
      x[rep(1L, n), , drop = FALSE]
    } else if (nrow(x) == 0L && n > 0L) {
      x[rep(NA_integer_, n), , drop = FALSE]
    } else {
      stop("Row count mismatch in non-scalar input.")
    }
  } else { # vector/scalar
    if (length(x) == n) {
      data.frame(value = x, check.names = FALSE)
    } else if (length(x) == 1L && n > 1L) {
      data.frame(value = rep(x, n), check.names = FALSE)
    } else if (length(x) == 0L && n > 0L) {
      data.frame(value = rep(NA, n), check.names = FALSE)
    } else {
      stop("Length mismatch in vector/scalar input.")
    }
  }
}

# Expand each input and assemble columns with clear naming
expanded <- lapply(names(inputs_list), function(nm) {
  obj <- inputs_list[[nm]]
  df  <- expand_to_n(obj, n_rows)
  if (ncol(df) == 1L && colnames(df)[1L] == "value") {
    colnames(df) <- nm
  } else {
    colnames(df) <- paste(nm, colnames(df), sep = ".")
  }
  df
})

result <- do.call(cbind, expanded)

# Write compact CSV output
write.csv(result, file = file.path(out_dir, "result.csv"), row.names = FALSE)

# Also write full result object as RDS for inspection
saveRDS(result, file = file.path(out_dir, "result.rds"))
```

## Current Prompt Execution Logs

**`stderr.txt`**

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

**`stdout.txt`**

```text

```

## Current Prompt Output Files

**`result.csv`**

```csv
"path.path","res_dose_slides.res_dose_slides","title.title"
"AVAL","AVAL","AVAL"
"AVISITN","AVISITN","AVISITN"
"USUBJID","USUBJID","USUBJID"

```

**`result.rds`**

```text
[binary artifact: result.rds, 178 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(tidyr)
  library(purrr)
})

# I/O ----------------------------------------------------------------------

in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

path_file  <- file.path(in_dir, "path.tsv")
dose_file  <- file.path(in_dir, "res_dose_slides.tsv")
title_file <- file.path(in_dir, "title.tsv")

path_df  <- read_tsv(path_file, show_col_types = FALSE)
dose_df  <- read_tsv(dose_file, show_col_types = FALSE)
title_df <- read_tsv(title_file, show_col_types = FALSE)

# Prepare simple joined structure (by common columns) ----------------------

common_cols <- Reduce(intersect, list(names(path_df), names(dose_df), names(title_df)))

joined <-
  path_df %>%
  full_join(dose_df,  by = common_cols) %>%
  full_join(title_df, by = common_cols)

# Create a minimal "HTML dose slide" content per row -----------------------

make_html <- function(row) {
  nm   <- names(row)
  vals <- as.list(row)
  body_tbl <- paste0(
    "<table border='1' cellpadding='4' cellspacing='0'>",
    paste0(
      mapply(function(n, v) {
        sprintf("<tr><th align='left'>%s</th><td>%s</td></tr>",
                htmltools::htmlEscape(as.character(n)),
                htmltools::htmlEscape(as.character(v)))
      }, nm, vals),
      collapse = ""
    ),
    "</table>"
  )
  paste0(
    "<!DOCTYPE html>",
    "<html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body>",
    body_tbl,
    "</body></html>"
  )
}

# Ensure htmltools is available for escaping --------------------------------
if (!requireNamespace("htmltools", quietly = TRUE)) {
  stop("Package 'htmltools' is required but not installed.")
}

html_vec <- joined %>%
  mutate(.row_id = row_number()) %>%
  split(.$.row_id) %>%
  map_chr(~ make_html(select(.x, - .row_id)))

# Write HTML files and summary CSV -----------------------------------------

html_files <- sprintf("dose_slide_%03d.html", seq_along(html_vec))
html_paths <- file.path(out_dir, html_files)

walk2(html_paths, html_vec, ~ writeLines(.y, .x, useBytes = TRUE))

result_df <- tibble(
  slide_id   = seq_along(html_vec),
  html_file  = html_files,
  html_path  = html_paths
)

write_csv(result_df, file.path(out_dir, "result.csv"))
```

## Simple Prompt Execution Logs

**`stderr.txt`**

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
Warning message:
Using `by = character()` to perform a cross join was deprecated in dplyr 1.1.0.
ℹ Please use `cross_join()` instead. 

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`dose_slide_001.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>AVAL</td></tr><tr><th align='left'>title</th><td>AVAL</td></tr></table></body></html>

```

**`dose_slide_002.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>AVAL</td></tr><tr><th align='left'>title</th><td>AVISITN</td></tr></table></body></html>

```

**`dose_slide_003.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>AVAL</td></tr><tr><th align='left'>title</th><td>USUBJID</td></tr></table></body></html>

```

**`dose_slide_004.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>AVISITN</td></tr><tr><th align='left'>title</th><td>AVAL</td></tr></table></body></html>

```

**`dose_slide_005.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>AVISITN</td></tr><tr><th align='left'>title</th><td>AVISITN</td></tr></table></body></html>

```

**`dose_slide_006.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>AVISITN</td></tr><tr><th align='left'>title</th><td>USUBJID</td></tr></table></body></html>

```

**`dose_slide_007.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>USUBJID</td></tr><tr><th align='left'>title</th><td>AVAL</td></tr></table></body></html>

```

**`dose_slide_008.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>USUBJID</td></tr><tr><th align='left'>title</th><td>AVISITN</td></tr></table></body></html>

```

**`dose_slide_009.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVAL</td></tr><tr><th align='left'>res_dose_slides</th><td>USUBJID</td></tr><tr><th align='left'>title</th><td>USUBJID</td></tr></table></body></html>

```

**`dose_slide_010.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVISITN</td></tr><tr><th align='left'>res_dose_slides</th><td>AVAL</td></tr><tr><th align='left'>title</th><td>AVAL</td></tr></table></body></html>

```

**`dose_slide_011.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVISITN</td></tr><tr><th align='left'>res_dose_slides</th><td>AVAL</td></tr><tr><th align='left'>title</th><td>AVISITN</td></tr></table></body></html>

```

**`dose_slide_012.html`**

```text
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Dose Slide</title></head><body><table border='1' cellpadding='4' cellspacing='0'><tr><th align='left'>path</th><td>AVISITN</td></tr><tr><th align='left'>res_dose_slides</th><td>AVAL</td></tr><tr><th align='left'>title</th><td>USUBJID</td></tr></table></body></html>

```

_Omitted 16 additional files._

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/create_html_dose_slides",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "returncode": 0,
  "comparison": {
    "result.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(3, 3)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    }
  },
  "normalizations": []
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/aNCA/create_html_dose_slides",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "returncode": 0,
  "comparison": {
    "result.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(27, 3)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    }
  },
  "normalizations": []
}
```
