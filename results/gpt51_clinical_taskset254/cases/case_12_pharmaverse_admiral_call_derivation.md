# Case 12 - `pharmaverse/admiral/call_derivation`

**Package:** `admiral`  **Function:** `call_derivation`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `TIMEOUT` / tier `exec_fail`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `high`

## Audit Evidence

Reference solution effectively returns the input dataset; current prompt asks to "call a single derivation multiple times" with fixed/varying params, causing generated code to invent derivations and fail.

## Task Prompt From `task.json`

```text
Write R code to implement the **Call derivation** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/dataset.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'dataset.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/derivation.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'derivation.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/variable_params.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'variable_params.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Call Derivation** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
Write R code to call a single derivation multiple times using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset.tsv, inputs/derivation.tsv, inputs/variable_params.tsv). Call a single derivation multiple times with some parameters/arguments being fixed across iterations and others varying. Additional details: It is also possible to pass functions from outside the `{admiral}` package to `call_derivation()`, e.g. an extension package function, or `dplyr::mutate()`. The only requirement for a function being passed to `derivation` is that it must take a dataset as its first argument and return a dataset. Use admiral's call_derivation function with the following parameters: dataset (`r roxygen_param_dataset()`), derivation (The derivation function to call A function that performs a specific derivation is expected.), variable_params (A `list` of function arguments that are different across iterations.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with additional records/variables added depending on which `derivation` has been used.. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### dataset.tsv (5940 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.94	0	Baseline	2020-01-15	Y	105.37	-3.43	-3.2576	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.7	4	Week 4	2020-02-15	Y	105.37	-0.67	-0.6384	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.88	12	Week 12	2020-04-15	Y	105.37	-0.49	-0.4675	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.71	0	Baseline	2020-01-15	Y	83.29	-0.58	-0.6911	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.92	4	Week 4	2020-02-15	Y	83.29	-0.37	-0.439	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.16	12	Week 12	2020-04-15	Y	83.29	-1.13	-1.3515	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	97.63	0	Baseline	2020-01-15	Y	96.29	1.34	1.3913	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	98.23	4	Week 4	2020-02-15	Y	96.29	1.94	2.0145	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	100.48	12	Week 12	2020-04-15	Y	96.29	4.19	4.3511	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	92.07	0	Baseline	2020-01-15	Y	91.86	0.21	0.2315	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	93.32	4	Week 4	2020-02-15	Y	91.86	1.46	1.5923	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.68	12	Week 12	2020-04-15	Y	91.86	2.82	3.0729	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	79.78	0	Baseline	2020-01-15	Y	83.62	-3.84	-4.5941	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	82.98	4	Week 4	2020-02-15	Y	83.62	-0.64	-0.7674	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	83.12	12	Week 12	2020-04-15	Y	83.62	-0.5	-0.6	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	70.65	0	Baseline	2020-01-15	Y	71.73	-1.08	-1.501	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	72.22	4	Week 4	2020-02-15	Y	71.73	0.49	0.6879	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	75.35	12	Week 12	2020-04-15	Y	71.73	3.62	5.0517	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	122.24	0	Baseline	2020-01-15	Y	122.79	-0.55	-0.4478	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.3	4	Week 4	2020-02-15	Y	122.79	0.51	0.4155	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.41	12	Week 12	2020-04-15	Y	122.79	3.62	2.9483	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	73.42	0	Baseline	2020-01-15	Y	74.25	-0.83	-1.1212	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	74.08	4	Week 4	2020-02-15	Y	74.25	-0.17	-0.2323	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	71.12	12	Week 12	2020-04-15	Y	74.25	-3.13	-4.2187	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	65.29	0	Baseline	2020-01-15	Y	66.19	-0.9	-1.3597	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	69.02	4	Week 4	2020-02-15	Y	66.19	2.83	4.2756	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	64.57	12	Week 12	2020-04-15	Y	66.19	-1.62	-2.4475	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.09	0	Baseline	2020-01-15	Y	122.9	2.19	1.7853	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	120.58	4	Week 4	2020-02-15	Y	122.9	-2.32	-1.8844	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.55	12	Week 12	2020-04-15	Y	122.9	2.65	2.1596	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	64.56	0	Baseline	2020-01-15	Y	64.23	0.33	0.5116	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	63.84	4	Week 4	2020-02-15	Y	64.23	-0.39	-0.6093	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	65.65	12	Week 12	2020-04-15	Y	64.23	1.42	2.2086	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	81.52	0	Baseline	2020-01-15	Y	79.79	1.73	2.1646	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	77.14	4	Week 4	2020-02-15	Y	79.79	-2.65	-3.3246	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	80.7	12	Week 12	2020-04-15	Y	79.79	0.91	1.1369	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	113.87	0	Baseline	2020-01-15	Y	114.22	-0.35	-0.3044	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	112.73	4	Week 4	2020-02-15	Y	114.22	-1.49	-1.3025	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.44	12	Week 12	2020-04-15	Y	114.22	-2.78	-2.4319	
... [15 more lines omitted]

### derivation.tsv (32 bytes)
derivation
AVAL
AVISITN
USUBJID

### variable_params.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform call derivation using the admiral clinical task contract.

Input: dataset.tsv, derivation.tsv, variable_params.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### dataset.tsv (5940 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.94	0	Baseline	2020-01-15	Y	105.37	-3.43	-3.2576	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.7	4	Week 4	2020-02-15	Y	105.37	-0.67	-0.6384	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.88	12	Week 12	2020-04-15	Y	105.37	-0.49	-0.4675	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.71	0	Baseline	2020-01-15	Y	83.29	-0.58	-0.6911	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.92	4	Week 4	2020-02-15	Y	83.29	-0.37	-0.439	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	82.16	12	Week 12	2020-04-15	Y	83.29	-1.13	-1.3515	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	97.63	0	Baseline	2020-01-15	Y	96.29	1.34	1.3913	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	98.23	4	Week 4	2020-02-15	Y	96.29	1.94	2.0145	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	100.48	12	Week 12	2020-04-15	Y	96.29	4.19	4.3511	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	92.07	0	Baseline	2020-01-15	Y	91.86	0.21	0.2315	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	93.32	4	Week 4	2020-02-15	Y	91.86	1.46	1.5923	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.68	12	Week 12	2020-04-15	Y	91.86	2.82	3.0729	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	79.78	0	Baseline	2020-01-15	Y	83.62	-3.84	-4.5941	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	82.98	4	Week 4	2020-02-15	Y	83.62	-0.64	-0.7674	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	83.12	12	Week 12	2020-04-15	Y	83.62	-0.5	-0.6	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	70.65	0	Baseline	2020-01-15	Y	71.73	-1.08	-1.501	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	72.22	4	Week 4	2020-02-15	Y	71.73	0.49	0.6879	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	75.35	12	Week 12	2020-04-15	Y	71.73	3.62	5.0517	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	122.24	0	Baseline	2020-01-15	Y	122.79	-0.55	-0.4478	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.3	4	Week 4	2020-02-15	Y	122.79	0.51	0.4155	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.41	12	Week 12	2020-04-15	Y	122.79	3.62	2.9483	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	73.42	0	Baseline	2020-01-15	Y	74.25	-0.83	-1.1212	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	74.08	4	Week 4	2020-02-15	Y	74.25	-0.17	-0.2323	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	71.12	12	Week 12	2020-04-15	Y	74.25	-3.13	-4.2187	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	65.29	0	Baseline	2020-01-15	Y	66.19	-0.9	-1.3597	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	69.02	4	Week 4	2020-02-15	Y	66.19	2.83	4.2756	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	64.57	12	Week 12	2020-04-15	Y	66.19	-1.62	-2.4475	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.09	0	Baseline	2020-01-15	Y	122.9	2.19	1.7853	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	120.58	4	Week 4	2020-02-15	Y	122.9	-2.32	-1.8844	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.55	12	Week 12	2020-04-15	Y	122.9	2.65	2.1596	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	64.56	0	Baseline	2020-01-15	Y	64.23	0.33	0.5116	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	63.84	4	Week 4	2020-02-15	Y	64.23	-0.39	-0.6093	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	65.65	12	Week 12	2020-04-15	Y	64.23	1.42	2.2086	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	81.52	0	Baseline	2020-01-15	Y	79.79	1.73	2.1646	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	77.14	4	Week 4	2020-02-15	Y	79.79	-2.65	-3.3246	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	80.7	12	Week 12	2020-04-15	Y	79.79	0.91	1.1369	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	113.87	0	Baseline	2020-01-15	Y	114.22	-0.35	-0.3044	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	112.73	4	Week 4	2020-02-15	Y	114.22	-1.49	-1.3025	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.44	12	Week 12	2020-04-15	Y	114.22	-2.78	-2.4319	
... [15 more lines omitted]

### derivation.tsv (32 bytes)
derivation
AVAL
AVISITN
USUBJID

### variable_params.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`dataset.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

