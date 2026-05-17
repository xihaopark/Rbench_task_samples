# Case 31 - `pharmaverse/aNCA/g_pkcg01_log`

**Package:** `aNCA`  **Function:** `g_pkcg01_log`  **Expected artifacts:** `outputs/result.csv, outputs/result.rds`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `high`

## Audit Evidence

Reference requires `aNCA:::g_pkcg01_log(data)` and ggplot RDS; current prompt calls it the public routine. Both outputs differ (`result.csv` ref `(1, 2)` vs current `(1, 3)`, simple `(9, 11)`) and `result.rds` is unexpected.

## Task Prompt From `task.json`

```text
Write R code to produce the **log-scale** PK plot **`g_pkcg01_log`** using aNCA. Load `library(aNCA)` and `library(ggplot2)`.

**Inputs:** `inputs/data.tsv` — main analysis table as a `data.frame`.

**Computation:** Call **`aNCA:::g_pkcg01_log(data)`** (internal; not `aNCA::g_pkcg01_log`). Save ggplot to `outputs/result.rds` and a tabular summary to `outputs/result.csv`.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full ggplot object to the RDS file and a sensible tabular summary to the CSV.

```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for g pkcg01 log. The available input files are `inputs/data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. The target operation is the public aNCA routine `g_pkcg01_log`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### data.tsv (5948 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.56	0	Baseline	2020-01-15	Y	119.28	-0.72	-0.6069	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.55	4	Week 4	2020-02-15	Y	119.28	-4.73	-3.9686	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	121.37	12	Week 12	2020-04-15	Y	119.28	2.09	1.7488	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	81.8	0	Baseline	2020-01-15	Y	82.05	-0.25	-0.3072	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	83.01	4	Week 4	2020-02-15	Y	82.05	0.96	1.1674	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.27	12	Week 12	2020-04-15	Y	82.05	0.22	0.2656	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	95.35	0	Baseline	2020-01-15	Y	92.79	2.56	2.7592	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	92.49	4	Week 4	2020-02-15	Y	92.79	-0.3	-0.323	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	91.62	12	Week 12	2020-04-15	Y	92.79	-1.17	-1.2606	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.48	0	Baseline	2020-01-15	Y	102.3	-2.82	-2.7566	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.34	4	Week 4	2020-02-15	Y	102.3	2.04	1.9941	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.58	12	Week 12	2020-04-15	Y	102.3	-1.72	-1.6814	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	79.0	0	Baseline	2020-01-15	Y	76.41	2.59	3.3862	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.04	4	Week 4	2020-02-15	Y	76.41	-2.37	-3.1049	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	75.95	12	Week 12	2020-04-15	Y	76.41	-0.46	-0.6053	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	89.56	0	Baseline	2020-01-15	Y	92.6	-3.04	-3.2875	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	92.83	4	Week 4	2020-02-15	Y	92.6	0.23	0.2436	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	90.84	12	Week 12	2020-04-15	Y	92.6	-1.76	-1.9053	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	106.12	0	Baseline	2020-01-15	Y	102.45	3.67	3.5848	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.6	4	Week 4	2020-02-15	Y	102.45	3.15	3.0773	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.4	12	Week 12	2020-04-15	Y	102.45	-3.05	-2.9746	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	63.88	0	Baseline	2020-01-15	Y	66.76	-2.88	-4.3125	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	64.68	4	Week 4	2020-02-15	Y	66.76	-2.08	-3.1142	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	67.16	12	Week 12	2020-04-15	Y	66.76	0.4	0.6007	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	72.46	0	Baseline	2020-01-15	Y	72.78	-0.32	-0.4456	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	73.03	4	Week 4	2020-02-15	Y	72.78	0.25	0.3375	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	73.9	12	Week 12	2020-04-15	Y	72.78	1.12	1.5328	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.1	0	Baseline	2020-01-15	Y	102.86	1.24	1.2044	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.1	4	Week 4	2020-02-15	Y	102.86	-1.76	-1.7121	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	103.36	12	Week 12	2020-04-15	Y	102.86	0.5	0.485	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	89.28	0	Baseline	2020-01-15	Y	88.04	1.24	1.4039	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	87.78	4	Week 4	2020-02-15	Y	88.04	-0.26	-0.2998	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	87.2	12	Week 12	2020-04-15	Y	88.04	-0.84	-0.9586	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	93.36	0	Baseline	2020-01-15	Y	90.82	2.54	2.7999	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	90.11	4	Week 4	2020-02-15	Y	90.82	-0.71	-0.7787	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	91.83	12	Week 12	2020-04-15	Y	90.82	1.01	1.1152	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.43	0	Baseline	2020-01-15	Y	124.1	1.33	1.0726	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.25	4	Week 4	2020-02-15	Y	124.1	2.15	1.7334	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	122.29	12	Week 12	2020-04-15	Y	124.1	-1.81	-1.4576	
... [15 more lines omitted]

```

