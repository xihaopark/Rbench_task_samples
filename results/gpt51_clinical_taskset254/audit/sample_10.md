# Sample 10: pharmaverse/aNCA/add_exclusion_reasons

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/add_exclusion_reasons`
- package/function: `aNCA` / `add_exclusion_reasons`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `TIMEOUT` tier=`exec_fail`

## Reference Prompt
```text
Write R code to implement the **Add exclusion reasons** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/exclusion_list.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'exclusion_list.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/pknca_data.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'pknca_data.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Add Exclusion Reasons** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for add exclusion reasons. The available input files are `inputs/exclusion_list.tsv`, `inputs/pknca_data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### exclusion_list.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### pknca_data.tsv (5921 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.11	0	Baseline	2020-01-15	Y	94.9	0.21	0.2185	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.56	4	Week 4	2020-02-15	Y	94.9	0.66	0.6927	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.18	12	Week 12	2020-04-15	Y	94.9	2.28	2.3997	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	65.74	0	Baseline	2020-01-15	Y	64.87	0.87	1.3419	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	64.3	4	Week 4	2020-02-15	Y	64.87	-0.57	-0.8779	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	63.34	12	Week 12	2020-04-15	Y	64.87	-1.53	-2.3578	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	84.35	0	Baseline	2020-01-15	Y	85.5	-1.15	-1.3422	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	87.36	4	Week 4	2020-02-15	Y	85.5	1.86	2.1784	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	85.97	12	Week 12	2020-04-15	Y	85.5	0.47	0.5526	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	128.12	0	Baseline	2020-01-15	Y	127.59	0.53	0.4188	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	129.0	4	Week 4	2020-02-15	Y	127.59	1.41	1.1085	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.94	12	Week 12	2020-04-15	Y	127.59	0.35	0.2777	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	84.32	0	Baseline	2020-01-15	Y	83.92	0.4	0.4743	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	84.46	4	Week 4	2020-02-15	Y	83.92	0.54	0.6411	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	85.16	12	Week 12	2020-04-15	Y	83.92	1.24	1.4752	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	61.09	0	Baseline	2020-01-15	Y	63.14	-2.05	-3.2402	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	62.02	4	Week 4	2020-02-15	Y	63.14	-1.12	-1.7671	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	64.5	12	Week 12	2020-04-15	Y	63.14	1.36	2.1609	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.69	0	Baseline	2020-01-15	Y	98.14	1.55	1.5825	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.46	4	Week 4	2020-02-15	Y	98.14	-1.68	-1.7088	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.29	12	Week 12	2020-04-15	Y	98.14	-0.85	-0.863	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	80.41	0	Baseline	2020-01-15	Y	80.51	-0.1	-0.1184	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	80.05	4	Week 4	2020-02-15	Y	80.51	-0.46	-0.5656	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	80.93	12	Week 12	2020-04-15	Y	80.51	0.42	0.5275	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	88.34	0	Baseline	2020-01-15	Y	89.75	-1.41	-1.568	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	90.31	4	Week 4	2020-02-15	Y	89.75	0.56	0.6271	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	94.56	12	Week 12	2020-04-15	Y	89.75	4.81	5.3626	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.22	0	Baseline	2020-01-15	Y	129.34	0.88	0.6766	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	129.86	4	Week 4	2020-02-15	Y	129.34	0.52	0.3983	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.94	12	Week 12	2020-04-15	Y	129.34	1.6	1.2332	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	86.09	0	Baseline	2020-01-15	Y	87.37	-1.28	-1.4688	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	88.13	4	Week 4	2020-02-15	Y	87.37	0.76	0.866	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	87.45	12	Week 12	2020-04-15	Y	87.37	0.08	0.0878	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	98.53	0	Baseline	2020-01-15	Y	99.01	-0.48	-0.4825	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	101.82	4	Week 4	2020-02-15	Y	99.01	2.81	2.8405	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	96.41	12	Week 12	2020-04-15	Y	99.01	-2.6	-2.6237	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.67	0	Baseline	2020-01-15	Y	101.1	-1.43	-1.4103	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.34	4	Week 4	2020-02-15	Y	101.1	-1.76	-1.7367	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.67	12	Week 12	2020-04-15	Y	101.1	1.57	1.5572	
... [15 more lines omitted]

```

