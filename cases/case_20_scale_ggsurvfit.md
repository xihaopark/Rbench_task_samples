# Case 20 - `pharmaverse/ggsurvfit/scale_ggsurvfit`
**Package:** `ggsurvfit`  **Function:** `scale_ggsurvfit`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_01`  **Evaluation status:** `PASS`, pass=`True`, score=`1.0`
## Task Prompt

```text
Write R code to build a `ggsurvfit::scale_ggsurvfit()` scale object using the `ggsurvfit` package.
At the beginning, load: library(ggsurvfit).

**Inputs:**
- `inputs/x_scales.tsv` and `inputs/y_scales.tsv`: each has a header row; the **first cell of the first data row** (column 1) must contain a valid R expression that evaluates to a **named list** of arguments for `ggplot2::scale_x_continuous()` / `scale_y_continuous()` (for example `list(expand = c(0.015, 0), n.breaks = 8)`). Read with read.delim(..., check.names=FALSE, stringsAsFactors=FALSE), take `txt <- trimws(as.character(df[[1]][1]))`, then `eval(parse(text = txt))` to obtain each list.

**Required output:**
- `outputs/result.csv`: a one-row summary table with at least one column describing the returned object (for example `scale_classes` = paste(class(result), collapse='|')) after calling `ggsurvfit::scale_ggsurvfit(x_scales = ..., y_scales = ...)`.

Create `outputs/` with dir.create('outputs', showWarnings=FALSE). Use write.csv(..., row.names=FALSE).
```

## Input Files

**`inputs/x_scales.tsv`**

```tsv
expr
list(expand = c(0.015, 0), n.breaks = 8)
```

**`inputs/y_scales.tsv`**

```tsv
expr
list(expand = c(0.025, 0), limits = c(0, 1))
```

## Reference Code

```r
suppressPackageStartupMessages(library(ggsurvfit))

parse_scale_list <- function(fname) {
  path <- file.path("inputs", fname)
  if (!file.exists(path)) {
    stop(fname, " is required input")
  }
  df <- read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
  txt <- trimws(as.character(df[[1]][1]))
  if (!nzchar(txt) || identical(txt, "NA")) {
    return(list())
  }
  ev <- eval(parse(text = txt))
  if (!is.list(ev)) {
    stop("First data cell in ", fname, " must evaluate to an R list of scale_* arguments.")
  }
  ev
}

x_scales <- parse_scale_list("x_scales.tsv")
y_scales <- parse_scale_list("y_scales.tsv")

result <- ggsurvfit::scale_ggsurvfit(x_scales = x_scales, y_scales = y_scales)

outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)

result_df <- data.frame(
  scale_classes = paste(class(result), collapse = "|"),
  stringsAsFactors = FALSE
)
write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"scale_classes"
"scale_ggsurvfit"
```

## LLM Code

```r
library(ggsurvfit)

dir.create("outputs", showWarnings = FALSE)

# Read x_scales
x_df <- read.delim("inputs/x_scales.tsv", check.names = FALSE, stringsAsFactors = FALSE)
x_txt <- trimws(as.character(x_df[[1]][1]))
x_scales_list <- eval(parse(text = x_txt))

# Read y_scales
y_df <- read.delim("inputs/y_scales.tsv", check.names = FALSE, stringsAsFactors = FALSE)
y_txt <- trimws(as.character(y_df[[1]][1]))
y_scales_list <- eval(parse(text = y_txt))

# Build scale_ggsurvfit object
scale_obj <- ggsurvfit::scale_ggsurvfit(
  x_scales = x_scales_list,
  y_scales = y_scales_list
)

# Summarize result
result_summary <- data.frame(
  scale_classes = paste(class(scale_obj), collapse = "|"),
  stringsAsFactors = FALSE
)

write.csv(result_summary, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text
Loading required package: ggplot2
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"scale_classes"
"scale_ggsurvfit"
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/ggsurvfit/scale_ggsurvfit",
  "package": "ggsurvfit",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "report",
  "scoring_mode_id": "strict",
  "code_sha256": "dcaf4f9b623b79f3568544a97cdd495ad60185ede7ff287010f6323c186ac001",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:15:47.104837",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/ggsurvfit/scale_ggsurvfit",
  "sample_idx": 1,
  "model": "openai/gpt-5.1",
  "status": "PASS",
  "pass": true,
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "comparison": {
        "result.csv": {
          "match": true
        }
      },
      "returncode": 0,
      "normalizations": []
    }
  ]
}
```
