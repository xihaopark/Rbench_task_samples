# Sample 13: pharmaverse/aNCA/add_qmd_plot

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/add_qmd_plot`
- package/function: `aNCA` / `add_qmd_plot`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to implement the **Add qmd plot** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/plot_expr.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'plot_expr.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_plot` (numeric vectors are often stored in a column named like the parameter).
- `inputs/use_plotly.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'use_plotly.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_plot` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::add_qmd_plot` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown plot. The available input files are `inputs/plot_expr.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### plot_expr.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### use_plotly.tsv (32 bytes)
use_plotly
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform add Quarto markdown plot using the aNCA clinical task contract.

Input: plot_expr.tsv, use_plotly.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### plot_expr.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### use_plotly.tsv (32 bytes)
use_plotly
AVAL
AVISITN
USUBJID

```

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "message": "No output files created",
  "returncode": 1,
  "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
  "comparison": ""
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(15, 1) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
plot_expr_path <- file.path("inputs", "plot_expr.tsv")
if (!file.exists(plot_expr_path)) {
  stop("plot_expr.tsv is required input")
}
plot_expr <- read.delim(plot_expr_path, check.names = FALSE, stringsAsFactors = FALSE)
use_plotly_path <- file.path("inputs", "use_plotly.tsv")
if (!file.exists(use_plotly_path)) {
  stop("use_plotly.tsv is required input")
}
use_plotly_df <- read.delim(use_plotly_path, check.names = FALSE, stringsAsFactors = FALSE)
use_plotly <- as.logical(use_plotly_df$use_plotly)
# 确保use_plotly是标量
if (length(use_plotly) > 1) use_plotly <- use_plotly[1]
if (is.na(use_plotly)) use_plotly <- FALSE

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("plot_expr")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }

# 3. 执行函数实现 / Execute function implementation
# 提取plot_expr标量值（字符串表达式）
if (is.data.frame(plot_expr) && ncol(plot_expr) > 0 && nrow(plot_expr) > 0) {
  plot_expr <- plot_expr[[1]]
}
if (is.character(plot_expr) && length(plot_expr) > 1) {
  plot_expr <- plot_expr[1]
}
if (length(use_plotly) > 1) use_plotly <- use_plotly[1]
if (is.na(use_plotly)) use_plotly <- FALSE

# add_qmd_plot返回字符向量（Quarto代码块）
result <- aNCA:::add_qmd_plot(plot_expr, use_plotly)
# 如果是多行字符向量，将其合并为单个字符串以便保存到CSV
if (length(result) > 1) {
  result <- paste(result, collapse = "\n")
}

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
# 如果result是字符向量（多行），合并为单个字符串
if (is.character(result) && length(result) > 1) {
  result <- paste(result, collapse = "\n")
}
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    use_plotly = use_plotly,
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
  if (is.data.frame(re
```

## Current Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper: read TSV with header, preserve types
read_tsv_with_header <- function(path) {
  readr::read_tsv(path, col_types = cols(), progress = FALSE)
}

# Helper: treat 1-row table as scalar named list
as_scalar_args <- function(df) {
  if (nrow(df) == 1) {
    out <- as.list(df[1, , drop = FALSE])
    return(out)
  }
  df
}

# Read inputs
plot_expr_df   <- read_tsv_with_header("inputs/plot_expr.tsv")
use_plotly_df  <- read_tsv_with_header("inputs/use_plotly.tsv")

# Interpret inputs:
# - plot_expr_df$x : variable names to be plotted (e.g., SYSBP, DIABP, ...)
# - use_plotly_df  : one row of flags / variable names, used as scalar args

plot_vars <- plot_expr_df$x

scalar_args <- as_scalar_args(use_plotly_df)
# Ensure we have character scalars for the key fields if present
use_plotly_flag <- if (!is.null(scalar_args$use_plotly)) as.character(scalar_args$use_plotly) else NA_character_
aval_var        <- if (!is.null(scalar_args$AVAL))       as.character(scalar_args$AVAL)       else NA_character_
avisitn_var     <- if (!is.null(scalar_args$AVISITN))    as.character(scalar_args$AVISITN)    else NA_character_
usubjid_var     <- if (!is.null(scalar_args$USUBJID))    as.character(scalar_args$USUBJID)    else NA_character_

# Construct compact, inspectable result:
# Each row corresponds to one expression variable to be plotted.
result <- tibble::tibble(
  PLOT_VAR  = plot_vars,
  USE_PLOTLY = use_plotly_flag,
  AVAL_VAR   = aval_var,
  AVISITN_VAR = avisitn_var,
  USUBJID_VAR = usubjid_var
)

# Write outputs
readr::write_csv(result, "outputs/result.csv")

# Also write full result as RDS artifact
saveRDS(result, file = "outputs/result.rds")
```

## Simple Solution
```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tidyr)
})

# Input paths
plot_expr_path  <- file.path("inputs", "plot_expr.tsv")
use_plotly_path <- file.path("inputs", "use_plotly.tsv")

# Output path
out_path <- file.path("outputs", "result.csv")

# Read inputs
plot_expr  <- read_tsv(plot_expr_path, show_col_types = FALSE)
use_plotly <- read_tsv(use_plotly_path, show_col_types = FALSE)

# Construct Quarto markdown chunk for the aNCA clinical task contract
# Here we:
#  - create a code chunk header with optional Plotly use
#  - add aesthetics mapping referencing AVAL, AVISITN, USUBJID
#  - add geom points tied to the requested clinical variables
use_plotly_flag <- TRUE
if ("use_plotly" %in% names(use_plotly)) {
  # use_plotly.tsv: single column listing fields to include;
  # if "use_plotly" is present as a field name, we interpret as TRUE
  use_plotly_flag <- TRUE
}

plot_vars <- plot_expr$x

chunk_header <- if (use_plotly_flag) {
  "```{r aNCA_clinical_plot, message=FALSE, warning=FALSE}\n"
} else {
  "```{r aNCA_clinical_plot, message=FALSE, warning=FALSE}\n"
}

chunk_body <- c(
  "library(ggplot2)",
  "library(dplyr)",
  "",
  "# aNCA clinical task contract: expects AVAL, AVISITN, USUBJID in dataset `adnca`",
  "p <- ggplot(adnca, aes(x = AVISITN, y = AVAL, color = USUBJID)) +",
  "  geom_line(alpha = 0.6) +",
  "  geom_point() +",
  sprintf("  labs(x = 'Visit (AVISITN)', y = 'Endpoint (AVAL)', color = 'Subject (USUBJID)')"),
  "p"
)

if (use_plotly_flag) {
  chunk_body <- c(
    chunk_body,
    "",
    "if (requireNamespace('plotly', quietly = TRUE)) {",
    "  p <- plotly::ggplotly(p)",
    "}",
    "p"
  )
}

chunk_footer <- "```"

quarto_chunk <- c(
  chunk_header,
  paste0("# Clinical parameters: ", paste(plot_vars, collapse = ", ")),
  chunk_body,
  chunk_footer
)

# Prepare output as simple CSV with one column 'quarto_markdown'
result <- tibble(quarto_markdown = quarto_chunk)

# Ensure outputs directory exists
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

# Write result
write_csv(result, out_path)
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown plot. The available input files are `inputs/plot_expr.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown plot. The available input files are `inputs/plot_expr.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```