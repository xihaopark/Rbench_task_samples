# Case 05 - `pharmaverse/admiral/compute_rr`
**Package:** `admiral`  **Function:** `compute_rr`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Convert heart rate (bpm) to **RR interval (ms)** for ECG-style derivations. Load `library(admiral)`.

**Inputs:** `inputs/hr.tsv` with one numeric column named `hr`.

**Computation:** Read the `hr` vector and call `admiral::compute_rr(hr)`.

**Required outputs for grading (exact paths):**
- `outputs/result.csv` with columns `hr`, `result`
- `outputs/summary.csv` with columns `n_rows`, `n_cols`, `col_names`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` and write CSV with `write.csv(..., row.names=FALSE)`.
```

## Prompt Repair Note

This display prompt lightly clarifies the output schema and includes `summary.csv`, because the reference output and evaluator compare both files. The computation and inputs are unchanged from the stable task.

## Input Files

**`inputs/hr.tsv`**

```tsv
hr
0.1
1.5
10.0
100.0
1000.0
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

suppressPackageStartupMessages(library(rlang))
# Read input data
hr_path <- file.path("inputs", "hr.tsv")
if (!file.exists(hr_path)) {
  stop("hr.tsv is required input")
}
hr_df <- read.delim(hr_path, check.names = FALSE, stringsAsFactors = FALSE)
hr <- as.numeric(hr_df$hr)

# Execute function implementation
hr_path <- file.path("inputs", "hr.tsv")
if (!file.exists(hr_path)) {
  stop("hr.tsv is required input")
}
hr_df <- read.delim(hr_path, check.names = FALSE, stringsAsFactors = FALSE)
hr <- if(ncol(hr_df) > 0 && nrow(hr_df) > 0) hr_df[[1]] else hr_df
result <- admiral::compute_rr(hr)

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    hr = hr,
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
"hr","result"
0.1,6e+05
1.5,40000
10,6000
100,600
1000,60
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"hr, result"
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

hr <- read.delim("inputs/hr.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)

rr <- admiral::compute_rr(hr[[1]])

result <- data.frame(
  HR = hr[[1]],
  RR = rr
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
"HR","RR"
0.1,6e+05
1.5,40000
10,6000
100,600
1000,60
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/compute_rr",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "e0f3d9508ecee536ae65e14c9928ab0ef3640dc9143c6e2def0c9443bfba13ab",
  "raw_response": "```r\nlibrary(admiral)\n\ndir.create(\"outputs\", showWarnings = FALSE)\n\nhr <- read.delim(\"inputs/hr.tsv\", header = TRUE, sep = \"\\t\", stringsAsFactors = FALSE)\n\nrr <- admiral::compute_rr(hr[[1]])\n\nresult <- data.frame(\n  HR = hr[[1]],\n  RR = rr\n)\n\nwrite.csv(result, \"outputs/result.csv\", row.names = FALSE)\n```",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:11:42.441506",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/compute_rr",
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
          "reason": "Missing column: hr"
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
