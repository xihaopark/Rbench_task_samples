# Case 040: pharmaverse/aNCA/parse_annotation

## Case Metadata

- Task ID: `pharmaverse/aNCA/parse_annotation`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform parse annotation using the aNCA clinical task contract.

Input: data.tsv, text.tsv
Output: result.csv


Required columns for result.csv: text, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (85 bytes)
PARAMCD	PARAM	UNIT
AUC	Area under the curve	h*ng/mL
CMAX	Maximum concentration	ng/mL

### text.tsv (35 bytes)
text
Dose-normalized AUC (h*ng/mL)
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/parse_annotation/inputs/data.tsv`
- Size: 85 bytes

```text
PARAMCD	PARAM	UNIT
AUC	Area under the curve	h*ng/mL
CMAX	Maximum concentration	ng/mL
```

### `text.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/parse_annotation/inputs/text.tsv`
- Size: 35 bytes

```text
text
Dose-normalized AUC (h*ng/mL)
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/parse_annotation/solution.R`
- Size: 365 bytes

```r
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
read_tsv <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)
text <- as.character(read_tsv("text")[[1]])
write.csv(data.frame(text = text, result = text, stringsAsFactors = FALSE), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/parse_annotation/outputs/result.csv`
- Size: 80 bytes

```csv
"text","result"
"Dose-normalized AUC (h*ng/mL)","Dose-normalized AUC (h*ng/mL)"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
  library(jsonlite)
})

# Paths
input_dir  <- "inputs"
output_dir <- "outputs"
data_path  <- file.path(input_dir, "data.tsv")
text_path  <- file.path(input_dir, "text.tsv")
out_path   <- file.path(output_dir, "result.csv")

# Create outputs dir if needed
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

# Read inputs
data_dt <- fread(data_path, sep = "\t", header = TRUE, quote = "")
text_dt <- fread(text_path, sep = "\t", header = TRUE, quote = "")

# Simple parsing: match PARAM and UNIT occurrences in text
parse_one <- function(txt, ref_dt) {
  matches <- list()
  for (i in seq_len(nrow(ref_dt))) {
    row <- ref_dt[i]
    found_param <- grepl(row$PARAM, txt, fixed = TRUE)
    found_unit  <- grepl(row$UNIT,  txt, fixed = TRUE)
    if (found_param || found_unit) {
      matches[[length(matches) + 1]] <- list(
        PARAMCD = row$PARAMCD,
        PARAM   = row$PARAM,
        UNIT    = row$UNIT,
        found_param = found_param,
        found_unit  = found_unit
      )
    }
  }
  if (length(matches) == 0) {
    return(toJSON(list(), auto_unbox = TRUE))
  }
  toJSON(matches, auto_unbox = TRUE)
}

result_dt <- copy(text_dt)
result_dt[, result := vapply(text, parse_one, character(1), ref_dt = data_dt)]

fwrite(result_dt[, .(text, result)], out_path)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__parse_annotation/sample_00/case_01/llm_outputs/result.csv`
- Size: 286 bytes

```csv
text,result
Dose-normalized AUC (h*ng/mL),"[{""PARAMCD"":""AUC"",""PARAM"":""Area under the curve"",""UNIT"":""h*ng/mL"",""found_param"":false,""found_unit"":true},{""PARAMCD"":""CMAX"",""PARAM"":""Maximum concentration"",""UNIT"":""ng/mL"",""found_param"":false,""found_unit"":true}]"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__parse_annotation/sample_00/case_01/stderr.txt`
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
