# Case 158: pharmaverse/admiral/list_tte_source_objects

## Case Metadata

- Task ID: `pharmaverse/admiral/list_tte_source_objects`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform list tte source objects using the admiral clinical task contract.

Input: package.tsv
Output: result.csv


Required columns for result.csv: object, dataset_name, filter, date, censor, set_values_to
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### package.tsv (16 bytes)
package
admiral
```

## Input Data

### `package.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/list_tte_source_objects/inputs/package.tsv`
- Size: 16 bytes

```text
package
admiral
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/list_tte_source_objects/solution.R`
- Size: 357 bytes

```r
suppressPackageStartupMessages(library(admiral))

package <- as.character(read.delim(file.path("inputs", "package.tsv"), check.names = FALSE, stringsAsFactors = FALSE)[[1]][1])
result <- admiral::list_tte_source_objects(package = package)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/list_tte_source_objects/outputs/result.csv`
- Size: 1962 bytes

```csv
"object","dataset_name","filter","date","censor","set_values_to"
"ae_gr3_event","adae","TRTEMFL == ""Y"" & ATOXGR == ""3""","ASTDT",0,"EVNTDESC: ""GRADE 3 ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_wd_event","adae","TRTEMFL == ""Y"" & AEACN == ""DRUG WITHDRAWN""","ASTDT",0,"EVNTDESC: ""ADVERSE EVENT LEADING TO DRUG WITHDRAWAL""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_gr35_event","adae","TRTEMFL == ""Y"" & ATOXGR %in% c(""3"", ""4"", ""5"")","ASTDT",0,"EVNTDESC: ""GRADE 3-5 ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"lastalive_censor","adsl","NULL","LSTALVDT",1,"EVNTDESC: ""ALIVE""<br>SRCDOM: ""ADSL""<br>SRCVAR: ""LSTALVDT"""
"ae_gr1_event","adae","TRTEMFL == ""Y"" & ATOXGR == ""1""","ASTDT",0,"EVNTDESC: ""GRADE 1 ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_ser_event","adae","TRTEMFL == ""Y"" & AESER == ""Y""","ASTDT",0,"EVNTDESC: ""SERIOUS ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_gr2_event","adae","TRTEMFL == ""Y"" & ATOXGR == ""2""","ASTDT",0,"EVNTDESC: ""GRADE 2 ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_event","adae","TRTEMFL == ""Y""","ASTDT",0,"EVNTDESC: ""ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_gr4_event","adae","TRTEMFL == ""Y"" & ATOXGR == ""4""","ASTDT",0,"EVNTDESC: ""GRADE 4 ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_gr5_event","adae","TRTEMFL == ""Y"" & ATOXGR == ""5""","ASTDT",0,"EVNTDESC: ""GRADE 5 ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"ae_sev_event","adae","TRTEMFL == ""Y"" & AESEV == ""SEVERE""","ASTDT",0,"EVNTDESC: ""SEVERE ADVERSE EVENT""<br>SRCDOM: ""ADAE""<br>SRCVAR: ""ASTDT""<br>SRCSEQ: AESEQ"
"death_event","adsl","DTHFL == ""Y""","DTHDT",0,"EVNTDESC: ""DEATH""<br>SRCDOM: ""ADSL""<br>SRCVAR: ""DTHDT"""
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

# Load required packages
suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
  library(purrr)
  library(fs)
})

# Create outputs directory if it does not exist
if (!dir_exists("outputs")) dir_create("outputs")

# Read package.tsv
pkg_df <- read_tsv("inputs/package.tsv", show_col_types = FALSE)
pkg <- pkg_df$package[1]

# Load package
suppressPackageStartupMessages(library(pkg, character.only = TRUE))

# Helper to safely get object from namespace
get_obj <- function(x, pkg) {
  getFromNamespace(x, pkg)
}

# List all objects in package namespace
objs <- getNamespaceExports(pkg)

# Identify TTE source objects: assume objects containing "tte" or "TTE"
tte_objs <- objs[str_detect(objs, regex("tte", ignore_case = TRUE))]

# Fallback: if no obvious TTE objects, search all objects for class with "tte"
if (length(tte_objs) == 0) {
  all_objs <- objs
  tte_flag <- map_lgl(all_objs, function(o) {
    obj <- tryCatch(get_obj(o, pkg), error = function(e) NULL)
    if (is.null(obj)) return(FALSE)
    cl <- class(obj)
    any(str_detect(cl, regex("tte", ignore_case = TRUE)))
  })
  tte_objs <- all_objs[tte_flag]
}

# Extract fields for each TTE object
res <- map_dfr(tte_objs, function(o) {
  obj <- tryCatch(get_obj(o, pkg), error = function(e) NULL)
  if (is.null(obj)) {
    tibble(
      object = o,
      dataset_name = NA_character_,
      filter = NA_character_,
      date = NA_character_,
      censor = NA_character_,
      set_values_to = NA_character_
    )
  } else {
    # Try to extract named elements commonly used in TTE source objects
    dataset_name <- tryCatch(obj$dataset_name, error = function(e) NA_character_)
    filter      <- tryCatch(obj$filter,       error = function(e) NA_character_)
    date        <- tryCatch(obj$date,         error = function(e) NA_character_)
    censor      <- tryCatch(obj$censor,       error = function(e) NA_character_)
    set_values_to <- tryCatch(obj$set_values_to, error = function(e) NA_character_)

    # Coerce non-character elements to deparsed text
    to_chr <- function(x) {
      if (is.null(x) || (length(x) == 1 && is.na(x))) return(NA_character_)
      if (is.character(x)) return(paste(x, collapse = " "))
      paste(deparse(x), collapse = " ")
    }

    tibble(
      object = o,
      dataset_name = to_chr(dataset_name),
      filter = to_chr(filter),
      date = to_chr(date),
      censor = to_chr(censor),
      set_values_to = to_chr(set_values_to)
    )
  }
})

# Write result
write_csv(res, "outputs/result.csv", na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__list_tte_source_objects/sample_00/case_01/llm_outputs/result.csv`
- Size: 104 bytes

```csv
object,dataset_name,filter,date,censor,set_values_to
derive_param_tte,,,,,
list_tte_source_objects,,,,,
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__list_tte_source_objects/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(12, 6) vs llm=(2, 6)"
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
            "reason": "Shape mismatch: ref=(12, 6) vs llm=(2, 6)"
          }
        }
      }
    }
  ]
}
```
