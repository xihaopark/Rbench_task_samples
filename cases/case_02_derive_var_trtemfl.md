# Case 02 - `pharmaverse/admiral/derive_var_trtemfl`
**Package:** `admiral`  **Function:** `derive_var_trtemfl`  **Level:** `L3`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_01`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Derive **treatment-emergent flag** for AE toxicity. Load `library(admiral)` and `library(dplyr)`.

**Inputs:** The reference **builds a minimal AE-style `data.frame`** (not from TSV) with **`TRTSDTM`**, **`TRTEDTM`**, **`ASTDTM`**, **`AENDTM`**, **`AEITOXGR`**, **`AETOXGR`**, then calls **`admiral::derive_var_trtemfl`** with **`new_var = TRTEMFL`**, **`trt_end_date = TRTEDTM`**, **`end_window = 0`**, **`initial_intensity`**, **`intensity`**, and **`subject_keys = exprs(USUBJID)`** (as in `solution.R`). Match that pipeline.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
The reference may also emit `outputs/summary.csv` when the long template is used; follow `solution.R` if present.
```

## Input Files

**`inputs/admiral.tsv`**

```tsv
admiral
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(dplyr))

# 1. 创建最小 ADAE 数据集 (derive_var_trtemfl 需要 USUBJID, TRTSDTM, TRTEDTM, ASTDTM, AENDTM, AEITOXGR, AETOXGR)
dataset <- data.frame(
  USUBJID = c("1", "1", "2"),
  TRTSDTM = as.Date(c("2021-01-01", "2021-01-01", "2021-01-01")),
  TRTEDTM = as.Date(c("2021-12-31", "2021-12-31", "2021-12-31")),
  ASTDTM = as.Date(c("2020-12-20", "2021-12-20", "2021-12-20")),
  AENDTM = as.Date(c("2020-12-21", "2021-12-21", "2021-12-21")),
  AEITOXGR = c("2", "2", "2"),
  AETOXGR = c("2", "2", "2"),
  stringsAsFactors = FALSE
)

# 2. 执行函数
result <- admiral::derive_var_trtemfl(
  dataset,
  new_var = TRTEMFL,
  trt_end_date = TRTEDTM,
  end_window = 0,
  initial_intensity = AEITOXGR,
  intensity = AETOXGR,
  subject_keys = exprs(USUBJID)
)

# 3. 保存输出
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"USUBJID","TRTSDTM","TRTEDTM","ASTDTM","AENDTM","AEITOXGR","AETOXGR","TRTEMFL"
"1",2021-01-01,2021-12-31,2020-12-20,2020-12-21,"2","2",NA
"1",2021-01-01,2021-12-31,2021-12-20,2021-12-21,"2","2","Y"
"2",2021-01-01,2021-12-31,2021-12-20,2021-12-21,"2","2","Y"
```

## LLM Code

```r
library(admiral)
library(dplyr)

dir.create("outputs", showWarnings = FALSE)

ae <- data.frame(
  USUBJID    = c("01-001", "01-001", "01-002", "01-003"),
  TRTSDTM    = as.POSIXct(c("2021-01-01 09:00:00",
                            "2021-01-01 09:00:00",
                            "2021-02-15 08:30:00",
                            "2021-03-10 10:00:00")),
  TRTEDTM    = as.POSIXct(c("2021-01-31 17:00:00",
                            "2021-01-31 17:00:00",
                            "2021-03-17 16:45:00",
                            "2021-04-05 12:00:00")),
  ASTDTM     = as.POSIXct(c("2021-01-05 10:00:00",
                            "2021-02-01 11:00:00",
                            "2021-02-20 09:15:00",
                            "2021-04-10 13:30:00")),
  AENDTM     = as.POSIXct(c("2021-01-10 12:00:00",
                            "2021-02-10 15:00:00",
                            "2021-02-25 10:00:00",
                            "2021-04-20 09:00:00")),
  AEITOXGR   = c(NA, "1", "2", NA),
  AETOXGR    = c("2", "3", "3", "1"),
  stringsAsFactors = FALSE
)

result <- ae %>%
  derive_var_trtemfl(
    new_var = TRTEMFL,
    trt_end_date = TRTEDTM,
    end_window = 0,
    initial_intensity = AEITOXGR,
    intensity = AETOXGR,
    subject_keys = exprs(USUBJID)
  )

write.csv(result, "outputs/result.csv", row.names = FALSE)
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
"USUBJID","TRTSDTM","TRTEDTM","ASTDTM","AENDTM","AEITOXGR","AETOXGR","TRTEMFL"
"01-001",2021-01-01 09:00:00,2021-01-31 17:00:00,2021-01-05 10:00:00,2021-01-10 12:00:00,NA,"2","Y"
"01-001",2021-01-01 09:00:00,2021-01-31 17:00:00,2021-02-01 11:00:00,2021-02-10 15:00:00,"1","3",NA
"01-002",2021-02-15 08:30:00,2021-03-17 16:45:00,2021-02-20 09:15:00,2021-02-25 10:00:00,"2","3","Y"
"01-003",2021-03-10 10:00:00,2021-04-05 12:00:00,2021-04-10 13:30:00,2021-04-20 09:00:00,NA,"1",NA
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/derive_var_trtemfl",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "6187c8987c2008cdbffdf47ccee455d59291d5c8601bf78566ddff3b193d5dea",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:13:02.982570",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/derive_var_trtemfl",
  "sample_idx": 1,
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
          "reason": "Shape mismatch: ref=(3, 8) vs llm=(4, 8)"
        }
      },
      "returncode": 0,
      "normalizations": []
    }
  ]
}
```
