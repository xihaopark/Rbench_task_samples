# Case 102: pharmaverse/admiral/derive_var_base

## Case Metadata

- Task ID: `pharmaverse/admiral/derive_var_base`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform derive var base using the admiral clinical task contract.

Input: dataset.tsv, new_var.tsv, source_var.tsv
Output: result.csv


Required columns for result.csv: USUBJID, PARAMCD, AVISITN, AVAL, ABLFL, BASE
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (105 bytes)
USUBJID	PARAMCD	AVISITN	AVAL	ABLFL
01	ALT	0	20	Y
01	ALT	1	30	N
01	ALT	2	28	N
02	ALT	0	15	Y
02	ALT	1	22	N

### new_var.tsv (13 bytes)
new_var
BASE

### source_var.tsv (16 bytes)
source_var
AVAL
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_base/inputs/dataset.tsv`
- Size: 105 bytes

```text
USUBJID	PARAMCD	AVISITN	AVAL	ABLFL
01	ALT	0	20	Y
01	ALT	1	30	N
01	ALT	2	28	N
02	ALT	0	15	Y
02	ALT	1	22	N
```

### `new_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_base/inputs/new_var.tsv`
- Size: 13 bytes

```text
new_var
BASE
```

### `source_var.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_base/inputs/source_var.tsv`
- Size: 16 bytes

```text
source_var
AVAL
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_base/solution.R`
- Size: 747 bytes

```r
result_df <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
source_var <- as.character(read.delim(file.path("inputs", "source_var.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$source_var[1])
new_var <- as.character(read.delim(file.path("inputs", "new_var.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$new_var[1])
key <- paste(result_df$USUBJID, result_df$PARAMCD, sep = "\r")
base_key <- key[result_df$ABLFL == "Y"]
base_value <- result_df[[source_var]][result_df$ABLFL == "Y"]
lookup <- setNames(base_value, base_key)
result_df[[new_var]] <- unname(lookup[key])

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/derive_var_base/outputs/result.csv`
- Size: 152 bytes

```csv
"USUBJID","PARAMCD","AVISITN","AVAL","ABLFL","BASE"
1,"ALT",0,20,"Y",20
1,"ALT",1,30,"N",20
1,"ALT",2,28,"N",20
2,"ALT",0,15,"Y",15
2,"ALT",1,22,"N",15
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
dataset <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols()
)

new_var <- read_tsv(
  file = file.path("inputs", "new_var.tsv"),
  col_types = cols()
)

source_var <- read_tsv(
  file = file.path("inputs", "source_var.tsv"),
  col_types = cols()
)

# Expecting single values in new_var and source_var
new_var_name    <- new_var$new_var[1]
source_var_name <- source_var$source_var[1]

# Derive BASE as baseline AVAL (where ABLFL == "Y") per USUBJID, PARAMCD
# and merge back to all records for those subjects/parameters
baseline_vals <- dataset %>%
  filter(ABLFL == "Y") %>%
  select(USUBJID, PARAMCD, !!source_var_name) %>%
  rename(!!new_var_name := !!sym(source_var_name))

result <- dataset %>%
  left_join(baseline_vals, by = c("USUBJID", "PARAMCD")) %>%
  select(USUBJID, PARAMCD, AVISITN, AVAL, ABLFL, BASE = !!sym(new_var_name))

# Write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_base/sample_00/case_01/llm_outputs/result.csv`
- Size: 125 bytes

```csv
USUBJID,PARAMCD,AVISITN,AVAL,ABLFL,BASE
01,ALT,0,20,Y,20
01,ALT,1,30,N,20
01,ALT,2,28,N,20
02,ALT,0,15,Y,15
02,ALT,1,22,N,15
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__derive_var_base/sample_00/case_01/stderr.txt`
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
