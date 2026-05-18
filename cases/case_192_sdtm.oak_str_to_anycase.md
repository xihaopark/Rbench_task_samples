# Case 192: pharmaverse/sdtm.oak/str_to_anycase

## Case Metadata

- Task ID: `pharmaverse/sdtm.oak/str_to_anycase`
- Package: `sdtm.oak`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform str to anycase using the sdtm.oak clinical task contract.

Input: x.tsv
Output: result.csv


Required columns for result.csv: x, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### x.tsv (15 bytes)
x
abc
Dose1
Ae
```

## Input Data

### `x.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/str_to_anycase/inputs/x.tsv`
- Size: 15 bytes

```text
x
abc
Dose1
Ae
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/str_to_anycase/solution.R`
- Size: 595 bytes

```r
x <- as.character(read.delim(file.path("inputs", "x.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$x)
convert <- function(value) {
  chars <- strsplit(value, "", fixed = TRUE)[[1]]
  paste0(vapply(chars, function(ch) {
    if (grepl("^[A-Za-z]$", ch)) {
      paste0("[", toupper(ch), tolower(ch), "]")
    } else {
      ch
    }
  }, character(1)), collapse = "")
}
result_df <- data.frame(x = x, result = vapply(x, convert, character(1)), stringsAsFactors = FALSE)
dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/sdtm.oak/str_to_anycase/outputs/result.csv`
- Size: 78 bytes

```csv
"x","result"
"abc","[Aa][Bb][Cc]"
"Dose1","[Dd][Oo][Ss][Ee]1"
"Ae","[Aa][Ee]"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input
x_df <- read_tsv(
  file = file.path("inputs", "x.tsv"),
  col_types = cols(.default = col_character())
)

# sdtm.oak-style clinical anycase mapping
to_anycase <- function(x) {
  case_when(
    # Common SDTM-style clinical terms
    str_to_lower(x) == "ae"        ~ "AE",
    str_to_lower(x) == "aes"       ~ "AEs",
    str_to_lower(x) == "sae"       ~ "SAE",
    str_to_lower(x) == "saes"      ~ "SAEs",
    str_to_lower(x) == "conmed"    ~ "ConMed",
    str_to_lower(x) == "conmeds"   ~ "ConMeds",
    str_to_lower(x) == "dose1"     ~ "DOSE1",
    str_to_lower(x) == "dose2"     ~ "DOSE2",
    str_to_lower(x) == "dose"      ~ "Dose",
    str_to_lower(x) == "subject"   ~ "Subject",
    str_to_lower(x) == "patient"   ~ "Patient",
    str_to_lower(x) == "visit"     ~ "Visit",
    str_to_lower(x) == "visits"    ~ "Visits",
    str_to_lower(x) == "screening" ~ "Screening",
    str_to_lower(x) == "baseline"  ~ "Baseline",
    str_to_lower(x) == "followup"  ~ "FollowUp",
    str_to_lower(x) == "ecg"       ~ "ECG",
    str_to_lower(x) == "lab"       ~ "Lab",
    str_to_lower(x) == "labs"      ~ "Labs",
    str_to_lower(x) == "pk"        ~ "PK",
    str_to_lower(x) == "pd"        ~ "PD",
    str_to_lower(x) == "crf"       ~ "CRF",
    str_to_lower(x) == "sdtm"      ~ "SDTM",
    str_to_lower(x) == "adam"      ~ "ADaM",
    str_to_lower(x) == "dm"        ~ "DM",
    str_to_lower(x) == "ae"        ~ "AE",
    str_to_lower(x) == "cm"        ~ "CM",
    str_to_lower(x) == "vs"        ~ "VS",
    str_to_lower(x) == "ex"        ~ "EX",
    str_to_lower(x) == "mh"        ~ "MH",
    str_to_lower(x) == "eg"        ~ "EG",
    str_to_lower(x) == "lb"        ~ "LB",
    str_to_lower(x) == "qs"        ~ "QS",

    # Default: Title Case, but preserve all-caps and all-lower
    str_detect(x, "^[A-Z0-9_]+$")  ~ x,
    str_detect(x, "^[a-z0-9_]+$")  ~ x,
    TRUE                           ~ str_to_title(x)
  )
}

result_df <- x_df %>%
  mutate(result = to_anycase(x)) %>%
  select(x, result)

write_csv(result_df, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtm.oak__str_to_anycase/sample_00/case_01/llm_outputs/result.csv`
- Size: 35 bytes

```csv
x,result
abc,abc
Dose1,DOSE1
Ae,AE
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__sdtm.oak__str_to_anycase/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: result"
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
            "reason": "Value mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
