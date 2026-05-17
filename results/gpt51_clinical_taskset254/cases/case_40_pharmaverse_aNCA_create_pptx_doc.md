# Case 40 - `pharmaverse/aNCA/create_pptx_doc`

**Package:** `aNCA`  **Function:** `create_pptx_doc`  **Expected artifacts:** `outputs/result.csv, outputs/result.rds`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `medium`

## Audit Evidence

Reference solution creates a PPTX via `officer`, `aNCA:::add_pptx_sl_title`, then returns path summary. Current prompt says implement an equivalent data transformation directly, leading to generic summaries (`(1, 3)` and `(3, 8)`) instead of ref `(1, 2)`.

## Task Prompt From `task.json`

```text
Write R code to implement the **Create pptx doc** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/path.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'path.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/template.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'template.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).
- `inputs/title.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'title.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map input columns to the appropriate parameters (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Implement the **Create Pptx Doc** functionality. Reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for create PowerPoint doc. The available input files are `inputs/path.tsv`, `inputs/template.tsv`, `inputs/title.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### path.tsv (26 bytes)
path
AVAL
AVISITN
USUBJID

### template.tsv (30 bytes)
template
AVAL
AVISITN
USUBJID

### title.tsv (27 bytes)
title
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform create PowerPoint doc using the aNCA clinical task contract.

Input: path.tsv, template.tsv, title.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### path.tsv (26 bytes)
path
AVAL
AVISITN
USUBJID

### template.tsv (30 bytes)
template
AVAL
AVISITN
USUBJID

### title.tsv (27 bytes)
title
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`path.tsv`**

```tsv
path
"temp_file.txt"

```

**`template.tsv`**

```tsv
template
"temp_template.pptx"

```

**`title.tsv`**

```tsv
title
"yes"
"no"
"true"
"false"
"active"

```

## Reference Output Files

**`result.csv`**

```csv
"id","result"
1,"temp_file.txt.pptx"

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
1,2,"id, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
path_path <- file.path("inputs", "path.tsv")
if (!file.exists(path_path)) {
  stop("path.tsv is required input")
}
path_df <- read.delim(path_path, check.names = FALSE, stringsAsFactors = FALSE)
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
path <- path_df[[1]][1]
if (length(path) > 1) path <- path[1]
if (is.na(path) || path == "") path <- "temp_output.pptx"
# 确保path有正确的扩展名
if (!grepl("\\.pptx$", path, ignore.case = TRUE)) {
  path <- paste0(path, ".pptx")
}
title_path <- file.path("inputs", "title.tsv")
if (!file.exists(title_path)) {
  stop("title.tsv is required input")
}
title_df <- read.delim(title_path, check.names = FALSE, stringsAsFactors = FALSE)
title <- title_df[[1]][1]
if (length(title) > 1) title <- title[1]
if (is.na(title)) title <- "Document Title"
template_path <- file.path("inputs", "template.tsv")
if (!file.exists(template_path)) {
  stop("template.tsv is required input")
}
template_df <- read.delim(template_path, check.names = FALSE, stringsAsFactors = FALSE)
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
template <- template_df[[1]][1]
if (length(template) > 1) template <- template[1]
if (is.na(template) || template == "") template <- ""

# 2. 数据验证 / Data validation
# path、title、template都是标量字符串，不需要数据框验证

# 3. 执行函数实现 / Execute function implementation
suppressPackageStartupMessages(library(officer))
if (template == "" || !file.exists(template)) {
  pptx <- read_pptx()
} else {
  pptx <- read_pptx(template)
}
pptx <- aNCA:::add_pptx_sl_title(pptx, title)
print(pptx, target = path)
result <- path

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

# 7. 保存输出 / Save outputs
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
  library(tools)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper to read TSV preserving header
read_tsv_safe <- function(path) {
  read.table(
    file = path,
    header = TRUE,
    sep = "\t",
    quote = "",
    stringsAsFactors = FALSE,
    check.names = FALSE
  )
}

# Read inputs
path_df     <- read_tsv_safe("inputs/path.tsv")
template_df <- read_tsv_safe("inputs/template.tsv")
title_df    <- read_tsv_safe("inputs/title.tsv")

# Treat one-row tables as vectors (scalars per-column)
path_vec     <- unlist(path_df[1, , drop = TRUE], use.names = TRUE)
template_vec <- unlist(template_df[1, , drop = TRUE], use.names = TRUE)
title_vec    <- unlist(title_df[1, , drop = TRUE], use.names = TRUE)

# Determine maximum length to preserve alignment across inputs
n_path     <- length(path_vec)
n_template <- length(template_vec)
n_title    <- length(title_vec)
n_max      <- max(n_path, n_template, n_title)

# Recycle shorter inputs to match max length (aNCA-style vector handling)
recycle_to <- function(x, n) {
  if (length(x) == n) return(x)
  if (length(x) == 0) return(rep(NA_character_, n))
  rep(x, length.out = n)
}

path_vec_rep     <- recycle_to(path_vec, n_max)
template_vec_rep <- recycle_to(template_vec, n_max)
title_vec_rep    <- recycle_to(title_vec, n_max)

# Build compact, inspectable result
result <- data.frame(
  PATH     = path_vec_rep,
  TEMPLATE = template_vec_rep,
  TITLE    = title_vec_rep,
  stringsAsFactors = FALSE,
  check.names = FALSE
)

# Write outputs
write.csv(result, file = "outputs/result.csv", row.names = FALSE)
saveRDS(result, file = "outputs/result.rds")
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

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

**`result.csv`**

```csv
"PATH","TEMPLATE","TITLE"
"AVAL","AVAL","AVAL"

