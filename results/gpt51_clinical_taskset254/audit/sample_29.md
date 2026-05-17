# Sample 29: pharmaverse/aNCA/add_qmd_sl_plot

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/add_qmd_sl_plot`
- package/function: `aNCA` / `add_qmd_sl_plot`
- expected_artifacts: `outputs/result.csv`
- current_status: `TIMEOUT` tier=`exec_fail`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to implement the **Add qmd sl plot** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/plot.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'plot.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plot` (numeric vectors are often stored in a column named like the parameter).
- `inputs/quarto_path.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'quarto_path.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plot` (numeric vectors are often stored in a column named like the parameter).
- `inputs/use_plotly.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'use_plotly.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::add_qmd_sl_plot` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::add_qmd_sl_plot` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown sl plot. The available input files are `inputs/plot.tsv`, `inputs/quarto_path.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

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
Create R script to perform add Quarto markdown sl plot using the aNCA clinical task contract.

Input: plot.tsv, quarto_path.tsv, use_plotly.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

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
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "message": "Timeout after 120s",
  "returncode": "",
  "stderr": "",
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(3, 5) | summary.csv: match=False reason=File not generated"
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
# quarto_path是文件路径字符串，plot_expr是表达式字符串，不需要数据框验证
# 确保quarto_path文件存在（如果不存在则创建空文件）
if (dirname(quarto_path) != "." && !dir.exists(dirname(quarto_path))) {
  dir.create(dirname(quarto_path), recursive = TRUE, showWarnings = FALSE)
}
if (!file.exists(quarto_path)) {
  file.create(quarto_path)
}

# 3. 执行函数实现 / Execute function implementation
# add_qmd_sl_plot会写入文件并invisibly返回TRUE
result <- aNCA:::add_qmd_sl_plot(
  quarto_path = quarto_path,
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

```

## Current Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tidyr)
  library(purrr)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper to read TSV with header, preserve types
read_tsv_generic <- function(path) {
  readr::read_tsv(
    file = path,
    col_types = cols(.default = col_character())
  )
}

# Read inputs
plot_df        <- read_tsv_generic("inputs/plot.tsv")
quarto_df      <- read_tsv_generic("inputs/quarto_path.tsv")
use_plotly_df  <- read_tsv_generic("inputs/use_plotly.tsv")

# Treat one-row tables as scalars when appropriate:
# Here each TSV is a single-column vector of column names; keep row alignment.
# We'll create a compact mapping table of the parameters.

result <- tibble(
  param_name  = c("plot", "quarto_path", "use_plotly")
) %>%
  mutate(
    column     = list(plot_df$plot) %>%
      append(list(quarto_df$quarto_path)) %>%
      append(list(use_plotly_df$use_plotly))
  ) %>%
  unnest_longer(col = column, values_to = "column_name", indices_to = "row_id") %>%
  select(param_name, row_id, column_name)

# Write compact CSV
write_csv(result, "outputs/result.csv")

# Also write full result as RDS artifact
saveRDS(result, file = "outputs/result.rds")
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Directories
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

# Read inputs
plot_df       <- read_tsv(file.path(in_dir, "plot.tsv"), col_types = cols(.default = "c"))
quarto_df     <- read_tsv(file.path(in_dir, "quarto_path.tsv"), col_types = cols(.default = "c"))
use_plotly_df <- read_tsv(file.path(in_dir, "use_plotly.tsv"), col_types = cols(.default = "c"))

# Harmonize column name for joining
colnames(plot_df)       <- "key"
colnames(quarto_df)     <- "key"
colnames(use_plotly_df) <- "key"

# Combine to create a clinical task contract for an SL plot Quarto markdown
result <- plot_df %>%
  full_join(quarto_df,  by = "key") %>%
  full_join(use_plotly_df, by = "key") %>%
  distinct() %>%
  arrange(key) %>%
  mutate(
    field_type = case_when(
      key %in% c("AVAL")   ~ "numeric",
      key %in% c("AVISITN") ~ "integer",
      key %in% c("USUBJID") ~ "string",
      TRUE ~ "string"
    ),
    role = case_when(
      key == "AVAL"    ~ "y",
      key == "AVISITN" ~ "x",
      key == "USUBJID" ~ "id",
      TRUE ~ "meta"
    ),
    use_plotly = if_else(key %in% use_plotly_df$key, TRUE, FALSE),
    quarto_path = if_else(key %in% quarto_df$key, "sl_plot.qmd", NA_character_)
  )

# Write output
write_csv(result, file.path(out_dir, "result.csv"))
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown sl plot. The available input files are `inputs/plot.tsv`, `inputs/quarto_path.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add Quarto markdown sl plot. The available input files are `inputs/plot.tsv`, `inputs/quarto_path.tsv`, `inputs/use_plotly.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```