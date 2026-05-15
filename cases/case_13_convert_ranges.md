# Case 13 - `pharmaverse/admiral/convert_ranges`
**Package:** `admiral`  **Function:** `convert_ranges`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Fill in **numeric timepoint hours** for ADaM `xxtpt`-style strings that describe **hour ranges** (e.g. windows relative to infusion). Load `library(admiral)`, `library(dplyr)`, and `library(stringr)`.

**Inputs:** `inputs/xxtpt.tsv`, `inputs/result.tsv` (initial numeric `result` column), `inputs/na_idx.tsv` (logical mask), `inputs/range_method.tsv` (`start` / `end` / `midpoint`).

**Computation:** The reference does **not** call a single `convert_ranges` export: it uses **`stringr::str_match`** with two documented regex patterns, then **`admiral::calculate_range_value(start, end, range_method)`** to get a positive span, and applies sign rules for “prior/before” vs “post/after” directions. Only update positions where `result` is `NA` and `na_idx` is false, as in `solution.R`.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.

The reference may also write `outputs/summary.csv` for diagnostics; follow the same layout as `solution.R` when present.
```

## Input Files

**`inputs/may.tsv`**

```tsv
may
"test_value"
```

**`inputs/midpoint.tsv`**

```tsv
midpoint
"yes"
"no"
"true"
"false"
"active"
```

**`inputs/na_idx.tsv`**

```tsv
na_idx
FALSE
```

**`inputs/no.tsv`**

```tsv
no
"test_value"
```

**`inputs/range_method.tsv`**

```tsv
range_method
"test_value"
```

**`inputs/result.tsv`**

```tsv
result
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/xxtpt.tsv`**

```tsv
xxtpt
"item1"
"item2"
"item3"
"item4"
"item5"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(stringr))
suppressPackageStartupMessages(library(dplyr))

# Read input data
xxtpt_path <- file.path("inputs", "xxtpt.tsv")
if (!file.exists(xxtpt_path)) {
  stop("xxtpt.tsv is required input")
}
xxtpt_df <- read.delim(xxtpt_path, check.names = FALSE, stringsAsFactors = FALSE)
xxtpt <- xxtpt_df$xxtpt
result_path <- file.path("inputs", "result.tsv")
if (!file.exists(result_path)) {
  stop("result.tsv is required input")
}
result_df <- read.delim(result_path, check.names = FALSE, stringsAsFactors = FALSE)
result <- as.numeric(result_df$result)
na_idx_path <- file.path("inputs", "na_idx.tsv")
if (!file.exists(na_idx_path)) {
  stop("na_idx.tsv is required input")
}
na_idx_df <- read.delim(na_idx_path, check.names = FALSE, stringsAsFactors = FALSE)
na_idx <- as.logical(na_idx_df$na_idx)
range_method_path <- file.path("inputs", "range_method.tsv")
if (!file.exists(range_method_path)) {
  stop("range_method.tsv is required input")
}
range_method <- read.delim(range_method_path, check.names = FALSE, stringsAsFactors = FALSE)

# Data validation
if (nrow(range_method) == 0 || ncol(range_method) == 0) {
  stop("range_method is empty or has no columns")
}
range_method_val <- as.character(range_method[[1]][1])

