# Case 20 - `pharmaverse/admiral/get_highest_imputation_level`
**Package:** `admiral`  **Function:** `get_highest_imputation_level`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Map imputation level flags to the **highest** granularity. Load `library(admiral)`.

**Inputs:** `highest_imputation.tsv`, optional `create_datetime.tsv`.

Some admiral helpers are **not exported**; the reference uses `get("<fn>", envir = asNamespace("admiral"))(...)`. Using the same call is fair game and avoids false failures from `admiral::<fn>` not existing.

**Computation:** Call **`get_highest_imputation_level(highest_imputation, create_datetime = ...)`** from the admiral namespace as in `solution.R`.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.
```

## Input Files

**`inputs/create_datetime.tsv`**

```tsv
create_datetime
FALSE
```

**`inputs/highest_imputation.tsv`**

```tsv
highest_imputation
"yes"
"no"
"true"
"false"
"active"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

highest_imputation_df <- read.delim(file.path("inputs", "highest_imputation.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
highest_imputation <- as.character(highest_imputation_df[[ncol(highest_imputation_df)]][1])
if (!highest_imputation %in% c("Y", "M", "D", "n")) highest_imputation <- "n"
create_datetime <- TRUE
if (file.exists(file.path("inputs", "create_datetime.tsv"))) {
  cd <- read.delim(file.path("inputs", "create_datetime.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
  v <- as.character(cd[[ncol(cd)]][1])
  create_datetime <- tolower(v) %in% c("true", "y", "yes", "1")
}

get_highest_imputation_level <- get("get_highest_imputation_level", envir = asNamespace("admiral"))
result <- get_highest_imputation_level(highest_imputation, create_datetime = create_datetime)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(highest_imputation = highest_imputation, create_datetime = create_datetime, result = as.character(result)), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"highest_imputation","create_datetime","result"
"n",FALSE,"n"
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

highest_imputation <- read.delim("highest_imputation.tsv", stringsAsFactors = FALSE)

create_datetime_path <- "create_datetime.tsv"
if (file.exists(create_datetime_path)) {
  create_datetime <- read.delim(create_datetime_path, stringsAsFactors = FALSE)
} else {
  create_datetime <- NULL
}

result <- get("get_highest_imputation_level", envir = asNamespace("admiral"))(
  highest_imputation = highest_imputation,
  create_datetime = create_datetime
)

write.csv(result, "outputs/result.csv", row.names = FALSE)
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
  cannot open file 'highest_imputation.tsv': No such file or directory
Execution halted
```

## LLM Output Files

_No files generated._

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/get_highest_imputation_level",
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
      "stderr": "Error in file(file, \"rt\") : cannot open the connection\nCalls: read.delim -> read.table -> file\nIn addition: Warning message:\nIn file(file, \"rt\") :\n  cannot open file 'highest_imputation.tsv': No such file or directory\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
