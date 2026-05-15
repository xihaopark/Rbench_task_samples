# Case 08 - `pharmaverse/admiral/default_qtc_paramcd`
**Package:** `admiral`  **Function:** `default_qtc_paramcd`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to implement the **Default qtc paramcd** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/method.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'method.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Default Qtc Paramcd** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Input Files

**`inputs/method.tsv`**

```tsv
method
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(admiraldev))

# Read input data
method_path <- file.path("inputs", "method.tsv")
if (!file.exists(method_path)) {
  stop("method.tsv is required input")
}
method <- read.delim(method_path, check.names = FALSE, stringsAsFactors = FALSE)

# Data validation
if (nrow(method) == 0 || ncol(method) == 0) {
  stop("method is empty or has no columns")
}

# Execute function implementation
method_val <- trimws(as.character(method[[1]][1]))
method_val <- switch(tolower(method_val),
  "bazett" = "Bazett", "fridericia" = "Fridericia", "sagie" = "Sagie",
  "Bazett")
admiraldev::assert_character_scalar(method_val, values = c("Bazett", "Fridericia", "Sagie"))
paramcd_map <- c(Bazett = "QTCBR", Fridericia = "QTCFR", Sagie = "QTLCR")
result <- paramcd_map[[method_val]]

# Create result dataframe
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

# Generate summary statistics
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

# Save outputs
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
```

## Reference Output

**`outputs/result.csv`**

```csv
"id","result"
1,"QTCBR"
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"id, result"
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

method <- read.delim(
  file.path("inputs", "method.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

args_list <- list()

if ("aval" %in% names(method)) {
  args_list$aval <- method[["aval"]]
}
if ("aval2" %in% names(method)) {
  args_list$aval2 <- method[["aval2"]]
}
if ("aval3" %in% names(method)) {
  args_list$aval3 <- method[["aval3"]]
}
if ("aval4" %in% names(method)) {
  args_list$aval4 <- method[["aval4"]]
}
if ("analysis_type" %in% names(method)) {
  args_list$analysis_type <- method[["analysis_type"]]
}
if ("analysis_var" %in% names(method)) {
  args_list$analysis_var <- method[["analysis_var"]]
}
if ("analysis_var2" %in% names(method)) {
  args_list$analysis_var2 <- method[["analysis_var2"]]
}
if ("analysis_var3" %in% names(method)) {
  args_list$analysis_var3 <- method[["analysis_var3"]]
}
if ("analysis_var4" %in% names(method)) {
  args_list$analysis_var4 <- method[["analysis_var4"]]
}
if ("by_vars" %in% names(method)) {
  bv <- method[["by_vars"]]
  bv <- unique(bv[!is.na(bv) & nzchar(bv)])
  if (length(bv) > 0) {
    args_list$by_vars <- syms(bv)
  }
}
if ("method" %in% names(method)) {
  args_list$method <- method[["method"]]
}
if ("rounding" %in% names(method)) {
  args_list$rounding <- method[["rounding"]]
}
if ("decimals" %in% names(method)) {
  args_list$decimals <- method[["decimals"]]
}
if ("unit" %in% names(method)) {
  args_list$unit <- method[["unit"]]
}
if ("paramcd" %in% names(method)) {
  args_list$paramcd <- method[["paramcd"]]
}
if ("param" %in% names(method)) {
  args_list$param <- method[["param"]]
}

result <- do.call(admiral::default_qtc_paramcd, args_list)

write.csv(result, file = file.path("outputs", "result.csv"), row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error:
! Argument `method` must be equal to one of "Bazett", "Fridericia", or
  "Sagie".
Backtrace:
    ▆
 1. ├─base::do.call(admiral::default_qtc_paramcd, args_list)
 2. └─admiral (local) `<fn>`(method = "test_value")
 3.   └─admiraldev::assert_character_scalar(...)
 4.     └─cli::cli_abort(...)
 5.       └─rlang::abort(...)
Execution halted
```

## LLM Output Files

_No files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/default_qtc_paramcd",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "6e3d5418ddf3c2f2c53a96f456d906cd812869d26c6dc5a81bd96f2283a059d9",
  "raw_response": "```r\nlibrary(admiral)\n\ndir.create(\"outputs\", showWarnings = FALSE)\n\nmethod <- read.delim(\n  file.path(\"inputs\", \"method.tsv\"),\n  check.names = FALSE,\n  stringsAsFactors = FALSE\n)\n\nargs_list <- list()\n\nif (\"aval\" %in% names(method)) {\n  args_list$aval <- method[[\"aval\"]]\n}\nif (\"aval2\" %in% names(method)) {\n  args_list$aval2 <- method[[\"aval2\"]]\n}\nif (\"aval3\" %in% names(method)) {\n  args_list$aval3 <- method[[\"aval3\"]]\n}\nif (\"aval4\" %in% names(method)) {\n  args_list$aval4 <- method[[\"aval4\"]]\n}\nif (\"analysis_type\" %in% names(method)) {\n  args_list$analysis_type <- method[[\"analysis_type\"]]\n}\nif (\"analysis_var\" %in% names(method)) {\n  args_list$analysis_var <- method[[\"analysis_var\"]]\n}\nif (\"analysis_var2\" %in% names(method)) {\n  args_list$analysis_var2 <- method[[\"analysis_var2\"]]\n}\nif (\"analysis_var3\" %in% names(method)) {\n  args_list$analysis_var3 <- method[[\"analysis_var3\"]]\n}\nif (\"analysis_var4\" %in% names(method)) {\n  args_list$analysis_var4 <- method[[\"analysis_var4\"]]\n}\nif (\"by_vars\" %in% names(method)) {\n  bv <- method[[\"by_vars\"]]\n  bv <- unique(bv[!is.na(bv) & nzchar(bv)])\n  if (length(bv) > 0) {\n    args_list$by_vars <- syms(bv)\n  }\n}\nif (\"method\" %in% names(method)) {\n  args_list$method <- method[[\"method\"]]\n}\nif (\"rounding\" %in% names(method)) {\n  args_list$rounding <- method[[\"rounding\"]]\n}\nif (\"decimals\" %in% names(method)) {\n  args_list$decimals <- method[[\"decimals\"]]\n}\nif (\"unit\" %in% names(method)) {\n  args_list$unit <- method[[\"unit\"]]\n}\nif (\"paramcd\" %in% names(method)) {\n  args_list$paramcd <- method[[\"paramcd\"]]\n}\nif (\"param\" %in% names(method)) {\n  args_list$param <- method[[\"param\"]]\n}\n\nresult <- do.call(admiral::default_qtc_paramcd, args_list)\n\nwrite.csv(result, file = file.path(\"outputs\", \"result.csv\"), row.names = FALSE)\n```",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:12:31.964576",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/default_qtc_paramcd",
  "sample_idx": 0,
  "model": "openai/gpt-5.1",
  "status": "NO_OUTPUT",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "message": "No output files created",
      "stderr": "Error:\n! Argument `method` must be equal to one of \"Bazett\", \"Fridericia\", or\n  \"Sagie\".\nBacktrace:\n    ▆\n 1. ├─base::do.call(admiral::default_qtc_paramcd, args_list)\n 2. └─admiral (local) `<fn>`(method = \"test_value\")\n 3.   └─admiraldev::assert_character_scalar(...)\n 4.     └─cli::cli_abort(...)\n 5.       └─rlang::abort(...)\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
