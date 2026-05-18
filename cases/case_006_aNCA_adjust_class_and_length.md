# Case 006: pharmaverse/aNCA/adjust_class_and_length

## Case Metadata

- Task ID: `pharmaverse/aNCA/adjust_class_and_length`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform adjust class and length using the aNCA clinical task contract.

Input: adjust_length.tsv, df.tsv, metadata.tsv
Output: result.csv


Required columns for result.csv: id, value, group, category
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### adjust_length.tsv (41 bytes)
adjust_length
"value"
"group"
"category"

### df.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### metadata.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

## Input Data

### `adjust_length.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/adjust_class_and_length/inputs/adjust_length.tsv`
- Size: 41 bytes

```text
adjust_length
"value"
"group"
"category"
```

### `df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/adjust_class_and_length/inputs/df.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `metadata.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/adjust_class_and_length/inputs/metadata.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/adjust_class_and_length/solution.R`
- Size: 381 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
df <- read_tsv("df")
# Class and length metadata adjustments are not represented in CSV; preserve the aligned data table.
write.csv(df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/adjust_class_and_length/outputs/result.csv`
- Size: 127 bytes

```csv
"id","value","group","category"
1,10.5,"A","Type1"
2,20.3,"B","Type2"
3,30.7,"A","Type1"
4,40.2,"B","Type2"
5,50.9,"A","Type1"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
adjust <- read_tsv("inputs/adjust_length.tsv", show_col_types = FALSE)
df <- read_tsv("inputs/df.tsv", show_col_types = FALSE)
meta <- read_tsv("inputs/metadata.tsv", show_col_types = FALSE)

# Ensure required columns exist and classes/lengths are adjusted based on metadata
common_cols <- intersect(colnames(df), colnames(meta))
df <- df[, common_cols]
meta <- meta[, common_cols]

# Coerce df column classes to match metadata
for (col in common_cols) {
  target_class <- class(meta[[col]])[1]
  if (!inherits(df[[col]], target_class)) {
    if (target_class %in% c("numeric", "integer", "double")) {
      df[[col]] <- suppressWarnings(as.numeric(df[[col]]))
    } else if (target_class == "character") {
      df[[col]] <- as.character(df[[col]])
    } else if (target_class == "factor") {
      df[[col]] <- factor(df[[col]], levels = levels(meta[[col]]))
    } else if (target_class == "logical") {
      df[[col]] <- as.logical(df[[col]])
    } else {
      mode(df[[col]]) <- mode(meta[[col]])
    }
  }
}

# Adjust length according to adjust_length contract (use metadata as reference)
# Here we align df to metadata by id, keeping only ids present in metadata
if ("id" %in% common_cols) {
  df <- df %>%
    semi_join(meta %>% select(id), by = "id")
}

# Keep only required output columns
required_cols <- c("id", "value", "group", "category")
result <- df %>% select(all_of(required_cols))

# Write result
write_csv(result, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__adjust_class_and_length/sample_00/case_01/llm_outputs/result.csv`
- Size: 99 bytes

```csv
id,value,group,category
1,10.5,A,Type1
2,20.3,B,Type2
3,30.7,A,Type1
4,40.2,B,Type2
5,50.9,A,Type1
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__adjust_class_and_length/sample_00/case_01/stderr.txt`
- Size: 1123 bytes

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

## Evaluation Result

```json
{
  "status": "PASS",
  "failure_stage": "pass",
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "tier": "pass",
      "tier_value": "pass",
      "failure_stage": "pass",
      "comparison": {
        "result.csv": {
          "match": true,
          "tier": "pass",
          "failure_stage": "pass"
        }
      },
      "returncode": 0,
      "normalizations": [],
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [
          "result.csv"
        ],
        "staged_artifacts": [
          "result.csv"
        ],
        "missing_artifacts": [],
        "extra_artifacts": [],
        "comparison_reasons": {}
      }
    }
  ]
}
```
