# Sample 24: pharmaverse/aNCA/translate_terms

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/translate_terms`
- package/function: `aNCA` / `translate_terms`
- expected_artifacts: `outputs/result.csv`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
```text
Write R code to map free-text terms using a metadata table. Load `library(aNCA)` and `library(purrr)`.

**Inputs:** `inputs/input_terms.tsv`, `inputs/mapping_col.tsv`, `inputs/target_col.tsv`, `inputs/metadata.tsv` — build `input_terms`, scalar column names `mapping_col` / `target_col`, and `metadata` data.frame.

**Computation:** Call **`aNCA:::translate_terms(input_terms=, mapping_col=, target_col=, metadata=)`** (internal; not exported as `aNCA::translate_terms`).

**Outputs:** The reference also writes `outputs/summary.csv`.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.

```

## Current Prompt
```text
I am preparing an aNCA clinical pharmacokinetic support task for translate terms. The available input files are `inputs/input_terms.tsv`, `inputs/mapping_col.tsv`, `inputs/metadata.tsv`, `inputs/target_col.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `translate_terms`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### input_terms.tsv (33 bytes)
input_terms
AVAL
AVISITN
USUBJID

### mapping_col.tsv (33 bytes)
mapping_col
AVAL
AVISITN
USUBJID

### metadata.tsv (5939 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	128.19	0	Baseline	2020-01-15	Y	127.23	0.96	0.7565	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.46	4	Week 4	2020-02-15	Y	127.23	0.23	0.1827	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.23	12	Week 12	2020-04-15	Y	127.23	-4.0	-3.1421	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	75.56	0	Baseline	2020-01-15	Y	75.91	-0.35	-0.4631	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	75.14	4	Week 4	2020-02-15	Y	75.91	-0.77	-1.0163	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	76.38	12	Week 12	2020-04-15	Y	75.91	0.47	0.6171	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	74.63	0	Baseline	2020-01-15	Y	74.7	-0.07	-0.0905	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	71.53	4	Week 4	2020-02-15	Y	74.7	-3.17	-4.2406	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	73.47	12	Week 12	2020-04-15	Y	74.7	-1.23	-1.6435	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.41	0	Baseline	2020-01-15	Y	117.17	1.24	1.0603	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	115.29	4	Week 4	2020-02-15	Y	117.17	-1.88	-1.6025	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.64	12	Week 12	2020-04-15	Y	117.17	-2.53	-2.1573	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	77.16	0	Baseline	2020-01-15	Y	75.1	2.06	2.7364	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	77.52	4	Week 4	2020-02-15	Y	75.1	2.42	3.2157	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	75.76	12	Week 12	2020-04-15	Y	75.1	0.66	0.8723	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	102.78	0	Baseline	2020-01-15	Y	99.7	3.08	3.0903	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	101.94	4	Week 4	2020-02-15	Y	99.7	2.24	2.2478	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	99.82	12	Week 12	2020-04-15	Y	99.7	0.12	0.1214	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.9	0	Baseline	2020-01-15	Y	114.65	0.25	0.2158	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	116.93	4	Week 4	2020-02-15	Y	114.65	2.28	1.9863	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	116.4	12	Week 12	2020-04-15	Y	114.65	1.75	1.5241	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	64.75	0	Baseline	2020-01-15	Y	64.64	0.11	0.1651	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	62.96	4	Week 4	2020-02-15	Y	64.64	-1.68	-2.6039	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	63.12	12	Week 12	2020-04-15	Y	64.64	-1.52	-2.3564	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	77.65	0	Baseline	2020-01-15	Y	73.37	4.28	5.8303	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	75.35	4	Week 4	2020-02-15	Y	73.37	1.98	2.6956	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	74.98	12	Week 12	2020-04-15	Y	73.37	1.61	2.1913	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.95	0	Baseline	2020-01-15	Y	127.31	3.64	2.8582	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.92	4	Week 4	2020-02-15	Y	127.31	0.61	0.4782	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.24	12	Week 12	2020-04-15	Y	127.31	2.93	2.3005	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	75.07	0	Baseline	2020-01-15	Y	74.06	1.01	1.3703	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	73.78	4	Week 4	2020-02-15	Y	74.06	-0.28	-0.3716	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	75.88	12	Week 12	2020-04-15	Y	74.06	1.82	2.4641	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	70.98	0	Baseline	2020-01-15	Y	71.61	-0.63	-0.8808	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	72.26	4	Week 4	2020-02-15	Y	71.61	0.65	0.9067	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	63.97	12	Week 12	2020-04-15	Y	71.61	-7.64	-10.6698	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	129.17	0	Baseline	2020-01-15	Y	128.51	0.66	0.5132	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	128.83	4	Week 4	2020-02-15	Y	128.51	0.32	0.2487	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.05	12	Week 12	2020-04-15	Y	128.51	-2.46	-1.9146	
... [15 more lines omitted]

### target_col.tsv (24 bytes)
arg
2020-01-15T08:30:00

```

