# Case 03 - `pharmaverse/admiral/create_period_dataset`
**Package:** `admiral`  **Function:** `create_period_dataset`  **Level:** `L3`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_00`  **Evaluation status:** `NO_OUTPUT`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Build a **one-row-per-subject-per-period** dataset from wide period start/end columns. Load `library(admiral)`, `library(rlang)`, and `library(tibble)`.

**Inputs:** `inputs/datase.tsv` (subject-level data with `USUBJID` and period date columns such as `AP01SDT` / `AP01EDT`), `inputs/new_vars.tsv`, `inputs/subject_keys.tsv` — the reference coerces to a tibble, ensures minimal columns exist, sets **`new_vars <- rlang::exprs(APERSDT = APxxSDT, APEREDT = APxxEDT)`** and **`subject_keys <- rlang::exprs(USUBJID)`** (or the first dataset column), then calls **`admiral::create_period_dataset(dataset = dataset, new_vars = new_vars, subject_keys = subject_keys)`**.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
The reference may also emit `outputs/summary.csv` when the long template is used; follow `solution.R` if present.
```

## Input Files

**`inputs/datase.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
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

**`inputs/new_vars.tsv`**

```tsv
new_vars
"x + y"
"a * b"
"sum(z)"
"mean(values)"
"max(data)"
```

**`inputs/subject_keys.tsv`**

```tsv
subject_keys
"x + y"
"a * b"
"sum(z)"
"mean(values)"
"max(data)"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))
suppressPackageStartupMessages(library(tibble))

# 1. 读取输入数据 / Read input data
dataset_path <- file.path("inputs", "datase.tsv")
if (!file.exists(dataset_path)) {
  stop("datase.tsv is required input")
}
dataset <- read.delim(dataset_path, check.names = FALSE, stringsAsFactors = FALSE)

new_vars_path <- file.path("inputs", "new_vars.tsv")
if (!file.exists(new_vars_path)) {
  stop("new_vars.tsv is required input")
}
new_vars_df <- read.delim(new_vars_path, check.names = FALSE, stringsAsFactors = FALSE)

subject_keys_path <- file.path("inputs", "subject_keys.tsv")
if (!file.exists(subject_keys_path)) {
  stop("subject_keys.tsv is required input")
}
subject_keys_df <- read.delim(subject_keys_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 构建 dataset 与 new_vars (period 格式: APxxSDT, APxxEDT) / Build dataset and new_vars
if (nrow(dataset) == 0) {
  dataset <- data.frame(USUBJID = "S1", AP01SDT = as.Date("2020-01-01"), AP01EDT = as.Date("2020-01-31"))
}
if (!"USUBJID" %in% colnames(dataset)) {
  dataset$USUBJID <- paste0("S", seq_len(nrow(dataset)))
}
if (!"AP01SDT" %in% colnames(dataset)) {
  dataset$AP01SDT <- as.Date("2020-01-01") + seq_len(nrow(dataset)) - 1L
}
if (!"AP01EDT" %in% colnames(dataset)) {
  dataset$AP01EDT <- as.Date("2020-01-31") + seq_len(nrow(dataset)) - 1L
}
dataset <- tibble::as_tibble(dataset)
new_vars <- rlang::exprs(APERSDT = APxxSDT, APEREDT = APxxEDT)

# 3. 构建 subject_keys / Build subject_keys
subject_keys <- rlang::exprs(USUBJID)
if (ncol(subject_keys_df) > 0 && "USUBJID" %in% colnames(dataset)) {
  subject_keys <- rlang::exprs(USUBJID)
} else if (ncol(subject_keys_df) > 0) {
  key_col <- colnames(dataset)[1]
  subject_keys <- rlang::exprs(!!rlang::sym(key_col))
}

# 4. 执行函数实现 / Execute function implementation
result <- admiral::create_period_dataset(
  dataset = dataset,
  new_vars = new_vars,
  subject_keys = subject_keys
)

# 5. 保存输出 / Save outputs
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"USUBJID","APERIOD","APERSDT","APEREDT"
"S1",1,2020-01-01,2020-01-31
"S2",1,2020-01-02,2020-02-01
"S3",1,2020-01-03,2020-02-02
"S4",1,2020-01-04,2020-02-03
"S5",1,2020-01-05,2020-02-04
```

## LLM Code

```r
library(admiral)
library(rlang)
library(tibble)

dir.create("outputs", showWarnings = FALSE)

dataset <- read.delim("inputs/datase.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
new_vars_in <- read.delim("inputs/new_vars.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
subject_keys_in <- read.delim("inputs/subject_keys.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

dataset <- as_tibble(dataset)

if (ncol(subject_keys_in) > 0) {
  subj_key_name <- subject_keys_in[[1]][1]
} else {
  subj_key_name <- colnames(dataset)[1]
}
subject_keys <- rlang::exprs(!!rlang::sym(subj_key_name))

if (ncol(new_vars_in) >= 2) {
  ap_start <- new_vars_in[[1]][1]
  ap_end   <- new_vars_in[[2]][1]
} else {
  ap_start <- "APxxSDT"
  ap_end   <- "APxxEDT"
}
new_vars <- rlang::exprs(
  APERSDT = !!rlang::sym(ap_start),
  APEREDT = !!rlang::sym(ap_end)
)

result <- admiral::create_period_dataset(
  dataset = dataset,
  new_vars = new_vars,
  subject_keys = subject_keys
)

write.csv(result, file = "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text
Error in `admiral::create_period_dataset()`:
! Required variable `x + y` is missing in `dataset`
Backtrace:
    ▆
 1. └─admiral::create_period_dataset(dataset = dataset, new_vars = new_vars, subject_keys = subject_keys)
 2.   └─admiraldev::assert_data_frame(dataset, required_vars = subject_keys)
 3.     └─cli::cli_abort(...)
 4.       └─rlang::abort(...)
Execution halted
```

## LLM Output Files

_No output files generated._

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/create_period_dataset",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "e1aff8e38596963b22cb1889788a989189075aa95a3da39600099f554bf0c5f9",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:12:26.810300",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/create_period_dataset",
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
      "stderr": "Error in `admiral::create_period_dataset()`:\n! Required variable `x + y` is missing in `dataset`\nBacktrace:\n    ▆\n 1. └─admiral::create_period_dataset(dataset = dataset, new_vars = new_vars, subject_keys = subject_keys)\n 2.   └─admiraldev::assert_data_frame(dataset, required_vars = subject_keys)\n 3.     └─cli::cli_abort(...)\n 4.       └─rlang::abort(...)\nExecution halted\n",
      "returncode": 1
    }
  ]
}
```
