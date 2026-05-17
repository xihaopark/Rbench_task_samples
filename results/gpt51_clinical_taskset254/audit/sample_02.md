# Sample 02: pharmaverse/aNCA/g_pkcg03_log

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/g_pkcg03_log`
- package/function: `aNCA` / `g_pkcg03_log`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to implement the **G pkcg03 log** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/data.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'data.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::g_pkcg03_log` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::g_pkcg03_log` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg03 log. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### data.tsv (5940 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.17	0	Baseline	2020-01-15	Y	98.25	-1.08	-1.099	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.13	4	Week 4	2020-02-15	Y	98.25	-2.12	-2.1576	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.13	12	Week 12	2020-04-15	Y	98.25	0.88	0.8959	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	81.26	0	Baseline	2020-01-15	Y	79.87	1.39	1.7363	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	81.3	4	Week 4	2020-02-15	Y	79.87	1.43	1.7864	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	79.11	12	Week 12	2020-04-15	Y	79.87	-0.76	-0.9555	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	61.88	0	Baseline	2020-01-15	Y	64.28	-2.4	-3.7283	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	60.89	4	Week 4	2020-02-15	Y	64.28	-3.39	-5.2685	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	62.14	12	Week 12	2020-04-15	Y	64.28	-2.14	-3.3238	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	115.71	0	Baseline	2020-01-15	Y	114.45	1.26	1.1031	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.35	4	Week 4	2020-02-15	Y	114.45	3.9	3.4098	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	113.35	12	Week 12	2020-04-15	Y	114.45	-1.1	-0.959	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	88.25	0	Baseline	2020-01-15	Y	87.35	0.9	1.0274	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	88.46	4	Week 4	2020-02-15	Y	87.35	1.11	1.2678	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	87.97	12	Week 12	2020-04-15	Y	87.35	0.62	0.7068	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	69.28	0	Baseline	2020-01-15	Y	69.53	-0.25	-0.3525	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	69.32	4	Week 4	2020-02-15	Y	69.53	-0.21	-0.295	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	68.77	12	Week 12	2020-04-15	Y	69.53	-0.76	-1.0861	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.88	0	Baseline	2020-01-15	Y	97.32	-2.44	-2.5108	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.42	4	Week 4	2020-02-15	Y	97.32	-0.9	-0.9284	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.61	12	Week 12	2020-04-15	Y	97.32	-2.71	-2.7882	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	77.54	0	Baseline	2020-01-15	Y	77.52	0.02	0.0282	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	78.82	4	Week 4	2020-02-15	Y	77.52	1.3	1.6795	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	76.2	12	Week 12	2020-04-15	Y	77.52	-1.32	-1.7004	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	68.59	0	Baseline	2020-01-15	Y	70.07	-1.48	-2.1151	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	71.96	4	Week 4	2020-02-15	Y	70.07	1.89	2.6942	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	74.33	12	Week 12	2020-04-15	Y	70.07	4.26	6.0764	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	98.33	0	Baseline	2020-01-15	Y	95.42	2.91	3.0481	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.26	4	Week 4	2020-02-15	Y	95.42	-0.16	-0.1692	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.41	12	Week 12	2020-04-15	Y	95.42	-1.01	-1.06	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	64.82	0	Baseline	2020-01-15	Y	64.46	0.36	0.551	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	63.64	4	Week 4	2020-02-15	Y	64.46	-0.82	-1.2795	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	66.73	12	Week 12	2020-04-15	Y	64.46	2.27	3.5138	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	62.39	0	Baseline	2020-01-15	Y	59.26	3.13	5.2773	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	57.95	4	Week 4	2020-02-15	Y	59.26	-1.31	-2.2148	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	57.23	12	Week 12	2020-04-15	Y	59.26	-2.03	-3.4297	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	109.72	0	Baseline	2020-01-15	Y	111.32	-1.6	-1.4333	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.19	4	Week 4	2020-02-15	Y	111.32	-1.13	-1.0111	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	113.88	12	Week 12	2020-04-15	Y	111.32	2.56	2.3038	
... [15 more lines omitted]

```

