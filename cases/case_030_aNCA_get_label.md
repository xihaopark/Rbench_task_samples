# Case 030: pharmaverse/aNCA/get_label

## Case Metadata

- Task ID: `pharmaverse/aNCA/get_label`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform get label using the aNCA clinical task contract.

Input: labels_df.tsv, type.tsv, variable.tsv
Output: result.csv


Required columns for result.csv: id, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### labels_df.tsv (100 bytes)
Dataset	Variable	Label
ADPC	AVAL	Analysis Value
ADPC	PARAMCD	Parameter Code
ADPC	USUBJID	Subject ID

### type.tsv (10 bytes)
type
ADPC

### variable.tsv (22 bytes)
variable
AVAL
PARAMCD
```

## Input Data

### `labels_df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_label/inputs/labels_df.tsv`
- Size: 100 bytes

```text
Dataset	Variable	Label
ADPC	AVAL	Analysis Value
ADPC	PARAMCD	Parameter Code
ADPC	USUBJID	Subject ID
```

### `type.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_label/inputs/type.tsv`
- Size: 10 bytes

```text
type
ADPC
```

### `variable.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_label/inputs/variable.tsv`
- Size: 22 bytes

```text
variable
AVAL
PARAMCD
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_label/solution.R`
- Size: 4548 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

# 1. 读取输入数据 / Read input data
variable_path <- file.path("inputs", "variable.tsv")
if (!file.exists(variable_path)) {
  stop("variable.tsv is required input")
}
variable <- read.delim(variable_path, check.names = FALSE, stringsAsFactors = FALSE)
type_path <- file.path("inputs", "type.tsv")
if (!file.exists(type_path)) {
  stop("type.tsv is required input")
}
type <- read.delim(type_path, check.names = FALSE, stringsAsFactors = FALSE)
labels_df_path <- file.path("inputs", "labels_df.tsv")
if (!file.exists(labels_df_path)) {
  stop("labels_df.tsv is required input")
}
labels_df <- read.delim(labels_df_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("variable", "labels_df")) {
  df <- get(df_name)
  if (is.data.frame(df)) {
    if (nrow(df) == 0) {
      stop(paste("Data frame", df_name, "is empty"))
    }
    if (ncol(df) == 0) {
      stop(paste("Data frame", df_name, "has no columns"))
    }
  }
}

# 提取type参数
if (is.data.frame(type) && ncol(type) > 0 && nrow(type) > 0) {
  type <- type[[1]][1]
} else if (is.character(type)) {
  type <- type[1]
}

# 提取variable参数
if (is.data.frame(variable) && ncol(variable) > 0 && nrow(variable) > 0) {
  variable <- variable[[1]]
} else if (is.character(variable) || is.factor(variable)) {
  variable <- as.character(variable)
}

# 3. 执行函数实现 / Execute function implementation
suppressPackageStartupMessages(library(dplyr))
if (is.null(labels_df) || (is.data.frame(labels_df) && nrow(labels_df) == 0)) {
  result <- variable
} else {
  result <- tryCatch({
    if (!has_aNCA) stop("aNCA unavailable")
    aNCA:::get_label(variable = variable, type = type, labels_df = labels_df)
  }, error = function(e) {
    # 如果函数不存在，使用translate_terms
    if (exists("translate_terms") && is.data.frame(labels_df) && "Dataset" %in% names(labels_df)) {
      filtered_labels <- dplyr::filter(labels_df, Dataset == type)
      if (nrow(filtered_labels) > 0 && "Variable" %in% names(filtered_labels) && "Label" %in% names(filtered_labels)) {
        translate_terms(
          variable,
          "Variable",
          "Label",
          metadata = filtered_labels
        )
      } else {
        variable
      }
    } else {
      variable
    }
  })
}

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
unlink(file.path(outputs_dir, c("result.rds", "summary.csv")))
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/get_label/outputs/result.csv`
- Size: 52 bytes

```csv
"id","result"
1,"Analysis Value"
2,"Parameter Code"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
labels_df <- read_tsv(
  file = file.path("inputs", "labels_df.tsv"),
  show_col_types = FALSE
)

type_df <- read_tsv(
  file = file.path("inputs", "type.tsv"),
  show_col_types = FALSE
)

variable_df <- read_tsv(
  file = file.path("inputs", "variable.tsv"),
  show_col_types = FALSE
)

# Extract type and variable values
types <- unique(type_df$type)
variables <- unique(variable_df$variable)

# Filter labels_df by requested type(s) and variable(s)
result_df <- labels_df %>%
  filter(Dataset %in% types,
         Variable %in% variables) %>%
  transmute(
    id = Variable,
    result = Label
  )

# Write output
write_csv(result_df, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__get_label/sample_00/case_01/llm_outputs/result.csv`
- Size: 53 bytes

```csv
id,result
AVAL,Analysis Value
PARAMCD,Parameter Code
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__get_label/sample_00/case_01/stderr.txt`
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
  "status": "FAIL",
  "failure_stage": "value_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "schema_ok",
      "tier_value": "schema_ok",
      "failure_stage": "value_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "schema_ok",
          "failure_stage": "value_mismatch",
          "reason": "Numeric missingness mismatch in column: id"
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
        "comparison_reasons": {
          "result.csv": {
            "stage": "value_mismatch",
            "tier": "schema_ok",
            "reason": "Numeric missingness mismatch in column: id"
          }
        }
      }
    }
  ]
}
```
