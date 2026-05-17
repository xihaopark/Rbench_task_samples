# Sample 38: pharmaverse/aNCA/g_pkcg02_lin

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/g_pkcg02_lin`
- package/function: `aNCA` / `g_pkcg02_lin`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to produce the **linear-scale** PK plot **`g_pkcg02_lin`** using aNCA. Load `library(aNCA)` and `library(ggplot2)`.

**Inputs:** `inputs/data.tsv` — main analysis table as a `data.frame`.

**Computation:** Call **`aNCA:::g_pkcg02_lin(data)`** (internal). Save ggplot to `outputs/result.rds` and CSV summary as required.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full ggplot object to the RDS file and a sensible tabular summary to the CSV.

```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg02 lin. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. The target operation is the public aNCA routine `g_pkcg02_lin`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### data.tsv (5933 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	89.55	0	Baseline	2020-01-15	Y	91.77	-2.22	-2.4222	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	89.92	4	Week 4	2020-02-15	Y	91.77	-1.85	-2.019	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	89.93	12	Week 12	2020-04-15	Y	91.77	-1.84	-2.0081	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	86.99	0	Baseline	2020-01-15	Y	86.41	0.58	0.6738	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	87.06	4	Week 4	2020-02-15	Y	86.41	0.65	0.7548	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	86.84	12	Week 12	2020-04-15	Y	86.41	0.43	0.5002	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	62.22	0	Baseline	2020-01-15	Y	63.0	-0.78	-1.2371	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	63.44	4	Week 4	2020-02-15	Y	63.0	0.44	0.6994	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	62.39	12	Week 12	2020-04-15	Y	63.0	-0.61	-0.9673	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.9	0	Baseline	2020-01-15	Y	93.14	3.76	4.0347	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	92.23	4	Week 4	2020-02-15	Y	93.14	-0.91	-0.9791	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	90.4	12	Week 12	2020-04-15	Y	93.14	-2.74	-2.9439	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	67.62	0	Baseline	2020-01-15	Y	69.26	-1.64	-2.3733	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	66.0	4	Week 4	2020-02-15	Y	69.26	-3.26	-4.7122	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	69.58	12	Week 12	2020-04-15	Y	69.26	0.32	0.4564	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	87.46	0	Baseline	2020-01-15	Y	90.67	-3.21	-3.5444	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	90.17	4	Week 4	2020-02-15	Y	90.67	-0.5	-0.5557	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	91.02	12	Week 12	2020-04-15	Y	90.67	0.35	0.3818	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.91	0	Baseline	2020-01-15	Y	124.87	-0.96	-0.7719	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.77	4	Week 4	2020-02-15	Y	124.87	2.9	2.3193	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.58	12	Week 12	2020-04-15	Y	124.87	-1.29	-1.0361	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	60.28	0	Baseline	2020-01-15	Y	61.42	-1.14	-1.8575	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	62.29	4	Week 4	2020-02-15	Y	61.42	0.87	1.415	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	61.67	12	Week 12	2020-04-15	Y	61.42	0.25	0.4056	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	91.88	0	Baseline	2020-01-15	Y	93.59	-1.71	-1.8304	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	92.69	4	Week 4	2020-02-15	Y	93.59	-0.9	-0.965	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	92.26	12	Week 12	2020-04-15	Y	93.59	-1.33	-1.4244	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.12	0	Baseline	2020-01-15	Y	110.12	-0.0	-0.0011	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.08	4	Week 4	2020-02-15	Y	110.12	-0.04	-0.0375	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	107.26	12	Week 12	2020-04-15	Y	110.12	-2.86	-2.5983	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	67.4	0	Baseline	2020-01-15	Y	66.45	0.95	1.4245	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	66.85	4	Week 4	2020-02-15	Y	66.45	0.4	0.5968	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	69.82	12	Week 12	2020-04-15	Y	66.45	3.37	5.0661	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	79.73	0	Baseline	2020-01-15	Y	83.0	-3.27	-3.9425	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	84.77	4	Week 4	2020-02-15	Y	83.0	1.77	2.1296	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	82.26	12	Week 12	2020-04-15	Y	83.0	-0.74	-0.8944	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.3	0	Baseline	2020-01-15	Y	105.09	0.21	0.1993	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.18	4	Week 4	2020-02-15	Y	105.09	5.09	4.8429	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.75	12	Week 12	2020-04-15	Y	105.09	0.66	0.6275	
... [15 more lines omitted]

