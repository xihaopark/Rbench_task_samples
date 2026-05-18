# Case 157: pharmaverse/admiral/list_all_templates

## Case Metadata

- Task ID: `pharmaverse/admiral/list_all_templates`
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
Write an R script to perform list all templates using the admiral clinical task contract.

Input: package.tsv
Output: result.csv


Required columns for result.csv: template
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### package.tsv (18 bytes)
package
"admiral"
```

## Input Data

### `package.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/list_all_templates/inputs/package.tsv`
- Size: 18 bytes

```text
package
"admiral"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/list_all_templates/solution.R`
- Size: 486 bytes

```r
suppressPackageStartupMessages(library(admiral))

package_df <- read.delim(file.path("inputs", "package.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
package <- as.character(package_df[[ncol(package_df)]][1])
if (package == "test_value" || !nzchar(package)) package <- "admiral"

result <- admiral::list_all_templates(package = package)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(template = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/list_all_templates/outputs/result.csv`
- Size: 105 bytes

```csv
"template"
"ADAB"
"ADAE"
"ADCM"
"ADEG"
"ADEX"
"ADLB"
"ADLBHY"
"ADMH"
"ADPC"
"ADPP"
"ADPPK"
"ADSL"
"ADVS"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(jsonlite)
  library(tools)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read package.tsv
pkg_df <- read.delim(
  file = file.path("inputs", "package.tsv"),
  header = TRUE,
  sep = "\t",
  quote = "\"",
  stringsAsFactors = FALSE
)

# Get package name
pkg <- pkg_df$package[1]

# Ensure package is installed and load it
if (!requireNamespace(pkg, quietly = TRUE)) {
  install.packages(pkg, repos = "https://cloud.r-project.org")
}
suppressPackageStartupMessages(library(pkg, character.only = TRUE))

# Use admiral clinical task contract to list templates
# Assuming admiral exports this via admiraldev-style contract helpers
# and that the function is named "clinical_task_contract"
ctc_fun <- get("clinical_task_contract", asNamespace(pkg))

# Get contract information
ctc <- ctc_fun()

# Expecting templates listed in a component named "template" or "templates"
if (!is.null(ctc$templates)) {
  templates <- ctc$templates
} else if (!is.null(ctc$template)) {
  templates <- ctc$template
} else if (!is.null(ctc[["templates"]])) {
  templates <- ctc[["templates"]]
} else if (!is.null(ctc[["template"]])) {
  templates <- ctc[["template"]]
} else {
  # Fallback: try to infer from any character vector element named like templates
  char_elems <- Filter(is.character, ctc)
  if (length(char_elems) == 0) {
    templates <- character(0)
  } else if (!is.null(names(char_elems))) {
    idx <- grep("template", names(char_elems), ignore.case = TRUE)
    if (length(idx) > 0) {
      templates <- char_elems[[idx[1]]]
    } else {
      templates <- unlist(char_elems, use.names = FALSE)
    }
  } else {
    templates <- unlist(char_elems, use.names = FALSE)
  }
}

templates <- unique(as.character(templates))
templates <- templates[!is.na(templates) & nzchar(templates)]

result <- data.frame(
  template = templates,
  stringsAsFactors = FALSE
)

write.csv(
  result,
  file = file.path("outputs", "result.csv"),
  row.names = FALSE,
  quote = TRUE
)
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__list_all_templates/sample_00/case_01/stderr.txt`
- Size: 1244 bytes

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
Error in get("clinical_task_contract", asNamespace(pkg)) :
  object 'clinical_task_contract' not found
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
