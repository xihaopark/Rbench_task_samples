# Case 45 - `pharmaverse/admiraldev/assert_unit`

**Package:** `admiraldev`  **Function:** `assert_unit`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Audit root cause:** `data_or_fixture_issue`  **Confidence:** `medium`

## Audit Evidence

Fixture values are not usable unit specs: `required_unit.tsv` contains `AVAL`, `AVISITN`, `USUBJID`, and `get_unit_expr.tsv` contains parameter-like values (`SYSBP`, `DIABP`, ...), while the dataset has units embedded in `PARAM`. Generated solutions reasonably fail or emit no `result.csv` when trying to apply `assert_unit`.

## Task Prompt From `task.json`

```text
Assert **unit** strings with `admiraldev::assert_unit`. Load `library(admiraldev)`, `library(cli)`, `library(dplyr)`.

Follow `solution.R` for column extraction and assertion.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` (and `outputs/result.rds` when the reference writes both)

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
Follow `solution.R` for any additional `summary.csv` in the long template.

```

## Current Generated Prompt

```text
Write R code to asserts that a parameter is provided in the expected unit using admiraldev. At the beginning, load the required packages: library(admiraldev). The input data files are stored in inputs/ directory (inputs/dataset.tsv, inputs/param.tsv, inputs/required_unit.tsv, inputs/get_unit_expr.tsv). Checks if a parameter (`PARAMCD`) in a dataset is provided in the expected unit. Use admiraldev's assert_unit function with the following parameters: dataset (Dataset to be checked The variable `PARAMCD` and those used in `get_unit_expr` are expected.), param (Parameter code of the parameter to check), required_unit (Expected unit(s) If the argument is set to `NULL`, it is checked only whether the unit is unique within the parameter.), get_unit_expr (Expression used to provide the unit of `param`). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The function throws an error - if there is more than one non-missing unit in the dataset or - if the unit variable differs from the expected unit for any observation of the parameter in the input dataset. Otherwise, the dataset is returned invisibly.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### dataset.tsv (5914 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	117.95	0	Baseline	2020-01-15	Y	119.88	-1.93	-1.6061	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	120.63	4	Week 4	2020-02-15	Y	119.88	0.75	0.6295	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	117.7	12	Week 12	2020-04-15	Y	119.88	-2.18	-1.8147	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	91.21	0	Baseline	2020-01-15	Y	88.45	2.76	3.1212	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	90.37	4	Week 4	2020-02-15	Y	88.45	1.92	2.1715	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	88.93	12	Week 12	2020-04-15	Y	88.45	0.48	0.5435	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	95.83	0	Baseline	2020-01-15	Y	98.15	-2.32	-2.3637	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	96.73	4	Week 4	2020-02-15	Y	98.15	-1.42	-1.4467	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	96.93	12	Week 12	2020-04-15	Y	98.15	-1.22	-1.2429	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.83	0	Baseline	2020-01-15	Y	127.62	-0.79	-0.6175	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.22	4	Week 4	2020-02-15	Y	127.62	-0.4	-0.3119	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	124.38	12	Week 12	2020-04-15	Y	127.62	-3.24	-2.5373	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	72.39	0	Baseline	2020-01-15	Y	72.89	-0.5	-0.6821	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	72.56	4	Week 4	2020-02-15	Y	72.89	-0.33	-0.4489	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.3	12	Week 12	2020-04-15	Y	72.89	1.41	1.9384	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	75.36	0	Baseline	2020-01-15	Y	75.5	-0.14	-0.1819	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	76.08	4	Week 4	2020-02-15	Y	75.5	0.58	0.7718	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	76.28	12	Week 12	2020-04-15	Y	75.5	0.78	1.0367	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.95	0	Baseline	2020-01-15	Y	97.91	-0.96	-0.9817	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.03	4	Week 4	2020-02-15	Y	97.91	-0.88	-0.9	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.89	12	Week 12	2020-04-15	Y	97.91	-0.02	-0.0216	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	71.15	0	Baseline	2020-01-15	Y	68.4	2.75	4.0253	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	68.57	4	Week 4	2020-02-15	Y	68.4	0.17	0.2532	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	65.37	12	Week 12	2020-04-15	Y	68.4	-3.03	-4.4254	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	83.54	0	Baseline	2020-01-15	Y	84.53	-0.99	-1.1746	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	83.74	4	Week 4	2020-02-15	Y	84.53	-0.79	-0.938	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	84.04	12	Week 12	2020-04-15	Y	84.53	-0.49	-0.5831	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	116.0	0	Baseline	2020-01-15	Y	111.92	4.08	3.6459	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.35	4	Week 4	2020-02-15	Y	111.92	2.43	2.1717	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.42	12	Week 12	2020-04-15	Y	111.92	2.5	2.2342	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	64.31	0	Baseline	2020-01-15	Y	63.93	0.38	0.5943	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	63.89	4	Week 4	2020-02-15	Y	63.93	-0.04	-0.0627	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	65.03	12	Week 12	2020-04-15	Y	63.93	1.1	1.7205	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	65.93	0	Baseline	2020-01-15	Y	63.0	2.93	4.6504	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	62.9	4	Week 4	2020-02-15	Y	63.0	-0.1	-0.1591	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	64.77	12	Week 12	2020-04-15	Y	63.0	1.77	2.8091	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.35	0	Baseline	2020-01-15	Y	109.0	1.35	1.2352	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	108.08	4	Week 4	2020-02-15	Y	109.0	-0.92	-0.8473	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.34	12	Week 12	2020-04-15	Y	109.0	1.34	1.226	
... [15 more lines omitted]