## Simple Prompt
```text
Create R script to perform translate terms using the aNCA clinical task contract.

Input: input_terms.tsv, mapping_col.tsv, metadata.tsv, target_col.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### input_terms.tsv (33 bytes)
input_terms
AVAL
AVISITN
USUBJID

### mapping_col.tsv (33 bytes)
mapping_col
AVAL
AVISITN
USUBJID

### metadata.tsv (5939 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	128.19	0	Baseline	2020-01-15	Y	127.23	0.96	0.7565	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.46	4	Week 4	2020-02-15	Y	127.23	0.23	0.1827	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.23	12	Week 12	2020-04-15	Y	127.23	-4.0	-3.1421	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	75.56	0	Baseline	2020-01-15	Y	75.91	-0.35	-0.4631	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	75.14	4	Week 4	2020-02-15	Y	75.91	-0.77	-1.0163	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	76.38	12	Week 12	2020-04-15	Y	75.91	0.47	0.6171	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	74.63	0	Baseline	2020-01-15	Y	74.7	-0.07	-0.0905	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	71.53	4	Week 4	2020-02-15	Y	74.7	-3.17	-4.2406	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	73.47	12	Week 12	2020-04-15	Y	74.7	-1.23	-1.6435	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.41	0	Baseline	2020-01-15	Y	117.17	1.24	1.0603	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	115.29	4	Week 4	2020-02-15	Y	117.17	-1.88	-1.6025	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.64	12	Week 12	2020-04-15	Y	117.17	-2.53	-2.1573	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	77.16	0	Baseline	2020-01-15	Y	75.1	2.06	2.7364	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	77.52	4	Week 4	2020-02-15	Y	75.1	2.42	3.2157	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	75.76	12	Week 12	2020-04-15	Y	75.1	0.66	0.8723	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	102.78	0	Baseline	2020-01-15	Y	99.7	3.08	3.0903	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	101.94	4	Week 4	2020-02-15	Y	99.7	2.24	2.2478	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	99.82	12	Week 12	2020-04-15	Y	99.7	0.12	0.1214	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	114.9	0	Baseline	2020-01-15	Y	114.65	0.25	0.2158	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	116.93	4	Week 4	2020-02-15	Y	114.65	2.28	1.9863	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	116.4	12	Week 12	2020-04-15	Y	114.65	1.75	1.5241	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	64.75	0	Baseline	2020-01-15	Y	64.64	0.11	0.1651	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	62.96	4	Week 4	2020-02-15	Y	64.64	-1.68	-2.6039	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	63.12	12	Week 12	2020-04-15	Y	64.64	-1.52	-2.3564	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	77.65	0	Baseline	2020-01-15	Y	73.37	4.28	5.8303	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	75.35	4	Week 4	2020-02-15	Y	73.37	1.98	2.6956	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	74.98	12	Week 12	2020-04-15	Y	73.37	1.61	2.1913	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.95	0	Baseline	2020-01-15	Y	127.31	3.64	2.8582	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	127.92	4	Week 4	2020-02-15	Y	127.31	0.61	0.4782	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.24	12	Week 12	2020-04-15	Y	127.31	2.93	2.3005	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	75.07	0	Baseline	2020-01-15	Y	74.06	1.01	1.3703	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	73.78	4	Week 4	2020-02-15	Y	74.06	-0.28	-0.3716	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	75.88	12	Week 12	2020-04-15	Y	74.06	1.82	2.4641	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	70.98	0	Baseline	2020-01-15	Y	71.61	-0.63	-0.8808	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	72.26	4	Week 4	2020-02-15	Y	71.61	0.65	0.9067	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	63.97	12	Week 12	2020-04-15	Y	71.61	-7.64	-10.6698	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	129.17	0	Baseline	2020-01-15	Y	128.51	0.66	0.5132	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	128.83	4	Week 4	2020-02-15	Y	128.51	0.32	0.2487	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	126.05	12	Week 12	2020-04-15	Y	128.51	-2.46	-1.9146	
... [15 more lines omitted]

### target_col.tsv (24 bytes)
arg
2020-01-15T08:30:00

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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(0, 1) vs llm=(1, 1) | summary.csv: match=False reason=File not generated"
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
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(0, 1) vs llm=(3, 5) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(aNCA))
suppressPackageStartupMessages(library(purrr))


# 1. 读取输入数据 / Read input data
input_terms_path <- file.path("inputs", "input_terms.tsv")
if (!file.exists(input_terms_path)) {
  stop("input_terms.tsv is required input")
}
input_terms_df <- read.delim(input_terms_path, check.names = FALSE, stringsAsFactors = FALSE)
input_terms <- input_terms_df$input_terms
mapping_col_path <- file.path("inputs", "mapping_col.tsv")
if (!file.exists(mapping_col_path)) {
  stop("mapping_col.tsv is required input")
}
mapping_col_df <- read.delim(mapping_col_path, check.names = FALSE, stringsAsFactors = FALSE)
mapping_col <- mapping_col_df$mapping_col
target_col_path <- file.path("inputs", "target_col.tsv")
if (!file.exists(target_col_path)) {
  stop("target_col.tsv is required input")
}
target_col_df <- read.delim(target_col_path, check.names = FALSE, stringsAsFactors = FALSE)
target_col <- target_col_df$target_col
metadata_path <- file.path("inputs", "metadata.tsv")
if (!file.exists(metadata_path)) {
  stop("metadata.tsv is required input")
}
metadata <- read.delim(metadata_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("metadata")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
    if (ncol(df) == 0) {
      stop(paste("Data frame", df_name, "has no columns"))
    }
}

# 3. 执行函数实现 / Execute function implementation
# 提取标量参数
if (is.data.frame(mapping_col) && ncol(mapping_col) > 0 && nrow(mapping_col) > 0) {
  mapping_col <- mapping_col[[1]][1]
} else if (is.character(mapping_col)) {
  mapping_col <- mapping_col[1]
}
if (is.data.frame(target_col) && ncol(target_col) > 0 && nrow(target_col) > 0) {
  target_col <- target_col[[1]][1]
} else if (is.character(target_col)) {
  target_col <- target_col[1]
}

result <- tryCatch({
  aNCA:::translate_terms(
    input_terms = input_terms,
    mapping_col = mapping_col,
    target_col = target_col,
    metadata = metadata
  )
}, error = function(e) {
  # 如果函数调用失败，返回NULL
  NULL
})


# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    input_terms = input_terms, mapping_col = mapping_col,
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
    max_value = max(result, na.rm
```

