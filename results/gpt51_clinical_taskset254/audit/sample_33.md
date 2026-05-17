# Sample 33: pharmaverse/admiral/slice_derivation

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiral/slice_derivation`
- package/function: `admiral` / `slice_derivation`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to implement the **Slice derivation** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/args.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'args.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::slice_derivation` (numeric vectors are often stored in a column named like the parameter).
- `inputs/dataset.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'dataset.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::slice_derivation` (numeric vectors are often stored in a column named like the parameter).
- `inputs/derivation.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'derivation.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::slice_derivation` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use `admiral::slice_derivation` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Prompt
```text
Write R code to execute a derivation with different arguments for subsets of the input dataset using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset.tsv, inputs/derivation.tsv, inputs/args.tsv). The input dataset is split into slices (subsets) and for each slice the derivation is called separately. Some or all arguments of the derivation may vary depending on the slice. Additional details: For each slice the derivation is called on the subset defined by the `filter` field of the `derivation_slice()` object and with the parameters specified by the `args` parameter and the `args` field of the `derivation_slice()` object. If a parameter is specified for both, the value in `derivation_slice()` overwrites the one in `args`. - Observations that match with more than one slice are only considered for the first matching slice. - The derivation is called for slices with no observations. - Observations with no match to any of the slices are included in the output dataset but the derivation is not called for them. It is also possible to pass functions from outside the `{admiral}` package to `slice_derivation()`, e.g. an extension package function, or `dplyr::mutate()`. The only requirement for a function being passed to `derivation` is that it must take a dataset as its first argument and return a dataset. Use admiral's slice_derivation function with the following parameters: dataset (`r roxygen_param_dataset()`), derivation (Derivation A function that performs a specific derivation is expected.), args (Arguments of the derivation A `params()` object is expected.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with the variables derived by the derivation added. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### args.tsv (24 bytes)
arg
2020-01-15T08:30:00

### dataset.tsv (5930 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.16	0	Baseline	2020-01-15	Y	98.16	-1.0	-1.017	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.45	4	Week 4	2020-02-15	Y	98.16	-1.71	-1.7403	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.01	12	Week 12	2020-04-15	Y	98.16	-4.15	-4.2261	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	62.09	0	Baseline	2020-01-15	Y	60.69	1.4	2.2992	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	61.51	4	Week 4	2020-02-15	Y	60.69	0.82	1.3436	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	59.72	12	Week 12	2020-04-15	Y	60.69	-0.97	-1.6056	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	88.9	0	Baseline	2020-01-15	Y	91.98	-3.08	-3.3473	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	91.37	4	Week 4	2020-02-15	Y	91.98	-0.61	-0.6619	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	92.26	12	Week 12	2020-04-15	Y	91.98	0.28	0.3057	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.64	0	Baseline	2020-01-15	Y	95.79	-1.15	-1.1967	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.26	4	Week 4	2020-02-15	Y	95.79	-1.53	-1.5934	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.07	12	Week 12	2020-04-15	Y	95.79	-0.72	-0.7478	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	58.98	0	Baseline	2020-01-15	Y	61.46	-2.48	-4.0323	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	63.65	4	Week 4	2020-02-15	Y	61.46	2.19	3.5664	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	62.67	12	Week 12	2020-04-15	Y	61.46	1.21	1.9718	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	62.36	0	Baseline	2020-01-15	Y	61.92	0.44	0.7083	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	63.03	4	Week 4	2020-02-15	Y	61.92	1.11	1.7904	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	62.08	12	Week 12	2020-04-15	Y	61.92	0.16	0.2562	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.33	0	Baseline	2020-01-15	Y	125.94	0.39	0.3112	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.5	4	Week 4	2020-02-15	Y	125.94	4.56	3.6223	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.11	12	Week 12	2020-04-15	Y	125.94	0.17	0.1365	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	59.73	0	Baseline	2020-01-15	Y	61.71	-1.98	-3.215	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	60.63	4	Week 4	2020-02-15	Y	61.71	-1.08	-1.7567	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	61.52	12	Week 12	2020-04-15	Y	61.71	-0.19	-0.3145	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	83.63	0	Baseline	2020-01-15	Y	85.83	-2.2	-2.5622	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	90.56	4	Week 4	2020-02-15	Y	85.83	4.73	5.512	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	88.77	12	Week 12	2020-04-15	Y	85.83	2.94	3.4265	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.16	0	Baseline	2020-01-15	Y	110.36	0.8	0.7239	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	108.94	4	Week 4	2020-02-15	Y	110.36	-1.42	-1.2876	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.81	12	Week 12	2020-04-15	Y	110.36	1.45	1.3129	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	72.7	0	Baseline	2020-01-15	Y	72.5	0.2	0.2788	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	74.31	4	Week 4	2020-02-15	Y	72.5	1.81	2.4996	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	74.85	12	Week 12	2020-04-15	Y	72.5	2.35	3.2444	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	90.25	0	Baseline	2020-01-15	Y	89.44	0.81	0.9053	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	89.51	4	Week 4	2020-02-15	Y	89.44	0.07	0.078	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	90.52	12	Week 12	2020-04-15	Y	89.44	1.08	1.2072	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.77	0	Baseline	2020-01-15	Y	101.15	0.62	0.6131	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.13	4	Week 4	2020-02-15	Y	101.15	-1.02	-1.0083	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.4	12	Week 12	2020-04-15	Y	101.15	1.25	1.2359	
... [15 more lines omitted]

### derivation.tsv (32 bytes)
derivation
AVAL
AVISITN
USUBJID

```

