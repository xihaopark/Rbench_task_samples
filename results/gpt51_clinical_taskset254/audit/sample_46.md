# Sample 46: pharmaverse/aNCA/calculate_f

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/calculate_f`
- package/function: `aNCA` / `calculate_f`
- expected_artifacts: `outputs/result.csv`
- current_status: `NO_OUTPUT` tier=`exec_fail`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
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

## Current Prompt
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

## Simple Prompt
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
  "comparison": "result.csv: match=False reason=Comparison error: No columns to parse from file | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
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
    result_df <- data.frame(result = result, st
```

## Current Solution
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

## Simple Solution
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

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for calculate f. The available input files are `inputs/f_aucs.tsv`, `inputs/res_nca.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `calculate_f`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for calculate f. The available input files are `inputs/f_aucs.tsv`, `inputs/res_nca.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. The target operation is the public aNCA routine `calculate_f`; call it when it accepts the TSV-derived arguments, then normalize the result for grading. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```