# Execute function implementation
range_dir_pattern <- stringr::regex(
  paste0(
    "^(?<start>\\d+(?:\\.\\d+)?)\\s*-\\s*(?<end>\\d+(?:\\.\\d+)?)\\s*",
    "h(?:r|our)?s?\\s+",
    "(?<direction>prior|before|post|after)\\s+",
    "(?:start|end)(?:\\s+of\\s+(?:infusion|treatment))?"
  ),
  ignore_case = TRUE
)
range_dir_matches <- stringr::str_match(xxtpt, range_dir_pattern)
range_dir_idx <- !is.na(range_dir_matches[, 1]) & is.na(result) & !na_idx
if (any(range_dir_idx)) {
  start_val <- as.numeric(range_dir_matches[range_dir_idx, "start"])
  end_val <- as.numeric(range_dir_matches[range_dir_idx, "end"])
  direction <- tolower(range_dir_matches[range_dir_idx, "direction"])
  range_val <- admiral::calculate_range_value(start_val, end_val, range_method_val)
  result[range_dir_idx] <- dplyr::if_else(
    direction %in% c("prior", "before"),
    -range_val,
    range_val
  )
}
range_pattern <- stringr::regex(
  paste0(
    "^(?<start>\\d+(?:\\.\\d+)?)\\s*-\\s*(?<end>\\d+(?:\\.\\d+)?)\\s*",
    "h(?:r|our)?s?(?:\\s+(?:post|after)(?:\\s*-?\\s*dose)?)?$"
  ),
  ignore_case = TRUE,
  comments = TRUE
)
range_matches <- stringr::str_match(xxtpt, range_pattern)
range_idx <- !is.na(range_matches[, 1]) & is.na(result) & !na_idx
if (any(range_idx)) {
  start_val <- as.numeric(range_matches[range_idx, "start"])
  end_val <- as.numeric(range_matches[range_idx, "end"])
  result[range_idx] <- admiral::calculate_range_value(start_val, end_val, range_method_val)
}

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    xxtpt = xxtpt, result = result,
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
"xxtpt","result"
"item1",0.1
"item2",1.5
"item3",10
"item4",100
"item5",1000
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"xxtpt, result"
```

## LLM Code

```r
library(admiral)
library(dplyr)
library(stringr)

dir.create("outputs", showWarnings = FALSE)

xxtpt <- read.delim("inputs/xxtpt.tsv", sep = "\t", stringsAsFactors = FALSE)
res_df <- read.delim("inputs/result.tsv", sep = "\t", stringsAsFactors = FALSE)
na_idx <- read.delim("inputs/na_idx.tsv", sep = "\t", stringsAsFactors = FALSE)
range_method_df <- read.delim("inputs/range_method.tsv", sep = "\t", stringsAsFactors = FALSE)

result <- res_df$result
na_idx_logical <- as.logical(na_idx$na_idx)
range_method <- range_method_df$range_method[1]

txt <- xxtpt$xxtpt

# Two documented regex patterns for hour ranges
# 1) "(-?\\d+(?:\\.\\d+)?)\\s*(?:to|-|–|—)\\s*(-?\\d+(?:\\.\\d+)?)\\s*h"
# 2) "between\\s+(-?\\d+(?:\\.\\d+)?)\\s*and\\s*(-?\\d+(?:\\.\\d+)?)\\s*h"
re1 <- "(-?\\d+(?:\\.\\d+)?)\\s*(?:to|-|–|—)\\s*(-?\\d+(?:\\.\\d+)?)\\s*h"
re2 <- "between\\s+(-?\\d+(?:\\.\\d+)?)\\s*and\\s*(-?\\d+(?:\\.\\d+)?)\\s*h"

m1 <- str_match(txt, re1)
m2 <- str_match(txt, re2)

# choose pattern that matched (non-NA start)
start_chr <- ifelse(!is.na(m1[, 2]), m1[, 2], m2[, 2])
end_chr   <- ifelse(!is.na(m1[, 3]), m1[, 3], m2[, 3])

start_num <- suppressWarnings(as.numeric(start_chr))
end_num   <- suppressWarnings(as.numeric(end_chr))

# Positive span per ADMIRAL helper
span <- admiral::calculate_range_value(start = start_num,
                                       end   = end_num,
                                       range_method = range_method)

# Direction rules:
# if both bounds are <= 0  -> prior/before -> negative
# if both bounds are >= 0  -> post/after  -> positive
# otherwise (spanning zero) -> use sign of end
dir_sign <- ifelse(!is.na(start_num) & !is.na(end_num) & start_num <= 0 & end_num <= 0, -1,
            ifelse(!is.na(start_num) & !is.na(end_num) & start_num >= 0 & end_num >= 0,  1,
            ifelse(!is.na(end_num) & end_num < 0, -1,
            ifelse(!is.na(end_num) & end_num > 0,  1, NA))))

computed <- span * dir_sign

update_idx <- is.na(result) & !na_idx_logical & !is.na(computed)
result[update_idx] <- computed[update_idx]

out_df <- res_df
out_df$result <- result

write.csv(out_df, "outputs/result.csv", row.names = FALSE)

# Optional summary similar to solution.R if needed
summary_df <- data.frame(
  xxtpt        = xxtpt$xxtpt,
  start        = start_num,
  end          = end_num,
  span         = span,
  dir_sign     = dir_sign,
  computed     = computed,
  initial_res  = res_df$result,
  final_res    = result,
  na_idx       = na_idx_logical,
  stringsAsFactors = FALSE
)

