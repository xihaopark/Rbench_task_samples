# Case 195: pharmaverse/tidytlg/add_indent

## Case Metadata

- Task ID: `pharmaverse/tidytlg/add_indent`
- Package: `tidytlg`
- Model: `openai/gpt-5.1`
- Status: `NO_OUTPUT`
- Failure stage: `execution_failure`
- Attribution bucket: `llm_error`
- Attribution note: generated R failed under clear input/output contract

## Prompt

```text
Write an R script to perform add indent using the tidytlg clinical task contract.

Input: df.tsv
Output: result.csv


Required columns for result.csv: anbr, row_type, label, nested_level, group_level, indent
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### df.tsv (152 bytes)
anbr	row_type	label	nested_level	group_level
1	HEADER	Demographics	0	0
1	N	Total	0	0
1	VALUE	Age	0	0
2	TABLE_BY_HEADER	Treatment	0	1
2	VALUE	Drug A	0	1
```

## Input Data

### `df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/tidytlg/add_indent/inputs/df.tsv`
- Size: 152 bytes

```text
anbr	row_type	label	nested_level	group_level
1	HEADER	Demographics	0	0
1	N	Total	0	0
1	VALUE	Age	0	0
2	TABLE_BY_HEADER	Treatment	0	1
2	VALUE	Drug A	0	1
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/tidytlg/add_indent/solution.R`
- Size: 742 bytes

```r
df <- read.delim(file.path("inputs", "df.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
df$nested_level <- as.integer(df$nested_level)
df$group_level <- as.integer(df$group_level)
table_offset <- as.integer(any(df$row_type == "TABLE_BY_HEADER"))
df$indent <- ifelse(
  grepl("BY_HEADER", df$row_type) | df$row_type == "HEADER",
  df$group_level + table_offset,
  ifelse(
    df$row_type == "N",
    1L + df$group_level + table_offset,
    ifelse(
      df$row_type == "VALUE",
      2L + df$group_level + table_offset,
      ifelse(df$row_type == "NESTED", df$nested_level + df$group_level + table_offset, 0L)
    )
  )
)
dir.create("outputs", showWarnings = FALSE)
write.csv(df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/tidytlg/add_indent/outputs/result.csv`
- Size: 201 bytes

```csv
"anbr","row_type","label","nested_level","group_level","indent"
1,"HEADER","Demographics",0,0,1
1,"N","Total",0,0,2
1,"VALUE","Age",0,0,3
2,"TABLE_BY_HEADER","Treatment",0,1,2
2,"VALUE","Drug A",0,1,4
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(tidyr)
  library(tidytlg)
  library(stringr)
})

# ensure outputs directory exists
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# read input
df <- read_tsv(
  file = file.path("inputs", "df.tsv"),
  col_types = cols(
    anbr         = col_double(),
    row_type     = col_character(),
    label        = col_character(),
    nested_level = col_double(),
    group_level  = col_double()
  )
)

# perform add_indent using tidytlg clinical task contract
# infer indenting columns and labels based on provided structure
df_indented <- df %>%
  # ensure correct ordering if not already
  arrange(anbr, group_level, nested_level, row_type) %>%
  add_indent(
    col_label = "label",
    nested_indent = TRUE,
    nested_level = "nested_level",
    group_level = "group_level"
  )

# keep only required columns in required order
result <- df_indented %>%
  select(anbr, row_type, label, nested_level, group_level, indent)

# write output
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

No LLM output artifact was produced.

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__tidytlg__add_indent/sample_00/case_01/stderr.txt`
- Size: 1375 bytes

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
Error in add_indent(., col_label = "label", nested_indent = TRUE, nested_level = "nested_level",  :
  unused arguments (col_label = "label", nested_indent = TRUE, nested_level = "nested_level", group_level = "group_level")
Calls: %>%
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
