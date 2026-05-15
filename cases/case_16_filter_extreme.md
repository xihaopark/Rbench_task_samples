# Case 16 - `pharmaverse/admiral/filter_extreme`
**Package:** `admiral`  **Function:** `filter_extreme`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Keep **first/last/min/max** row per group. Load `library(admiral)`, `library(rlang)`.

**Inputs:** `dataset.tsv`, `by_vars.tsv`.

**Computation:** **`admiral::filter_extreme(dataset, by_vars = exprs(!!sym(...)), order = exprs(...), mode = "first")`** as in `solution.R`.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.
```

## Input Files

**`inputs/by_vars.tsv`**

```tsv
by_vars
"item1"
"item2"
"item3"
"item4"
"item5"
```

**`inputs/check_type.tsv`**

```tsv
check_type
"test_value"
```

**`inputs/dataset.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/mode.tsv`**

```tsv
mode
"test_value"
```

**`inputs/order.tsv`**

```tsv
order
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
by_vars_df <- read.delim(file.path("inputs", "by_vars.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
by_col <- names(by_vars_df)[1]
if (!by_col %in% names(dataset)) by_col <- names(dataset)[1]
by_vars <- exprs(!!sym(by_col))
order <- exprs(!!sym(names(dataset)[min(2, ncol(dataset))]))
mode <- "first"

result <- admiral::filter_extreme(dataset, by_vars = by_vars, order = order, mode = mode)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"id","value","group","category"
1,10.5,"A","Type1"
2,20.3,"B","Type2"
3,30.7,"A","Type1"
4,40.2,"B","Type2"
5,50.9,"A","Type1"
```

## LLM Code

```r
library(admiral)
library(rlang)

dir.create("outputs", showWarnings = FALSE)

dataset <- read.delim("dataset.tsv", sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)
by_vars_tbl <- read.delim("by_vars.tsv", sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)

# Expecting by_vars.tsv to contain a column 'by_var' listing grouping variables in order
by_vars_syms <- lapply(by_vars_tbl$by_var, sym)

# Expecting task.json-like info encoded in by_vars.tsv:
# columns: by_var, keep (first/last/min/max), order_var
# This script assumes:
#  - 'keep' is the same for all rows (one task)
#  - 'order_var' is the variable used in `order = exprs(...)`

keep_mode   <- unique(by_vars_tbl$keep)
order_var   <- unique(by_vars_tbl$order_var)

if (length(keep_mode) != 1L) {
  stop("by_vars.tsv must specify a single keep mode per file (first/last/min/max).")
}
if (length(order_var) != 1L) {
  stop("by_vars.tsv must specify a single order_var per file.")
}

order_expr <- exprs(!!sym(order_var))

res_first <- switch(
  keep_mode,
  "first" = admiral::filter_extreme(
    dataset,
    by_vars = !!!by_vars_syms,
    order   = order_expr,
    mode    = "first"
  ),
  "last" = admiral::filter_extreme(
    dataset,
    by_vars = !!!by_vars_syms,
    order   = order_expr,
    mode    = "last"
  ),
  "min" = admiral::filter_extreme(
    dataset,
    by_vars = !!!by_vars_syms,
    order   = order_expr,
    mode    = "first"
  ),
  "max" = admiral::filter_extreme(
    dataset,
    by_vars = !!!by_vars_syms,
    order   = order_expr,
    mode    = "last"
  ),
  stop("Invalid keep mode: must be one of first/last/min/max.")
)

write.csv(res_first, file = "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error in file(file, "rt") : cannot open the connection
Calls: read.delim -> read.table -> file
In addition: Warning message:
In file(file, "rt") :
  cannot open file 'dataset.tsv': No such file or directory
Execution halted
```

## LLM Output Files

_No files generated._

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/filter_extreme",
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
      "stderr": "Error in file(file, \"rt\") : cannot open the connection\nCalls: read.delim -> read.table -> file\nIn addition: Warning message:\nIn file(file, \"rt\") :\n  cannot open file 'dataset.tsv': No such file or directory\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