```

**`result.rds`**

```text
[binary artifact: result.rds, 142 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(tidyr)
  library(stringr)
  library(officer)
})

in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

path_df     <- read_tsv(file.path(in_dir, "path.tsv"), show_col_types = FALSE)
template_df <- read_tsv(file.path(in_dir, "template.tsv"), show_col_types = FALSE)
title_df    <- read_tsv(file.path(in_dir, "title.tsv"), show_col_types = FALSE)

# Harmonize column names
names(path_df)     <- tolower(names(path_df))
names(template_df) <- tolower(names(template_df))
names(title_df)    <- tolower(names(title_df))

# Assume each file has a single column describing clinical task contract fields
col_path     <- names(path_df)[1]
col_template <- names(template_df)[1]
col_title    <- names(title_df)[1]

df <- full_join(
  full_join(
    path_df  %>% mutate(source_path = !!sym(col_path)),
    template_df %>% mutate(source_template = !!sym(col_template)),
    by = setNames(col_template, col_path)
  ),
  title_df %>% mutate(source_title = !!sym(col_title)),
  by = setNames(col_title, col_path)
)

df <- df %>%
  rename(field = !!sym(col_path)) %>%
  mutate(across(everything(), as.character))

# Dummy metadata columns to mimic a clinical task contract mapping
result <- df %>%
  mutate(
    in_path     = !is.na(source_path),
    in_template = !is.na(source_template),
    in_title    = !is.na(source_title),
    status      = case_when(
      in_path & in_template & in_title ~ "OK",
      in_path & in_template & !in_title ~ "MISSING_TITLE",
      in_path & !in_template & in_title ~ "MISSING_TEMPLATE",
      !in_path & in_template & in_title ~ "MISSING_PATH",
      TRUE ~ "PARTIAL"
    )
  ) %>%
  arrange(field)

write_csv(result, file.path(out_dir, "result.csv"))
saveRDS(result, file.path(out_dir, "result.rds"))

# Create a simple PowerPoint summarizing the contract
ppt <- read_pptx()

ppt <- add_slide(ppt, layout = "Title Slide", master = "Office Theme")
ppt <- ph_with(ppt, value = "aNCA Clinical Task Contract", location = ph_location_type(type = "ctrTitle"))
ppt <- ph_with(ppt, value = format(Sys.Date()), location = ph_location_type(type = "subTitle"))

ppt <- add_slide(ppt, layout = "Title and Content", master = "Office Theme")
ppt <- ph_with(ppt, value = "Field Summary", location = ph_location_type(type = "title"))

tbl <- result %>%
  select(field, in_path, in_template, in_title, status)

ppt <- ph_with(
  ppt,
  value = flextable::flextable(tbl),
  location = ph_location_type(type = "body")
)

print(ppt, target = file.path(out_dir, "aNCA_clinical_task_contract.pptx"))
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

**`aNCA_clinical_task_contract.pptx`**

```text
[binary artifact: aNCA_clinical_task_contract.pptx, 25459 bytes]
```

**`result.csv`**

```csv
field,source_path,source_template,source_title,in_path,in_template,in_title,status
AVAL,AVAL,AVAL,AVAL,TRUE,TRUE,TRUE,OK
AVISITN,AVISITN,AVISITN,AVISITN,TRUE,TRUE,TRUE,OK
USUBJID,USUBJID,USUBJID,USUBJID,TRUE,TRUE,TRUE,OK

```

**`result.rds`**

```text
[binary artifact: result.rds, 233 bytes]
```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/create_pptx_doc",
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
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(1, 3)"
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

### Simple Prompt

```json
{
  "task_id": "pharmaverse/aNCA/create_pptx_doc",
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
      "reason": "Shape mismatch: ref=(1, 2) vs llm=(3, 8)"
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