```

## Simple Prompt
```text
Create R script to perform g pkcg02 lin using the aNCA clinical task contract.

Input: data.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### data.tsv (5933 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	89.55	0	Baseline	2020-01-15	Y	91.77	-2.22	-2.4222	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	89.92	4	Week 4	2020-02-15	Y	91.77	-1.85	-2.019	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	89.93	12	Week 12	2020-04-15	Y	91.77	-1.84	-2.0081	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	86.99	0	Baseline	2020-01-15	Y	86.41	0.58	0.6738	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	87.06	4	Week 4	2020-02-15	Y	86.41	0.65	0.7548	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	86.84	12	Week 12	2020-04-15	Y	86.41	0.43	0.5002	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	62.22	0	Baseline	2020-01-15	Y	63.0	-0.78	-1.2371	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	63.44	4	Week 4	2020-02-15	Y	63.0	0.44	0.6994	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	62.39	12	Week 12	2020-04-15	Y	63.0	-0.61	-0.9673	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.9	0	Baseline	2020-01-15	Y	93.14	3.76	4.0347	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	92.23	4	Week 4	2020-02-15	Y	93.14	-0.91	-0.9791	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	90.4	12	Week 12	2020-04-15	Y	93.14	-2.74	-2.9439	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	67.62	0	Baseline	2020-01-15	Y	69.26	-1.64	-2.3733	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	66.0	4	Week 4	2020-02-15	Y	69.26	-3.26	-4.7122	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	69.58	12	Week 12	2020-04-15	Y	69.26	0.32	0.4564	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	87.46	0	Baseline	2020-01-15	Y	90.67	-3.21	-3.5444	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	90.17	4	Week 4	2020-02-15	Y	90.67	-0.5	-0.5557	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	91.02	12	Week 12	2020-04-15	Y	90.67	0.35	0.3818	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.91	0	Baseline	2020-01-15	Y	124.87	-0.96	-0.7719	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.77	4	Week 4	2020-02-15	Y	124.87	2.9	2.3193	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.58	12	Week 12	2020-04-15	Y	124.87	-1.29	-1.0361	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	60.28	0	Baseline	2020-01-15	Y	61.42	-1.14	-1.8575	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	62.29	4	Week 4	2020-02-15	Y	61.42	0.87	1.415	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	61.67	12	Week 12	2020-04-15	Y	61.42	0.25	0.4056	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	91.88	0	Baseline	2020-01-15	Y	93.59	-1.71	-1.8304	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	92.69	4	Week 4	2020-02-15	Y	93.59	-0.9	-0.965	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	92.26	12	Week 12	2020-04-15	Y	93.59	-1.33	-1.4244	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.12	0	Baseline	2020-01-15	Y	110.12	-0.0	-0.0011	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.08	4	Week 4	2020-02-15	Y	110.12	-0.04	-0.0375	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	107.26	12	Week 12	2020-04-15	Y	110.12	-2.86	-2.5983	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	67.4	0	Baseline	2020-01-15	Y	66.45	0.95	1.4245	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	66.85	4	Week 4	2020-02-15	Y	66.45	0.4	0.5968	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	69.82	12	Week 12	2020-04-15	Y	66.45	3.37	5.0661	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	79.73	0	Baseline	2020-01-15	Y	83.0	-3.27	-3.9425	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	84.77	4	Week 4	2020-02-15	Y	83.0	1.77	2.1296	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	82.26	12	Week 12	2020-04-15	Y	83.0	-0.74	-0.8944	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.3	0	Baseline	2020-01-15	Y	105.09	0.21	0.1993	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.18	4	Week 4	2020-02-15	Y	105.09	5.09	4.8429	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.75	12	Week 12	2020-04-15	Y	105.09	0.66	0.6275	
... [15 more lines omitted]

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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(1, 3) | summary.csv: match=False reason=File not generated | result.rds: match=False reason=Unexpected: "
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(3, 10) | summary.csv: match=False reason=File not generated | result.rds: match=False reason=Unexpected: "
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
data_path <- file.path("inputs", "data.tsv")
if (!file.exists(data_path)) {
  stop("data.tsv is required input")
}
data <- read.delim(data_path, check.names = FALSE, stringsAsFactors = FALSE)

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
# 确保data是data.frame
if (!is.data.frame(data)) {
  data <- as.data.frame(data)
}

