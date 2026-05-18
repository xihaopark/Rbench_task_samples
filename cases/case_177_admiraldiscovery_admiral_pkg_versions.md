# Case 177: pharmaverse/admiraldiscovery/admiral_pkg_versions

## Case Metadata

- Task ID: `pharmaverse/admiraldiscovery/admiral_pkg_versions`
- Package: `admiraldiscovery`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: exact environment version string

## Prompt

```text
Write an R script to perform admiral pkg versions using the admiraldiscovery clinical task contract.

Input: none
Output: result.csv


Required columns for result.csv: id, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.
```

## Input Data

No input files.

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldiscovery/admiral_pkg_versions/solution.R`
- Size: 363 bytes

```r
suppressPackageStartupMessages(library(admiraldiscovery))

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

result <- admiraldiscovery::admiral_pkg_versions()
result_df <- data.frame(
  id = seq_along(result),
  result = as.character(result),
  stringsAsFactors = FALSE
)

write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiraldiscovery/admiral_pkg_versions/outputs/result.csv`
- Size: 127 bytes

```csv
"id","result"
1,"admiral v1.4.1, admiralonco v1.4.0, admiralophtha v1.4.0, admiralvaccine v0.6.0, and admiralmetabolic v0.3.0"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(jsonlite)
  library(tools)
})

# Ensure outputs directory exists
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Determine package path and DESCRIPTION file
pkg_path <- find.package("admiraldiscovery", quiet = TRUE)
if (length(pkg_path) == 0) {
  stop("Package 'admiraldiscovery' not found. Please install it before running this script.")
}

desc_file <- file.path(pkg_path, "DESCRIPTION")
if (!file.exists(desc_file)) {
  stop("DESCRIPTION file for 'admiraldiscovery' not found.")
}

# Read DESCRIPTION
desc <- read.dcf(desc_file)
if (!"admiraldiscovery" %in% desc[, "Package"]) {
  stop("Loaded package is not 'admiraldiscovery'.")
}

# Extract relevant fields
pkg_version <- if ("Version" %in% colnames(desc)) desc[, "Version"] else NA_character_
pkg_title   <- if ("Title"   %in% colnames(desc)) desc[, "Title"]   else NA_character_
pkg_desc    <- if ("Description" %in% colnames(desc)) desc[, "Description"] else NA_character_
pkg_maint   <- if ("Maintainer"  %in% colnames(desc)) desc[, "Maintainer"]  else NA_character_
pkg_date    <- if ("Date"        %in% colnames(desc)) desc[, "Date"]        else NA_character_
pkg_url     <- if ("URL"         %in% colnames(desc)) desc[, "URL"]         else NA_character_

# Build result object following a simple clinical task contract style
result_list <- list(
  package = "admiraldiscovery",
  version = pkg_version,
  title = pkg_title,
  description = pkg_desc,
  maintainer = pkg_maint,
  date = pkg_date,
  url = pkg_url,
  timestamp = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
  r_version = R.version$version.string,
  platform = R.version$platform
)

result_json <- toJSON(result_list, auto_unbox = TRUE, pretty = FALSE)

# Create result data frame for CSV
out_df <- data.frame(
  id = "admiral_pkg_versions",
  result = result_json,
  stringsAsFactors = FALSE
)

# Write result.csv
write.csv(out_df, file = file.path("outputs", "result.csv"), row.names = FALSE, quote = TRUE)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldiscovery__admiral_pkg_versions/sample_00/case_01/llm_outputs/result.csv`
- Size: 622 bytes

```csv
"id","result"
"admiral_pkg_versions","{""package"":""admiraldiscovery"",""version"":""0.5.0"",""title"":""Discover admiral Functions"",""description"":""Package exports a function that creates an interactive gt or\nreactable table to help users discover the admiral functions that are\nused to derive ADaM variables."",""maintainer"":""Jeff Dickinson <jeffowf@gmail.com>"",""date"":null,""url"":""https://pharmaverse.github.io/admiraldiscovery/,\nhttps://github.com/pharmaverse/admiraldiscovery"",""timestamp"":""2026-05-18T13:25:20Z"",""r_version"":""R version 4.5.2 (2025-10-31)"",""platform"":""x86_64-pc-linux-gnu""}"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiraldiscovery__admiral_pkg_versions/sample_00/case_01/stderr.txt`
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
          "reason": "Numeric missingness mismatch in column: id"
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
            "reason": "Numeric missingness mismatch in column: id"
          }
        }
      }
    }
  ]
}
```