## Simple Prompt
```text
Create R script to perform g pkcg03 log using the aNCA clinical task contract.

Input: data.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### data.tsv (5940 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.17	0	Baseline	2020-01-15	Y	98.25	-1.08	-1.099	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.13	4	Week 4	2020-02-15	Y	98.25	-2.12	-2.1576	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.13	12	Week 12	2020-04-15	Y	98.25	0.88	0.8959	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	81.26	0	Baseline	2020-01-15	Y	79.87	1.39	1.7363	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	81.3	4	Week 4	2020-02-15	Y	79.87	1.43	1.7864	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	79.11	12	Week 12	2020-04-15	Y	79.87	-0.76	-0.9555	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	61.88	0	Baseline	2020-01-15	Y	64.28	-2.4	-3.7283	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	60.89	4	Week 4	2020-02-15	Y	64.28	-3.39	-5.2685	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	62.14	12	Week 12	2020-04-15	Y	64.28	-2.14	-3.3238	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	115.71	0	Baseline	2020-01-15	Y	114.45	1.26	1.1031	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.35	4	Week 4	2020-02-15	Y	114.45	3.9	3.4098	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	113.35	12	Week 12	2020-04-15	Y	114.45	-1.1	-0.959	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	88.25	0	Baseline	2020-01-15	Y	87.35	0.9	1.0274	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	88.46	4	Week 4	2020-02-15	Y	87.35	1.11	1.2678	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	87.97	12	Week 12	2020-04-15	Y	87.35	0.62	0.7068	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	69.28	0	Baseline	2020-01-15	Y	69.53	-0.25	-0.3525	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	69.32	4	Week 4	2020-02-15	Y	69.53	-0.21	-0.295	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	68.77	12	Week 12	2020-04-15	Y	69.53	-0.76	-1.0861	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.88	0	Baseline	2020-01-15	Y	97.32	-2.44	-2.5108	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.42	4	Week 4	2020-02-15	Y	97.32	-0.9	-0.9284	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.61	12	Week 12	2020-04-15	Y	97.32	-2.71	-2.7882	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	77.54	0	Baseline	2020-01-15	Y	77.52	0.02	0.0282	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	78.82	4	Week 4	2020-02-15	Y	77.52	1.3	1.6795	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	76.2	12	Week 12	2020-04-15	Y	77.52	-1.32	-1.7004	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	68.59	0	Baseline	2020-01-15	Y	70.07	-1.48	-2.1151	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	71.96	4	Week 4	2020-02-15	Y	70.07	1.89	2.6942	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	74.33	12	Week 12	2020-04-15	Y	70.07	4.26	6.0764	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	98.33	0	Baseline	2020-01-15	Y	95.42	2.91	3.0481	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.26	4	Week 4	2020-02-15	Y	95.42	-0.16	-0.1692	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.41	12	Week 12	2020-04-15	Y	95.42	-1.01	-1.06	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	64.82	0	Baseline	2020-01-15	Y	64.46	0.36	0.551	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	63.64	4	Week 4	2020-02-15	Y	64.46	-0.82	-1.2795	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	66.73	12	Week 12	2020-04-15	Y	64.46	2.27	3.5138	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	62.39	0	Baseline	2020-01-15	Y	59.26	3.13	5.2773	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	57.95	4	Week 4	2020-02-15	Y	59.26	-1.31	-2.2148	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	57.23	12	Week 12	2020-04-15	Y	59.26	-2.03	-3.4297	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	109.72	0	Baseline	2020-01-15	Y	111.32	-1.6	-1.4333	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.19	4	Week 4	2020-02-15	Y	111.32	-1.13	-1.0111	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	113.88	12	Week 12	2020-04-15	Y	111.32	2.56	2.3038	
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(54, 13) | summary.csv: match=False reason=File not generated | result.rds: match=False reason=Unexpected: "
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(1, 2) vs llm=(18, 21) | summary.csv: match=False reason=File not generated | result.rds: match=False reason=Unexpected: "
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
  aNCA:::g_pkcg03_log(data)
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
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  } else if (is.
```