```

**`derivation.tsv`**

```tsv
derivation
"test_value"

```

**`variable_params.tsv`**

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
"id","value","group","category"
1,10.5,"A","Type1"
2,20.3,"B","Type2"
3,30.7,"A","Type1"
4,40.2,"B","Type2"
5,50.9,"A","Type1"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,4,"id, value, group, category"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(admiral))

suppressPackageStartupMessages(library(cli))
suppressPackageStartupMessages(library(purrr))
suppressPackageStartupMessages(library(rlang))

# 1. 读取输入数据 / Read input data
dataset_path <- file.path("inputs", "dataset.tsv")
if (!file.exists(dataset_path)) {
  stop("dataset.tsv is required input")
}
dataset <- read.delim(dataset_path, check.names = FALSE, stringsAsFactors = FALSE)
derivation_path <- file.path("inputs", "derivation.tsv")
if (!file.exists(derivation_path)) {
  stop("derivation.tsv is required input")
}
derivation <- read.delim(derivation_path, check.names = FALSE, stringsAsFactors = FALSE)
variable_params_path <- file.path("inputs", "variable_params.tsv")
if (!file.exists(variable_params_path)) {
  stop("variable_params.tsv is required input")
}
variable_params <- read.delim(variable_params_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证
if (nrow(dataset) == 0) stop("dataset is empty")

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  dataset
}, error = function(e) dataset)

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
    result <- saveRDS(result, file.path(outputs_dir, "result.rds"))
  } else if (is.vector(result) || is.numeric(result) || is.character(result)) {
    result_df <- data.frame(result = result, stringsAsFactors = FALSE)
    write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else {
    result <- saveRDS(result, file.path(outputs_dir, "result.rds"))
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
library(admiral)
library(readr)
library(dplyr)
library(purrr)
library(rlang)

#--------------------------
# Helper: safe file check
#--------------------------
check_file_exists <- function(path) {
  if (!file.exists(path)) {
    stop(glue::glue("Required file not found: {path}"))
  }
}

#--------------------------
# Paths
#--------------------------
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

dataset_path        <- file.path(in_dir, "dataset.tsv")
derivation_path     <- file.path(in_dir, "derivation.tsv")
variable_params_path <- file.path(in_dir, "variable_params.tsv")

walk(
  c(dataset_path, derivation_path, variable_params_path),
  check_file_exists
)

#--------------------------
# Read inputs
#--------------------------
dataset <- read_tsv(
  dataset_path,
  col_types = cols(.default = col_character()),
  progress = FALSE
)

# Convert known numeric/date columns safely
dataset <- dataset %>%
  mutate(
    AVAL    = suppressWarnings(as.numeric(AVAL)),
    AVISITN = suppressWarnings(as.integer(AVISITN)),
    ADT     = suppressWarnings(as.Date(ADT))
  )

if (anyNA(dataset$AVAL)) {
  warning("Missing or non-numeric values detected in AVAL after parsing.")
}
if (anyNA(dataset$AVISITN)) {
  warning("Missing or non-integer values detected in AVISITN after parsing.")
}

derivation_spec <- read_tsv(
  derivation_path,
  col_types = cols(.default = col_character()),
  progress = FALSE
)

variable_params_spec <- read_tsv(
  variable_params_path,
  col_types = cols(.default = col_character()),
  progress = FALSE
)

#--------------------------
# Basic validation
#--------------------------
required_cols <- c("USUBJID", "AVAL", "AVISITN")
missing_cols  <- setdiff(required_cols, names(dataset))
if (length(missing_cols) > 0) {
  stop("Dataset is missing required columns: ", paste(missing_cols, collapse = ", "))
}

if (!"id" %in% names(variable_params_spec)) {
  stop("`variable_params.tsv` must contain column `id`.")
}

# Ensure uniqueness of variable-parameter rows
if (any(duplicated(variable_params_spec$id))) {
  stop("Duplicate `id` values found in `variable_params.tsv`.")
}

#--------------------------
# Example derivation
#--------------------------
# A simple derivation that adds a derived flag based on AVAL cutoffs.
# It satisfies: first argument is `dataset`, returns dataset.
derive_flag_by_param <- function(dataset,
                                 cutoff_low,
                                 cutoff_high,
                                 flag_var,
                                 paramcd_filter = NULL) {
  if (!is.null(paramcd_filter)) {
    dataset <- dataset %>%
      mutate(
        !!sym(flag_var) :=
          if_else(
            PARAMCD %in% paramcd_filter & !is.na(AVAL),
            case_when(
              AVAL < cutoff_low  ~ "LOW",
              AVAL > cutoff_high ~ "HIGH",
              TRUE               ~ "NORMAL"
            ),
            NA_character_
          )
      )
  } else {
    dataset <- dataset %>%
      mutate(
        !!sym(flag_var) :=
          if_else(
            !is.na(AVAL),
            case_when(
              AVAL < cutoff_low  ~ "LOW",
              AVAL > cutoff_high ~ "HIGH",
              TRUE               ~ "NORMAL"
            ),
            NA_character_
          )
      )
  }

  dataset
}

#--------------------------
# Build variable_params list
#--------------------------
# Example:
# - fixed params across iterations:
#     cutoff_low  = 70
#     cutoff_high = 120
# - varying params:
#     flag_var, paramcd_filter derived per row in variable_params.tsv

# Here we interpret variable_params.tsv rows as iteration-specific settings.
# We create, for each row, a list of arguments that differ.
variable_params_list <- variable_params_spec %>%
  mutate(
    # example varying parameters from the spec:
    flag_var = paste0("FLG_", id),
    # For demonstration, alternate PARAMCD filters using the input value
    paramcd_filter = if_else(
      AVAL == "SYSBP", "SYSBP",
      if_else(AVAL == "DIABP", "DIABP", NA_character_)
    )
  ) %>%
  transpose() %>%
  map(function(x) {
    vp <- list()
    vp[["flag_var"]] <- x$flag_var

    if (!is.na(x$paramcd_filter)) {
      vp[["paramcd_filter"]] <- x$paramcd_filter
    } else {
      vp[["paramcd_filter"]] <- NULL
    }

    vp
  })

#--------------------------
# Call derivation multiple times
#--------------------------
# We fix cutoff_low and cutoff_high across iterations.
# We vary flag_var and paramcd_filter from variable_params_list.

result <- tryCatch(
  {
    call_derivation(
      dataset        = dataset,
      derivation     = derive_flag_by_param,
      variable_params = variable_params_list,
      cutoff_low     = 70,
      cutoff_high    = 120
    )
  },
  error = function(e) {
    stop("Error in call_derivation: ", conditionMessage(e))
  }
)

#--------------------------
# Additional example:
# using a non-admiral function, e.g. dplyr::mutate via call_derivation
#--------------------------
mutate_params_list <- list(
  list(new_mean_aval = TRUE),
  list(new_mean_aval = FALSE)
)

mutate_wrapper <- function(dataset, new_mean_aval = TRUE) {
  if (new_mean_aval) {
    dataset %>%
      group_by(STUDYID, USUBJID, PARAMCD) %>%
      mutate(MEAN_AVAL = mean(AVAL, na.rm = TRUE)) %>%
      ungroup()
  } else {
    dataset %>%
      mutate(AVAL_SQUARED = AVAL^2)
  }
}

result2 <- tryCatch(
  {
    call_derivation(
      dataset        = result,
      derivation     = mutate_wrapper,
      variable_params = mutate_params_list
    )
  },
  error = function(e) {
    stop("Error in call_derivation (mutate_wrapper): ", conditionMessage(e))
  }
)

#--------------------------
# Data validation / sanity checks
#--------------------------
if (!is.data.frame(result2)) {
  stop("Final result is not a data frame as expected.")
}

if (nrow(result2) == 0) {
  warning("Final result contains 0 rows.")
}

expected_new_cols <- c(
  unique(paste0("FLG_", variable_params_spec$id)),
  "MEAN_AVAL",
  "AVAL_SQUARED"
)

missing_new_cols <- setdiff(expected_new_cols, names(result2))
if (length(missing_new_cols) > 0) {
  warning(
    "Some expected derived columns are missing: ",
    paste(missing_new_cols, collapse = ", ")
  )
}

if (any(is.na(result2$USUBJID))) {
  warning("NA values found in USUBJID after derivations.")
}

# Quick misalignment check: ensure no duplicated key rows exploded unexpectedly
key_check <- result2 %>%
  count(STUDYID, USUBJID, PARAMCD, AVISITN, ADT, name = "n_recs")

if (any(key_check$n_recs > 1L)) {
  warning("Key combination has more than one record after derivations; check for unintended duplication.")
}

#--------------------------
# Write outputs
#--------------------------
out_csv  <- file.path(out_dir, "derived_dataset.csv")
out_rds  <- file.path(out_dir, "derived_dataset.rds")

write_csv(result2, out_csv, na = "")
saveRDS(result2, out_rds)

# Confirm files written
if (!file.exists(out_csv)) {
  stop("CSV output file was not written: ", out_csv)
}
if (!file.exists(out_rds)) {
  stop("RDS output file was not written: ", out_rds)
)

# Lightweight re-read check for parsing issues
reloaded <- read_csv(
  out_csv,
  col_types = cols(.default = col_character()),
  progress = FALSE
)

if (nrow(reloaded) != nrow(result2)) {
  warning("Row count mismatch between in-memory result and reloaded CSV.")
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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union


Attaching package: ‘rlang’

The following objects are masked from ‘package:purrr’:

    flatten, flatten_chr, flatten_dbl, flatten_int, flatten_lgl,
    flatten_raw, invoke, splice

Error in `mutate()`:
ℹ In argument: `paramcd_filter = if_else(...)`.
Caused by error:
! object 'AVAL' not found
Backtrace:
     ▆
  1. ├─... %>% ...
  2. ├─purrr::map(...)
  3. │ └─purrr:::map_("list", .x, .f, ..., .progress = .progress)
  4. │   └─purrr:::vctrs_vec_compat(.x, .purrr_user_env)
  5. ├─purrr::transpose(.)
  6. ├─dplyr::mutate(...)
  7. ├─dplyr:::mutate.data.frame(...)
  8. │ └─dplyr:::mutate_cols(.data, dplyr_quosures(...), by)
  9. │   ├─base::withCallingHandlers(...)
 10. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
 11. │     └─mask$eval_all_mutate(quo)
 12. │       └─dplyr (local) eval()
 13. ├─dplyr::if_else(...)
 14. │ └─vctrs::vec_if_else(...)
 15. └─base::.handleSimpleError(`<fn>`, "object 'AVAL' not found", base::quote(NULL))
 16.   └─dplyr (local) h(simpleError(msg, call))
 17.     └─rlang::abort(message, class = error_class, parent = parent, call = error_call)
Execution halted

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

_No files found._

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tidyr)
library(purrr)
library(stringr)
library(admiral)

# Paths -------------------------------------------------------------------
in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

dataset_path        <- file.path(in_dir,  "dataset.tsv")
derivation_path     <- file.path(in_dir,  "derivation.tsv")
variable_params_path<- file.path(in_dir,  "variable_params.tsv")
result_path         <- file.path(out_dir, "result.csv")

# Read inputs -------------------------------------------------------------
adslike <- read_tsv(
  dataset_path,
  col_types = cols(.default = col_character())
)

deriv_spec <- read_tsv(
  derivation_path,
  col_types = cols(.default = col_character())
)

var_params <- read_tsv(
  variable_params_path,
  col_types = cols(.default = col_character())
)

# Prepare data ------------------------------------------------------------
# Convert standard numeric/date columns
adslike <- adslike %>%
  mutate(
    AVAL    = suppressWarnings(as.numeric(AVAL)),
    AVISITN = suppressWarnings(as.numeric(AVISITN)),
    BASE    = suppressWarnings(as.numeric(BASE)),
    CHG     = suppressWarnings(as.numeric(CHG)),
    PCHG    = suppressWarnings(as.numeric(PCHG)),
    ADT     = as.Date(ADT)
  )

# Determine key variables from variable_params (id column)
key_vars <- setdiff(var_params$id, deriv_spec$derivation)

# If key variables are empty, default to USUBJID + PARAMCD + AVISITN
if (length(key_vars) == 0) {
  key_vars <- intersect(c("USUBJID", "PARAMCD", "AVISITN"), names(adslike))
}

# Derivation according to admiral clinical task contract ------------------
# Here we interpret "call derivation" as performing a grouped summary
# per key variables for the requested derivation variables.

# Variables to derive/carry
deriv_vars <- intersect(deriv_spec$derivation, names(adslike))

# For simplicity: take first non-missing value within each key group
result <- adslike %>%
  group_by(across(all_of(key_vars))) %>%
  summarise(
    across(
      all_of(deriv_vars),
      ~ .x[which(!is.na(.x))[1]],
      .names = "{.col}"
    ),
    .groups = "drop"
  )

# Ensure column ordering: keys first, then derivation vars in spec order
result <- result %>%
  select(any_of(key_vars), any_of(deriv_vars))

# Write output ------------------------------------------------------------
write_csv(result, result_path)
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

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error in `summarise()`:
ℹ In argument: `across(all_of(deriv_vars), ~.x[which(!is.na(.x))[1]],
  .names = "{.col}")`.
Caused by error in `across()`:
ℹ In argument: `all_of(deriv_vars)`.
Caused by error in `all_of()`:
! Can't subset elements that don't exist.
✖ Elements `AVISITN` and `USUBJID` don't exist.
Backtrace:
     ▆
  1. ├─adslike %>% group_by(across(all_of(key_vars))) %>% ...
  2. ├─dplyr::summarise(...)
  3. ├─dplyr:::summarise.grouped_df(...)
  4. │ └─dplyr:::summarise_cols(.data, dplyr_quosures(...), by, "summarise")
  5. │   ├─base::withCallingHandlers(...)
  6. │   └─dplyr:::expand_across(dot)
  7. │     └─dplyr:::across_setup(...)
  8. │       └─tidyselect::eval_select(cols, data = data, error_call = error_call)
  9. │         └─tidyselect:::eval_select_impl(...)
 10. │           ├─tidyselect:::with_subscript_errors(...)
 11. │           │ └─base::withCallingHandlers(...)
 12. │           └─tidyselect:::vars_select_eval(...)
 13. │             └─tidyselect:::walk_data_tree(expr, data_mask, context_mask)
 14. │               └─tidyselect:::eval_context(expr, context_mask, call = error_call)
 15. │                 ├─tidyselect:::with_chained_errors(...)
 16. │                 │ └─base::withCallingHandlers(...)
 17. │                 └─rlang::eval_tidy(as_quosure(expr, env), context_mask)
 18. ├─tidyselect::all_of(deriv_vars)
 19. │ └─tidyselect:::as_indices_impl(x, vars = vars, strict = TRUE)
 20. │   └─tidyselect:::chr_as_locations(x, vars, call = call, arg = arg)
 21. │     └─vctrs::vec_as_location(...)
 22. └─vctrs (local) `<fn>`()
 23.   └─vctrs:::stop_subscript_oob(...)
 24.     └─vctrs:::stop_subscript(...)
 25.       └─rlang::abort(...)
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
  "task_id": "pharmaverse/admiral/call_derivation",
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

### Simple Prompt

```json
{
  "task_id": "pharmaverse/admiral/call_derivation",
  "status": "TIMEOUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "returncode": null,
  "comparison": null,
  "normalizations": null
}
```
