# Case 02 - `pharmaverse/admiral/derive_var_pchg`
**Package:** `admiral`  **Function:** `derive_var_pchg`  **Level:** `L1`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Derive **percent change from baseline** (`PCHG`). Load `library(admiral)`.

**Inputs:** `inputs/dataset.tsv` with a header row. Read it with `read.delim(..., check.names=FALSE, stringsAsFactors=FALSE)`. If `AVAL` is missing, create it from the numeric `value` column. If `BASE` is missing, set it to the first `AVAL`, matching the reference.

**Computation:** Call `admiral::derive_var_pchg(dataset)` after ensuring `AVAL` and `BASE` exist.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` and write CSV with `write.csv(..., row.names=FALSE)`.
```

## Prompt Repair Note

This display prompt lightly clarifies the fallback from `value` to `AVAL` and the default `BASE`, which are already implemented in the reference solution.

## Input Files

**`inputs/dataset.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

# 1. 读取输入数据
dataset_path <- file.path("inputs", "dataset.tsv")
if (!file.exists(dataset_path)) stop("dataset.tsv is required input")
dataset <- read.delim(dataset_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 确保有 AVAL 和 BASE 列
if (!"AVAL" %in% names(dataset)) {
  val_col <- if ("value" %in% names(dataset)) "value" else names(dataset)[2]
  dataset$AVAL <- as.numeric(dataset[[val_col]])
}
if (!"BASE" %in% names(dataset)) dataset$BASE <- dataset$AVAL[1]

# 3. 执行函数
result <- admiral::derive_var_pchg(dataset)

# 4. 保存输出
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"id","value","group","category","AVAL","BASE","PCHG"
1,10.5,"A","Type1",10.5,10.5,0
2,20.3,"B","Type2",20.3,10.5,93.3333333333333
3,30.7,"A","Type1",30.7,10.5,192.380952380952
4,40.2,"B","Type2",40.2,10.5,282.857142857143
5,50.9,"A","Type1",50.9,10.5,384.761904761905
```

## LLM Code

```r
library(admiral)

# Ensure outputs directory exists
dir.create("outputs", showWarnings = FALSE)

# Read input
dat <- read.table(
  "inputs/dataset.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE,
  check.names = FALSE
)

# Ensure AVAL exists: if not, try to infer from common value column names
if (!"AVAL" %in% names(dat)) {
  val_candidates <- c("AVALC", "VALUE", "VAL", "AVAL_NUM")
  val_col <- val_candidates[val_candidates %in% names(dat)]
  if (length(val_col) == 0L) {
    stop("No AVAL column found and no suitable value column to derive it from.")
  }
  dat$AVAL <- as.numeric(dat[[val_col[1L]]])
}

# Ensure BASE exists: if not, try to infer from common baseline column names
if (!"BASE" %in% names(dat)) {
  base_candidates <- c("BASEC", "BASELINE", "BASE_VAL")
  base_col <- base_candidates[base_candidates %in% names(dat)]
  if (length(base_col) == 0L) {
    stop("No BASE column found and no suitable baseline column to derive it from.")
  }
  dat$BASE <- as.numeric(dat[[base_col[1L]]])
}

# Derive percent change from baseline
result <- admiral::derive_var_pchg(dat)

# Write result
write.csv(result, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text
```

**`stderr.txt`**

```text
Error: No AVAL column found and no suitable value column to derive it from.
Execution halted
```

## LLM Output Files

_No files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/derive_var_pchg",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "8d6b41e8f4d4b7e04b43130042d0cef3456492c76aa59c5efcfe33f8af9e551f",
  "raw_response": "```r\nlibrary(admiral)\n\n# Ensure outputs directory exists\ndir.create(\"outputs\", showWarnings = FALSE)\n\n# Read input\ndat <- read.table(\n  \"inputs/dataset.tsv\",\n  header = TRUE,\n  sep = \"\\t\",\n  stringsAsFactors = FALSE,\n  check.names = FALSE\n)\n\n# Ensure AVAL exists: if not, try to infer from common value column names\nif (!\"AVAL\" %in% names(dat)) {\n  val_candidates <- c(\"AVALC\", \"VALUE\", \"VAL\", \"AVAL_NUM\")\n  val_col <- val_candidates[val_candidates %in% names(dat)]\n  if (length(val_col) == 0L) {\n    stop(\"No AVAL column found and no suitable value column to derive it from.\")\n  }\n  dat$AVAL <- as.numeric(dat[[val_col[1L]]])\n}\n\n# Ensure BASE exists: if not, try to infer from common baseline column names\nif (!\"BASE\" %in% names(dat)) {\n  base_candidates <- c(\"BASEC\", \"BASELINE\", \"BASE_VAL\")\n  base_col <- base_candidates[base_candidates %in% names(dat)]\n  if (length(base_col) == 0L) {\n    stop(\"No BASE column found and no suitable baseline column to derive it from.\")\n  }\n  dat$BASE <- as.numeric(dat[[base_col[1L]]])\n}\n\n# Derive percent change from baseline\nresult <- admiral::derive_var_pchg(dat)\n\n# Write result\nwrite.csv(result, \"outputs/result.csv\", row.names = FALSE)\n```",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:12:58.522295",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/derive_var_pchg",
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
      "stderr": "Error: No AVAL column found and no suitable value column to derive it from.\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
