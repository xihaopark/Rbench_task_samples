# Case 023: pharmaverse/aNCA/format_unit_string

## Case Metadata

- Task ID: `pharmaverse/aNCA/format_unit_string`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform format unit string using the aNCA clinical task contract.

Input: data.tsv, unit_var.tsv
Output: result.csv


Required columns for result.csv: id, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (53 bytes)
id	conc	concu
1	10.5	ng/mL
2	20.3	ng/mL
3	30.7	ng/mL

### unit_var.tsv (15 bytes)
unit_var
concu
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/format_unit_string/inputs/data.tsv`
- Size: 53 bytes

```text
id	conc	concu
1	10.5	ng/mL
2	20.3	ng/mL
3	30.7	ng/mL
```

### `unit_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/format_unit_string/inputs/unit_var.tsv`
- Size: 15 bytes

```text
unit_var
concu
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/format_unit_string/solution.R`
- Size: 2890 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)

suppressPackageStartupMessages(library(dplyr))

# 1. 读取输入数据 / Read input data
data_path <- file.path("inputs", "data.tsv")
if (!file.exists(data_path)) {
  stop("data.tsv is required input")
}
data <- read.delim(data_path, check.names = FALSE, stringsAsFactors = FALSE)
unit_var_path <- file.path("inputs", "unit_var.tsv")
if (!file.exists(unit_var_path)) {
  stop("unit_var.tsv is required input")
}
unit_var_df <- read.delim(unit_var_path, check.names = FALSE, stringsAsFactors = FALSE)
unit_var <- if (ncol(unit_var_df) > 0 && nrow(unit_var_df) > 0) {
  unit_var_df[[1]][1]
} else {
  NULL
}

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

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
result <- tryCatch({
  if (!has_aNCA) stop("aNCA unavailable")
  aNCA:::format_unit_string(data = data, unit_var = unit_var)
}, error = function(e) {
  # 如果函数不存在或失败，手动实现逻辑
  if (is.null(unit_var) || !unit_var %in% names(data)) {
    ""
  } else {
    distinct_units <- unique(data[[unit_var]])
    if (length(distinct_units) == 1) {
      paste0(" (", distinct_units[1], ")")
    } else {
      ""
    }
  }
})

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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/format_unit_string/outputs/result.csv`
- Size: 27 bytes

```csv
"id","result"
1," (ng/mL)"
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
data_path <- file.path("inputs", "data.tsv")
unit_var_path <- file.path("inputs", "unit_var.tsv")

dat <- read_tsv(data_path, show_col_types = FALSE)
unit_var <- read_tsv(unit_var_path, show_col_types = FALSE)

# Get unit variable name(s)
unit_cols <- unit_var$unit_var

# Function to format unit string according to aNCA clinical task contract
format_unit <- function(x) {
  # Example implementation: normalize spacing around slash and per-symbol
  # Adjust as needed to fully comply with the contract specification.
  x <- trimws(x)
  x <- gsub("\\s*/\\s*", "/", x)
  x <- gsub("\\s+per\\s+", "/", x, ignore.case = TRUE)
  x
}

# Apply formatting
dat_formatted <- dat %>%
  mutate(across(all_of(unit_cols), format_unit))

# Prepare result: id + formatted unit string(s) collapsed if multiple
if (length(unit_cols) == 1) {
  res <- dat_formatted %>%
    transmute(
      id = .data[["id"]],
      result = .data[[unit_cols]]
    )
} else {
  res <- dat_formatted %>%
    mutate(result = do.call(
      paste,
      c(across(all_of(unit_cols)), sep = " ")
    )) %>%
    select(id, result)
}

# Write output
write_csv(res, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__format_unit_string/sample_00/case_01/llm_outputs/result.csv`
- Size: 34 bytes

```csv
id,result
1,ng/mL
2,ng/mL
3,ng/mL
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__format_unit_string/sample_00/case_01/stderr.txt`
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
  "failure_stage": "schema_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "schema_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "schema_mismatch",
          "reason": "Shape mismatch: ref=(1, 2) vs llm=(3, 2)"
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
            "stage": "schema_mismatch",
            "tier": "output_bad",
            "reason": "Shape mismatch: ref=(1, 2) vs llm=(3, 2)"
          }
        }
      }
    }
  ]
}
```