### get_unit_expr.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### param.tsv (29 bytes)
parameters
SYSBP
DIABP
PULSE

### required_unit.tsv (35 bytes)
required_unit
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform assert unit using the admiraldev clinical task contract.

Input: dataset.tsv, get_unit_expr.tsv, param.tsv, required_unit.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### dataset.tsv (5914 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	117.95	0	Baseline	2020-01-15	Y	119.88	-1.93	-1.6061	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	120.63	4	Week 4	2020-02-15	Y	119.88	0.75	0.6295	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	117.7	12	Week 12	2020-04-15	Y	119.88	-2.18	-1.8147	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	91.21	0	Baseline	2020-01-15	Y	88.45	2.76	3.1212	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	90.37	4	Week 4	2020-02-15	Y	88.45	1.92	2.1715	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	88.93	12	Week 12	2020-04-15	Y	88.45	0.48	0.5435	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	95.83	0	Baseline	2020-01-15	Y	98.15	-2.32	-2.3637	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	96.73	4	Week 4	2020-02-15	Y	98.15	-1.42	-1.4467	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	96.93	12	Week 12	2020-04-15	Y	98.15	-1.22	-1.2429	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.83	0	Baseline	2020-01-15	Y	127.62	-0.79	-0.6175	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.22	4	Week 4	2020-02-15	Y	127.62	-0.4	-0.3119	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	124.38	12	Week 12	2020-04-15	Y	127.62	-3.24	-2.5373	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	72.39	0	Baseline	2020-01-15	Y	72.89	-0.5	-0.6821	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	72.56	4	Week 4	2020-02-15	Y	72.89	-0.33	-0.4489	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.3	12	Week 12	2020-04-15	Y	72.89	1.41	1.9384	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	75.36	0	Baseline	2020-01-15	Y	75.5	-0.14	-0.1819	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	76.08	4	Week 4	2020-02-15	Y	75.5	0.58	0.7718	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	76.28	12	Week 12	2020-04-15	Y	75.5	0.78	1.0367	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.95	0	Baseline	2020-01-15	Y	97.91	-0.96	-0.9817	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.03	4	Week 4	2020-02-15	Y	97.91	-0.88	-0.9	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.89	12	Week 12	2020-04-15	Y	97.91	-0.02	-0.0216	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	71.15	0	Baseline	2020-01-15	Y	68.4	2.75	4.0253	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	68.57	4	Week 4	2020-02-15	Y	68.4	0.17	0.2532	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	65.37	12	Week 12	2020-04-15	Y	68.4	-3.03	-4.4254	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	83.54	0	Baseline	2020-01-15	Y	84.53	-0.99	-1.1746	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	83.74	4	Week 4	2020-02-15	Y	84.53	-0.79	-0.938	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	84.04	12	Week 12	2020-04-15	Y	84.53	-0.49	-0.5831	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	116.0	0	Baseline	2020-01-15	Y	111.92	4.08	3.6459	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.35	4	Week 4	2020-02-15	Y	111.92	2.43	2.1717	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.42	12	Week 12	2020-04-15	Y	111.92	2.5	2.2342	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	64.31	0	Baseline	2020-01-15	Y	63.93	0.38	0.5943	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	63.89	4	Week 4	2020-02-15	Y	63.93	-0.04	-0.0627	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	65.03	12	Week 12	2020-04-15	Y	63.93	1.1	1.7205	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	65.93	0	Baseline	2020-01-15	Y	63.0	2.93	4.6504	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	62.9	4	Week 4	2020-02-15	Y	63.0	-0.1	-0.1591	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	64.77	12	Week 12	2020-04-15	Y	63.0	1.77	2.8091	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.35	0	Baseline	2020-01-15	Y	109.0	1.35	1.2352	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	108.08	4	Week 4	2020-02-15	Y	109.0	-0.92	-0.8473	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	110.34	12	Week 12	2020-04-15	Y	109.0	1.34	1.226	
... [15 more lines omitted]