result <- tryCatch({
  aNCA:::g_pkcg02_lin(data)
}, error = function(e) {
  # 如果函数调用失败，返回一个默认的ggplot对象
  suppressPackageStartupMessages(library(ggplot2))
  ggplot2::ggplot(data.frame(x = 1:10, y = 1:10), ggplot2::aes(x = x, y = y)) + ggplot2::geom_point()
})

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (inherits(result, "ggplot")) {
  # 对于ggplot对象，不创建data.frame，直接保存为RDS
  result_df <- NULL
} else if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    id = seq_along(result),
    result = result,
    stringsAsFactors = FALSE)
} else if (is.data.frame(result)) {
  result_df <- result
} else {
  # 尝试创建data.frame，如果失败则跳过
  result_df <- tryCatch({
    data.frame(result = result, stringsAsFactors = FALSE)
  }, error = function(e) NULL)
}

# 5. 生成汇总统计 / Generate summary statistics
if (!is.null(result_df) && is.data.frame(result_df)) {
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
if (exists("result_df") && !is.null(result_df) && is.data.frame(result_df)) {
  write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
} else if (exists("result")) {
  if (inherits(result, "ggplot")) {
    # 对于ggplot对象，保存为RDS
    saveRDS(result, file.path(outputs_dir, "result.rds"))
    # 也创建一个CSV报告
    result_df <- data.frame(
      plot_type = "ggplot",
      success = TRUE,
      stringsAsFactors = FALSE
    )
    write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (is.data.frame(result)) {
    write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (is.list(result)) {
    saveRDS(result, file.path(outputs_dir, "result.rds"
```

## Current Solution
```r
#!/usr/bin/env Rscript

## aNCA clinical PK support task for g_pkcg02_lin

suppressPackageStartupMessages({
  ## add any required libraries here; keep dependencies minimal
})

## helper: read TSV with header
read_tsv_keep <- function(path) {
  read.delim(path, header = TRUE, sep = "\t", check.names = FALSE,
             stringsAsFactors = FALSE)
}

## Input
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

data_path <- file.path(in_dir, "data.tsv")
if (!file.exists(data_path)) {
  stop("Input file not found: ", data_path)
}

dat <- read_tsv_keep(data_path)

## ---- Prepare arguments for g_pkcg02_lin --------------------------------
## NOTE:
##  - This script assumes g_pkcg02_lin is available on the search path
##    (e.g., from an attached aNCA package or sourced file).
##  - data.tsv appears to be in ADaM-ish format; without a formal
##    interface specification for g_pkcg02_lin, we pass the table as a
##    single argument when possible.

## Try to discover g_pkcg02_lin interface
if (!exists("g_pkcg02_lin", mode = "function")) {
  stop("Function g_pkcg02_lin not found in current R environment.")
}

gfun <- get("g_pkcg02_lin", mode = "function")
form <- formals(gfun)

## Strategy:
##  - If the function has a single formal argument (apart from ...),
##    pass the full data.frame as that argument.
##  - If it has a formal called 'data' or 'dat', pass as that.
##  - Otherwise, attempt to match column names to formal argument names.
##  - Scalars: if a formal is not a column and has length 1 default,
##    use the default (do not override).
##  - Preserve vector alignment by passing full columns as-is.

arg_names <- setdiff(names(form), "...")
call_args <- list()

if (length(arg_names) == 1L) {
  ## Single-argument interface; assume it wants the full dataset
  call_args[[arg_names]] <- dat
} else if ("data" %in% arg_names) {
  call_args[["data"]] <- dat
} else if ("dat" %in% arg_names) {
  call_args[["dat"]] <- dat
} else {
  ## Attempt mapping by name: if a formal name equals a column, pass it
  for (an in arg_names) {
    if (an %in% names(dat)) {
      call_args[[an]] <- dat[[an]]
    } else {
      ## leave as default scalar / missing; do not guess
      next
    }
  }
}

## ---- Call g_pkcg02_lin -------------------------------------------------
res <- do.call(gfun, call_args)

## ---- Normalize result for grading --------------------------------------
## Accept common output types and coerce to a compact data.frame for CSV.
## Always store the full object to RDS.

norm_df <- NULL

if (is.data.frame(res)) {
  norm_df <- res
} else if (is.matrix(res)) {
  norm_df <- as.data.frame(res, stringsAsFactors = FALSE)
} else if (is.vector(res) || is.factor(res)) {
  norm_df <- data.frame(value = as.vector(res), stringsAsFactors = FALSE)
} else if (is.list(res)) {
  ## If list elements have equal lengths >1, bind as columns; otherwise,
  ## create a key-value expansion to keep CSV inspectable.
  lens <- vapply(res, length, integer(1))
  if (length(res) > 0 && length(unique(lens[lens > 0])) == 1L && unique(lens[lens > 0]) > 1L) {
    norm_df <- as.data.frame(res, stringsAsFactors = FALSE, check.names = FALSE)
  } else {
    norm_df <- data.frame(
      name  = rep(names(res), pmax(lens, 1L)),
      index = unlist(lapply(lens, function(z) if (z == 0) 1L else seq_len(z))),
      value = unlist(lapply(res, function(x) if (length(x) == 0) NA else x)),
      stringsAsFactors = FALSE
    )
  }
} else {
  ## Fallback: wrap as scalar
  norm_df <- data.frame(value = I(list(res)))
}

## Keep CSV compact and inspectable:
##  - avoid extremely wide outputs by truncating to a reasonable
##    number of columns if necessary, but do not alter row alignment.
max_cols <- 50L
if (ncol(norm_df) > max_cols) {
  keep_cols <- seq_len(max_cols)
  extra     <- ncol(norm_df) - max_cols
  norm_df   <- norm_df[, keep_cols, drop = FALSE]
  attr(norm_df, "note") <- paste0("Output had ", ncol(res), 
                                  " columns; truncated to first ", max_cols,
                                  " for CSV. Full object is in result.rds.")
}

## ---- Write outputs ------------------------------------------------------
csv_path <- file.path(out_dir, "result.csv")
rds_path <- file.path(out_dir, "result.rds")

write.csv(norm_df, file = csv_path, row.names = FALSE, na = "")

saveRDS(res, file = rds_path)
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

#----------------------------------------------------------------------
# Paths
#----------------------------------------------------------------------
infile  <- file.path("inputs", "data.tsv")
out_csv <- file.path("outputs", "result.csv")
out_rds <- file.path("outputs", "result.rds")

if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#----------------------------------------------------------------------
# Read input
#----------------------------------------------------------------------
dat <- read_tsv(
  infile,
  col_types = cols(
    USUBJID = col_character(),
    STUDYID = col_character(),
    PARAMCD = col_character(),
    PARAM   = col_character(),
    AVAL    = col_double(),
    AVISITN = col_double(),
    AVISIT  = col_character(),
    ADT     = col_date(),
    ANL01FL = col_character(),
    BASE    = col_double(),
    CHG     = col_double(),
    PCHG    = col_double(),
    ABLFL   = col_character()
  )
)

#----------------------------------------------------------------------
# Placeholder implementation of "g pkcg02 lin using the aNCA clinical
# task contract".
#
# Here, implement a per-parameter, per-visit linear model of change
# from baseline over time (AVISITN), and summarize the model fits.
#----------------------------------------------------------------------

# Fit linear model CHG ~ AVISITN within each STUDYID/PARAMCD/USUBJID
fits <- dat %>%
  group_by(STUDYID, PARAMCD, PARAM, USUBJID) %>%
  filter(!is.na(AVISITN), !is.na(CHG)) %>%
  do({
    df <- .
    if (nrow(df) < 2L) {
      tibble(
        n       = nrow(df),
        intercept = NA_real_,
        slope     = NA_real_,
        r2        = NA_real_
      )
    } else {
      m <- lm(CHG ~ AVISITN, data = df)
      s <- summary(m)
      tibble(
        n         = nrow(df),
        intercept = coef(m)[1],
        slope     = coef(m)[2],
        r2        = unname(s$r.squared)
      )
    }
  }) %>%
  ungroup()

# Aggregate to study/parameter level (example summary for contract)
result <- fits %>%
  group_by(STUDYID, PARAMCD, PARAM) %>%
  summarise(
    n_subjects        = n_distinct(USUBJID),
    mean_slope        = mean(slope, na.rm = TRUE),
    sd_slope          = sd(slope, na.rm = TRUE),
    mean_intercept    = mean(intercept, na.rm = TRUE),
    sd_intercept      = sd(intercept, na.rm = TRUE),
    mean_r2           = mean(r2, na.rm = TRUE),
    sd_r2             = sd(r2, na.rm = TRUE),
    .groups = "drop"
  )

#----------------------------------------------------------------------
# Write outputs
#----------------------------------------------------------------------
write_csv(result, out_csv)
saveRDS(list(
  per_subject_fits = fits,
  summary          = result
), out_rds)
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg02 lin. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. The target operation is the public aNCA routine `g_pkcg02_lin`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg02 lin. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. The target operation is the public aNCA routine `g_pkcg02_lin`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```