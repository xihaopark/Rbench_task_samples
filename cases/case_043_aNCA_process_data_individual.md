# Case 043: pharmaverse/aNCA/process_data_individual

## Case Metadata

- Task ID: `pharmaverse/aNCA/process_data_individual`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform process data individual using the aNCA clinical task contract.

Input: conc_col.tsv, filtering_list.tsv, pknca_data.tsv, show_dose.tsv, use_time_since_last_dose.tsv, ylog_scale.tsv
Output: result.csv


Required columns for result.csv: USUBJID, ARM, TIME, CONC, DOSE, PARAM, ROUTE, TSLD, BLQFL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### conc_col.tsv (14 bytes)
conc_col
CONC

### filtering_list.tsv (26 bytes)
variable	value
ARM	100 mg

### pknca_data.tsv (328 bytes)
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
... [3 more lines omitted]

### show_dose.tsv (15 bytes)
show_dose
TRUE

### use_time_since_last_dose.tsv (31 bytes)
use_time_since_last_dose
FALSE

### ylog_scale.tsv (17 bytes)
ylog_scale
FALSE
```

## Input Data

### `conc_col.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/inputs/conc_col.tsv`
- Size: 14 bytes

```text
conc_col
CONC
```

### `filtering_list.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/inputs/filtering_list.tsv`
- Size: 26 bytes

```text
variable	value
ARM	100 mg
```

### `pknca_data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/inputs/pknca_data.tsv`
- Size: 328 bytes

```text
USUBJID	ARM	TIME	CONC	DOSE	PARAM	ROUTE	TSLD	BLQFL
101	100 mg	0	0.0	100	AUC	oral	0	Y
101	100 mg	1	34.2	100	AUC	oral	1	N
101	100 mg	2	61.5	100	AUC	oral	2	N
101	100 mg	4	38.1	100	AUC	oral	4	N
102	100 mg	0	0.0	100	AUC	oral	0	Y
102	100 mg	1	29.8	100	AUC	oral	1	N
102	100 mg	2	55.4	100	AUC	oral	2	N
102	100 mg	4	33.6	100	AUC	oral	4	N
```

### `show_dose.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/inputs/show_dose.tsv`
- Size: 15 bytes

```text
show_dose
TRUE
```

### `use_time_since_last_dose.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/inputs/use_time_since_last_dose.tsv`
- Size: 31 bytes

```text
use_time_since_last_dose
FALSE
```

### `ylog_scale.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/inputs/ylog_scale.tsv`
- Size: 17 bytes

```text
ylog_scale
FALSE
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/solution.R`
- Size: 4562 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

# 1. 读取输入数据 / Read input data
pknca_data_path <- file.path("inputs", "pknca_data.tsv")
if (!file.exists(pknca_data_path)) {
  stop("pknca_data.tsv is required input")
}
pknca_data <- read.delim(pknca_data_path, check.names = FALSE, stringsAsFactors = FALSE)
filtering_list_path <- file.path("inputs", "filtering_list.tsv")
if (!file.exists(filtering_list_path)) {
  stop("filtering_list.tsv is required input")
}
filtering_list <- read.delim(filtering_list_path, check.names = FALSE, stringsAsFactors = FALSE)
ylog_scale_path <- file.path("inputs", "ylog_scale.tsv")
if (!file.exists(ylog_scale_path)) {
  stop("ylog_scale.tsv is required input")
}
ylog_scale_df <- read.delim(ylog_scale_path, check.names = FALSE, stringsAsFactors = FALSE)
ylog_scale <- as.logical(ylog_scale_df$ylog_scale)
conc_col_path <- file.path("inputs", "conc_col.tsv")
if (!file.exists(conc_col_path)) {
  stop("conc_col.tsv is required input")
}
conc_col <- read.delim(conc_col_path, check.names = FALSE, stringsAsFactors = FALSE)
show_dose_path <- file.path("inputs", "show_dose.tsv")
if (!file.exists(show_dose_path)) {
  stop("show_dose.tsv is required input")
}
show_dose_df <- read.delim(show_dose_path, check.names = FALSE, stringsAsFactors = FALSE)
show_dose <- as.logical(show_dose_df$show_dose)
use_time_since_last_dose_path <- file.path("inputs", "use_time_since_last_dose.tsv")
if (!file.exists(use_time_since_last_dose_path)) {
  stop("use_time_since_last_dose.tsv is required input")
}
use_time_since_last_dose_df <- read.delim(use_time_since_last_dose_path, check.names = FALSE, stringsAsFactors = FALSE)
use_time_since_last_dose <- as.logical(use_time_since_last_dose_df$use_time_since_last_dose)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证
if (nrow(pknca_data) == 0) stop("pknca_data is empty")

# 3. 执行函数实现 / Execute function implementation
conc_col_val <- if (ncol(conc_col) > 0) conc_col[[1]][1] else names(pknca_data)[1]
result <- tryCatch({
  if (!has_aNCA) stop("aNCA unavailable")
  aNCA::process_data_individual(
    pknca_data = pknca_data,
    filtering_list = filtering_list,
    ylog_scale = ylog_scale,
    show_dose = show_dose,
    use_time_since_last_dose = use_time_since_last_dose,
    conc_col = conc_col_val
  )
}, error = function(e) pknca_data)
if (is.null(result) || (is.list(result) && !is.data.frame(result))) result <- pknca_data


# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    ylog_scale = ylog_scale, show_dose = show_dose,
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
unlink(file.path(outputs_dir, "summary.csv"))
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
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/process_data_individual/outputs/result.csv`
- Size: 406 bytes