### get_unit_expr.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### param.tsv (29 bytes)
parameters
SYSBP
DIABP
PULSE

### required_unit.tsv (35 bytes)
required_unit
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`dataset.tsv`**

```tsv
dataset
"x + y"
"a * b"
"sum(z)"
"mean(values)"
"max(data)"

```

**`get_unit_expr.tsv`**

```tsv
get_unit_expr
"x + y"
"a * b"
"sum(z)"
"mean(values)"
"max(data)"

```

**`param.tsv`**

```tsv
param
"test_value"

```

**`required_unit.tsv`**

```tsv
required_unit
"test_value"

```

## Reference Output Files

**`result.csv`**

```csv
"id","result"
1,"Error: Required variable `PARAMCD` is missing in `dataset`"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"id, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiraldev))

suppressPackageStartupMessages(library(cli))
suppressPackageStartupMessages(library(dplyr))

# 1. 读取输入数据 / Read input data
dataset_path <- file.path("inputs", "dataset.tsv")
if (!file.exists(dataset_path)) {
  stop("dataset.tsv is required input")
}
dataset <- read.delim(dataset_path, check.names = FALSE, stringsAsFactors = FALSE)
param_path <- file.path("inputs", "param.tsv")
if (!file.exists(param_path)) {
  stop("param.tsv is required input")
}
param <- read.delim(param_path, check.names = FALSE, stringsAsFactors = FALSE)
required_unit_path <- file.path("inputs", "required_unit.tsv")
if (!file.exists(required_unit_path)) {
  stop("required_unit.tsv is required input")
}
required_unit <- read.delim(required_unit_path, check.names = FALSE, stringsAsFactors = FALSE)
get_unit_expr_path <- file.path("inputs", "get_unit_expr.tsv")
if (!file.exists(get_unit_expr_path)) {
  stop("get_unit_expr.tsv is required input")
}
get_unit_expr <- read.delim(get_unit_expr_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 3. 对齐数据 / Align data
# 确保所有数据框使用相同的标识符对齐
if (length(c("dataset", "param", "required_unit", "get_unit_expr")) > 1) {
  # 尝试找到共同的ID列
  common_id_cols <- c("id", "sample", "subject", "patient", "usubjid", "usubj_id", "studyid")
  found_id_col <- NULL
  for (id_col in common_id_cols) {
    if (id_col %in% colnames(dataset)) {
      found_id_col <- id_col
      break
    }
  if (!is.null(found_id_col)) {
    common_ids <- dataset[[found_id_col]]
    for (df_name in c("param", "required_unit", "get_unit_expr")) {
      df <- get(df_name)
      if (found_id_col %in% colnames(df)) {
        common_ids <- intersect(common_ids, df[[found_id_col]])
      }
    }
    if (length(common_ids) > 0) {
      # 对齐所有数据框
      dataset <- dataset[dataset[[found_id_col]] %in% common_ids, , drop = FALSE]
      for (df_name in c("param", "required_unit", "get_unit_expr")) {
        df <- get(df_name)
        if (found_id_col %in% colnames(df)) {
          assign(df_name, df[df[[found_id_col]] %in% common_ids, , drop = FALSE])
        }
      }
    }
  }
}
for (df_name in c("dataset", "param", "required_unit", "get_unit_expr")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 3. 执行函数实现 / Execute function implementation
# 提取参数值
dataset_val <- if(is.data.frame(dataset) && ncol(dataset) > 0 && nrow(dataset) > 0) dataset else dataset
param_val <- if(is.data.frame(param) && ncol(param) > 0 && nrow(param) > 0) if(ncol(param) >= 1 && nrow(param) > 0) param[[1]] else NULL else param
required_unit_val <- if(is.data.frame(required_unit) && ncol(required_unit) > 0 && nrow(required_unit) > 0) if(ncol(required_unit) >= 1 && nrow(required_unit) > 0) required_unit[[1]] else NULL else required_unit
get_unit_expr_val <- if(is.data.frame(get_unit_expr) && ncol(get_unit_expr) > 0 && nrow(get_unit_expr) > 0) if(ncol(get_unit_expr) >= 1 && nrow(get_unit_expr) > 0) get_unit_expr[[1]] else NULL else get_unit_expr

result <- tryCatch({
  admiraldev::assert_unit(
    dataset = dataset_val,
    param = param_val,
    required_unit = required_unit_val,
    get_unit_expr = get_unit_expr_val
  )
}, error = function(e) {
  paste("Error:", conditionMessage(e))
})

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
}
```