## Simple Prompt
```text
Create R script to perform slice derivation using the admiral clinical task contract.

Input: args.tsv, dataset.tsv, derivation.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### args.tsv (24 bytes)
arg
2020-01-15T08:30:00

### dataset.tsv (5930 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	97.16	0	Baseline	2020-01-15	Y	98.16	-1.0	-1.017	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	96.45	4	Week 4	2020-02-15	Y	98.16	-1.71	-1.7403	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.01	12	Week 12	2020-04-15	Y	98.16	-4.15	-4.2261	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	62.09	0	Baseline	2020-01-15	Y	60.69	1.4	2.2992	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	61.51	4	Week 4	2020-02-15	Y	60.69	0.82	1.3436	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	59.72	12	Week 12	2020-04-15	Y	60.69	-0.97	-1.6056	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	88.9	0	Baseline	2020-01-15	Y	91.98	-3.08	-3.3473	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	91.37	4	Week 4	2020-02-15	Y	91.98	-0.61	-0.6619	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	92.26	12	Week 12	2020-04-15	Y	91.98	0.28	0.3057	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.64	0	Baseline	2020-01-15	Y	95.79	-1.15	-1.1967	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	94.26	4	Week 4	2020-02-15	Y	95.79	-1.53	-1.5934	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	95.07	12	Week 12	2020-04-15	Y	95.79	-0.72	-0.7478	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	58.98	0	Baseline	2020-01-15	Y	61.46	-2.48	-4.0323	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	63.65	4	Week 4	2020-02-15	Y	61.46	2.19	3.5664	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	62.67	12	Week 12	2020-04-15	Y	61.46	1.21	1.9718	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	62.36	0	Baseline	2020-01-15	Y	61.92	0.44	0.7083	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	63.03	4	Week 4	2020-02-15	Y	61.92	1.11	1.7904	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	62.08	12	Week 12	2020-04-15	Y	61.92	0.16	0.2562	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.33	0	Baseline	2020-01-15	Y	125.94	0.39	0.3112	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.5	4	Week 4	2020-02-15	Y	125.94	4.56	3.6223	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.11	12	Week 12	2020-04-15	Y	125.94	0.17	0.1365	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	59.73	0	Baseline	2020-01-15	Y	61.71	-1.98	-3.215	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	60.63	4	Week 4	2020-02-15	Y	61.71	-1.08	-1.7567	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	61.52	12	Week 12	2020-04-15	Y	61.71	-0.19	-0.3145	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	83.63	0	Baseline	2020-01-15	Y	85.83	-2.2	-2.5622	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	90.56	4	Week 4	2020-02-15	Y	85.83	4.73	5.512	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	88.77	12	Week 12	2020-04-15	Y	85.83	2.94	3.4265	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.16	0	Baseline	2020-01-15	Y	110.36	0.8	0.7239	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	108.94	4	Week 4	2020-02-15	Y	110.36	-1.42	-1.2876	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.81	12	Week 12	2020-04-15	Y	110.36	1.45	1.3129	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	72.7	0	Baseline	2020-01-15	Y	72.5	0.2	0.2788	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	74.31	4	Week 4	2020-02-15	Y	72.5	1.81	2.4996	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	74.85	12	Week 12	2020-04-15	Y	72.5	2.35	3.2444	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	90.25	0	Baseline	2020-01-15	Y	89.44	0.81	0.9053	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	89.51	4	Week 4	2020-02-15	Y	89.44	0.07	0.078	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	90.52	12	Week 12	2020-04-15	Y	89.44	1.08	1.2072	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.77	0	Baseline	2020-01-15	Y	101.15	0.62	0.6131	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.13	4	Week 4	2020-02-15	Y	101.15	-1.02	-1.0083	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.4	12	Week 12	2020-04-15	Y	101.15	1.25	1.2359	
... [15 more lines omitted]

### derivation.tsv (32 bytes)
derivation
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(5, 4) vs llm=(18, 3) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(admiral))

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
args_path <- file.path("inputs", "args.tsv")
if (!file.exists(args_path)) {
  stop("args.tsv is required input")
}
args <- read.delim(args_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证
if (nrow(dataset) == 0) stop("dataset is empty")

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  admiral::slice_derivation(derivation = list(), dataset = dataset)
}, error = function(e) dataset)


# 4. 创建结果数据框 / Create result dataframe
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
  write.csv(summary_stats, file.path(ou
```

