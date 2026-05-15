# Case 18 - `pharmaverse/admiral/impute_dtc_dt`
**Package:** `admiral`  **Function:** `impute_dtc_dt`  **Level:** `L3`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Impute a **complete date** from partial `*DTC` text. Load `library(admiral)`.

**Inputs:** `dtc.tsv`, optional `highest_imputation.tsv`.

**Computation:** **`admiral::impute_dtc_dt(dtc, highest_imputation = ..., date_imputation = "mid")`**.

**Required outputs:** `outputs/result.csv` per task `expected` in `task.json`; use `dir.create('outputs', showWarnings=FALSE)` and `write.csv(..., row.names=FALSE)` as needed.
```

## Input Files

**`inputs/date_imputation.tsv`**

```tsv
date_imputation
"yes"
"no"
"true"
"false"
"active"
```

**`inputs/dtc.tsv`**

```tsv
dtc
"yes"
"no"
"true"
"false"
"active"
```

**`inputs/highest_imputation.tsv`**

```tsv
highest_imputation
"test_value"
```

**`inputs/max_dates.tsv`**

```tsv
max_dates
"test_value"
```

**`inputs/min_dates.tsv`**

```tsv
min_dates
"test_value"
```

**`inputs/preserve.tsv`**

```tsv
preserve
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

dtc_df <- read.delim(file.path("inputs", "dtc.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dtc <- as.character(dtc_df[[ncol(dtc_df)]])
if (length(dtc) == 0 || dtc[1] == "test_value") dtc <- "2020-01-15"
highest_imputation <- "n"
if (file.exists(file.path("inputs", "highest_imputation.tsv"))) {
  hi <- read.delim(file.path("inputs", "highest_imputation.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
  v <- as.character(hi[[1]][1])
  if (v %in% c("Y", "M", "D", "n")) highest_imputation <- v
}
date_imputation <- "mid"

result <- admiral::impute_dtc_dt(dtc, highest_imputation = highest_imputation, date_imputation = date_imputation)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(dtc = dtc, result = as.character(result)), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"dtc","result"
"yes",NA
"no",NA
"true",NA
"false",NA
"active",NA
```

## LLM Code

```r
library(admiral)

# Create outputs directory
dir.create("outputs", showWarnings = FALSE)

# Read inputs
dtc <- read.delim("dtc.tsv", stringsAsFactors = FALSE)

highest_imp_path <- "highest_imputation.tsv"
if (file.exists(highest_imp_path)) {
  highest_imputation_df <- read.delim(highest_imp_path, stringsAsFactors = FALSE)
  # Assume a single value in a column named 'highest_imputation'
  if ("highest_imputation" %in% names(highest_imputation_df)) {
    highest_imputation <- highest_imputation_df$highest_imputation[1]
  } else {
    highest_imputation <- NULL
  }
} else {
  highest_imputation <- NULL
}

# Impute dates
res <- impute_dtc_dt(
  dtc,
  highest_imputation = highest_imputation,
  date_imputation = "mid"
)

# Ensure data.frame for writing
res_df <- as.data.frame(res)

# Write result
write.csv(res_df, file = "outputs/result.csv", row.names = FALSE)
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
In file(file, "rt") : cannot open file 'dtc.tsv': No such file or directory
Execution halted
```

## LLM Output Files

_No files generated._

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/impute_dtc_dt",
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
      "stderr": "Error in file(file, \"rt\") : cannot open the connection\nCalls: read.delim -> read.table -> file\nIn addition: Warning message:\nIn file(file, \"rt\") : cannot open file 'dtc.tsv': No such file or directory\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
