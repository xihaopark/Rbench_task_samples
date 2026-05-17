# Case 46 - `pharmaverse/aNCA/calculate_f`

**Package:** `aNCA`  **Function:** `calculate_f`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `NO_OUTPUT` / tier `exec_fail`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `high`

## Audit Evidence

Reference prompt/solution require coercing `res_nca` to `PKNCAresults` and calling `pknca_calculate_f(res_nca, f_aucs)`. Current/simple prompt asks for a public `calculate_f` routine and only lists `result.csv`, so generated code calls the wrong API or performs a column intersection.

## Task Prompt From `task.json`

```text
Compute **f** statistics for PKNCA results. Load `library(aNCA)` and `library(dplyr)`.

**Inputs:** `inputs/res_nca.tsv`, `inputs/f_aucs.tsv`. Coerce `res_nca` to **PKNCAresults** if needed. Extract numeric vector `f_aucs` from `f_aucs.tsv`.

**Computation:** Call **`pknca_calculate_f(res_nca, f_aucs)`**, then shape outputs (e.g. `pivot_wider_pknca_results`, `mutate`, `select`) as needed to match required artifacts. Do **not** assume a single exported wrapper named exactly the required functionality is the whole solution.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for calculate f. The available input files are `inputs/f_aucs.tsv`, `inputs/res_nca.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `calculate_f`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### f_aucs.tsv (28 bytes)
f_aucs
AVAL
AVISITN
USUBJID

### res_nca.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform calculate f using the aNCA clinical task contract.

Input: f_aucs.tsv, res_nca.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### f_aucs.tsv (28 bytes)
f_aucs
AVAL
AVISITN
USUBJID

### res_nca.tsv (24 bytes)
id
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`f_aucs.tsv`**

```tsv
f_aucs
"test_value"

```

**`res_nca.tsv`**

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
""

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
0,0,""

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(aNCA))
suppressPackageStartupMessages(library(dplyr))

# 1. 读取输入数据 / Read input data
res_nca_path <- file.path("inputs", "res_nca.tsv")
if (!file.exists(res_nca_path)) {
  stop("res_nca.tsv is required input")
}
res_nca <- read.delim(res_nca_path, check.names = FALSE, stringsAsFactors = FALSE)
f_aucs_path <- file.path("inputs", "f_aucs.tsv")
if (!file.exists(f_aucs_path)) {
  stop("f_aucs.tsv is required input")
}
f_aucs_df <- read.delim(f_aucs_path, check.names = FALSE, stringsAsFactors = FALSE)
f_aucs <- f_aucs_df$f_aucs

# 2. 数据验证 / Data validation
# res_nca需要是PKNCAresults对象，如果只是数据框则创建模拟对象
if (!inherits(res_nca, "PKNCAresults")) {
  # 创建模拟的PKNCAresults对象结构
  res_nca <- list(result = res_nca)
  class(res_nca) <- "PKNCAresults"
}

# 3. 执行函数实现 / Execute function implementation
pknca_result <- tryCatch({
  pknca_calculate_f(res_nca, f_aucs)
}, warning = function(w) {
  warning(w$message)
  NULL
}, error = function(e) {
  stop(e$message)
})

if (is.null(pknca_result) || nrow(pknca_result) == 0) {
  # 如果没有结果，创建一个空的数据框
  result <- data.frame()
} else {
  res_nca$result <- pknca_result %>%
    mutate(PPSTRESU = "")
  result <- pivot_wider_pknca_results(res_nca) %>%
    select(any_of(c(
      names(PKNCA::getGroups(res_nca)),
      "end",
      paste0(f_aucs),
      "Exclude"
    )))
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

# 6. 保存输出 / Save outputs
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

## Current Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(aNCA)      # assumes calculate_f is exported from aNCA
  library(readr)
  library(dplyr)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper: read TSV with header preservation
read_tsv_file <- function(path) {
  readr::read_tsv(
    file = path,
    col_types = readr::cols(.default = readr::col_character())
  )
}

# Helper: treat one-row tables as scalars when appropriate
# (return vector of appropriate type; keep data.frame if >1 row)
collapse_if_scalar <- function(df) {
  if (!is.data.frame(df)) return(df)
  if (nrow(df) == 1L && ncol(df) == 1L) {
    # Single cell -> scalar
    return(df[[1]][1])
  }
  df
}

# Read inputs
f_aucs_df  <- read_tsv_file("inputs/f_aucs.tsv")
res_nca_df <- read_tsv_file("inputs/res_nca.tsv")

# Convert single-cell tables to scalar when appropriate
f_aucs_arg  <- collapse_if_scalar(f_aucs_df)
res_nca_arg <- collapse_if_scalar(res_nca_df)

# Call calculate_f with TSV-derived arguments.
# Adjust argument names here if calculate_f expects different names.
result <- calculate_f(
  f_aucs  = f_aucs_arg,
  res_nca = res_nca_arg
)

# Normalize result for grading:
# - convert to data.frame if needed
# - keep row alignment
norm_result <-
  if (is.data.frame(result)) {
    result
  } else if (is.vector(result) || is.factor(result)) {
    tibble::tibble(value = result)
  } else if (is.list(result)) {
    # Try to coerce to tibble/data.frame row-wise
    tryCatch(
      tibble::as_tibble(result),
      error = function(e) tibble::tibble(value = I(list(result)))
    )
  } else {
    tibble::tibble(value = result)
  }

# Make CSV output compact and inspectable:
# - avoid list-columns when possible
# - ensure character representation for complex types
norm_result_compact <- norm_result

for (cn in names(norm_result_compact)) {
  col <- norm_result_compact[[cn]]
  if (is.list(col)) {
    norm_result_compact[[cn]] <- vapply(
      col,
      function(x) {
        if (is.atomic(x) && length(x) == 1L) {
          as.character(x)
        } else {
          paste(capture.output(str(x, give.attr = FALSE)), collapse = "; ")
        }
      },
      character(1)
    )
  }
}

# Write full result object as RDS
saveRDS(result, file = "outputs/result.rds")

# Write normalized compact CSV
readr::write_csv(norm_result_compact, file = "outputs/result.csv", na = "")
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
Error in UseMethod("mutate") : 
  no applicable method for 'mutate' applied to an object of class "NULL"
Calls: calculate_f -> %>% -> mutate
In addition: Warning messages:
1: Unknown or uninitialised column: `result`. 
2: In pknca_calculate_f(res_nca, f_aucs) :
  No AUC extracted from f_aucs available in res_nca (PPTESTCD): c("AVAL", "AVISITN", "USUBJID")
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

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Directories
in_dir  <- "inputs"
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Read input files
f_aucs_path  <- file.path(in_dir, "f_aucs.tsv")
res_nca_path <- file.path(in_dir, "res_nca.tsv")

f_aucs  <- read_tsv(f_aucs_path, col_types = cols(.default = col_character()))
res_nca <- read_tsv(res_nca_path, col_types = cols(.default = col_character()))

# Select common columns between res_nca and f_aucs header
common_cols <- intersect(names(res_nca), names(f_aucs))
result <- res_nca %>% select(all_of(common_cols))

# Write output
out_path <- file.path(out_dir, "result.csv")
write_csv(result, out_path)
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

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/calculate_f",
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
  "task_id": "pharmaverse/aNCA/calculate_f",
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
      "reason": "Comparison error: No columns to parse from file"
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