## Current Solution
```r
library(admiral)
library(dplyr)
library(readr)
library(purrr)
library(rlang)

#---------------------------
# Helper: robust file read
#---------------------------
safe_read_tsv <- function(path, ...) {
  res <- tryCatch(
    readr::read_tsv(path, show_col_types = FALSE, progress = FALSE, ...),
    error = function(e) {
      stop(paste0("Failed to read file '", path, "': ", conditionMessage(e)))
    }
  )
  if (!is.data.frame(res) || nrow(res) == 0L) {
    warning(paste0("File '", path, "' has zero rows or is not a data.frame."))
  }
  res
}

#---------------------------
# Read inputs
#---------------------------
dataset_path    <- file.path("inputs", "dataset.tsv")
derivation_path <- file.path("inputs", "derivation.tsv")
args_path       <- file.path("inputs", "args.tsv")

dataset_in  <- safe_read_tsv(dataset_path)
deriv_spec  <- safe_read_tsv(derivation_path)
args_spec   <- safe_read_tsv(args_path)

# Basic validation
req_cols_dataset <- c("USUBJID", "STUDYID", "PARAMCD", "PARAM", "AVAL",
                      "AVISITN", "AVISIT", "ADT")
missing_ds <- setdiff(req_cols_dataset, names(dataset_in))
if (length(missing_ds) > 0) {
  stop("Missing required columns in dataset.tsv: ", paste(missing_ds, collapse = ", "))
}

if (!"derivation" %in% names(deriv_spec)) {
  stop("derivation.tsv must contain a 'derivation' column.")
}
if (!"arg" %in% names(args_spec)) {
  stop("args.tsv must contain an 'arg' column.")
}

# Ensure ADT is Date
if (!inherits(dataset_in$ADT, "Date")) {
  dataset_in <- dataset_in %>%
    mutate(ADT = as.Date(ADT))
}

#---------------------------
# Build derivation function
#---------------------------
# Example "Derivation A": create a flag if ADT >= ref_date and keep only given columns
derivation_A <- function(dataset,
                         ref_date,
                         keep_vars) {
  if (!inherits(ref_date, "Date")) {
    stop("ref_date must be a Date object.")
  }
  if (!all(keep_vars %in% names(dataset))) {
    missing_k <- setdiff(keep_vars, names(dataset))
    stop("Some keep_vars are not in the dataset: ",
         paste(missing_k, collapse = ", "))
  }

  dataset %>%
    mutate(AFTER_REF = if_else(ADT >= ref_date, "Y", "N")) %>%
    select(all_of(unique(c(names(dataset), "AFTER_REF")))) %>%
    select(all_of(keep_vars), everything())
}

#---------------------------
# Global args from args.tsv
#---------------------------
# Assume first row of args.tsv is a reference datetime; use date component
global_ref_datetime <- args_spec$arg[1]
global_ref_date <- tryCatch(
  as.Date(global_ref_datetime),
  warning = function(w) NA,
  error   = function(e) NA
)

if (is.na(global_ref_date)) {
  stop("Could not parse global reference date from args.tsv: ", global_ref_datetime)
}

# Derivation columns from derivation.tsv
derivation_cols <- deriv_spec$derivation
if (anyNA(derivation_cols) || length(derivation_cols) == 0) {
  stop("derivation.tsv 'derivation' column must contain at least one non-NA value.")
}

# Global args object
global_args <- params(
  ref_date  = global_ref_date,
  keep_vars = derivation_cols
)

#---------------------------
# Define slices
#---------------------------
# Example slices with overlapping and empty subsets to exercise requirements

slices_list <- list(
  derivation_slice(
    filter = PARAMCD == "SYSBP",
    args   = params(
      keep_vars = c(derivation_cols, "PARAMCD", "PARAM")
    )
  ),
  derivation_slice(
    filter = PARAMCD == "DIABP" & AVISITN >= 4,
    args   = params(
      ref_date = global_ref_date + 30
    )
  ),
  derivation_slice(
    filter = PARAMCD == "PULSE" & AVISITN == 999, # intentionally no matches
    args   = params(
      keep_vars = c(derivation_cols, "PARAMCD")
    )
  )
)

#---------------------------
# Run slice_derivation
#---------------------------
result <- tryCatch(
  slice_derivation(
    dataset   = dataset_in,
    derivation = derivation_A,
    args       = global_args,
    slices     = slices_list
  ),
  error = function(e) {
    stop("slice_derivation failed: ", conditionMessage(e))
  }
)

#---------------------------
# Basic post-derivation checks
#---------------------------
if (!is.data.frame(result)) {
  stop("Result of slice_derivation is not a data.frame.")
}

if (!nrow(result) == nrow(dataset_in)) {
  warning("Number of rows changed after slice_derivation: ",
          "input = ", nrow(dataset_in), ", output = ", nrow(result))
}

# Check that all original rows are present (by key subset)
key_cols <- c("USUBJID", "STUDYID", "PARAMCD", "AVISITN", "ADT")
if (all(key_cols %in% names(dataset_in)) && all(key_cols %in% names(result))) {
  merged_check <- dataset_in %>%
    select(all_of(key_cols)) %>%
    mutate(.in_input = TRUE) %>%
    left_join(
      result %>%
        select(all_of(key_cols)) %>%
        mutate(.in_output = TRUE),
      by = key_cols
    )

  if (any(is.na(merged_check$.in_output))) {
    warning("Some input records were not found in the output based on key columns.")
  }
} else {
  warning("Key col
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(tidyr)
library(stringr)
library(purrr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
args_df <- readr::read_tsv(
  file = file.path("inputs", "args.tsv"),
  col_types = cols(.default = col_character())
)

dataset <- readr::read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols(.default = col_character())
)

derivation <- readr::read_tsv(
  file = file.path("inputs", "derivation.tsv"),
  col_types = cols(.default = col_character())
)

# Extract slice key from args (first data row of arg column)
slice_key <- args_df$arg[1]

# Convert date-like column ADT if present
if ("ADT" %in% names(dataset)) {
  suppressWarnings({
    dataset <- dataset %>%
      mutate(ADT = as.Date(ADT))
  })
}

# Generic clinical slice: filter rows whose ADT is on or before slice_key datetime (if possible)
slice_dt <- suppressWarnings(as.POSIXct(slice_key, tz = "UTC"))
if (!is.na(slice_dt) && "ADT" %in% names(dataset)) {
  # If ADT available, use it as date filter
  slice_date <- as.Date(slice_dt)
  dataset_slice <- dataset %>%
    filter(is.na(ADT) | ADT <= slice_date)
} else {
  # Fallback: no temporal slicing
  dataset_slice <- dataset
}

# Determine variables to keep from derivation contract
vars_to_keep <- intersect(derivation$derivation, names(dataset_slice))

# If none intersect, return empty with requested columns
if (length(vars_to_keep) == 0) {
  result <- tibble()
} else {
  result <- dataset_slice %>%
    select(all_of(vars_to_keep))
}

# Write result
readr::write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## Current Candidate Prompt File
```text
Write R code to execute a derivation with different arguments for subsets of the input dataset using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset.tsv, inputs/derivation.tsv, inputs/args.tsv). The input dataset is split into slices (subsets) and for each slice the derivation is called separately. Some or all arguments of the derivation may vary depending on the slice. Additional details: For each slice the derivation is called on the subset defined by the `filter` field of the `derivation_slice()` object and with the parameters specified by the `args` parameter and the `args` field of the `derivation_slice()` object. If a parameter is specified for both, the value in `derivation_slice()` overwrites the one in `args`. - Observations that match with more than one slice are only considered for the first matching slice. - The derivation is called for slices with no observations. - Observations with no match to any of the slices are included in the output dataset but the derivation is not called for them. It is also possible to pass functions from outside the `{admiral}` package to `slice_derivation()`, e.g. an extension package function, or `dplyr::mutate()`. The only requirement for a function being passed to `derivation` is that it must take a dataset as its first argument and return a dataset. Use admiral's slice_derivation function with the following parameters: dataset (`r roxygen_param_dataset()`), derivation (Derivation A function that performs a specific derivation is expected.), args (Arguments of the derivation A `params()` object is expected.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with the variables derived by the derivation added. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to execute a derivation with different arguments for subsets of the input dataset using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/dataset.tsv, inputs/derivation.tsv, inputs/args.tsv). The input dataset is split into slices (subsets) and for each slice the derivation is called separately. Some or all arguments of the derivation may vary depending on the slice. Additional details: For each slice the derivation is called on the subset defined by the `filter` field of the `derivation_slice()` object and with the parameters specified by the `args` parameter and the `args` field of the `derivation_slice()` object. If a parameter is specified for both, the value in `derivation_slice()` overwrites the one in `args`. - Observations that match with more than one slice are only considered for the first matching slice. - The derivation is called for slices with no observations. - Observations with no match to any of the slices are included in the output dataset but the derivation is not called for them. It is also possible to pass functions from outside the `{admiral}` package to `slice_derivation()`, e.g. an extension package function, or `dplyr::mutate()`. The only requirement for a function being passed to `derivation` is that it must take a dataset as its first argument and return a dataset. Use admiral's slice_derivation function with the following parameters: dataset (`r roxygen_param_dataset()`), derivation (Derivation A function that performs a specific derivation is expected.), args (Arguments of the derivation A `params()` object is expected.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with the variables derived by the derivation added. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```