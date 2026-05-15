# Case 03 - `pharmaverse/admiral/compute_qtc`
**Package:** `admiral`  **Function:** `compute_qtc`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to compute **heart-rate-corrected QT (QTc)** from QT and RR intervals. Load `library(admiral)` and `library(admiraldev)`.

**Inputs:** `inputs/qt.tsv`, `inputs/rr.tsv`, `inputs/method.tsv`. `qt.tsv` has a numeric `qt` column and `rr.tsv` has a numeric `rr` column. The method should be read from the first cell of `method.tsv`; if it is not one of `bazett`, `fridericia`, or `sagie` after lower-casing, default to `bazett`, matching the reference.

**Computation:** Apply `admiraldev::assert_numeric_vector` to `qt` and `rr`, normalize `rr` in ms, and compute exactly one vector named `result` using the reference formulas:
- Bazett: `qt / sqrt(rr / 1000)`
- Fridericia: `qt / (rr / 1000)^(1 / 3)`
- Sagie: `1000 * (qt / 1000 + 0.154 * (1 - rr / 1000))`

**Required outputs for grading (exact paths):**
- `outputs/result.csv` with columns `qt`, `rr`, `result`
- `outputs/summary.csv` with columns `n_rows`, `n_cols`, `col_names`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` and write CSV with `write.csv(..., row.names=FALSE)`.
```

## Prompt Repair Note

This display prompt lightly clarifies the output schema and includes `summary.csv`, because the reference output and evaluator compare both files. The computation and inputs are unchanged from the stable task.

## Input Files

**`inputs/method.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/qt.tsv`**

```tsv
qt
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/rr.tsv`**

```tsv
rr
0.1
1.5
10.0
100.0
1000.0
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(admiraldev))
suppressPackageStartupMessages(library(rlang))
# Read input data
qt_path <- file.path("inputs", "qt.tsv")
if (!file.exists(qt_path)) {
  stop("qt.tsv is required input")
}
qt_df <- read.delim(qt_path, check.names = FALSE, stringsAsFactors = FALSE)
qt <- as.numeric(qt_df$qt)
rr_path <- file.path("inputs", "rr.tsv")
if (!file.exists(rr_path)) {
  stop("rr.tsv is required input")
}
rr_df <- read.delim(rr_path, check.names = FALSE, stringsAsFactors = FALSE)
rr <- as.numeric(rr_df$rr)
method_path <- file.path("inputs", "method.tsv")
if (!file.exists(method_path)) {
  stop("method.tsv is required input")
}
method <- read.delim(method_path, check.names = FALSE, stringsAsFactors = FALSE)

if (nrow(method) == 0) stop("method is empty")

# Execute function implementation
admiraldev::assert_numeric_vector(arg = qt)
admiraldev::assert_numeric_vector(arg = rr)
method_val <- tolower(as.character(method[[1]][1]))
valid_methods <- c("bazett", "fridericia", "sagie")
if (length(method_val) == 0 || is.na(method_val) || !method_val %in% valid_methods) method_val <- "bazett"
method_val <- paste0(toupper(substring(method_val, 1, 1)), substring(method_val, 2))
formulae <- list(
  Bazett = qt / sqrt(rr / 1000),
  Fridericia = qt / (rr / 1000)^(1 / 3),
  Sagie = 1000 * (qt / 1000 + 0.154 * (1 - rr / 1000))
)
result <- formulae[[method_val]]

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    qt = qt, rr = rr,
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
"qt","rr","result"
0.1,0.1,10
1.5,1.5,38.7298334620742
10,10,100
100,100,316.227766016838
1000,1000,1000
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"qt, rr, result"
```

## LLM Code

```r
library(admiral)
library(admiraldev)

dir.create("outputs", showWarnings = FALSE)

qt_df <- read.table("inputs/qt.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
rr_df <- read.table("inputs/rr.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
method_df <- read.table("inputs/method.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)

qt <- qt_df$qt
rr <- rr_df$rr

admiraldev::assert_numeric_vector(qt)
admiraldev::assert_numeric_vector(rr)

method <- if ("method" %in% names(method_df)) method_df$method[1] else NA
method <- tolower(method)

if (!method %in% c("bazett", "fridericia", "sagie")) {
  method <- "bazett"
}

rr_sec <- rr / 1000

qtc <- switch(
  method,
  "bazett" = qt / sqrt(rr_sec),
  "fridericia" = qt / (rr_sec^(1/3)),
  "sagie" = qt + 0.154 * (1 - rr_sec),
  qt / sqrt(rr_sec)
)

result <- data.frame(
  qt = qt,
  rr = rr,
  method = method,
  qtc = qtc
)

write.csv(result, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"qt","rr","method","qtc"
0.1,0.1,"bazett",10
1.5,1.5,"bazett",38.7298334620742
10,10,"bazett",100
100,100,"bazett",316.227766016838
1000,1000,"bazett",1000
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/compute_qtc",
  "sample_idx": 0,
  "model": "openai/gpt-5.1",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "comparison": {
        "result.csv": {
          "match": false,
          "reason": "Shape mismatch: ref=(5, 3) vs llm=(5, 4)"
        },
        "summary.csv": {
          "match": false,
          "reason": "File not generated"
        }
      },
      "returncode": 0,
      "normalizations": []
    }
  ]
}
```
