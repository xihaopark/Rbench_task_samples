# Case 008: pharmaverse/aNCA/apply_labels

## Case Metadata

- Task ID: `pharmaverse/aNCA/apply_labels`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `PASS`
- Failure stage: `pass`

## Prompt

```text
Write an R script to perform apply labels using the aNCA clinical task contract.

Input: data.tsv, labels_df.tsv, type.tsv
Output: result.csv


Required columns for result.csv: id, value, group, category
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### labels_df.tsv (125 bytes)
Dataset	Variable	Label
ADPC	id	Subject ID
ADPC	value	Concentration
ADPC	group	Treatment Group
ADPC	category	Analyte Category

### type.tsv (10 bytes)
type
ADPC
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_labels/inputs/data.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `labels_df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_labels/inputs/labels_df.tsv`
- Size: 125 bytes

```text
Dataset	Variable	Label
ADPC	id	Subject ID
ADPC	value	Concentration
ADPC	group	Treatment Group
ADPC	category	Analyte Category
```

### `type.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_labels/inputs/type.tsv`
- Size: 10 bytes

```text
type
ADPC
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_labels/solution.R`
- Size: 389 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
data <- read_tsv("data")
# Applied labels are R attributes and do not survive CSV serialization; the tabular data is unchanged.
write.csv(data, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/apply_labels/outputs/result.csv`
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

# Load required package
suppressWarnings({
  if (!requireNamespace("readr", quietly = TRUE)) {
    install.packages("readr", repos = "https://cloud.r-project.org")
  }
  if (!requireNamespace("dplyr", quietly = TRUE)) {
    install.packages("dplyr", repos = "https://cloud.r-project.org")
  }
})

library(readr)
library(dplyr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input files
data_path   <- file.path("inputs", "data.tsv")
labels_path <- file.path("inputs", "labels_df.tsv")
type_path   <- file.path("inputs", "type.tsv")

data_df   <- read_tsv(data_path, col_types = cols())
labels_df <- read_tsv(labels_path, col_types = cols())
type_df   <- read_tsv(type_path, col_types = cols())

# Determine dataset type
current_type <- type_df$type[1]

# Filter labels for current dataset
labels_filtered <- labels_df %>%
  filter(Dataset == current_type)

# Ensure only required columns in result
required_cols <- c("id", "value", "group", "category")
data_df <- data_df %>% select(all_of(required_cols))

# Optionally, you could apply labels as attributes (not visible in CSV)
for (var in required_cols) {
  label_val <- labels_filtered %>%
    filter(Variable == var) %>%
    pull(Label)
  if (length(label_val) == 1) {
    attr(data_df[[var]], "label") <- label_val
  }
}

# Write output
write_csv(data_df, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__apply_labels/sample_00/case_01/llm_outputs/result.csv`
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

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__apply_labels/sample_00/case_01/stderr.txt`
- Size: 1333 bytes

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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union
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