## Current Solution
```r
#!/usr/bin/env Rscript

# aNCA translate_terms support script

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Load aNCA package (adjust if namespace differs)
suppressPackageStartupMessages({
  library(aNCA)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

#-----------------------
# Read inputs
#-----------------------

# input_terms.tsv: vector of input terms
input_terms_df <- read_tsv(
  "inputs/input_terms.tsv",
  col_types = cols(.default = col_character())
)
input_terms <- input_terms_df[[1]]

# mapping_col.tsv: vector of mapping columns
mapping_col_df <- read_tsv(
  "inputs/mapping_col.tsv",
  col_types = cols(.default = col_character())
)
mapping_col <- mapping_col_df[[1]]

# metadata.tsv: main metadata table
metadata <- read_tsv(
  "inputs/metadata.tsv",
  col_types = cols(.default = col_character())
)

# target_col.tsv: scalar or vector argument
target_col_df <- read_tsv(
  "inputs/target_col.tsv",
  col_types = cols(.default = col_character())
)
# Treat one-row table (excluding header) as scalar; otherwise vector
if (nrow(target_col_df) == 1L) {
  target_col <- target_col_df[[1]][1]
} else {
  target_col <- target_col_df[[1]]
}

#-----------------------
# Call translate_terms
#-----------------------

res <- translate_terms(
  input_terms   = input_terms,
  mapping_col   = mapping_col,
  metadata      = metadata,
  target_col    = target_col
)

#-----------------------
# Normalize result
#-----------------------

# For grading, create a compact, inspectable CSV.
# If result is not a data.frame, coerce to tibble first.
res_tbl <-
  if (is.data.frame(res)) {
    as_tibble(res)
  } else if (is.vector(res) && !is.list(res)) {
    tibble::tibble(value = res)
  } else {
    # For lists or other structures, flatten to character
    tibble::tibble(value = I(list(res)))
  }

#-----------------------
# Write outputs
#-----------------------

# Full object as RDS (if required by harness)
saveRDS(res, file = "outputs/result.rds")

# Compact CSV for grading
write_csv(res_tbl, "outputs/result.csv")
```

