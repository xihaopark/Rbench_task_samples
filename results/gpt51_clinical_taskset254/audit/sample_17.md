# Sample 17: pharmaverse/aNCA/error_plot

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/error_plot`
- package/function: `aNCA` / `error_plot`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to implement the **Error plot** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/msg.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'msg.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::error_plot` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::error_plot` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for error plot. The available input files are `inputs/msg.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### msg.tsv (25 bytes)
msg
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform error plot using the aNCA clinical task contract.

Input: msg.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### msg.tsv (25 bytes)
msg
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 3) vs llm=(9, 4) | summary.csv: match=False reason=File not generated"
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 3) vs llm=(4, 7) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
msg_path <- file.path("inputs", "msg.tsv")
if (!file.exists(msg_path)) {
  stop("msg.tsv is required input")
}
msg_df <- read.delim(msg_path, check.names = FALSE, stringsAsFactors = FALSE)
msg <- msg_df$msg

# 3. 执行函数实现 / Execute function implementation
msg_path <- file.path("inputs", "msg.tsv")
if (!file.exists(msg_path)) {
  stop("msg.tsv is required input")
}
msg_df <- read.delim(msg_path, check.names = FALSE, stringsAsFactors = FALSE)
msg <- if(ncol(msg_df) > 0 && nrow(msg_df) > 0) if(ncol(msg_df) >= 1 && nrow(msg_df) > 0) msg_df[[1]] else NULL else msg_df
result <- aNCA:::error_plot(msg)

# 4. 创建结果数据框 / Create result dataframe
# result是ggplot对象
if (inherits(result, "ggplot")) {
  result_df <- data.frame(
    operation = "error_plot",
    success = TRUE,
    result_type = "ggplot",
    stringsAsFactors = FALSE)
} else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(
    operation = "error_plot",
    result_type = class(result)[1],
    stringsAsFactors = FALSE)
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

## Current Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read message / request description
msg_path <- file.path("inputs", "msg.tsv")
msg <- fread(msg_path, sep = "\t", header = TRUE, data.table = FALSE)

# aNCA-style: treat this as a request to compute PK error-plot support
# With only variable names provided, return a compact, inspectable template
# describing expected structure for an error-plot benchmark.

# Define required columns for an aNCA error-plot support table
required_cols <- c(
  "USUBJID",   # subject identifier
  "AVISITN",   # visit or nominal time index
  "AVAL",      # analysis value
  "PRED",      # model-predicted value
  "RES",       # residual = AVAL - PRED
  "PRES",      # percent residual = 100 * (AVAL - PRED)/PRED
  "TIME",      # nominal or actual time
  "DV",        # dependent variable (e.g., conc)
  "CMT"        # compartment (for compatibility)
)

# Build a metadata-style description frame, compact and human-inspectable
result <- data.frame(
  COLNAME = required_cols,
  ROLE = c(
    "ID",
    "VISIT_INDEX",
    "OBSERVED",
    "PREDICTED",
    "RESIDUAL",
    "PERCENT_RESIDUAL",
    "TIME",
    "DV",
    "COMPARTMENT"
  ),
  TYPE = c(
    "character",
    "numeric",
    "numeric",
    "numeric",
    "numeric",
    "numeric",
    "numeric",
    "numeric",
    "integer"
  ),
  REQUIRED = c(
    TRUE, TRUE, TRUE,
    TRUE, FALSE, FALSE,
    FALSE, FALSE, FALSE
  ),
  stringsAsFactors = FALSE
)

# Attach original msg (scalar request) as attribute to preserve intent
attr(result, "msg") <- msg

# Write compact CSV output
fwrite(result, file.path("outputs", "result.csv"), quote = TRUE)

# Write full R object as RDS
saveRDS(result, file.path("outputs", "result.rds"))
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(ggplot2)
})

# Paths
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read msg.tsv
msg_path <- file.path(in_dir, "msg.tsv")
msg <- readr::read_tsv(msg_path, show_col_types = FALSE)

# Simulate example aNCA-like data according to the contract
set.seed(1)
n_subj   <- 50
n_visit  <- 4
subjects <- sprintf("SUBJ%03d", seq_len(n_subj))
visits   <- seq_len(n_visit)

dat <- expand.grid(
  USUBJID = subjects,
  AVISITN = visits,
  KEEP.OUT.ATTRS = FALSE,
  stringsAsFactors = FALSE
) |>
  as_tibble() |>
  mutate(
    AVAL = rnorm(n(), mean = AVISITN * 10, sd = 5)
  )

# Error plot: mean +/- SD by visit
sumdat <- dat |>
  group_by(AVISITN) |>
  summarise(
    n    = n(),
    mean = mean(AVAL),
    sd   = sd(AVAL),
    se   = sd / sqrt(n),
    .groups = "drop"
  ) |>
  mutate(
    ymin_sd = mean - sd,
    ymax_sd = mean + sd
  )

p <- ggplot(sumdat, aes(x = AVISITN, y = mean)) +
  geom_line(color = "steelblue") +
  geom_point(color = "steelblue") +
  geom_errorbar(aes(ymin = ymin_sd, ymax = ymax_sd), width = 0.1) +
  labs(
    x = "Visit Number (AVISITN)",
    y = "Mean AVAL (± SD)",
    title = "Error Plot of AVAL by Visit"
  ) +
  theme_minimal()

# Save plot (optional visualization artifact)
ggsave(file.path(out_dir, "error_plot.png"), p, width = 6, height = 4, dpi = 300)

# Outputs
# result.csv: summary statistics used for error plot
result_csv_path <- file.path(out_dir, "result.csv")
write_csv(sumdat, result_csv_path)

# result.rds: list containing raw data and ggplot object
result_rds <- list(
  data_raw   = dat,
  data_summary = sumdat,
  plot       = p,
  msg        = msg
)
saveRDS(result_rds, file.path(out_dir, "result.rds"))
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for error plot. The available input files are `inputs/msg.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for error plot. The available input files are `inputs/msg.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```