## Simple Prompt
```text
Create R script to perform add exclusion reasons using the aNCA clinical task contract.

Input: exclusion_list.tsv, pknca_data.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### exclusion_list.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### pknca_data.tsv (5921 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.11	0	Baseline	2020-01-15	Y	94.9	0.21	0.2185	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.56	4	Week 4	2020-02-15	Y	94.9	0.66	0.6927	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.18	12	Week 12	2020-04-15	Y	94.9	2.28	2.3997	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	65.74	0	Baseline	2020-01-15	Y	64.87	0.87	1.3419	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	64.3	4	Week 4	2020-02-15	Y	64.87	-0.57	-0.8779	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	63.34	12	Week 12	2020-04-15	Y	64.87	-1.53	-2.3578	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	84.35	0	Baseline	2020-01-15	Y	85.5	-1.15	-1.3422	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	87.36	4	Week 4	2020-02-15	Y	85.5	1.86	2.1784	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	85.97	12	Week 12	2020-04-15	Y	85.5	0.47	0.5526	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	128.12	0	Baseline	2020-01-15	Y	127.59	0.53	0.4188	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	129.0	4	Week 4	2020-02-15	Y	127.59	1.41	1.1085	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.94	12	Week 12	2020-04-15	Y	127.59	0.35	0.2777	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	84.32	0	Baseline	2020-01-15	Y	83.92	0.4	0.4743	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	84.46	4	Week 4	2020-02-15	Y	83.92	0.54	0.6411	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	85.16	12	Week 12	2020-04-15	Y	83.92	1.24	1.4752	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	61.09	0	Baseline	2020-01-15	Y	63.14	-2.05	-3.2402	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	62.02	4	Week 4	2020-02-15	Y	63.14	-1.12	-1.7671	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	64.5	12	Week 12	2020-04-15	Y	63.14	1.36	2.1609	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.69	0	Baseline	2020-01-15	Y	98.14	1.55	1.5825	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.46	4	Week 4	2020-02-15	Y	98.14	-1.68	-1.7088	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.29	12	Week 12	2020-04-15	Y	98.14	-0.85	-0.863	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	80.41	0	Baseline	2020-01-15	Y	80.51	-0.1	-0.1184	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	80.05	4	Week 4	2020-02-15	Y	80.51	-0.46	-0.5656	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	80.93	12	Week 12	2020-04-15	Y	80.51	0.42	0.5275	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	88.34	0	Baseline	2020-01-15	Y	89.75	-1.41	-1.568	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	90.31	4	Week 4	2020-02-15	Y	89.75	0.56	0.6271	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	94.56	12	Week 12	2020-04-15	Y	89.75	4.81	5.3626	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.22	0	Baseline	2020-01-15	Y	129.34	0.88	0.6766	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	129.86	4	Week 4	2020-02-15	Y	129.34	0.52	0.3983	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.94	12	Week 12	2020-04-15	Y	129.34	1.6	1.2332	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	86.09	0	Baseline	2020-01-15	Y	87.37	-1.28	-1.4688	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	88.13	4	Week 4	2020-02-15	Y	87.37	0.76	0.866	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	87.45	12	Week 12	2020-04-15	Y	87.37	0.08	0.0878	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	98.53	0	Baseline	2020-01-15	Y	99.01	-0.48	-0.4825	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	101.82	4	Week 4	2020-02-15	Y	99.01	2.81	2.8405	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	96.41	12	Week 12	2020-04-15	Y	99.01	-2.6	-2.6237	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.67	0	Baseline	2020-01-15	Y	101.1	-1.43	-1.4103	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.34	4	Week 4	2020-02-15	Y	101.1	-1.76	-1.7367	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.67	12	Week 12	2020-04-15	Y	101.1	1.57	1.5572	
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(5, 4) vs llm=(0, 13) | summary.csv: match=False reason=File not generated"
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
pknca_data_path <- file.path("inputs", "pknca_data.tsv")
if (!file.exists(pknca_data_path)) {
  stop("pknca_data.tsv is required input")
}
pknca_data <- read.delim(pknca_data_path, check.names = FALSE, stringsAsFactors = FALSE)
exclusion_list_path <- file.path("inputs", "exclusion_list.tsv")
if (!file.exists(exclusion_list_path)) {
  stop("exclusion_list.tsv is required input")
}
exclusion_list_df <- read.delim(exclusion_list_path, check.names = FALSE, stringsAsFactors = FALSE)
exclusion_list <- exclusion_list_df$exclusion_list

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("pknca_data")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }

# 3. 执行函数实现 / Execute function implementation
# pknca_data需要是PKNCAdata对象，如果只是数据框则跳过
if (inherits(pknca_data, "PKNCAdata") && !is.null(pknca_data$conc) && !is.null(pknca_data$conc$data)) {
  exclude_col <- pknca_data$conc$columns[["exclude"]]
  if (is.null(exclude_col)) {
    pknca_data$conc$data$exclude <- rep("", nrow(pknca_data$conc$data))
    pknca_data$conc$columns[["exclude"]] <- "exclude"
    exclude_col <- "exclude"
  }
  # exclusion_list需要是列表的列表
  if (is.character(exclusion_list) || is.vector(exclusion_list)) {
    # 如果是字符向量，转换为简单的排除列表
    result <- pknca_data
  } else if (is.list(exclusion_list) && length(exclusion_list) > 0) {
    for (excl in exclusion_list) {
      if (is.list(excl) && "reason" %in% names(excl) && "rows" %in% names(excl)) {
        reason <- excl$reason
        rows <- excl$rows
        if (any(rows < 1 | rows > nrow(pknca_data$conc$data))) {
          stop(
            "Row indices in exclusion_list are out of bounds",
            " for the exclusion: ", reason)
        } else {
          pknca_data$conc$data[[exclude_col]][rows] <- ifelse(
            pknca_data$conc$data[[exclude_col]][rows] == "",
            reason,
            paste0(pknca_data$conc$data[[exclude_col]][rows], "; ", reason)
          )
        }
      }
    }
    result <- pknca_data
  } else {
    result <- pknca_data
  }
} else {
  # 如果不是PKNCAdata对象，返回原数据
  result <- pknca_data
}

# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    exclusion_list = exclusion_list,
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
  summary_stats <- data
```

