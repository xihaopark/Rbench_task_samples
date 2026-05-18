# Case 057: pharmaverse/admiral/chr2vars

## Case Metadata

- Task ID: `pharmaverse/admiral/chr2vars`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform chr2vars using the admiral clinical task contract.

Input: chr.tsv
Output: result.csv


Required columns for result.csv: chr, symbol
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### chr.tsv (28 bytes)
chr
STUDYID
USUBJID
PARAMCD
```

## Input Data

### `chr.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/chr2vars/inputs/chr.tsv`
- Size: 28 bytes

```text
chr
STUDYID
USUBJID
PARAMCD
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/chr2vars/solution.R`
- Size: 527 bytes

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

chr_df <- read.delim(file.path("inputs", "chr.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
chr <- as.character(chr_df[[1]])
result <- admiral::chr2vars(chr)

dir.create("outputs", showWarnings = FALSE)
saveRDS(result, file.path("outputs", "result.rds"))
write.csv(data.frame(chr = chr, symbol = vapply(result, as.character, character(1)), stringsAsFactors = FALSE), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/chr2vars/outputs/result.csv`
- Size: 75 bytes

```csv
"chr","symbol"
"STUDYID","STUDYID"
"USUBJID","USUBJID"
"PARAMCD","PARAMCD"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)
library(stringr)
library(fs)

# Create outputs directory if it does not exist
if (!dir_exists("outputs")) {
  dir_create("outputs")
}

# Read input
chr <- read_tsv(
  file = "inputs/chr.tsv",
  col_types = cols(.default = col_character())
)

# Derive chr and symbol according to admiral clinical task contract assumptions
# Here we assume PARAMCD contains the "chr" information, and USUBJID the "symbol" placeholder.
# Adapt mapping logic as needed once real metadata is available.
result <- chr %>%
  transmute(
    chr   = PARAMCD,
    symbol = USUBJID
  )

# Keep only required columns and ensure they exist
result <- result %>%
  select(chr, symbol)

# Write output
write_csv(result, "outputs/result.csv", na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__chr2vars/sample_00/case_01/stderr.txt`
- Size: 2123 bytes

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

Error in `transmute()`:
ℹ In argument: `chr = PARAMCD`.
Caused by error:
! object 'PARAMCD' not found
Backtrace:
     ▆
  1. ├─chr %>% transmute(chr = PARAMCD, symbol = USUBJID)
  2. ├─dplyr::transmute(., chr = PARAMCD, symbol = USUBJID)
  3. ├─dplyr:::transmute.data.frame(., chr = PARAMCD, symbol = USUBJID)
  4. │ └─dplyr:::mutate_cols(.data, dots, by)
  5. │   ├─base::withCallingHandlers(...)
  6. │   └─dplyr:::mutate_col(dots[[i]], data, mask, new_columns)
  7. │     └─mask$eval_all_mutate(quo)
  8. │       └─dplyr (local) eval()
  9. └─base::.handleSimpleError(...)
 10.   └─dplyr (local) h(simpleError(msg, call))
 11.     └─rlang::abort(message, class = error_class, parent = parent, call = error_call)
Execution halted
```

## Evaluation Result

```json
{
  "status": "NO_OUTPUT",
  "failure_stage": "execution_failure",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "NO_OUTPUT",
      "tier": "exec_fail",
      "failure_stage": "execution_failure",
      "message": "No output files created",
      "stderr": "[RBioBench Library Aliases] Library aliasing disabled (using stub layer)\n[Admiraldev Stub] Created admiraldev namespace with 10 stub functions\n[RBioBench Stub Layer] Loaded admiraldev stubs\n[aNCA Stub] Created aNCA namespace with 57 stub functions\n[RBioBench Stub Layer] Loaded aNCA stubs\n[Logrx Stub] Created logrx namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded logrx stubs\n[Sdtmchecks Stub] Created sdtmchecks namespace with 2 stub functions\n[RBioBench Stub Layer] Loaded sdtmchecks stubs\n[Other Stubs] Registered 5 stub functions from 5 packages\n[RBioBench Stub Layer] Loaded other package stubs\n[RBioBench Stub Layer] Registered attach hook for admiral\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stubs registered in admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[Admiral Stub] Injected 40 functions into admiral namespace\n[RBioBench Stub Layer] Stub",
      "returncode": 1,
      "diagnostics": {
        "expected_artifacts": [
          "result.csv"
        ],
        "produced_artifacts": [],
        "missing_artifacts": [
          "result.csv"
        ]
      }
    }
  ]
}
```
