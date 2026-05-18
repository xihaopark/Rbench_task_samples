# Case 026: pharmaverse/aNCA/generate_tooltip_text

## Case Metadata

- Task ID: `pharmaverse/aNCA/generate_tooltip_text`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform generate tooltip text using the aNCA clinical task contract.

Input: data.tsv, labels_df.tsv, tooltip_vars.tsv, type.tsv
Output: result.csv


Required columns for result.csv: row_id, tooltip_text
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### labels_df.tsv (94 bytes)
Dataset	Variable	Label
ADPC	id	Subject ID
ADPC	value	Concentration
ADPC	group	Treatment Group

### tooltip_vars.tsv (28 bytes)
tooltip_vars
id
value
group

### type.tsv (10 bytes)
type
ADPC
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_tooltip_text/inputs/data.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `labels_df.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_tooltip_text/inputs/labels_df.tsv`
- Size: 94 bytes

```text
Dataset	Variable	Label
ADPC	id	Subject ID
ADPC	value	Concentration
ADPC	group	Treatment Group
```

### `tooltip_vars.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_tooltip_text/inputs/tooltip_vars.tsv`
- Size: 28 bytes

```text
tooltip_vars
id
value
group
```

### `type.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_tooltip_text/inputs/type.tsv`
- Size: 10 bytes

```text
type
ADPC
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_tooltip_text/solution.R`
- Size: 1986 bytes

```r
suppressPackageStartupMessages({
  has_anca <- requireNamespace("aNCA", quietly = TRUE)
})

data <- read.delim(
  file.path("inputs", "data.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
labels_df <- read.delim(
  file.path("inputs", "labels_df.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
tooltip_vars_df <- read.delim(
  file.path("inputs", "tooltip_vars.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
tooltip_vars <- tooltip_vars_df$tooltip_vars
type_df <- read.delim(
  file.path("inputs", "type.tsv"),
  check.names = FALSE,
  stringsAsFactors = FALSE
)
type <- type_df[[1]][1]

fallback_tooltips <- function(data, labels_df, tooltip_vars, type) {
  if (nrow(data) == 0) {
    return(character())
  }

  tooltip_vars <- tooltip_vars[tooltip_vars %in% names(data)]

  if (length(tooltip_vars) == 0) {
    return(rep("", nrow(data)))
  }

  lookup_label <- function(var_name) {
    required_cols <- c("Dataset", "Variable", "Label")
    if (all(required_cols %in% names(labels_df))) {
      matches <- labels_df$Dataset == type & labels_df$Variable == var_name
      if (any(matches, na.rm = TRUE)) {
        return(labels_df$Label[which(matches)[1]])
      }
    }
    var_name
  }

  tooltip_components <- lapply(tooltip_vars, function(var_name) {
    label <- lookup_label(var_name)
    paste0("<b>", label, "</b>: ", data[[var_name]])
  })

  do.call(paste, c(tooltip_components, sep = "<br>"))
}

if (has_anca && "generate_tooltip_text" %in% getNamespaceExports("aNCA")) {
  tooltips <- aNCA::generate_tooltip_text(data, labels_df, tooltip_vars, type)
} else {
  tooltips <- fallback_tooltips(data, labels_df, tooltip_vars, type)
}

result <- data.frame(
  row_id = seq_along(tooltips),
  tooltip_text = tooltips,
  stringsAsFactors = FALSE
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
unlink(file.path("outputs", c("summary.csv", "result.rds")))
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/generate_tooltip_text/outputs/result.csv`
- Size: 444 bytes

```csv
"row_id","tooltip_text"
1,"<b>Subject ID</b>: 1<br><b>Concentration</b>: 10.5<br><b>Treatment Group</b>: A"
2,"<b>Subject ID</b>: 2<br><b>Concentration</b>: 20.3<br><b>Treatment Group</b>: B"
3,"<b>Subject ID</b>: 3<br><b>Concentration</b>: 30.7<br><b>Treatment Group</b>: A"
4,"<b>Subject ID</b>: 4<br><b>Concentration</b>: 40.2<br><b>Treatment Group</b>: B"
5,"<b>Subject ID</b>: 5<br><b>Concentration</b>: 50.9<br><b>Treatment Group</b>: A"
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

# Read inputs
data_df       <- readr::read_tsv("inputs/data.tsv", col_types = cols(.default = col_character()))
labels_df     <- readr::read_tsv("inputs/labels_df.tsv", col_types = cols(.default = col_character()))
tooltip_vars  <- readr::read_tsv("inputs/tooltip_vars.tsv", col_types = cols(.default = col_character()))
type_df       <- readr::read_tsv("inputs/type.tsv", col_types = cols(.default = col_character()))

dataset_type <- type_df$type[1]

# Filter labels for selected dataset and tooltip vars
label_map <- labels_df %>%
  filter(Dataset == dataset_type,
         Variable %in% tooltip_vars$tooltip_vars) %>%
  select(Variable, Label)

# Ensure all tooltip_vars are present in data
vars <- intersect(tooltip_vars$tooltip_vars, colnames(data_df))

# Build named vector of labels (fallback to variable name if no label)
label_lookup <- setNames(label_map$Label, label_map$Variable)

format_var_value <- function(var, value) {
  label <- if (!is.na(label_lookup[[var]])) label_lookup[[var]] else var
  paste0(label, ": ", value)
}

# Generate tooltip_text
result <- data_df %>%
  mutate(
    row_id = row_number(),
    tooltip_text = purrr::pmap_chr(
      as.list(.),
      function(...) {
        row <- list(...)
        txts <- vapply(
          vars,
          function(v) format_var_value(v, row[[v]]),
          character(1)
        )
        paste(txts, collapse = "\n")
      }
    )
  ) %>%
  select(row_id, tooltip_text)

# Write output
readr::write_csv(result, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__generate_tooltip_text/sample_00/case_01/llm_outputs/result.csv`
- Size: 305 bytes

```csv
row_id,tooltip_text
1,"Subject ID: 1
Concentration: 10.5
Treatment Group: A"
2,"Subject ID: 2
Concentration: 20.3
Treatment Group: B"
3,"Subject ID: 3
Concentration: 30.7
Treatment Group: A"
4,"Subject ID: 4
Concentration: 40.2
Treatment Group: B"
5,"Subject ID: 5
Concentration: 50.9
Treatment Group: A"
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__generate_tooltip_text/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: tooltip_text"
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
            "reason": "Value mismatch in column: tooltip_text"
          }
        }
      }
    }
  ]
}
```
