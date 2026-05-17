# Case 49 - `pharmaverse/aNCA/create_qmd_doc`

**Package:** `aNCA`  **Function:** `create_qmd_doc`  **Expected artifacts:** `outputs/result.csv`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `high`

## Audit Evidence

Reference prompt says to use `aNCA:::create_qmd_doc`; current/simple prompt explicitly asks for an equivalent direct data transformation. Generated outputs have wrong shapes (`5x8` or `1x5` vs reference `5x3`) and miss the reference workflow.

## Task Prompt From `task.json`

```text
Write R code to implement the **Create qmd doc** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/extra_setup.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'extra_setup.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::create_qmd_doc` (numeric vectors are often stored in a column named like the parameter).
- `inputs/libraries.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'libraries.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::create_qmd_doc` (numeric vectors are often stored in a column named like the parameter).
- `inputs/quarto_path.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'quarto_path.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::create_qmd_doc` (numeric vectors are often stored in a column named like the parameter).
- `inputs/rda_path.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'rda_path.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::create_qmd_doc` (numeric vectors are often stored in a column named like the parameter).
- `inputs/template.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'template.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::create_qmd_doc` (numeric vectors are often stored in a column named like the parameter).
- `inputs/title.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'title.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::create_qmd_doc` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::create_qmd_doc` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for create Quarto markdown doc. The available input files are `inputs/extra_setup.tsv`, `inputs/libraries.tsv`, `inputs/quarto_path.tsv`, `inputs/rda_path.tsv`, `inputs/template.tsv`, `inputs/title.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### extra_setup.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### libraries.tsv (31 bytes)
libraries
AVAL
AVISITN
USUBJID

### quarto_path.tsv (33 bytes)
quarto_path
AVAL
AVISITN
USUBJID

### rda_path.tsv (30 bytes)
rda_path
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
Create R script to perform create Quarto markdown doc using the aNCA clinical task contract.

Input: extra_setup.tsv, libraries.tsv, quarto_path.tsv, rda_path.tsv, template.tsv, title.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### extra_setup.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### libraries.tsv (31 bytes)
libraries
AVAL
AVISITN
USUBJID

### quarto_path.tsv (33 bytes)
quarto_path
AVAL
AVISITN
USUBJID

### rda_path.tsv (30 bytes)
rda_path
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

**`extra_setup.tsv`**

```tsv
extra_setup
"test_value"

```

**`libraries.tsv`**

```tsv
libraries
"item1"
"item2"
"item3"
"item4"
"item5"

```

**`quarto_path.tsv`**

```tsv
quarto_path
"temp_output.qmd"

```

**`rda_path.tsv`**

```tsv
rda_path
"temp_file.txt"

```

**`template.tsv`**

