# Case 013: pharmaverse/aNCA/create_metabfl

## Case Metadata

- Task ID: `pharmaverse/aNCA/create_metabfl`
- Package: `aNCA`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform create metabfl using the aNCA clinical task contract.

Input: dataset.tsv, metabolites.tsv
Output: result.csv


Required columns for result.csv: id, value, group, category, PARAM, METABFL
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### dataset.tsv (99 bytes)
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

### metabolites.tsv (39 bytes)
metabolites
"AUC"
"CMAX"
"METABOLITE1"
```

## Input Data

### `dataset.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/create_metabfl/inputs/dataset.tsv`
- Size: 99 bytes

```text
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

### `metabolites.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/create_metabfl/inputs/metabolites.tsv`
- Size: 39 bytes

```text
metabolites
"AUC"
"CMAX"
"METABOLITE1"
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/create_metabfl/solution.R`
- Size: 939 bytes

```r
read_tsv <- function(name) {
  path <- file.path("inputs", name)
  if (!file.exists(path)) {
    stop(name, " is required")
  }
  read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
}

first_column <- function(df) {
  if (ncol(df) == 0) {
    return(character())
  }
  df[[1]]
}

scalar_numeric <- function(df) {
  values <- suppressWarnings(as.numeric(first_column(df)))
  values <- values[!is.na(values)]
  if (length(values) == 0) NA_real_ else values[[1]]
}

write_result <- function(result) {
  dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
  write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE, na = "NA")
}

dataset <- read_tsv("dataset.tsv")
metabolites <- as.character(first_column(read_tsv("metabolites.tsv")))
if (!"PARAM" %in% names(dataset)) {
  dataset$PARAM <- "PARAM1"
}
dataset$METABFL <- ifelse(as.character(dataset$PARAM) %in% metabolites, "Y", "N")
write_result(dataset)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/create_metabfl/outputs/result.csv`
- Size: 210 bytes

```csv
"id","value","group","category","PARAM","METABFL"
1,10.5,"A","Type1","PARAM1","N"
2,20.3,"B","Type2","PARAM1","N"
3,30.7,"A","Type1","PARAM1","N"
4,40.2,"B","Type2","PARAM1","N"
5,50.9,"A","Type1","PARAM1","N"
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
dataset_path <- file.path("inputs", "dataset.tsv")
metabolites_path <- file.path("inputs", "metabolites.tsv")

dat <- fread(dataset_path, sep = "\t", header = TRUE)
mets <- fread(metabolites_path, sep = "\t", header = TRUE)

# Ensure columns
required_cols <- c("id", "value", "group", "category")
missing_cols <- setdiff(required_cols, names(dat))
if (length(missing_cols) > 0) {
  stop("Missing required columns in dataset.tsv: ", paste(missing_cols, collapse = ", "))
}

# aNCA clinical task contract: create METABFL flag
# METABFL = "Y" if PARAM corresponds to a metabolite, else "N"
met_vec <- unique(gsub('"', "", mets$metabolites))

# For demonstration, create records for each PARAM per id
# Here we assign PARAM directly from metabolites list
res <- rbindlist(lapply(met_vec, function(p) {
  tmp <- copy(dat)
  tmp[, PARAM := p]
  tmp
}))

res[, METABFL := ifelse(PARAM %in% met_vec, "Y", "N")]

# Keep required columns in specified order
out <- res[, .(id, value, group, category, PARAM, METABFL)]

# Write result
fwrite(out, file.path("outputs", "result.csv"))
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__create_metabfl/sample_00/case_01/llm_outputs/result.csv`
- Size: 398 bytes

```csv
id,value,group,category,PARAM,METABFL
1,10.5,A,Type1,AUC,Y
2,20.3,B,Type2,AUC,Y
3,30.7,A,Type1,AUC,Y
4,40.2,B,Type2,AUC,Y
5,50.9,A,Type1,AUC,Y
1,10.5,A,Type1,CMAX,Y
2,20.3,B,Type2,CMAX,Y
3,30.7,A,Type1,CMAX,Y
4,40.2,B,Type2,CMAX,Y
5,50.9,A,Type1,CMAX,Y
1,10.5,A,Type1,METABOLITE1,Y
2,20.3,B,Type2,METABOLITE1,Y
3,30.7,A,Type1,METABOLITE1,Y
4,40.2,B,Type2,METABOLITE1,Y
5,50.9,A,Type1,METABOLITE1,Y
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__create_metabfl/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(5, 6) vs llm=(15, 6)"
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
            "reason": "Shape mismatch: ref=(5, 6) vs llm=(15, 6)"
          }
        }
      }
    }
  ]
}
```