## Simple Solution
```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(tidyr)
})

in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

input_terms_path <- file.path(in_dir, "input_terms.tsv")
mapping_col_path <- file.path(in_dir, "mapping_col.tsv")
metadata_path    <- file.path(in_dir, "metadata.tsv")
target_col_path  <- file.path(in_dir, "target_col.tsv")

input_terms <- read_tsv(input_terms_path, show_col_types = FALSE)
mapping_col <- read_tsv(mapping_col_path, show_col_types = FALSE)
metadata    <- read_tsv(metadata_path, show_col_types = FALSE)
target_col  <- read_tsv(target_col_path, show_col_types = FALSE)

terms <- input_terms[[1]]
mapping_vars <- mapping_col[[1]]

# For this task, we assume that terms refer to column names in metadata
available_cols <- colnames(metadata)

result <- tibble(
  input_term   = terms,
  mapped_col   = ifelse(terms %in% mapping_vars, terms, NA_character_),
  exists_in_metadata = terms %in% available_cols
)

# Attach simple metadata about each mapped column if present
meta_info <- tibble(
  mapped_col = intersect(result$mapped_col, available_cols)
) %>%
  mutate(
    example_value = purrr::map_chr(
      mapped_col,
      ~ as.character(metadata[[.x]][[1]])
    )
  )

result_final <- result %>%
  left_join(meta_info, by = "mapped_col") %>%
  mutate(
    translation_status = case_when(
      is.na(mapped_col) ~ "not_mapped",
      !exists_in_metadata ~ "mapped_missing_in_metadata",
      TRUE ~ "mapped"
    )
  )

write_csv(result_final, file.path(out_dir, "result.csv"))
```

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for translate terms. The available input files are `inputs/input_terms.tsv`, `inputs/mapping_col.tsv`, `inputs/metadata.tsv`, `inputs/target_col.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `translate_terms`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for translate terms. The available input files are `inputs/input_terms.tsv`, `inputs/mapping_col.tsv`, `inputs/metadata.tsv`, `inputs/target_col.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `translate_terms`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```