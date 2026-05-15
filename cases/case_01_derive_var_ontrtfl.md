# Case 01 - `pharmaverse/admiral/derive_var_ontrtfl`
**Package:** `admiral`  **Function:** `derive_var_ontrtfl`  **Level:** `L3`  **LLM sample:** GPT-5.1 direct LLM pass5, `sample_01`  **Evaluation status:** `FAIL`, pass=`False`, score=`0.0`
**Evaluation message:** Failed at case_embedded

## Task Prompt

```text
Derive **on-treatment flag** from visit vs exposure dates. Load `library(admiral)`.

**Inputs:** The reference **does not read fixture TSVs**; it builds a minimal `data.frame` with **`ADT`**, **`TRTSDT`**, **`TRTEDT`** and calls **`admiral::derive_var_ontrtfl(dataset, start_date = ADT, ref_start_date = TRTSDT, ref_end_date = TRTEDT)`**. Match that object and call pattern so grading aligns with the canonical solution.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
The reference may also emit `outputs/summary.csv` when the long template is used; follow `solution.R` if present.
```

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

**`inputs/end_date.tsv`**

```tsv
end_date
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/end_date_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/filter_pre_timepoint.tsv`**

```tsv
filter_pre_timepoint
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/filter_pre_timepoint_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/ignore_time_for_ref_end_dat.tsv`**

```tsv
ignore_time_for_ref_end_dat
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/ignore_time_for_ref_end_dat_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/new_var.tsv`**

```tsv
new_var
"test_value"
```

**`inputs/ref_end_date.tsv`**

```tsv
ref_end_date
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/ref_end_date_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/ref_end_window.tsv`**

```tsv
ref_end_window
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/ref_end_window_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/ref_start_date.tsv`**

```tsv
ref_start_date
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/ref_start_date_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/span_period.tsv`**

```tsv
span_period
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/span_period_df.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/start_date.tsv`**

```tsv
start_date
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/start_date_df.tsv`**

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

# 1. 创建最小数据集 (需 ADT, TRTSDT, TRTEDT)
dataset <- data.frame(
  USUBJID = c("P01", "P02", "P03"),
  ADT = as.Date(c("2020-02-24", "2020-01-01", "2019-12-31")),
  TRTSDT = as.Date(c("2020-01-01", "2020-01-01", "2020-01-01")),
  TRTEDT = as.Date(c("2020-03-01", "2020-03-01", "2020-03-01")),
  stringsAsFactors = FALSE
)

# 2. 执行函数
result <- admiral::derive_var_ontrtfl(
  dataset,
  start_date = ADT,
  ref_start_date = TRTSDT,
  ref_end_date = TRTEDT
)

# 3. 保存输出
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
```

## Reference Output

**`outputs/result.csv`**

```csv
"USUBJID","ADT","TRTSDT","TRTEDT","ONTRTFL"
"P01",2020-02-24,2020-01-01,2020-03-01,"Y"
"P02",2020-01-01,2020-01-01,2020-03-01,"Y"
"P03",2019-12-31,2020-01-01,2020-03-01,NA
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

# Minimal example data
df <- data.frame(
  ADT     = as.Date(c("2023-01-01", "2023-01-10", "2023-02-01", "2023-03-01")),
  TRTSDT  = as.Date(c("2023-01-05", "2023-01-01", "2023-01-15", "2023-02-15")),
  TRTEDT  = as.Date(c("2023-02-15", "2023-01-20", "2023-02-15", "2023-02-20"))
)

result <- derive_var_ontrtfl(
  dataset        = df,
  start_date     = ADT,
  ref_start_date = TRTSDT,
  ref_end_date   = TRTEDT
)

write.csv(result, "outputs/result.csv", row.names = FALSE)
```

## LLM Execution Output

**`stdout.txt`**

```text

```

**`stderr.txt`**

```text

```

## LLM Output Files

**`outputs/result.csv`**

```csv
"ADT","TRTSDT","TRTEDT","ONTRTFL"
2023-01-01,2023-01-05,2023-02-15,NA
2023-01-10,2023-01-01,2023-01-20,"Y"
2023-02-01,2023-01-15,2023-02-15,"Y"
2023-03-01,2023-02-15,2023-02-20,NA
```

## LLM Metadata

```json
{
  "task_id": "pharmaverse/admiral/derive_var_ontrtfl",
  "package": "admiral",
  "track_id": "clinical_pilot",
  "content_tag_id": "clinical",
  "flow_tag_id": "transform",
  "scoring_mode_id": "strict",
  "code_sha256": "7816c587c7cd8bbd32b734aee5b9a8b46661d6519d74506279677c03d740d0f9",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-03-30T16:12:54.665844",
  "source": "direct_llm"
}
```

## Evaluation Record

```json
{
  "task_id": "pharmaverse/admiral/derive_var_ontrtfl",
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
          "reason": "Shape mismatch: ref=(3, 5) vs llm=(4, 4)"
        }
      },
      "returncode": 0,
      "normalizations": []
    }
  ]
}
```