```tsv
template
"test_value"

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
"libraries","extra_setup","result"
"item1","test_value",TRUE
"item2","test_value",TRUE
"item3","test_value",TRUE
"item4","test_value",TRUE
"item5","test_value",TRUE

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
5,3,"libraries, extra_setup, result"

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
quarto_path_path <- file.path("inputs", "quarto_path.tsv")
if (!file.exists(quarto_path_path)) {
  stop("quarto_path.tsv is required input")
}
quarto_path_df <- read.delim(quarto_path_path, check.names = FALSE, stringsAsFactors = FALSE)
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
quarto_path <- quarto_path_df[[1]][1]
if (length(quarto_path) > 1) quarto_path <- quarto_path[1]
if (is.na(quarto_path)) quarto_path <- "temp_output.qmd"
title_path <- file.path("inputs", "title.tsv")
if (!file.exists(title_path)) {
  stop("title.tsv is required input")
}
title_df <- read.delim(title_path, check.names = FALSE, stringsAsFactors = FALSE)
title <- title_df[[1]][1]
if (length(title) > 1) title <- title[1]
if (is.na(title)) title <- "Document Title"
libraries_path <- file.path("inputs", "libraries.tsv")
if (!file.exists(libraries_path)) {
  stop("libraries.tsv is required input")
}
libraries_df <- read.delim(libraries_path, check.names = FALSE, stringsAsFactors = FALSE)
libraries <- libraries_df$libraries
if (is.data.frame(libraries)) {
  libraries <- libraries[[1]]
}
rda_path_path <- file.path("inputs", "rda_path.tsv")
if (!file.exists(rda_path_path)) {
  stop("rda_path.tsv is required input")
}
rda_path_df <- read.delim(rda_path_path, check.names = FALSE, stringsAsFactors = FALSE)
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
rda_path <- rda_path_df[[1]][1]
if (length(rda_path) > 1) rda_path <- rda_path[1]
if (is.na(rda_path)) rda_path <- ""
template_path <- file.path("inputs", "template.tsv")
if (!file.exists(template_path)) {
  stop("template.tsv is required input")
}
template_df <- read.delim(template_path, check.names = FALSE, stringsAsFactors = FALSE)
template <- template_df[[1]][1]
if (length(template) > 1) template <- template[1]
if (is.na(template)) template <- ""
extra_setup_path <- file.path("inputs", "extra_setup.tsv")
if (!file.exists(extra_setup_path)) {
  stop("extra_setup.tsv is required input")
}
extra_setup_df <- read.delim(extra_setup_path, check.names = FALSE, stringsAsFactors = FALSE)
extra_setup <- extra_setup_df$extra_setup
if (is.data.frame(extra_setup)) {
  extra_setup <- extra_setup[[1]]
}

# 2. 数据验证 / Data validation
# quarto_path、title、rda_path、template都是标量字符串，不需要数据框验证
# libraries和extra_setup是字符向量

# 3. 执行函数实现 / Execute function implementation
result <- aNCA:::create_qmd_doc(
  libraries = libraries,
  title = title,
  extra_setup = extra_setup,
  template = template,
  rda_path = rda_path,
  quarto_path = quarto_path
)


# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    libraries = libraries, extra_setup = extra_setup,
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
  library(readr)
  library(dplyr)
  library(tidyr)
  library(purrr)
})

# Create outputs directory
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Helper: read TSV with header, keep types simple
read_tsv_simple <- function(path) {
  read_tsv(
    file = path,
    col_types = cols(.default = col_character()),
    show_col_types = FALSE,
    progress = FALSE
  )
}

# Read inputs
extra_setup <- read_tsv_simple("inputs/extra_setup.tsv")
libraries   <- read_tsv_simple("inputs/libraries.tsv")
quarto_path <- read_tsv_simple("inputs/quarto_path.tsv")
rda_path    <- read_tsv_simple("inputs/rda_path.tsv")
template    <- read_tsv_simple("inputs/template.tsv")
title       <- read_tsv_simple("inputs/title.tsv")

# Treat one-column, multi-row tables as vectors; keep headers
vec_from_tbl <- function(tbl) {
  if (ncol(tbl) == 1) {
    setNames(list(tbl[[1]]), names(tbl))
  } else {
    as.list(tbl)
  }
}

inputs_list <- list(
  extra_setup = vec_from_tbl(extra_setup),
  libraries   = vec_from_tbl(libraries),
  quarto_path = vec_from_tbl(quarto_path),
  rda_path    = vec_from_tbl(rda_path),
  template    = vec_from_tbl(template),
  title       = vec_from_tbl(title)
)

# Align by row across vector/table inputs
# Get maximum length across all vectors
all_vectors <- unlist(lapply(inputs_list, function(x) x), recursive = FALSE)
max_len <- max(vapply(all_vectors, length, integer(1)))

# Recycle each vector to max_len
recycle_vec <- function(x, n) {
  if (length(x) == 0L) {
    rep(NA_character_, n)
  } else if (length(x) == n) {
    x
  } else {
    rep_len(x, n)
  }
}

# Build a single data frame with aligned rows
df <- tibble(idx = seq_len(max_len))

for (grp_name in names(inputs_list)) {
  grp <- inputs_list[[grp_name]]
  for (col_name in names(grp)) {
    full_name <- if (grp_name == "extra_setup") {
      # extra_setup is more like a scalar/vector config; keep its own name
      col_name
    } else {
      paste(grp_name, col_name, sep = "_")
    }
    df[[full_name]] <- recycle_vec(grp[[col_name]], max_len)
  }
}

# Derive an aNCA-compatible, compact configuration table
# Example: treat rows as parameter sets for Quarto PK support task
result <- df %>%
  mutate(
    run_id = sprintf("run_%03d", idx)
  ) %>%
  relocate(run_id, .before = 1)

# Write compact CSV output
write_csv(result, "outputs/result.csv", na = "")

# Also save full result object as RDS
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
run_id,idx,x,libraries_libraries,quarto_path_quarto_path,rda_path_rda_path,template_template,title_title
run_001,1,SYSBP,AVAL,AVAL,AVAL,AVAL,AVAL
run_002,2,DIABP,AVISITN,AVISITN,AVISITN,AVISITN,AVISITN
run_003,3,PULSE,USUBJID,USUBJID,USUBJID,USUBJID,USUBJID
run_004,4,WEIGHT,AVAL,AVAL,AVAL,AVAL,AVAL
run_005,5,HEIGHT,AVISITN,AVISITN,AVISITN,AVISITN,AVISITN

```

