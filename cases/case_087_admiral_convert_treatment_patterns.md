# Case 087: pharmaverse/admiral/convert_treatment_patterns

## Case Metadata

- Task ID: `pharmaverse/admiral/convert_treatment_patterns`
- Package: `admiral`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform convert treatment patterns using the admiral clinical task contract.

Input: treatment_duration.tsv, xxtpt.tsv
Output: result.csv


Required columns for result.csv: xxtpt, treatment_duration, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### treatment_duration.tsv (40 bytes)
treatment_duration
72
72
72
72
72
... [2 more lines omitted]

### xxtpt.tsv (127 bytes)
xxtpt
START OF TREATMENT
PRE-DOSE
30 MIN AFTER START
2 HOURS AFTER START
END OF TREATMENT
... [2 more lines omitted]
```

## Input Data

### `treatment_duration.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_treatment_patterns/inputs/treatment_duration.tsv`
- Size: 40 bytes

```text
treatment_duration
72
72
72
72
72
72
72
```

### `xxtpt.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_treatment_patterns/inputs/xxtpt.tsv`
- Size: 127 bytes

```text
xxtpt
START OF TREATMENT
PRE-DOSE
30 MIN AFTER START
2 HOURS AFTER START
END OF TREATMENT
4 HOURS BEFORE END
6 HOURS AFTER END
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_treatment_patterns/solution.R`
- Size: 1197 bytes

```r
xxtpt <- as.character(read.delim(file.path("inputs", "xxtpt.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$xxtpt)
treatment_duration <- as.numeric(read.delim(file.path("inputs", "treatment_duration.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$treatment_duration)

parse_hours <- function(label, duration) {
  text <- toupper(trimws(label))
  number <- suppressWarnings(as.numeric(sub(".*?([0-9]+(?:\\.[0-9]+)?).*", "\\1", text)))
  if (text == "START OF TREATMENT") {
    0
  } else if (text == "PRE-DOSE") {
    -1
  } else if (grepl("MIN AFTER START", text)) {
    number / 60
  } else if (grepl("HOURS? AFTER START", text)) {
    number
  } else if (text == "END OF TREATMENT") {
    duration
  } else if (grepl("HOURS? BEFORE END", text)) {
    duration - number
  } else if (grepl("HOURS? AFTER END", text)) {
    duration + number
  } else {
    NA_real_
  }
}

result <- mapply(parse_hours, xxtpt, treatment_duration)
result_df <- data.frame(xxtpt = xxtpt, treatment_duration = treatment_duration, result = as.numeric(result), stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/convert_treatment_patterns/outputs/result.csv`
- Size: 214 bytes

```csv
"xxtpt","treatment_duration","result"
"START OF TREATMENT",72,0
"PRE-DOSE",72,-1
"30 MIN AFTER START",72,0.5
"2 HOURS AFTER START",72,2
"END OF TREATMENT",72,72
"4 HOURS BEFORE END",72,68
"6 HOURS AFTER END",72,78
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
treatment_duration <- read_tsv(
  file = file.path("inputs", "treatment_duration.tsv"),
  show_col_types = FALSE
)

xxtpt <- read_tsv(
  file = file.path("inputs", "xxtpt.tsv"),
  show_col_types = FALSE
)

# Ensure equal length by recycling the shorter vector if needed
n_out <- max(nrow(treatment_duration), nrow(xxtpt))

td_vec <- rep(treatment_duration$treatment_duration, length.out = n_out)
tp_vec <- rep(xxtpt$xxtpt, length.out = n_out)

df <- tibble(
  xxtpt = tp_vec,
  treatment_duration = td_vec
)

# Example conversion of treatment patterns per admiral-like logic:
# Map text patterns to relative numeric times within treatment duration
df <- df %>%
  mutate(
    result = case_when(
      xxtpt == "START OF TREATMENT"        ~ 0,
      xxtpt == "PRE-DOSE"                  ~ -0.5,
      xxtpt == "30 MIN AFTER START"        ~ 0.5 / 60 * treatment_duration,
      xxtpt == "2 HOURS AFTER START"       ~ 2 / 24 * treatment_duration,
      xxtpt == "END OF TREATMENT"          ~ treatment_duration,
      TRUE                                 ~ NA_real_
    )
  )

# Write output
write_csv(df %>% select(xxtpt, treatment_duration, result),
          file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_treatment_patterns/sample_00/case_01/llm_outputs/result.csv`
- Size: 196 bytes

```csv
xxtpt,treatment_duration,result
START OF TREATMENT,72,0
PRE-DOSE,72,-0.5
30 MIN AFTER START,72,0.6
2 HOURS AFTER START,72,6
END OF TREATMENT,72,72
4 HOURS BEFORE END,72,NA
6 HOURS AFTER END,72,NA
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__convert_treatment_patterns/sample_00/case_01/stderr.txt`
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