## Current Solution
```r
## aNCA clinical PK support benchmark helper for g pkcg03 log

## Set up paths
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

## Helper to read TSV with header preservation
read_tsv_any <- function(path) {
  x <- read.delim(path, header = TRUE, sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)
  x
}

## Read input
data_path <- file.path(in_dir, "data.tsv")
dat <- read_tsv_any(data_path)

## Core transformation:
## For this helper, treat the ADaM-like VS dataset as the "result object"
## but keep a compact CSV subset for easy inspection.

## Ensure ADT is parsed as Date
if (!inherits(dat$ADT, "Date")) {
  suppressWarnings({
    dat$ADT <- as.Date(dat$ADT)
  })
}

## Order rows in a stable, analysis-friendly way
ord_vars <- intersect(c("STUDYID","USUBJID","PARAMCD","AVISITN","ADT"), names(dat))
if (length(ord_vars) > 0L) {
  dat <- dat[do.call(order, dat[ord_vars]), , drop = FALSE]
}

## Create a compact inspectable CSV: key identifiers + main analysis vars
compact_cols <- c(
  "STUDYID","USUBJID",
  "PARAMCD","PARAM",
  "AVISITN","AVISIT","ADT",
  "ANL01FL","ABLFL",
  "BASE","AVAL","CHG","PCHG"
)
compact_cols <- intersect(compact_cols, names(dat))
result_compact <- dat[, compact_cols, drop = FALSE]

## Write outputs
csv_path <- file.path(out_dir, "result.csv")
rds_path <- file.path(out_dir, "result.rds")

write.csv(result_compact, csv_path, row.names = FALSE)
saveRDS(dat, rds_path)
```

## Simple Solution
```r
#!/usr/bin/env Rscript

# g pkcg03 log using the aNCA clinical task contract
# Input:  inputs/data.tsv
# Output: outputs/result.csv, outputs/result.rds

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# I/O --------------------------------------------------------------------------
in_file  <- file.path("inputs", "data.tsv")
out_csv  <- file.path("outputs", "result.csv")
out_rds  <- file.path("outputs", "result.rds")

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

dat <- read_tsv(in_file, col_types = cols())

# Core derivations (example PKCG03-style log summary on vital signs) ----------
# Per-subject, per-parameter summaries over visits

res <- dat %>%
  mutate(
    ADT = as.Date(ADT),
    AVAL = as.numeric(AVAL),
    BASE = as.numeric(BASE),
    CHG  = as.numeric(CHG),
    PCHG = as.numeric(PCHG)
  ) %>%
  group_by(STUDYID, USUBJID, PARAMCD, PARAM) %>%
  summarise(
    N_AVAL      = sum(!is.na(AVAL)),
    AVISITN_MIN = min(AVISITN, na.rm = TRUE),
    AVISITN_MAX = max(AVISITN, na.rm = TRUE),
    ADT_MIN     = min(ADT, na.rm = TRUE),
    ADT_MAX     = max(ADT, na.rm = TRUE),
    BASE_FIRST  = BASE[which.min(AVISITN)],
    AVAL_BASE   = AVAL[which.min(AVISITN)],
    AVAL_MIN    = min(AVAL, na.rm = TRUE),
    AVAL_MAX    = max(AVAL, na.rm = TRUE),
    AVAL_MEAN   = mean(AVAL, na.rm = TRUE),
    AVAL_SD     = sd(AVAL,  na.rm = TRUE),
    CHG_MIN     = min(CHG,  na.rm = TRUE),
    CHG_MAX     = max(CHG,  na.rm = TRUE),
    CHG_MEAN    = mean(CHG, na.rm = TRUE),
    PCHG_MIN    = min(PCHG, na.rm = TRUE),
    PCHG_MAX    = max(PCHG, na.rm = TRUE),
    PCHG_MEAN   = mean(PCHG, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(STUDYID, USUBJID, PARAMCD)

# Write outputs ----------------------------------------------------------------
write_csv(res, out_csv)
saveRDS(res, out_rds)
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg03 log. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg03 log. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```