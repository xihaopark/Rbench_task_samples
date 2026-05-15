# Case 15 - `pharmaverse/aNCA/simplify_unit`
**Package:** `aNCA`  **Function:** `simplify_unit`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to simplify unit expressions with aNCA and **units**. Load `library(aNCA)` and `library(units)`.

**Inputs:** `inputs/x.tsv` (value or unit string / `units` object), `inputs/as_character.tsv` (logical `as_character`).

**Computation:** Call **`aNCA:::simplify_unit(x=, as_character=)`** (internal). The reference falls back to `units::set_units`, `deparse_unit`, and `units_options` logic if the call errors — match that behavior for NA, `unitless`, and parse failures.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both are required, write the primary analytic object or a sensible serialization to the RDS file and a tabular summary to the CSV.
```

## Input Files

**`inputs/as_character.tsv`**

```tsv
as_character
"yes"
"no"
"true"
"false"
"active"
```

**`inputs/x.tsv`**

```tsv
x
"item1"
"item2"
"item3"
"item4"
"item5"
```

## Reference Code

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
x_path <- file.path("inputs", "x.tsv")
if (!file.exists(x_path)) {
  stop("x.tsv is required input")
}
x_df <- read.delim(x_path, check.names = FALSE, stringsAsFactors = FALSE)
x <- x_df$x
as_character_path <- file.path("inputs", "as_character.tsv")
if (!file.exists(as_character_path)) {
  stop("as_character.tsv is required input")
}
as_character_df <- read.delim(as_character_path, check.names = FALSE, stringsAsFactors = FALSE)
as_character <- as_character_df$as_character

# 2. 执行函数实现 / Execute function implementation
suppressPackageStartupMessages(library(units))
result <- tryCatch({
  aNCA:::simplify_unit(
    x = x,
    as_character = as_character
  )
}, error = function(e) {
  # 如果函数调用失败，手动实现逻辑
  # Handle NA input
  if (length(x) == 1 && is.na(x)) {
    if (length(as_character) == 1 && as_character) {
      return(NA_character_)
    } else {
      return(NA_real_)
    }
  }

  # handle special case: unitless
  if (is.character(x) && length(x) == 1 && tolower(x) == "unitless") {
    if (length(as_character) == 1 && as_character) {
      return("unitless")
    } else {
      return(set_units(1, "unitless", check_is_valid = FALSE))
    }
  }

  # If input is a units object, use its value. Otherwise, default to 1.
  value <- if (inherits(x, "units")) drop_units(x) else 1
  # If input is a units object, deparse its units.
  unit_char <- if (inherits(x, "units")) deparse_unit(x) else x

  # Temporarily set the simplify option to TRUE
  old_opt <- units_options("simplify")
  on.exit(units_options(simplify = old_opt))
  units_options(simplify = TRUE)

  tryCatch({
    # Attempt to parse and simplify
    simplified_obj <- units::set_units(value, unit_char, mode = "standard")
    if (length(as_character) == 1 && as_character) {
      units::deparse_unit(simplified_obj)
    } else {
      simplified_obj
    }
  }, error = function(e2) {
    # Log warning and return original
    warning("Unit '", unit_char, "' could not be simplified.")
    if (length(as_character) == 1 && as_character) {
      unit_char
    } else {
      x
    }
  })
})

# 3. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    x = x, as_character = as_character,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# 4. 生成汇总统计 / Generate summary statistics
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

# 5. 保存输出 / Save outputs
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
"x","as_character","result"
"item1","yes","item1"
"item2","no","item2"
"item3","true","item3"
"item4","false","item4"
"item5","active","item5"
```

**`outputs/summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"x, as_character, result"
```

## LLM Code

```r
library(aNCA)
library(units)

dir.create("outputs", showWarnings = FALSE)

x_in   <- read.delim("inputs/x.tsv",   stringsAsFactors = FALSE)
asc_in <- read.delim("inputs/as_character.tsv", stringsAsFactors = FALSE)

# Expect columns named "x" and "as_character"; adjust if needed
x_vals   <- x_in[[1]]
as_char  <- asc_in[[1]]

simplify_one <- function(x, as_character) {
  # Try aNCA internal simplification first
  out <- try(aNCA:::simplify_unit(x = x, as_character = as_character), silent = TRUE)
  if (!inherits(out, "try-error")) return(out)

  # Fallback to units logic
  # x might already be a units object or a character
  old_parse <- units::units_options("parse")
  on.exit(units::units_options(parse = old_parse), add = TRUE)
  units::units_options(parse = TRUE)

  if (inherits(x, "units")) {
    uobj <- x
  } else {
    # Try to parse as units; on failure, return NA / NA_character_
    uobj <- try(units::set_units(1, x, mode = "standard"), silent = TRUE)
    if (inherits(uobj, "try-error")) {
      return(if (isTRUE(as_character)) NA_character_ else as.numeric(NA))
    }
  }

  # Handle unitless
  ustr <- units::deparse_unit(uobj)
  if (identical(ustr, "1") || identical(ustr, "")) {
    if (isTRUE(as_character)) {
      return("1")
    } else {
      # Strip units, return numeric 1 with no units
      return(as.numeric(units::drop_units(uobj)))
    }
  }

  if (isTRUE(as_character)) {
    ustr
  } else {
    uobj
  }
}

results <- mapply(
  simplify_one,
  x = x_vals,
  as_character = as_char,
  SIMPLIFY = FALSE
)

# Build a data.frame for CSV; coerce non-character to character
res_for_csv <- vapply(
  results,
  function(z) {
    if (inherits(z, "units")) {
      units::deparse_unit(z)
    } else if (is.numeric(z) && length(z) == 1L && !inherits(z, "units")) {
      as.character(z)
    } else if (is.character(z) && length(z) == 1L) {
      z
    } else {
      NA_character_
    }
  },
  character(1)
)

df_out <- data.frame(
  x = x_vals,
  as_character = as_char,
  result = res_for_csv,
  stringsAsFactors = FALSE
)

write.csv(df_out, file = "outputs/result.csv", row.names = FALSE)
saveRDS(results, file = "outputs/result.rds")
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text
Registered S3 method overwritten by 'tern':
  method   from 
  tidy.glm broom
udunits database from /usr/share/xml/udunits/udunits2.xml
```

## LLM Output Files

**`outputs/result.csv`**

```csv
"x","as_character","result"
"item1","yes",NA
"item2","no",NA
"item3","true",NA
"item4","false",NA
"item5","active",NA
```

**`outputs/result.rds`**

_RDS binary artifact generated; size: 101 bytes._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/aNCA/simplify_unit",
  "package": "aNCA",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "analyze",
  "scoring_mode_id": "strict",
  "code_sha256": "b1929f0215798749b12e44d4033c753b7db1e8694c1e7503c40e6cb3397433e1",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:10:52.447983",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/aNCA/simplify_unit",
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
          "reason": "Value mismatch in column: result"
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