```csv
"USUBJID","ARM","TIME","CONC","DOSE","PARAM","ROUTE","TSLD","BLQFL"
101,"100 mg",0,0,100,"AUC","oral",0,"Y"
101,"100 mg",1,34.2,100,"AUC","oral",1,"N"
101,"100 mg",2,61.5,100,"AUC","oral",2,"N"
101,"100 mg",4,38.1,100,"AUC","oral",4,"N"
102,"100 mg",0,0,100,"AUC","oral",0,"Y"
102,"100 mg",1,29.8,100,"AUC","oral",1,"N"
102,"100 mg",2,55.4,100,"AUC","oral",2,"N"
102,"100 mg",4,33.6,100,"AUC","oral",4,"N"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
conc_col <- fread("inputs/conc_col.tsv", header = TRUE, sep = "\t")[[1]]
filtering_list <- fread("inputs/filtering_list.tsv", header = TRUE, sep = "\t")
pknca_data <- fread("inputs/pknca_data.tsv", header = TRUE, sep = "\t")
show_dose <- fread("inputs/show_dose.tsv", header = TRUE, sep = "\t")[[1]]
use_tsld <- fread("inputs/use_time_since_last_dose.tsv", header = TRUE, sep = "\t")[[1]]
ylog_scale <- fread("inputs/ylog_scale.tsv", header = TRUE, sep = "\t")[[1]]

# Apply filtering_list (only equality filters assumed)
if (nrow(filtering_list) > 0) {
  for (i in seq_len(nrow(filtering_list))) {
    var <- filtering_list$variable[i]
    val <- filtering_list$value[i]
    if (var %in% names(pknca_data)) {
      pknca_data <- pknca_data[get(var) == val]
    }
  }
}

# Ensure required columns exist; select and order them
required_cols <- c("USUBJID", "ARM", "TIME", conc_col, "DOSE", "PARAM", "ROUTE", "TSLD", "BLQFL")

# Rename concentration column to CONC if different
if (conc_col != "CONC" && conc_col %in% names(pknca_data)) {
  setnames(pknca_data, conc_col, "CONC")
}

# After renaming, adjust required columns vector to use CONC
required_cols[required_cols == conc_col] <- "CONC"

# Keep only required columns that exist; missing ones will be created as NA
existing_cols <- intersect(required_cols, names(pknca_data))
result <- pknca_data[, ..existing_cols]

missing_cols <- setdiff(required_cols, names(result))
if (length(missing_cols) > 0) {
  for (mc in missing_cols) {
    result[, (mc) := NA]
  }
}

# Reorder columns
setcolorder(result, required_cols)

# Write output
fwrite(result, file = "outputs/result.csv", sep = ",", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__process_data_individual/sample_00/case_01/llm_outputs/result.csv`
- Size: 324 bytes

```csv
USUBJID,ARM,TIME,CONC,DOSE,PARAM,ROUTE,TSLD,BLQFL
101,100 mg,0,0,100,AUC,oral,0,Y
101,100 mg,1,34.2,100,AUC,oral,1,N
101,100 mg,2,61.5,100,AUC,oral,2,N
101,100 mg,4,38.1,100,AUC,oral,4,N
102,100 mg,0,0,100,AUC,oral,0,Y
102,100 mg,1,29.8,100,AUC,oral,1,N
102,100 mg,2,55.4,100,AUC,oral,2,N
102,100 mg,4,33.6,100,AUC,oral,4,N
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__process_data_individual/sample_00/case_01/stderr.txt`
- Size: 1123 bytes

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

## Evaluation Result

```json
{
  "status": "PASS",
  "failure_stage": "pass",
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "tier": "pass",
      "tier_value": "pass",
      "failure_stage": "pass",
      "comparison": {
        "result.csv": {
          "match": true,
          "tier": "pass",
          "failure_stage": "pass"
        }
      },
      "returncode": 0,
      "normalizations": [],
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [
          "result.csv"
        ],
        "staged_artifacts": [
          "result.csv"
        ],
        "missing_artifacts": [],
        "extra_artifacts": [],
        "comparison_reasons": {}
      }
    }
  ]
}
```