## Simple Generated Prompt

```text
Create R script to perform g pkcg01 log using the aNCA clinical task contract.

Input: data.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### data.tsv (5948 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.56	0	Baseline	2020-01-15	Y	119.28	-0.72	-0.6069	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.55	4	Week 4	2020-02-15	Y	119.28	-4.73	-3.9686	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	121.37	12	Week 12	2020-04-15	Y	119.28	2.09	1.7488	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	81.8	0	Baseline	2020-01-15	Y	82.05	-0.25	-0.3072	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	83.01	4	Week 4	2020-02-15	Y	82.05	0.96	1.1674	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.27	12	Week 12	2020-04-15	Y	82.05	0.22	0.2656	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	95.35	0	Baseline	2020-01-15	Y	92.79	2.56	2.7592	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	92.49	4	Week 4	2020-02-15	Y	92.79	-0.3	-0.323	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	91.62	12	Week 12	2020-04-15	Y	92.79	-1.17	-1.2606	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.48	0	Baseline	2020-01-15	Y	102.3	-2.82	-2.7566	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.34	4	Week 4	2020-02-15	Y	102.3	2.04	1.9941	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.58	12	Week 12	2020-04-15	Y	102.3	-1.72	-1.6814	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	79.0	0	Baseline	2020-01-15	Y	76.41	2.59	3.3862	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.04	4	Week 4	2020-02-15	Y	76.41	-2.37	-3.1049	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	75.95	12	Week 12	2020-04-15	Y	76.41	-0.46	-0.6053	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	89.56	0	Baseline	2020-01-15	Y	92.6	-3.04	-3.2875	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	92.83	4	Week 4	2020-02-15	Y	92.6	0.23	0.2436	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	90.84	12	Week 12	2020-04-15	Y	92.6	-1.76	-1.9053	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	106.12	0	Baseline	2020-01-15	Y	102.45	3.67	3.5848	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.6	4	Week 4	2020-02-15	Y	102.45	3.15	3.0773	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.4	12	Week 12	2020-04-15	Y	102.45	-3.05	-2.9746	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	63.88	0	Baseline	2020-01-15	Y	66.76	-2.88	-4.3125	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	64.68	4	Week 4	2020-02-15	Y	66.76	-2.08	-3.1142	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	67.16	12	Week 12	2020-04-15	Y	66.76	0.4	0.6007	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	72.46	0	Baseline	2020-01-15	Y	72.78	-0.32	-0.4456	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	73.03	4	Week 4	2020-02-15	Y	72.78	0.25	0.3375	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	73.9	12	Week 12	2020-04-15	Y	72.78	1.12	1.5328	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.1	0	Baseline	2020-01-15	Y	102.86	1.24	1.2044	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.1	4	Week 4	2020-02-15	Y	102.86	-1.76	-1.7121	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	103.36	12	Week 12	2020-04-15	Y	102.86	0.5	0.485	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	89.28	0	Baseline	2020-01-15	Y	88.04	1.24	1.4039	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	87.78	4	Week 4	2020-02-15	Y	88.04	-0.26	-0.2998	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	87.2	12	Week 12	2020-04-15	Y	88.04	-0.84	-0.9586	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	93.36	0	Baseline	2020-01-15	Y	90.82	2.54	2.7999	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	90.11	4	Week 4	2020-02-15	Y	90.82	-0.71	-0.7787	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	91.83	12	Week 12	2020-04-15	Y	90.82	1.01	1.1152	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.43	0	Baseline	2020-01-15	Y	124.1	1.33	1.0726	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.25	4	Week 4	2020-02-15	Y	124.1	2.15	1.7334	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	122.29	12	Week 12	2020-04-15	Y	124.1	-1.81	-1.4576	
... [15 more lines omitted]

```

## Actual Input Files

**`data.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

```

## Reference Output Files

**`result.csv`**

```csv
"plot_type","success"
"ggplot",TRUE

```

**`result.rds`**

```text
[binary artifact: result.rds, 110840 bytes]
```

**`summary.csv`**

```csv
"result_type"
"ggplot2::ggplot"

```

## Reference Code

**`solution.R`**

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
  aNCA:::g_pkcg01_log(data)
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

## g_pkcg01_log driver for aNCA clinical PK support
## Inputs:  inputs/data.tsv
## Outputs: outputs/result.csv, outputs/result.rds

suppressPackageStartupMessages({
  ## add libraries here if g_pkcg01_log needs any
})

## ---- helper: safe scalar coercion ----
as_scalar_if_one_row <- function(x) {
  if (is.data.frame(x)) {
    if (nrow(x) == 1L && ncol(x) == 1L) {
      return(x[[1L]])
    }
    return(x)
  }
  if (length(x) == 1L) x else x
}

