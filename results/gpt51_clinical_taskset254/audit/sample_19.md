# Sample 19: pharmaverse/aNCA/add_qmd_sl_plottabletable

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/add_qmd_sl_plottabletable`
- package/function: `aNCA` / `add_qmd_sl_plottabletable`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `TIMEOUT` tier=`exec_fail`

## Reference Prompt
```text
Write R code to implement the **Add qmd sl plottabletable** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/df1.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'df1.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plottabletable` (numeric vectors are often stored in a column named like the parameter).
- `inputs/df2.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'df2.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plottabletable` (numeric vectors are often stored in a column named like the parameter).
- `inputs/plot.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'plot.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plottabletable` (numeric vectors are often stored in a column named like the parameter).
- `inputs/quarto_path.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'quarto_path.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plottabletable` (numeric vectors are often stored in a column named like the parameter).
- `inputs/use_plotly.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'use_plotly.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plottabletable` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::add_qmd_sl_plottabletable` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown sl plottabletable. The available input files are `inputs/df1.tsv`, `inputs/df2.tsv`, `inputs/plot.tsv`, `inputs/quarto_path.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### df1.tsv (25 bytes)
df1
AVAL
AVISITN
USUBJID

### df2.tsv (25 bytes)
df2
AVAL
AVISITN
USUBJID

### plot.tsv (26 bytes)
plot
AVAL
AVISITN
USUBJID

### quarto_path.tsv (33 bytes)
quarto_path
AVAL
AVISITN
USUBJID

### use_plotly.tsv (32 bytes)
use_plotly
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform add Quarto markdown sl plottabletable using the aNCA clinical task contract.

Input: df1.tsv, df2.tsv, plot.tsv, quarto_path.tsv, use_plotly.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### df1.tsv (25 bytes)
df1
AVAL
AVISITN
USUBJID

### df2.tsv (25 bytes)
df2
AVAL
AVISITN
USUBJID

### plot.tsv (26 bytes)
plot
AVAL
AVISITN
USUBJID

### quarto_path.tsv (33 bytes)
quarto_path
AVAL
AVISITN
USUBJID

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
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "message": "Timeout after 120s",
  "returncode": "",
  "stderr": "",
  "comparison": ""
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
quarto_path_path <- file.path("inputs", "quarto_path.tsv")
if (!file.exists(quarto_path_path)) {
  stop("quarto_path.tsv is required input")
}
quarto_path_df <- read.delim(quarto_path_path, check.names = FALSE, stringsAsFactors = FALSE)
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
if (length(quarto_path) > 1) quarto_path <- quarto_path[1]
if (is.na(quarto_path) || quarto_path == "") quarto_path <- "temp_output.qmd"

df1_path <- file.path("inputs", "df1.tsv")
if (!file.exists(df1_path)) {
  stop("df1.tsv is required input")
}
df1_df <- read.delim(df1_path, check.names = FALSE, stringsAsFactors = FALSE)
df1_expr <- df1_df[[1]][1]
if (length(df1_expr) > 1) df1_expr <- df1_expr[1]

df2_path <- file.path("inputs", "df2.tsv")
if (!file.exists(df2_path)) {
  stop("df2.tsv is required input")
}
df2_df <- read.delim(df2_path, check.names = FALSE, stringsAsFactors = FALSE)
df2_expr <- df2_df[[1]][1]
if (length(df2_expr) > 1) df2_expr <- df2_expr[1]

plot_path <- file.path("inputs", "plot.tsv")
if (!file.exists(plot_path)) {
  stop("plot.tsv is required input")
}
plot_df <- read.delim(plot_path, check.names = FALSE, stringsAsFactors = FALSE)
plot_expr <- plot_df[[1]][1]
if (length(plot_expr) > 1) plot_expr <- plot_expr[1]

