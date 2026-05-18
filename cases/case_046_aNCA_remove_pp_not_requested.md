# Case 046: pharmaverse/aNCA/remove_pp_not_requested

## Case Metadata

- Task ID: `pharmaverse/aNCA/remove_pp_not_requested`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform remove pp not requested using the aNCA clinical task contract.

Input: pknca_res.tsv
Output: result.csv


Required columns for result.csv: subject, parameter, value, requested
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### pknca_res.tsv (92 bytes)
subject	parameter	value	requested
101	CMAX	10.5	TRUE
101	AUC	125.0	FALSE
102	CMAX	12.1	TRUE
```

## Input Data

### `pknca_res.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/remove_pp_not_requested/inputs/pknca_res.tsv`
- Size: 92 bytes

```text
subject	parameter	value	requested
101	CMAX	10.5	TRUE
101	AUC	125.0	FALSE
102	CMAX	12.1	TRUE
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/remove_pp_not_requested/solution.R`
- Size: 716 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

read_tsv <- function(name) {
  read.delim(file.path("inputs", name), check.names = FALSE, stringsAsFactors = FALSE)
}

is_false_like <- function(x) {
  value <- trimws(tolower(as.character(x)))
  value %in% c("false", "f", "no", "n", "0")
}

pknca_res <- read_tsv("pknca_res.tsv")
result <- pknca_res
flag_cols <- intersect(c("requested", "is_requested", "include", "analyze"), names(result))
if (length(flag_cols) > 0) {
  keep <- rep(TRUE, nrow(result))
  for (col in flag_cols) {
    keep <- keep & !is_false_like(result[[col]])
  }
  result <- result[keep, , drop = FALSE]
}

write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/remove_pp_not_requested/outputs/result.csv`
- Size: 84 bytes

```csv
"subject","parameter","value","requested"
101,"CMAX",10.5,TRUE
102,"CMAX",12.1,TRUE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read input
pknca_res <- read_tsv(
  file = file.path("inputs", "pknca_res.tsv"),
  col_types = cols(
    subject   = col_character(),
    parameter = col_character(),
    value     = col_double(),
    requested = col_logical()
  )
)

# Filter to only requested parameters
result <- pknca_res %>%
  filter(requested) %>%
  select(subject, parameter, value, requested)

# Write output
write_csv(result, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__remove_pp_not_requested/sample_00/case_01/llm_outputs/result.csv`
- Size: 72 bytes

```csv
subject,parameter,value,requested
101,CMAX,10.5,TRUE
102,CMAX,12.1,TRUE
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__remove_pp_not_requested/sample_00/case_01/stderr.txt`
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