## Current Prompt LLM Code

```r
library(admiraldev)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

#-----------------------------
# Read and validate input data
#-----------------------------

# Main dataset
dataset_path <- file.path("inputs", "dataset.tsv")
stopifnot(file.exists(dataset_path))
dataset <- tryCatch(
  read.delim(dataset_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) stop("Error reading dataset.tsv: ", conditionMessage(e))
)

# Parameters to check
param_path <- file.path("inputs", "param.tsv")
stopifnot(file.exists(param_path))
param_df <- tryCatch(
  read.delim(param_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) stop("Error reading param.tsv: ", conditionMessage(e))
)
if (!"parameters" %in% names(param_df)) {
  stop("param.tsv must contain a column named 'parameters'.")
}
params <- unique(na.omit(param_df$parameters))

# Required units
required_unit_path <- file.path("inputs", "required_unit.tsv")
stopifnot(file.exists(required_unit_path))
required_unit_df <- tryCatch(
  read.delim(required_unit_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) stop("Error reading required_unit.tsv: ", conditionMessage(e))
)
if (!"required_unit" %in% names(required_unit_df)) {
  stop("required_unit.tsv must contain a column named 'required_unit'.")
}
required_units <- unique(na.omit(required_unit_df$required_unit))

# get_unit_expr mapping
get_unit_expr_path <- file.path("inputs", "get_unit_expr.tsv")
stopifnot(file.exists(get_unit_expr_path))
get_unit_expr_df <- tryCatch(
  read.delim(get_unit_expr_path, stringsAsFactors = FALSE, check.names = FALSE),
  error = function(e) stop("Error reading get_unit_expr.tsv: ", conditionMessage(e))
)
if (!"x" %in% names(get_unit_expr_df)) {
  stop("get_unit_expr.tsv must contain a column named 'x'.")
}
unit_expr_params <- unique(na.omit(get_unit_expr_df$x))

# Basic validation
if (!"PARAMCD" %in% names(dataset)) {
  stop("dataset must contain a column named 'PARAMCD'.")
}

# Use PARAM variable as unit source, which must be present
if (!"PARAM" %in% names(dataset)) {
  stop("dataset must contain a column named 'PARAM' for unit derivation.")
}

# Ensure required variables used in get_unit_expr are present
missing_req <- setdiff(required_units, names(dataset))
if (length(missing_req) > 0) {
  stop(
    "The following required_unit variables are not present in dataset: ",
    paste(missing_req, collapse = ", ")
  )
}

# Ensure that every PARAMCD we will check is present in dataset
missing_paramcd <- setdiff(params, unique(dataset$PARAMCD))
if (length(missing_paramcd) > 0) {
  stop(
    "The following parameters from param.tsv are not found in dataset$PARAMCD: ",
    paste(missing_paramcd, collapse = ", ")
  )
}

# Ensure that every parameter in param.tsv has an entry in get_unit_expr.tsv
missing_in_unit_expr <- setdiff(params, unit_expr_params)
if (length(missing_in_unit_expr) > 0) {
  stop(
    "The following parameters from param.tsv are missing in get_unit_expr.tsv: ",
    paste(missing_in_unit_expr, collapse = ", ")
  )
}

#----------------------------------------
# Build get_unit_expr function generator
#----------------------------------------

# For this example, use PARAM as the "unit" source.
# Unit will be checked for uniqueness and/or equality against required_unit.
# Here we assume that required_unit.tsv actually encodes the expected unit
# string(s) for all parameters. If there are multiple rows, treat them as
# multiple allowed unit values.

get_unit <- function(data) {
  if (!"PARAM" %in% names(data)) {
    stop("get_unit_expr requires column 'PARAM' in dataset.")
  }
  data$PARAM
}

#---------------------------------
# Run assert_unit for each PARAMCD
#---------------------------------

# Collect results and any error messages
results_list <- list()
error_list <- list()

for (p in params) {
  # Determine expected unit(s) for this parameter
  # Here we assume the same expected_unit values apply to all parameters.
  # Adjust here if mapping should be parameter-specific.
  expected_unit <- if (length(required_units) == 0) NULL else required_units
  
  # Subset dataset for this parameter
  ds_param <- subset(dataset, PARAMCD == p)
  
  if (nrow(ds_param) == 0) {
    error_list[[p]] <- paste0("No records found in dataset for PARAMCD ", p)
    next
  }
  
  # Call assert_unit with error handling
  res <- tryCatch(
    {
      assert_unit(
        dataset      = ds_param,
        param        = p,
        required_unit = expected_unit,
        get_unit_expr = get_unit(dataset)
      )
    },
    error = function(e) e
  )
  
  if (inherits(res, "error")) {
    error_list[[p]] <- conditionMessage(res)
  } else {
    results_list[[p]] <- ds_param
  }
}

#---------------------------------
# Save outputs
#---------------------------------

# 1) Save per-parameter validated datasets (those that passed assert_unit)
if (length(results_list) > 0) {
  for (p in names(results_list)) {
    out_csv <- file.path("outputs", paste0("dataset_valid_", p, ".csv"))
    out_rds <- file.path("outputs", paste0("dataset_valid_", p, ".rds"))
    
    tryCatch(
      write.csv(results_list[[p]], out_csv, row.names = FALSE),
      error = function(e) stop("Failed to write CSV for PARAMCD ", p, ": ", conditionMessage(e))
    )
    
    tryCatch(
      saveRDS(results_list[[p]], out_rds),
      error = function(e) stop("Failed to write RDS for PARAMCD ", p, ": ", conditionMessage(e))
    )
  }
}

# 2) Save error summary (if any)
if (length(error_list) > 0) {
  error_df <- data.frame(
    PARAMCD = names(error_list),
    ERROR   = unlist(error_list),
    stringsAsFactors = FALSE
  )
  error_csv <- file.path("outputs", "assert_unit_errors.csv")
  error_rds <- file.path("outputs", "assert_unit_errors.rds")
  
  tryCatch(
    write.csv(error_df, error_csv, row.names = FALSE),
    error = function(e) stop("Failed to write error CSV: ", conditionMessage(e))
  )
  
  tryCatch(
    saveRDS(error_df, error_rds),
    error = function(e) stop("Failed to write error RDS: ", conditionMessage(e))
  )
}

#---------------------------------
# Confirm outputs and basic checks
#---------------------------------

output_files <- list.files("outputs", full.names = TRUE)
if (length(output_files) == 0) {
  stop("No output files were written to 'outputs/' directory.")
}

# Basic validation of CSVs and RDS files for read-back and obvious misalignment
for (f in output_files) {
  if (grepl("\\.csv$", f, ignore.case = TRUE)) {
    tmp <- tryCatch(
      read.csv(f, stringsAsFactors = FALSE, check.names = FALSE),
      error = function(e) stop("Failed to re-read CSV file ", f, ": ", conditionMessage(e))
    )
    
    if (!is.data.frame(tmp) || nrow(tmp) == 0) {
      stop("CSV file ", f, " appears empty or improperly formatted.")
    }
    
    # Simple heuristic: ensure no column with all NA (potential parse issue)
    all_na_cols <- vapply(tmp, function(col) all(is.na(col)), logical(1))
    if (any(all_na_cols)) {
      stop(
        "File ", f, " has column(s) with all NA values: ",
        paste(names(tmp)[all_na_cols], collapse = ", "),
        ". This may indicate parsing or alignment issues."
      )
    }
  } else if (grepl("\\.rds$", f, ignore.case = TRUE)) {
    tmp_rds <- tryCatch(
      readRDS(f),
      error = function(e) stop("Failed to re-read RDS file ", f, ": ", conditionMessage(e))
    )
    
    # No strict structure enforced, but ensure object is not NULL
    if (is.null(tmp_rds)) {
      stop("RDS file ", f, " contains a NULL object, which is unexpected.")
    }
  }
}
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

**`assert_unit_errors.csv`**

```csv
"PARAMCD","ERROR"
"SYSBP","It is expected that ""SYSBP"" has unit of ""AVAL"", ""AVISITN"", or ""USUBJID"".
In the input dataset the unit is ""SYSBP (mmHg)""."
"DIABP","It is expected that ""DIABP"" has unit of ""AVAL"", ""AVISITN"", or ""USUBJID"".
In the input dataset the unit is ""DIABP (mmHg)""."
"PULSE","It is expected that ""PULSE"" has unit of ""AVAL"", ""AVISITN"", or ""USUBJID"".
In the input dataset the unit is ""PULSE (beats/min)""."

