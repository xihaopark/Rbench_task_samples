# Case 050: pharmaverse/aNCA/translate_terms

## Case Metadata

- Task ID: `pharmaverse/aNCA/translate_terms`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform translate terms using the aNCA clinical task contract.

Input: input_terms.tsv, mapping_col.tsv, metadata.tsv, target_col.tsv
Output: result.csv


Required columns for result.csv: input_terms, mapping_col, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### input_terms.tsv (25 bytes)
input_terms
AVAL
PARAMCD

### mapping_col.tsv (21 bytes)
mapping_col
Variable

### metadata.tsv (77 bytes)
Variable	Label
AVAL	Analysis Value
PARAMCD	Parameter Code
USUBJID	Subject ID

### target_col.tsv (17 bytes)
target_col
Label
```

## Input Data

### `input_terms.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/translate_terms/inputs/input_terms.tsv`
- Size: 25 bytes

```text
input_terms
AVAL
PARAMCD
```

### `mapping_col.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/translate_terms/inputs/mapping_col.tsv`
- Size: 21 bytes

```text
mapping_col
Variable
```

### `metadata.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/translate_terms/inputs/metadata.tsv`
- Size: 77 bytes

```text
Variable	Label
AVAL	Analysis Value
PARAMCD	Parameter Code
USUBJID	Subject ID
```

### `target_col.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/translate_terms/inputs/target_col.tsv`
- Size: 17 bytes

```text
target_col
Label
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/translate_terms/solution.R`
- Size: 3631 bytes

```r
has_aNCA <- requireNamespace("aNCA", quietly = TRUE)
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
  if (!has_aNCA) stop("aNCA unavailable")
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
# 6. 保存输出 / Save outputs
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

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/translate_terms/outputs/result.csv`
- Size: 110 bytes

```csv
"input_terms","mapping_col","result"
"AVAL","Variable","Analysis Value"
"PARAMCD","Variable","Parameter Code"
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

# Read input files
input_terms <- read_tsv("inputs/input_terms.tsv", show_col_types = FALSE)
mapping_col <- read_tsv("inputs/mapping_col.tsv", show_col_types = FALSE)
metadata    <- read_tsv("inputs/metadata.tsv", show_col_types = FALSE)
target_col  <- read_tsv("inputs/target_col.tsv", show_col_types = FALSE)

# Extract column names
map_col_name    <- mapping_col$mapping_col[1]
target_col_name <- target_col$target_col[1]

# Check columns exist in metadata
if (!map_col_name %in% names(metadata)) {
  stop(paste("Mapping column", map_col_name, "not found in metadata"))
}
if (!target_col_name %in% names(metadata)) {
  stop(paste("Target column", target_col_name, "not found in metadata"))
}

# Perform translation
result <- input_terms %>%
  left_join(
    metadata %>%
      select(all_of(map_col_name), all_of(target_col_name)),
    by = setNames(map_col_name, "input_terms")
  ) %>%
  transmute(
    input_terms = input_terms,
    mapping_col = .data[[map_col_name]],
    result      = .data[[target_col_name]]
  )

# Write output
write_csv(result, "outputs/result.csv", na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__translate_terms/sample_00/case_01/stderr.txt`
- Size: 1942 bytes

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
Error in `transmute()`:
ℹ In argument: `mapping_col = .data[["Variable"]]`.
Caused by error in `.data[["Variable"]]`:
! Column `Variable` not found in `.data`.
Backtrace:
     ▆
  1. ├─... %>% ...
  2. ├─dplyr::transmute(...)
  3. ├─dplyr:::transmute.data.frame(...)
  4. │ └─dplyr:::mutate_cols(.data, dots, by)
  5. │   ├─base::withCallingHandlers(...)
  6. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  7. │     └─mask$eval_all_mutate(quo)
  8. │       └─dplyr (local) eval()
  9. ├─Variable
 10. ├─rlang:::`[[.rlang_data_pronoun`(.data, "Variable")
 11. │ └─rlang:::data_pronoun_get(...)
 12. └─rlang:::abort_data_pronoun(x, call = y)
 13.   └─rlang::abort(msg, "rlang_error_data_pronoun_not_found", call = call)
Execution halted
```

## Evaluation Result

```json
{
  "status": "NO_OUTPUT",
  "failure_stage": "execution_failure",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "tier": "exec_fail",
      "failure_stage": "execution_failure",
      "message": "No output files created",
      "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
      "returncode": 1,
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [],
        "missing_artifacts": [
          "result.csv"
        ]
      }
    }
  ]
}
```
