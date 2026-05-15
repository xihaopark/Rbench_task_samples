# Case 07 - `pharmaverse/admiral/compute_qual_imputation_dec`
**Package:** `admiral`  **Function:** `compute_qual_imputation_dec`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Derive the **decimal adjustment** used for qualitative imputation from a character vector. Load `library(admiral)`, `library(dplyr)`, and `library(stringr)`.

**Inputs:** `inputs/character_value_decimal.tsv` — one string per row (`character_value_decimal`).

**Computation:** For each trimmed string, if it contains a decimal point, the weight is **`1 / 10^(nchar after the dot)`**; otherwise **`1`**. The reference uses `stringr::str_trim`, `str_detect`, `str_length`, and `str_locate` with `dplyr::case_when` — reproduce that vector (equivalent to **the required functionality** where exported).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.

The reference may also write `outputs/summary.csv` for diagnostics; follow the same layout as `solution.R` when present.
```

## Input Files

**`inputs/character_value_decimal.tsv`**

```tsv
character_value_decimal
"yes"
"no"
"true"
"false"
"active"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(stringr))

# Read input data
character_value_decimal_path <- file.path("inputs", "character_value_decimal.tsv")
if (!file.exists(character_value_decimal_path)) {
  stop("character_value_decimal.tsv is required input")
}
character_value_decimal_df <- read.delim(character_value_decimal_path, check.names = FALSE, stringsAsFactors = FALSE)
character_value_decimal <- character_value_decimal_df$character_value_decimal

# Execute function implementation
x <- str_trim(character_value_decimal)

  decimal <- case_when(
    str_detect(x, "\\.") ~ 1 / (10^(str_length(x) - str_locate(x, "\\.")[, 1])),
    TRUE ~ 1
  )

  unname(decimal)
result <- decimal

# Create result dataframe
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    character_value_decimal = character_value_decimal,
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
"character_value_decimal","result"
"yes",1
"no",1
"true",1
"false",1
"active",1
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,2,"character_value_decimal, result"
```

## LLM Code

```r
library(admiral)
library(dplyr)
library(stringr)

dir.create("outputs", showWarnings = FALSE)

dat <- read.delim("inputs/character_value_decimal.tsv", stringsAsFactors = FALSE)

res <- dat %>%
  mutate(
    character_value_decimal = str_trim(character_value_decimal),
    dec_adj = case_when(
      str_detect(character_value_decimal, "\\.") ~
        1 / (10 ^ (str_length(character_value_decimal) -
                     str_locate(character_value_decimal, "\\.")[, "start"])),
      TRUE ~ 1
    )
  ) %>%
  select(dec_adj)

write.csv(res, "outputs/result.csv", row.names = FALSE)
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

```

## LLM Output Files

**`outputs/result.csv`**

```csv
"dec_adj"
1
1
1
1
1
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/compute_qual_imputation_dec",
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
          "reason": "Shape mismatch: ref=(5, 2) vs llm=(5, 1)"
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
