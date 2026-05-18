# Case 119: pharmaverse/admiral/derive_vars_merged

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_vars_merged`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive vars merged using the admiral clinical task contract.

Input: dataset.tsv, source.tsv
Output: result.csv


Required columns for result.csv: USUBJID, AVISIT, AVAL, SEX, AGE
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (59 bytes)
USUBJID	AVISIT	AVAL
01	Week 1	10
02	Week 1	20
03	Week 1	30

### source.tsv (32 bytes)
USUBJID	SEX	AGE
01	F	45
02	M	50
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged/inputs/dataset.tsv`
- Size: 59 bytes

```text
USUBJID	AVISIT	AVAL
01	Week 1	10
02	Week 1	20
03	Week 1	30
```

### `source.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged/inputs/source.tsv`
- Size: 32 bytes

```text
USUBJID	SEX	AGE
01	F	45
02	M	50
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged/solution.R`
- Size: 409 bytes

```r
dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
source <- read.delim(file.path("inputs", "source.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
result_df <- merge(dataset, source, by = "USUBJID", all.x = TRUE, sort = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_vars_merged/outputs/result.csv`
- Size: 100 bytes

```csv
"USUBJID","AVISIT","AVAL","SEX","AGE"
1,"Week 1",10,"F",45
2,"Week 1",20,"M",50
3,"Week 1",30,NA,NA
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required package
if (!requireNamespace("admiral", quietly = TRUE)) {
  install.packages("admiral", repos = "https://cloud.r-project.org")
}
library(admiral)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input data
dataset <- read.delim(
  file = "inputs/dataset.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

source <- read.delim(
  file = "inputs/source.tsv",
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE
)

# Derive merged variables using admiral-style derive_vars_merged
result <- derive_vars_merged(
  dataset = dataset,
  dataset_add = source,
  by_vars = exprs(USUBJID),
  new_vars = exprs(SEX, AGE)
)

# Keep only required columns
result_out <- result[, c("USUBJID", "AVISIT", "AVAL", "SEX", "AGE")]

# Write output
write.csv(
  result_out,
  file = "outputs/result.csv",
  row.names = FALSE,
  na = ""
)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_merged/sample_00/case_01/llm_outputs/result.csv`
- Size: 96 bytes

```csv
"USUBJID","AVISIT","AVAL","SEX","AGE"
1,"Week 1",10,"F",45
2,"Week 1",20,"M",50
3,"Week 1",30,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_vars_merged/sample_00/case_01/stderr.txt`
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
