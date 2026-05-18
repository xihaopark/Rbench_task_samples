# Case 137: pharmaverse/admiral/filter_relative

## Case Metadata

- Task ID: `pharmaverse/admiral/filter_relative`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: required columns were specified but model returned wrong row shape

## Prompt

```text
Write an R script to perform filter relative using the admiral clinical task contract.

Input: dataset.tsv
Output: result.csv


Required columns for result.csv: USUBJID, AVISITN, PARAMCD, AVAL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (137 bytes)
USUBJID	AVISITN	PARAMCD	AVAL
01	-1	SCREEN	8
01	1	BASE	10
01	2	POST	12
02	-1	SCREEN	9
02	1	POST	11
... [3 more lines omitted]
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_relative/inputs/dataset.tsv`
- Size: 137 bytes

```text
USUBJID	AVISITN	PARAMCD	AVAL
01	-1	SCREEN	8
01	1	BASE	10
01	2	POST	12
02	-1	SCREEN	9
02	1	POST	11
02	2	POST	13
03	1	BASE	20
03	2	POST	22
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_relative/solution.R`
- Size: 592 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

dataset <- read.delim(
  file.path("inputs", "dataset.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

result <- admiral::filter_relative(
  dataset = dataset,
  by_vars = exprs(USUBJID),
  order = exprs(AVISITN),
  condition = PARAMCD == "BASE",
  mode = "first",
  selection = "before",
  inclusive = TRUE,
  keep_no_ref_groups = FALSE,
  check_type = "warning"
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/filter_relative/outputs/result.csv`
- Size: 81 bytes

```csv
"USUBJID","AVISITN","PARAMCD","AVAL"
1,-1,"SCREEN",8
1,1,"BASE",10
3,1,"BASE",20
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(readr)
library(dplyr)

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
adsl <- read_tsv(
  file = file.path("inputs", "dataset.tsv"),
  col_types = cols()
)

# Apply "filter relative" per admiral clinical task contract:
# Keep records with AVISITN >= 1 and where a baseline (AVISITN == 1 & PARAMCD == "BASE")
# exists for the same USUBJID and PARAMCD
baseline <- adsl %>%
  filter(AVISITN == 1, PARAMCD == "BASE") %>%
  select(USUBJID, PARAMCD)

result <- adsl %>%
  semi_join(baseline, by = c("USUBJID", "PARAMCD")) %>%
  filter(AVISITN >= 1) %>%
  select(USUBJID, AVISITN, PARAMCD, AVAL)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__filter_relative/sample_00/case_01/llm_outputs/result.csv`
- Size: 55 bytes

```csv
USUBJID,AVISITN,PARAMCD,AVAL
01,1,BASE,10
03,1,BASE,20
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__filter_relative/sample_00/case_01/stderr.txt`
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
  "status": "FAIL",
  "failure_stage": "schema_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "output_bad",
      "tier_value": "output_bad",
      "failure_stage": "schema_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "output_bad",
          "failure_stage": "schema_mismatch",
          "reason": "Shape mismatch: ref=(3, 4) vs llm=(2, 4)"
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
        "comparison_reasons": {
          "result.csv": {
            "stage": "schema_mismatch",
            "tier": "output_bad",
            "reason": "Shape mismatch: ref=(3, 4) vs llm=(2, 4)"
          }
        }
      }
    }
  ]
}
```