use_plotly_path <- file.path("inputs", "use_plotly.tsv")
if (!file.exists(use_plotly_path)) {
  stop("use_plotly.tsv is required input")
}
use_plotly_df <- read.delim(use_plotly_path, check.names = FALSE, stringsAsFactors = FALSE)
use_plotly <- as.logical(use_plotly_df$use_plotly)
if (length(use_plotly) > 1) use_plotly <- use_plotly[1]
if (is.na(use_plotly)) use_plotly <- FALSE

# 2. 数据验证 / Data validation
# quarto_path是文件路径字符串，plot_expr、df1_expr、df2_expr是表达式字符串，不需要数据框验证
# 确保quarto_path文件存在（如果不存在则创建空文件）
if (dirname(quarto_path) != "." && !dir.exists(dirname(quarto_path))) {
  dir.create(dirname(quarto_path), recursive = TRUE, showWarnings = FALSE)
}
if (!file.exists(quarto_path)) {
  file.create(quarto_path)
}

# 3. 执行函数实现 / Execute function implementation
# add_qmd_sl_plottabletable会写入文件并invisibly返回TRUE
result <- aNCA:::add_qmd_sl_plottabletable(
  quarto_path = quarto_path,
  df1 = df1_expr,
  df2 = df2_expr,
  plot = plot_expr,
  use_plotly = use_plotly
)
# 函数invisibly返回TRUE，我们需要显式获取返回值
if (is.null(result)) result <- TRUE

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
# 如果result是字符向量（多行），合并为单个字符串
if (is.character(result) && length(result) > 1) {
  result <- paste(result, collapse = "\n")
}
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    use_plotly = use_plotly,
   
```

## Current Solution
```r
#!/usr/bin/env Rscript

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper to read a TSV and drop all-NA columns
read_tsv_keep <- function(path) {
  x <- read.delim(path, header = TRUE, sep = "\t", check.names = FALSE, stringsAsFactors = FALSE)
  x
}

# Read inputs
df1         <- read_tsv_keep("inputs/df1.tsv")
df2         <- read_tsv_keep("inputs/df2.tsv")
plot_cfg    <- read_tsv_keep("inputs/plot.tsv")
quarto_path <- read_tsv_keep("inputs/quarto_path.tsv")
use_plotly  <- read_tsv_keep("inputs/use_plotly.tsv")

# Treat one-row tables as scalar arguments when appropriate
scalar_from_df <- function(x) {
  if (nrow(x) == 1L && ncol(x) == 1L) {
    return(x[[1]][1])
  }
  x
}

df1_scalar         <- scalar_from_df(df1)
df2_scalar         <- scalar_from_df(df2)
plot_cfg_scalar    <- scalar_from_df(plot_cfg)
quarto_path_scalar <- scalar_from_df(quarto_path)
use_plotly_scalar  <- scalar_from_df(use_plotly)

# Preserve row alignment across vector or table inputs:
# For this simple helper, bind all original tables with explicit source tagging.
add_src <- function(x, src) {
  if (is.data.frame(x)) {
    x$SOURCE <- src
    x
  } else {
    data.frame(VALUE = x, SOURCE = src, stringsAsFactors = FALSE)
  }
}

res_list <- list(
  add_src(df1, "df1"),
  add_src(df2, "df2"),
  add_src(plot_cfg, "plot"),
  add_src(quarto_path, "quarto_path"),
  add_src(use_plotly, "use_plotly")
)

# Compact, inspectable result table
result <- do.call(rbind, res_list)
row.names(result) <- NULL

# Write outputs
write.csv(result, file = "outputs/result.csv", row.names = FALSE)
saveRDS(result, file = "outputs/result.rds")
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Input paths
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

df1_path        <- file.path(in_dir, "df1.tsv")
df2_path        <- file.path(in_dir, "df2.tsv")
plot_path       <- file.path(in_dir, "plot.tsv")
quarto_path_in  <- file.path(in_dir, "quarto_path.tsv")
use_plotly_path <- file.path(in_dir, "use_plotly.tsv")

# Read TSVs (first column is a dummy header per preview)
read_single_col <- function(path, colname) {
  if (!file.exists(path)) return(NA_character_)
  x <- read_tsv(path, show_col_types = FALSE)
  if (!colname %in% names(x)) return(NA_character_)
  x[[colname]][1]
}

