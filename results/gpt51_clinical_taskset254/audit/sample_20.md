# Sample 20: pharmaverse/aNCA/create_html_dose_slides

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/create_html_dose_slides`
- package/function: `aNCA` / `create_html_dose_slides`
- expected_artifacts: `outputs/result.csv`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
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

## Current Prompt
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

## Simple Prompt
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

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(3, 3) | summary.csv: match=False reason=File not generated"
}
```

## Simple Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(27, 3) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
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
    stringsAsFactors = 
```

## Current Solution
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

## Simple Solution
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

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for create HTML dose slides. The available input files are `inputs/path.tsv`, `inputs/res_dose_slides.tsv`, `inputs/title.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for create HTML dose slides. The available input files are `inputs/path.tsv`, `inputs/res_dose_slides.tsv`, `inputs/title.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```