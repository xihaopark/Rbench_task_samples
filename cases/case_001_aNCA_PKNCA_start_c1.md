# Case 001: pharmaverse/aNCA/PKNCA_impute_method_start_c1

## Case Metadata

- Task ID: `pharmaverse/aNCA/PKNCA_impute_method_start_c1`
- Package: `aNCA`
- Model: `openai/gpt-5.1`
- Status: `FAIL`
- Failure stage: `schema_mismatch`
- Attribution bucket: `benchmark_or_prompt_issue`
- Attribution note: row semantics/function behavior under-specified by simple prompt

## Prompt

```text
Write an R script to perform PKNCA impute method start c1 using the aNCA clinical task contract.

Input: conc.tsv, end.tsv, options.tsv, start.tsv, time.tsv
Output: result.csv


Required columns for result.csv: conc, time
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### conc.tsv (31 bytes)
conc
0.1
1.5
10.0
100.0
1000.0

### end.tsv (8 bytes)
end
4.5

### options.tsv (42 bytes)
options
method=start_conc0
allow_blq=TRUE

### start.tsv (10 bytes)
start
1.5

### time.tsv (25 bytes)
time
1.0
2.0
3.0
4.0
5.0
```

## Input Data

### `conc.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/inputs/conc.tsv`
- Size: 31 bytes

```text
conc
0.1
1.5
10.0
100.0
1000.0
```

### `end.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/inputs/end.tsv`
- Size: 8 bytes

```text
end
4.5
```

### `options.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/inputs/options.tsv`
- Size: 42 bytes

```text
options
method=start_conc0
allow_blq=TRUE
```

### `start.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/inputs/start.tsv`
- Size: 10 bytes

```text
start
1.5
```

### `time.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/inputs/time.tsv`
- Size: 25 bytes

```text
time
1.0
2.0
3.0
4.0
5.0
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/solution.R`
- Size: 1399 bytes

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

conc <- suppressWarnings(as.numeric(first_column(read_tsv("conc.tsv"))))
time <- suppressWarnings(as.numeric(first_column(read_tsv("time.tsv"))))
start <- scalar_numeric(read_tsv("start.tsv"))
end <- scalar_numeric(read_tsv("end.tsv"))

keep <- !is.na(conc) & !is.na(time)
result <- data.frame(conc = conc[keep], time = time[keep])

if (!is.na(start) && !is.na(end) && !any(result$time == start)) {
  interval <- result[result$time >= start & result$time <= end, , drop = FALSE]
  if (nrow(interval) > 0) {
    interval <- interval[order(interval$time), , drop = FALSE]
    result <- rbind(result, data.frame(conc = interval$conc[[1]], time = start))
    result <- result[order(result$time), , drop = FALSE]
  }
}

write_result(result)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/aNCA/PKNCA_impute_method_start_c1/outputs/result.csv`
- Size: 52 bytes

```csv
"conc","time"
0.1,1
1.5,1.5
1.5,2
10,3
100,4
1000,5
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  if (!requireNamespace("PKNCA", quietly = TRUE)) {
    install.packages("PKNCA", repos = "https://cloud.r-project.org")
  }
  library(PKNCA)
})

# Create outputs directory if it does not exist
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

# Read inputs
conc_df   <- read.table("inputs/conc.tsv",   header = TRUE, sep = "\t", check.names = FALSE)
time_df   <- read.table("inputs/time.tsv",   header = TRUE, sep = "\t", check.names = FALSE)
start_df  <- read.table("inputs/start.tsv",  header = TRUE, sep = "\t", check.names = FALSE)
end_df    <- read.table("inputs/end.tsv",    header = TRUE, sep = "\t", check.names = FALSE)
options_df<- read.table("inputs/options.tsv",header = TRUE, sep = "\t", check.names = FALSE)

# Extract vectors
conc  <- conc_df$conc
time  <- time_df$time
tstart<- start_df$start[1]
tend  <- end_df$end[1]

# Parse options
method <- "start_conc0"
allow_blq <- TRUE
if (nrow(options_df) > 0) {
  opts <- options_df$options
  for (opt in opts) {
    if (grepl("^method=", opt)) {
      method <- sub("^method=", "", opt)
    } else if (grepl("^allow_blq=", opt)) {
      val <- sub("^allow_blq=", "", opt)
      allow_blq <- as.logical(val)
    }
  }
}

# Build concentration-time data frame for PKNCA
data_ct <- data.frame(conc = conc, time = time)

# PKNCA expects columns named conc and time by default for concentration-time data
# Impute method start c1: use start_conc0 option in PKNCADose?
# We will impute concentration at tstart using linear interpolation/extrapolation

# Ensure time and conc are sorted by time
ord <- order(time)
time <- time[ord]
conc <- conc[ord]

# Function to evaluate concentration at arbitrary time by linear interpolation
interp_conc <- function(t, time, conc) {
  if (t <= min(time)) {
    # Extrapolate using first two points
    if (length(time) == 1) return(conc[1])
    x1 <- time[1]; x2 <- time[2]
    y1 <- conc[1]; y2 <- conc[2]
  } else if (t >= max(time)) {
    # Extrapolate using last two points
    if (length(time) == 1) return(conc[1])
    x1 <- time[length(time)-1]; x2 <- time[length(time)]
    y1 <- conc[length(conc)-1]; y2 <- conc[length(conc)]
  } else {
    # Interpolate between nearest neighbors
    idx2 <- which(time >= t)[1]
    idx1 <- idx2 - 1
    x1 <- time[idx1]; x2 <- time[idx2]
    y1 <- conc[idx1]; y2 <- conc[idx2]
  }
  if (x2 == x1) return(y1)
  y1 + (y2 - y1) * (t - x1) / (x2 - x1)
}

# Compute imputed concentration at tstart (c1)
c1 <- interp_conc(tstart, time, conc)

# Subset to the interval [tstart, tend] and include imputed start concentration
sel <- time >= tstart & time <= tend

time_out <- c(tstart, time[sel][time[sel] != tstart])
conc_out <- c(c1, conc[sel][time[sel] != tstart])

result <- data.frame(conc = conc_out, time = time_out)

write.csv(result, file = "outputs/result.csv", row.names = FALSE, quote = TRUE)
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__PKNCA_impute_method_start_c1/sample_00/case_01/llm_outputs/result.csv`
- Size: 39 bytes

```csv
"conc","time"
0.8,1.5
1.5,2
10,3
100,4
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__aNCA__PKNCA_impute_method_start_c1/sample_00/case_01/stderr.txt`
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
          "reason": "Shape mismatch: ref=(6, 2) vs llm=(4, 2)"
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
            "reason": "Shape mismatch: ref=(6, 2) vs llm=(4, 2)"
          }
        }
      }
    }
  ]
}
```