```

**`assert_unit_errors.rds`**

```text
[binary artifact: assert_unit_errors.rds, 277 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

library(admiraldev)
library(dplyr)
library(readr)
library(rlang)
library(purrr)
library(stringr)

# Input paths
dataset_path       <- file.path("inputs", "dataset.tsv")
get_unit_expr_path <- file.path("inputs", "get_unit_expr.tsv")
param_path         <- file.path("inputs", "param.tsv")
required_path      <- file.path("inputs", "required_unit.tsv")

# Output path
output_path <- file.path("outputs", "result.csv")

# Read inputs
dataset       <- read_tsv(dataset_path, col_types = cols(.default = col_character()))
get_unit_expr <- read_tsv(get_unit_expr_path, col_types = cols(.default = col_character()))
param         <- read_tsv(param_path, col_types = cols(.default = col_character()))
required_unit <- read_tsv(required_path, col_types = cols(.default = col_character()))

# Prepare vectors
parameters_vec   <- param$parameters
required_vec     <- required_unit$required_unit
unit_expr_vec    <- get_unit_expr$x

# Build a named list of expressions per parameter matching admiraldev clinical task contract
# Here we assume each parameter listed in param.tsv must be checked and the expression
# list is derived from required_unit.tsv (columns that must be present/not missing).
# We construct an expression that all required variables are non-missing.
unit_expr_list <- map(
  parameters_vec,
  ~ expr(
    !!!map(
      required_vec,
      function(v) expr(!is.na(!!sym(v)))
    ) %>%
      reduce(~ expr(!!..1 & !!..2))
  )
)
names(unit_expr_list) <- parameters_vec

# Run assert_unit_contract from admiraldev
# This will create a data frame describing which records fail the unit assertion.
result <- assert_unit_contract(
  dataset,
  param_var   = PARAMCD,
  par_values  = parameters_vec,
  unit_expr   = unit_expr_list
)

# Ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Write result
write_csv(result, output_path)
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

Attaching package: ‘dplyr’

The following object is masked from ‘package:admiraldev’:

    filter_if

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union


Attaching package: ‘purrr’

The following objects are masked from ‘package:rlang’:

    flatten, flatten_chr, flatten_dbl, flatten_int, flatten_lgl,
    flatten_raw, invoke, splice

Error in `map()`:
ℹ In index: 1.
Caused by error in `enexpr()`:
! Can't use `!!!` at top level.
Backtrace:
    ▆
 1. ├─purrr::map(...)
 2. │ └─purrr:::map_("list", .x, .f, ..., .progress = .progress)
 3. │   ├─purrr:::with_indexed_errors(...)
 4. │   │ └─base::withCallingHandlers(...)
 5. │   ├─purrr:::call_with_cleanup(...)
 6. │   └─global .f(.x[[i]], ...)
 7. │     └─rlang::expr(...)
 8. │       └─rlang::enexpr(expr)
 9. └─rlang::abort(message = message)
Execution halted

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

_No files found._

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/admiraldev/assert_unit",
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
      "reason": "File not generated"
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
  "task_id": "pharmaverse/admiraldev/assert_unit",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "NO_OUTPUT",
  "tier": "exec_fail",
  "returncode": 1,
  "comparison": null,
  "normalizations": null
}
```