## ---- locate and read input ----
infile <- file.path("inputs", "data.tsv")
if (!file.exists(infile)) {
  stop("Input file not found: ", infile)
}

data <- read.delim(
  infile,
  header = TRUE,
  sep = "\t",
  check.names = FALSE,
  stringsAsFactors = FALSE
)

## ---- prepare arguments for g_pkcg01_log ----
## Treat the table as a single argument; any scalar arguments would be
## derived from 1-row TSVs (not present here, but scaffolding in place).
args_list <- list(data = data)
args_list <- lapply(args_list, as_scalar_if_one_row)

## ---- call public aNCA routine g_pkcg01_log ----
if (!exists("g_pkcg01_log")) {
  stop("Function g_pkcg01_log not found in the R environment.")
}

res <- do.call(g_pkcg01_log, args_list)

## ---- normalize result for grading ----
## Preserve full object to RDS; export a compact, inspectable CSV.
## If result is not a data.frame, attempt to coerce reasonably.
normalize_for_csv <- function(x) {
  if (is.data.frame(x)) return(x)
  if (is.matrix(x)) return(as.data.frame(x, stringsAsFactors = FALSE))
  if (is.list(x) && !is.null(names(x))) {
    ## try to bind list elements row-wise if they are vectors of equal length
    lens <- vapply(x, length, integer(1L))
    if (length(unique(lens)) == 1L) {
      return(as.data.frame(x, check.names = FALSE, stringsAsFactors = FALSE))
    }
  }
  ## fallback: wrap into a data.frame column
  data.frame(result = I(list(x)))
}

res_df <- normalize_for_csv(res)

## ---- write outputs ----
outdir <- "outputs"
if (!dir.exists(outdir)) dir.create(outdir, recursive = TRUE)

csv_file <- file.path(outdir, "result.csv")
rds_file <- file.path(outdir, "result.rds")

## keep CSV compact and inspectable
write.csv(
  res_df,
  file = csv_file,
  row.names = FALSE,
  na = ""
)

saveRDS(res, file = rds_file)
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
NULL

```

## Current Prompt Output Files

**`result.csv`**

```csv
"status","message","timestamp"
"success","g_pkcg01_log stub",2026-05-17 12:01:21.129693

```

**`result.rds`**

```text
[binary artifact: result.rds, 168 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#----------------------------
# Read input
#----------------------------
infile  <- file.path("inputs", "data.tsv")
advs    <- read_tsv(infile, col_types = cols(.default = col_guess()))

#----------------------------
# g pkcg01 log (aNCA clinical task contract)
# Here: derive simple descriptive stats by PARAMCD and AVISIT
#----------------------------

result <- advs %>%
  group_by(STUDYID, PARAMCD, PARAM, AVISITN, AVISIT) %>%
  summarise(
    N      = n(),
    MEAN   = mean(AVAL, na.rm = TRUE),
    SD     = sd(AVAL, na.rm = TRUE),
    MEDIAN = median(AVAL, na.rm = TRUE),
    MIN    = min(AVAL, na.rm = TRUE),
    MAX    = max(AVAL, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(STUDYID, PARAMCD, AVISITN, AVISIT)

#----------------------------
# Write outputs
#----------------------------

# CSV
outfile_csv <- file.path("outputs", "result.csv")
write_csv(result, outfile_csv)

# RDS
outfile_rds <- file.path("outputs", "result.rds")
saveRDS(result, outfile_rds)
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

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
STUDYID,PARAMCD,PARAM,AVISITN,AVISIT,N,MEAN,SD,MEDIAN,MIN,MAX
CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,6,74.405,10.466930304535328,73.515,63.88,89.28
CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,6,74.23,9.427003765778391,72.27000000000001,64.68,87.78
CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,6,74.08,9.369298799803538,72.37,63.11,87.2
CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,6,81.78999999999999,12.269122217990985,81.00999999999999,67.8,95.35
CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,6,82.02833333333334,11.00224780063904,82.78,68.26,92.83
CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,6,81.88333333333334,10.624572775724522,82.49000000000001,68.97,91.83
CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,6,112.19333333333333,10.321917780464378,112.34,99.48,125.43
CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,6,111.64833333333333,9.63193732676177,110.07499999999999,101.1,126.25
CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,6,110.74666666666667,10.752788785550784,110.42,99.4,122.29

```

**`result.rds`**

```text
[binary artifact: result.rds, 631 bytes]
```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/g_pkcg01_log",
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
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(1, 3)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    },
    "result.rds": {
      "match": false,
      "tier": "output_bad",
      "reason": "Unexpected: "
    }
  },
  "normalizations": []
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/aNCA/g_pkcg01_log",
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
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(9, 11)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    },
    "result.rds": {
      "match": false,
      "tier": "output_bad",
      "reason": "Unexpected: "
    }
  },
  "normalizations": []
}
```
