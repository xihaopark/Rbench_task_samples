# Case 194: pharmaverse/sdtmchecks/pass

## Case Metadata

- Task ID: `pharmaverse/sdtmchecks/pass`
- Package: `sdtmchecks`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: simple prompt dropped boolean TRUE return contract

## Prompt

```text
Write an R script to perform pass using the sdtmchecks clinical task contract.

Input: none
Output: result.csv


Required columns for result.csv: result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.
```

## Input Data

No input files.

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtmchecks/pass/solution.R`
- Size: 283 bytes

```r
suppressPackageStartupMessages(library(sdtmchecks))

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

result <- sdtmchecks::pass()
result_df <- data.frame(result = unname(as.logical(result)))

write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtmchecks/pass/outputs/result.csv`
- Size: 14 bytes

```csv
"result"
TRUE
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required package ---------------------------------------------------
suppressPackageStartupMessages({
  if (!requireNamespace("sdtmchecks", quietly = TRUE)) {
    stop("Package 'sdtmchecks' is required but not installed.")
  }
})

library(sdtmchecks)

# Create outputs directory ------------------------------------------------
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
}

# Run sdtmchecks contract / task ------------------------------------------
# Assumes that the sdtmchecks clinical task contract is implemented as a
# function that can be called to validate inputs/ and return pass/fail.
# Adapt the function name/usage here if your contract is different.

# Example: using a generic contract runner
result_flag <- "FAIL"

try({
  # Example contract runner call; replace with the actual function
  # for your specific clinical task contract if different.
  #
  # The assumption is that this function:
  #   - reads SDTM data from 'inputs/'
  #   - performs checks defined by the clinical task contract
  #   - returns TRUE/FALSE or "PASS"/"FAIL"
  #
  # Here we try a few reasonable conventions:

  if (exists("run_clinical_task_contract", where = asNamespace("sdtmchecks"))) {
    res <- sdtmchecks::run_clinical_task_contract(input_dir = "inputs")
  } else if (exists("run_contract", where = asNamespace("sdtmchecks"))) {
    res <- sdtmchecks::run_contract(input_dir = "inputs")
  } else if (exists("run_checks", where = asNamespace("sdtmchecks"))) {
    res <- sdtmchecks::run_checks(path = "inputs")
  } else {
    stop("No suitable clinical task contract runner found in 'sdtmchecks'.")
  }

  if (is.logical(res)) {
    result_flag <- ifelse(isTRUE(res), "PASS", "FAIL")
  } else if (is.character(res)) {
    # Normalize string to PASS/FAIL
    res_up <- toupper(trimws(res[1]))
    if (res_up %in% c("PASS", "OK", "SUCCESS")) {
      result_flag <- "PASS"
    } else {
      result_flag <- "FAIL"
    }
  } else {
    # If result object has a status field
    if (is.list(res) && !is.null(res$status)) {
      status_up <- toupper(trimws(as.character(res$status)))
      if (status_up %in% c("PASS", "OK", "SUCCESS")) {
        result_flag <- "PASS"
      } else {
        result_flag <- "FAIL"
      }
    } else {
      result_flag <- "FAIL"
    }
  }
}, silent = TRUE)

# Write result.csv --------------------------------------------------------
result_df <- data.frame(result = result_flag, stringsAsFactors = FALSE)

write.csv(
  result_df,
  file = file.path("outputs", "result.csv"),
  row.names = FALSE,
  quote = TRUE
)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtmchecks__pass/sample_00/case_01/llm_outputs/result.csv`
- Size: 16 bytes

```csv
"result"
"FAIL"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtmchecks__pass/sample_00/case_01/stderr.txt`
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
  "status": "FAIL",
  "failure_stage": "value_mismatch",
  "score": 0.0,
  "message": "Failed at case_embedded",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "FAIL",
      "tier": "schema_ok",
      "tier_value": "schema_ok",
      "failure_stage": "value_mismatch",
      "comparison": {
        "result.csv": {
          "match": false,
          "tier": "schema_ok",
          "failure_stage": "value_mismatch",
          "reason": "Numeric missingness mismatch in column: result"
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
            "stage": "value_mismatch",
            "tier": "schema_ok",
            "reason": "Numeric missingness mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
