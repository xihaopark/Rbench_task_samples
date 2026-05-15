# Case 17 - `pharmaverse/admiral/filter_exist`
**Package:** `admiral`  **Function:** `filter_exist`  **Level:** `L2`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Write R code to implement the **Filter exist** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

**Inputs:**
- `inputs/by_vars.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'by_vars.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::filter_exist` (numeric vectors are often stored in a column named like the parameter).
- `inputs/dataset.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'dataset.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::filter_exist` (numeric vectors are often stored in a column named like the parameter).
- `inputs/dataset_add.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'dataset_add.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::filter_exist` (numeric vectors are often stored in a column named like the parameter).
- `inputs/filter_add.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'filter_add.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `admiral::filter_exist` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use `admiral::filter_exist` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
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

**`inputs/dataset.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/dataset_add.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/filter_add.tsv`**

```tsv
filter_add
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(rlang))

dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dataset_add <- read.delim(file.path("inputs", "dataset_add.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
by_col <- intersect(names(dataset), names(dataset_add))[1]
by_vars <- exprs(!!sym(by_col))

result <- admiral::filter_exist(dataset, dataset_add, by_vars = by_vars)

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

# Create outputs directory
dir.create("outputs", showWarnings = FALSE)

# Read inputs
by_vars_df <- read.delim(
  file.path("inputs", "by_vars.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
dataset <- read.delim(
  file.path("inputs", "dataset.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
dataset_add <- read.delim(
  file.path("inputs", "dataset_add.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
filter_add_df <- read.delim(
  file.path("inputs", "filter_add.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

# by_vars: assume a single row and all columns are variable names to use
by_vars <- vars(!!!rlang::syms(as.character(unlist(by_vars_df[1, , drop = TRUE]))))

# filter_add: assume this contains an R expression in a column named "filter"
# that should be combined with '&' if multiple rows
if (!("filter" %in% names(filter_add_df))) {
  stop("filter_add.tsv must contain a column named 'filter' with filter expressions")
}
filter_exprs_chr <- filter_add_df$filter
filter_exprs_chr <- filter_exprs_chr[filter_exprs_chr != "" & !is.na(filter_exprs_chr)]

if (length(filter_exprs_chr) == 0) {
  filter_add <- NULL
} else {
  # combine multiple expressions with &
  combined_filter_chr <- paste0("(", filter_exprs_chr, ")", collapse = " & ")
  filter_add <- rlang::parse_expr(combined_filter_chr)
}

# Run filter_exist
result <- filter_exist(
  dataset     = dataset,
  dataset_add = dataset_add,
  by_vars     = by_vars,
  filter_add  = filter_add
)

# Write output
write.csv(result, file = file.path("outputs", "result.csv"), row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error in vars(!!!rlang::syms(as.character(unlist(by_vars_df[1, , drop = TRUE])))) : 
  could not find function "vars"
Execution halted
```

## LLM Output Files

_No files generated._

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/filter_exist",
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
      "stderr": "Error in vars(!!!rlang::syms(as.character(unlist(by_vars_df[1, , drop = TRUE])))) : \n  could not find function \"vars\"\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