write.csv(summary_df, "outputs/summary.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union

Error: 'calculate_range_value' is not an exported object from 'namespace:admiral'
Execution halted
```

## LLM Output Files

_No files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/convert_ranges",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "79814b5ea7ccb0cc2d7896b44171f9dc4c2b2c078b0c10eb2e047d2816a33ba8",
  "raw_response": "```r\nlibrary(admiral)\nlibrary(dplyr)\nlibrary(stringr)\n\ndir.create(\"outputs\", showWarnings = FALSE)\n\nxxtpt <- read.delim(\"inputs/xxtpt.tsv\", sep = \"\\t\", stringsAsFactors = FALSE)\nres_df <- read.delim(\"inputs/result.tsv\", sep = \"\\t\", stringsAsFactors = FALSE)\nna_idx <- read.delim(\"inputs/na_idx.tsv\", sep = \"\\t\", stringsAsFactors = FALSE)\nrange_method_df <- read.delim(\"inputs/range_method.tsv\", sep = \"\\t\", stringsAsFactors = FALSE)\n\nresult <- res_df$result\nna_idx_logical <- as.logical(na_idx$na_idx)\nrange_method <- range_method_df$range_method[1]\n\ntxt <- xxtpt$xxtpt\n\n# Two documented regex patterns for hour ranges\n# 1) \"(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*(?:to|-|–|—)\\\\s*(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*h\"\n# 2) \"between\\\\s+(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*and\\\\s*(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*h\"\nre1 <- \"(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*(?:to|-|–|—)\\\\s*(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*h\"\nre2 <- \"between\\\\s+(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*and\\\\s*(-?\\\\d+(?:\\\\.\\\\d+)?)\\\\s*h\"\n\nm1 <- str_match(txt, re1)\nm2 <- str_match(txt, re2)\n\n# choose pattern that matched (non-NA start)\nstart_chr <- ifelse(!is.na(m1[, 2]), m1[, 2], m2[, 2])\nend_chr   <- ifelse(!is.na(m1[, 3]), m1[, 3], m2[, 3])\n\nstart_num <- suppressWarnings(as.numeric(start_chr))\nend_num   <- suppressWarnings(as.numeric(end_chr))\n\n# Positive span per ADMIRAL helper\nspan <- admiral::calculate_range_value(start = start_num,\n                                       end   = end_num,\n                                       range_method = range_method)\n\n# Direction rules:\n# if both bounds are <= 0  -> prior/before -> negative\n# if both bounds are >= 0  -> post/after  -> positive\n# otherwise (spanning zero) -> use sign of end\ndir_sign <- ifelse(!is.na(start_num) & !is.na(end_num) & start_num <= 0 & end_num <= 0, -1,\n            ifelse(!is.na(start_num) & !is.na(end_num) & start_num >= 0 & end_num >= 0,  1,\n            ifelse(!is.na(end_num) & end_num < 0, -1,\n            ifelse(!is.na(end_num) & end_num > 0,  1, NA))))\n\ncomputed <- span * dir_sign\n\nupdate_idx <- is.na(result) & !na_idx_logical & !is.na(computed)\nresult[update_idx] <- computed[update_idx]\n\nout_df <- res_df\nout_df$result <- result\n\nwrite.csv(out_df, \"outputs/result.csv\", row.names = FALSE)\n\n# Optional summary similar to solution.R if needed\nsummary_df <- data.frame(\n  xxtpt        = xxtpt$xxtpt,\n  start        = start_num,\n  end          = end_num,\n  span         = span,\n  dir_sign     = dir_sign,\n  computed     = computed,\n  initial_res  = res_df$result,\n  final_res    = result,\n  na_idx       = na_idx_logical,\n  stringsAsFactors = FALSE\n)\n\nwrite.csv(summary_df, \"outputs/summary.csv\", row.names = FALSE)\n```",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:12:11.996751",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/convert_ranges",
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
      "stderr": "\nAttaching package: ‘dplyr’\n\nThe following objects are masked from ‘package:stats’:\n\n    filter, lag\n\nThe following objects are masked from ‘package:base’:\n\n    intersect, setdiff, setequal, union\n\nError: 'calculate_range_value' is not an exported object from 'namespace:admiral'\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