df1_name        <- read_single_col(df1_path, "df1")
df2_name        <- read_single_col(df2_path, "df2")
plot_name       <- read_single_col(plot_path, "plot")
quarto_path_val <- read_single_col(quarto_path_in, "quarto_path")
use_plotly_val  <- read_single_col(use_plotly_path, "use_plotly")

# Default / normalize values
if (is.na(df1_name))        df1_name        <- "df1"
if (is.na(df2_name))        df2_name        <- "df2"
if (is.na(plot_name))       plot_name       <- "plot"
if (is.na(quarto_path_val)) quarto_path_val <- "report.qmd"
if (is.na(use_plotly_val))  use_plotly_val  <- "FALSE"

use_plotly_flag <- tolower(use_plotly_val) %in% c("true", "t", "1", "yes", "y")

# Build Quarto YAML and body
yaml_lines <- c(
  "---",
  "title: \"aNCA Clinical Task Contract Report\"",
  "format:",
  "  html:",
  paste0("    df-print: ", if (use_plotly_flag) "paged" else "kable"),
  "---",
  ""
)

# Chunk for libraries and data
setup_chunk <- c(
  "```{r setup, include=FALSE}",
  "library(dplyr)",
  "library(ggplot2)",
  if (use_plotly_flag) "library(plotly)" else NULL,
  "",
  "# Placeholder data frames (replace with real data loading as needed)",
  paste0(df1_name, " <- data.frame(USUBJID = character(), AVISITN = numeric(), AVAL = numeric())"),
  paste0(df2_name, " <- data.frame(USUBJID = character(), AVISITN = numeric(), AVAL = numeric())"),
  paste0(plot_name, " <- data.frame(USUBJID = character(), AVISITN = numeric(), AVAL = numeric())"),
  "```",
  ""
)

# Plottable table chunk
table_chunk <- c(
  "## Plottable Table",
  "",
  "```{r plottable-table}",
  paste0("tbl <- ", df1_name, " %>%",
         " dplyr::inner_join(", df2_name, ", by = c(\"USUBJID\", \"AVISITN\", \"AVAL\"))"),
  "tbl",
  "```",
  ""
)

# Plot chunk
plot_chunk <- c(
  "## Plot",
  "",
  if (use_plotly_flag) {
    c(
      "```{r interactive-plot}",
      paste0("p <- ggplot(", plot_name, ", aes(x = AVISITN, y = AVAL, group = USUBJID, color = USUBJID)) +"),
      "  geom_line() +",
      "  geom_point() +",
      "  theme_minimal()",
      "plotly::ggplotly(p)",
      "```",
      ""
    )
  } else {
    c(
      "```{r static-plot}",
      paste0("ggplot(", plot_name, ", aes(x = AVISITN, y = AVAL, group = USUBJID, color = USUBJID)) +"),
      "  geom_line() +",
      "  geom_point() +",
      "  theme_minimal()",
      "```",
      ""
    )
  }
)

# Write Quarto file
quarto_out_path <- file.path(out_dir, basename(quarto_path_val))
writeLines(c(yaml_lines, setup_chunk, table_chunk, plot_chunk), quarto_out_path)

# Prepare result.csv summary
result_df <- tibble::tibble(
  key   = c("df1_name", "df2_name", "plot_name", "quarto_path", "use_plotly", "quarto_generated"),
  value = c(df1_name,
            df2_name,
            plot_name,
            quarto_out_path,
            as.character(use_plotly_flag),
            if (file.exists(quarto_out_path)) "TRUE" else "FALSE")
)

write_csv(result_df, file.path(out_dir, "result.csv"))
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown sl plottabletable. The available input files are `inputs/df1.tsv`, `inputs/df2.tsv`, `inputs/plot.tsv`, `inputs/quarto_path.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown sl plottabletable. The available input files are `inputs/df1.tsv`, `inputs/df2.tsv`, `inputs/plot.tsv`, `inputs/quarto_path.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```