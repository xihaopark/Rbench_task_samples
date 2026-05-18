# Case 016: pharmaverse/aNCA/detect_study_types

## Case Metadata

- Task ID: `pharmaverse/aNCA/detect_study_types`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `llm_error`
- Attribution note: schema matched but values wrong

## Prompt

```text
Write an R script to perform detect study types using the aNCA clinical task contract.

Input: data.tsv, groups.tsv, metabfl_column.tsv, route_column.tsv, volume_column.tsv
Output: result.csv


Required columns for result.csv: subject, study_type
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### data.tsv (136 bytes)
subject	period	route	urine_volume	metabfl
101	1	oral	0	parent
101	2	oral	0	parent
102	1	iv infusion	0	parent
103	1	urine	150	metabolite

### groups.tsv (15 bytes)
groups
subject

### metabfl_column.tsv (23 bytes)
metabfl_column
metabfl

### route_column.tsv (19 bytes)
route_column
route

### volume_column.tsv (27 bytes)
volume_column
urine_volume
```

## Input Data

### `data.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/inputs/data.tsv`
- Size: 136 bytes

```text
subject	period	route	urine_volume	metabfl
101	1	oral	0	parent
101	2	oral	0	parent
102	1	iv infusion	0	parent
103	1	urine	150	metabolite
```

### `groups.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/inputs/groups.tsv`
- Size: 15 bytes

```text
groups
subject
```

### `metabfl_column.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/inputs/metabfl_column.tsv`
- Size: 23 bytes

```text
metabfl_column
metabfl
```

### `route_column.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/inputs/route_column.tsv`
- Size: 19 bytes

```text
route_column
route
```

### `volume_column.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/inputs/volume_column.tsv`
- Size: 27 bytes

```text
volume_column
urine_volume
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/solution.R`
- Size: 2294 bytes

```r
read_table <- function(name) {
  read.delim(file.path("inputs", name), check.names = FALSE, stringsAsFactors = FALSE)
}

first_value <- function(df, default = "") {
  if (nrow(df) == 0 || ncol(df) == 0 || is.na(df[[1]][[1]])) return(default)
  as.character(df[[1]][[1]])
}

is_extravascular <- function(route) {
  grepl("^(extravascular|oral|po|subcutaneous|sc|intramuscular|im)$", tolower(route))
}

classify_group <- function(df, route_col, volume_col) {
  if (volume_col %in% names(df)) {
    volume <- suppressWarnings(as.numeric(df[[volume_col]]))
    if (any(!is.na(volume) & volume > 0)) return("Excretion Data")
  }
  route <- if (route_col %in% names(df)) df[[route_col]][[1]] else NA_character_
  multiple <- ("TRTRINT" %in% names(df) && any(!is.na(df$TRTRINT))) || ("DOSNO" %in% names(df) && length(unique(df$DOSNO)) > 1)
  bolus <- "ADOSEDUR" %in% names(df) && suppressWarnings(as.numeric(df$ADOSEDUR[[1]])) == 0
  if (is.na(route)) return("Unknown")
  if (is_extravascular(route)) return(ifelse(multiple, "Multiple Extravascular Doses", "Single Extravascular Dose"))
  if (bolus) return(ifelse(multiple, "Multiple IV Bolus Doses", "Single IV Bolus Dose"))
  ifelse(multiple, "Multiple IV Infusion Doses", "Single IV Infusion Dose")
}

data <- read_table("data.tsv")
groups <- as.character(read_table("groups.tsv")[[1]])
groups <- groups[groups %in% names(data)]
route_col <- first_value(read_table("route_column.tsv"), "route")
volume_col <- first_value(read_table("volume_column.tsv"), "volume")

if (!(route_col %in% names(data)) && !(volume_col %in% names(data))) {
  result <- data.frame(study_type = "unknown", stringsAsFactors = FALSE)
} else if (length(groups) == 0) {
  result <- data.frame(study_type = classify_group(data, route_col, volume_col), stringsAsFactors = FALSE)
} else {
  keys <- unique(data[groups])
  study_type <- character(nrow(keys))
  for (i in seq_len(nrow(keys))) {
    keep <- rep(TRUE, nrow(data))
    for (col in groups) keep <- keep & data[[col]] == keys[[col]][[i]]
    study_type[[i]] <- classify_group(data[keep, , drop = FALSE], route_col, volume_col)
  }
  result <- cbind(keys, study_type = study_type)
}

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/detect_study_types/outputs/result.csv`
- Size: 106 bytes

```csv
"subject","study_type"
101,"Single Extravascular Dose"
102,"Single IV Infusion Dose"
103,"Excretion Data"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

data_path   <- file.path("inputs", "data.tsv")
groups_path <- file.path("inputs", "groups.tsv")
metab_path  <- file.path("inputs", "metabfl_column.tsv")
route_path  <- file.path("inputs", "route_column.tsv")
vol_path    <- file.path("inputs", "volume_column.tsv")

data   <- read_tsv(data_path, show_col_types = FALSE)
groups <- read_tsv(groups_path, show_col_types = FALSE)
metab_col <- read_tsv(metab_path, show_col_types = FALSE)$metabfl_column[1]
route_col <- read_tsv(route_path, show_col_types = FALSE)$route_column[1]
vol_col   <- read_tsv(vol_path, show_col_types = FALSE)$volume_column[1]

subject_col <- groups$groups[1]

if (!subject_col %in% names(data)) stop("Subject column not in data")
if (!metab_col %in% names(data))   stop("Metab flag column not in data")
if (!route_col %in% names(data))   stop("Route column not in data")
if (!vol_col %in% names(data))     stop("Volume column not in data")

d <- data %>%
  mutate(
    .subject = .data[[subject_col]],
    .metabfl = as.character(.data[[metab_col]]),
    .route   = tolower(as.character(.data[[route_col]])),
    .volume  = suppressWarnings(as.numeric(.data[[vol_col]]))
  )

# Heuristic for aNCA study types (clinical task contract style)
# PK: parent only, non-urine routes, volumes zero or NA
# CL: urine route with metabolite data and positive volume
# PKCL: mixture (both IV/oral parent and urine metabolite with volume)
study_summary <- d %>%
  group_by(.subject) %>%
  summarise(
    any_urine_route = any(.route %in% c("urine", "urinary", "urine collection"), na.rm = TRUE),
    any_pos_volume  = any(!is.na(.volume) & .volume > 0),
    any_parent      = any(tolower(.metabfl) %in% c("parent", "p"), na.rm = TRUE),
    any_metabolite  = any(tolower(.metabfl) %in% c("metabolite", "m"), na.rm = TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    study_type = case_when(
      any_urine_route & any_pos_volume & any_metabolite & any_parent ~ "PKCL",
      any_urine_route & any_pos_volume & any_metabolite              ~ "CL",
      TRUE                                                           ~ "PK"
    )
  )

result <- study_summary %>%
  transmute(
    subject = .subject,
    study_type
  ) %>%
  arrange(subject)

write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__detect_study_types/sample_00/case_01/llm_outputs/result.csv`
- Size: 40 bytes

```csv
subject,study_type
101,PK
102,PK
103,CL
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__detect_study_types/sample_00/case_01/stderr.txt`
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
          "reason": "Value mismatch in column: study_type"
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
            "reason": "Value mismatch in column: study_type"
          }
        }
      }
    }
  ]
}
```