## Current Solution
```r
#!/usr/bin/env Rscript

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper: read TSV with header, strings as is
read_tsv <- function(path) {
  read.delim(path,
             header = TRUE,
             sep = "\t",
             stringsAsFactors = FALSE,
             check.names = FALSE)
}

# Read inputs
excl <- read_tsv("inputs/exclusion_list.tsv")
pknca <- read_tsv("inputs/pknca_data.tsv")

# Treat one-column exclusion_list as vector of PARAMCD values
excl_vec <- unique(as.character(excl[[1]]))

# Exclude rows from pknca where PARAMCD is in exclusion list
result <- subset(pknca, !(PARAMCD %in% excl_vec))

# Write compact CSV (no row names)
write.csv(result,
          file = "outputs/result.csv",
          row.names = FALSE,
          quote = TRUE)

# Write full result object to RDS
saveRDS(result, file = "outputs/result.rds")
```

## Simple Solution
```r
library(dplyr)
library(readr)
library(tidyr)
library(stringr)

# directories
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# read inputs
excl <- read_tsv(file.path(in_dir, "exclusion_list.tsv"), col_types = cols(.default = "c"))
pknca <- read_tsv(file.path(in_dir, "pknca_data.tsv"), col_types = cols(.default = "c"))

# vector of PARAMCD to exclude
excl_paramcd <- excl[[1]] %>% unique() %>% na.omit()

# add exclusion flag and reason per aNCA-style contract
result <- pknca %>%
  mutate(
    EXCLUDE = if_else(PARAMCD %in% excl_paramcd, "Y", "N"),
    EXCLUSION_REASON = if_else(
      EXCLUDE == "Y",
      paste0("Excluded by exclusion_list for PARAMCD=", PARAMCD),
      NA_character_
    )
  )

# write outputs
write_csv(result, file.path(out_dir, "result.csv"), na = "")

saveRDS(result, file.path(out_dir, "result.rds"))
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add exclusion reasons. The available input files are `inputs/exclusion_list.tsv`, `inputs/pknca_data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for add exclusion reasons. The available input files are `inputs/exclusion_list.tsv`, `inputs/pknca_data.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```