**`result.rds`**

```text
[binary artifact: result.rds, 337 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(tidyr)
})

in_dir  <- "inputs"
out_dir <- "outputs"

if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

extra_setup <- read_tsv(file.path(in_dir, "extra_setup.tsv"), show_col_types = FALSE)
libraries   <- read_tsv(file.path(in_dir, "libraries.tsv"),   show_col_types = FALSE)
quarto_path <- read_tsv(file.path(in_dir, "quarto_path.tsv"), show_col_types = FALSE)
rda_path    <- read_tsv(file.path(in_dir, "rda_path.tsv"),    show_col_types = FALSE)
template    <- read_tsv(file.path(in_dir, "template.tsv"),    show_col_types = FALSE)
title_tab   <- read_tsv(file.path(in_dir, "title.tsv"),       show_col_types = FALSE)

get_first_val <- function(tbl) {
  col <- tbl[[1]]
  col[1]
}

extra_vec <- extra_setup[[1]][-1]
extra_vec <- extra_vec[!is.na(extra_vec) & extra_vec != ""]

libs_val    <- get_first_val(libraries)
qpath_val   <- get_first_val(quarto_path)
rda_val     <- get_first_val(rda_path)
template_val<- get_first_val(template)
title_val   <- get_first_val(title_tab)

yaml_lines <- c(
  "---",
  paste0('title: "', title_val, '"'),
  'format:',
  '  html:',
  '    toc: true',
  '    number-sections: true',
  'execute:',
  '  echo: true',
  '  warning: false',
  '  message: false',
  "---",
  ""
)

setup_chunks <- c(
  "```{r}",
  "options(stringsAsFactors = FALSE)",
  "```",
  ""
)

lib_chunk <- c(
  "```{r libraries}",
  paste0("library(", libs_val, ")"),
  "```",
  ""
)

rda_chunk <- c(
  "```{r load-data}",
  paste0("load(\"", rda_val, "\")"),
  "```",
  ""
)

extra_chunk <- character(0)
if (length(extra_vec) > 0) {
  extra_chunk <- c(
    "```{r extra-setup}",
    paste0("# Extra setup variables from extra_setup.tsv: ", paste(extra_vec, collapse = ", ")),
    "```",
    ""
  )
}

body_lines <- c(
  "# Introduction",
  "",
  "This Quarto document was generated from the aNCA clinical task contract inputs.",
  "",
  "## Methods",
  "",
  "Describe analysis methods here.",
  "",
  "## Results",
  "",
  "Summarize main findings here.",
  "",
  "## Discussion",
  "",
  "Interpret the results here.",
  ""
)

qmd_content <- c(
  yaml_lines,
  setup_chunks,
  lib_chunk,
  rda_chunk,
  extra_chunk,
  body_lines
)

qmd_path <- file.path(out_dir, qpath_val)
writeLines(qmd_content, qmd_path)

result <- tibble::tibble(
  file = basename(qmd_path),
  path = qmd_path,
  title = title_val,
  template = template_val,
  rda_path = rda_val
)

write_csv(result, file.path(out_dir, "result.csv"))
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

**`AVAL`**

```text
---
title: "AVAL"
format:
  html:
    toc: true
    number-sections: true
execute:
  echo: true
  warning: false
  message: false
---

```{r}
options(stringsAsFactors = FALSE)
```

```{r libraries}
library(AVAL)
```

```{r load-data}
load("AVAL")
```

```{r extra-setup}
# Extra setup variables from extra_setup.tsv: DIABP, PULSE, WEIGHT, HEIGHT
```

# Introduction

This Quarto document was generated from the aNCA clinical task contract inputs.

## Methods

Describe analysis methods here.

## Results

Summarize main findings here.

## Discussion

Interpret the results here.


```

**`result.csv`**

```csv
file,path,title,template,rda_path
AVAL,outputs/AVAL,AVAL,AVAL,AVAL

```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/create_qmd_doc",
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
      "reason": "Shape mismatch: ref=(5, 3) vs llm=(5, 8)"
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
  "task_id": "pharmaverse/aNCA/create_qmd_doc",
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
      "reason": "Shape mismatch: ref=(5, 3) vs llm=(1, 5)"
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
