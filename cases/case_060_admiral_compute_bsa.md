# Case 060: pharmaverse/admiral/compute_bsa

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_bsa`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `PASS`
- Failure stage: `pass`
- Attribution bucket: `pass`

## Prompt

```text
Write an R script to perform compute BSA using the admiral clinical task contract.

Input: height.tsv, method.tsv, weight.tsv
Output: result.csv


Required columns for result.csv: height, weight, method, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### height.tsv (19 bytes)
height
170
180
160

### method.tsv (17 bytes)
method
Mosteller

### weight.tsv (16 bytes)
weight
70
80
55
```

## Input Data

### `height.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bsa/inputs/height.tsv`
- Size: 19 bytes

```text
height
170
180
160
```

### `method.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bsa/inputs/method.tsv`
- Size: 17 bytes

```text
method
Mosteller
```

### `weight.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bsa/inputs/weight.tsv`
- Size: 16 bytes

```text
weight
70
80
55
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bsa/solution.R`
- Size: 695 bytes

```r
suppressPackageStartupMessages(library(admiral))

height <- as.numeric(read.delim(file.path("inputs", "height.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$height)
weight <- as.numeric(read.delim(file.path("inputs", "weight.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$weight)
method <- as.character(read.delim(file.path("inputs", "method.tsv"), check.names = FALSE, stringsAsFactors = FALSE)$method[[1]])
result <- admiral::compute_bsa(height = height, weight = weight, method = method)

dir.create("outputs", showWarnings = FALSE)
write.csv(data.frame(height = height, weight = weight, method = method, result = result), file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_bsa/outputs/result.csv`
- Size: 129 bytes

```csv
"height","weight","method","result"
170,70,"Mosteller",1.81811868577262
180,80,"Mosteller",2
160,55,"Mosteller",1.56347191994114
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read inputs
height_df <- read_tsv(
  "inputs/height.tsv",
  show_col_types = FALSE,
  progress = FALSE
)

weight_df <- read_tsv(
  "inputs/weight.tsv",
  show_col_types = FALSE,
  progress = FALSE
)

method_df <- read_tsv(
  "inputs/method.tsv",
  show_col_types = FALSE,
  progress = FALSE
)

# Prepare vectors
heights <- height_df$height
weights <- weight_df$weight
method  <- method_df$method[1]

# Recycle height to match length of weight if needed
if (length(heights) != length(weights)) {
  heights <- rep(heights, length.out = length(weights))
}

# Supported methods (admiral clinical task contract: Mosteller)
compute_bsa <- function(height_cm, weight_kg, method) {
  if (method == "Mosteller") {
    return(sqrt(height_cm * weight_kg / 3600))
  } else {
    stop("Unsupported method: ", method)
  }
}

result_vec <- compute_bsa(heights, weights, method)

result_df <- tibble(
  height = heights,
  weight = weights,
  method = method,
  result = result_vec
)

write_csv(result_df, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_bsa/sample_00/case_01/llm_outputs/result.csv`
- Size: 118 bytes

```csv
height,weight,method,result
170,70,Mosteller,1.818118685772619
180,80,Mosteller,2
160,55,Mosteller,1.5634719199411433
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_bsa/sample_00/case_01/stderr.txt`
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
  "status": "PASS",
  "failure_stage": "pass",
  "score": 1.0,
  "message": "",
  "test_cases": [
    {
      "case": "case_embedded",
      "status": "PASS",
      "tier": "pass",
      "tier_value": "pass",
      "failure_stage": "pass",
      "comparison": {
        "result.csv": {
          "match": true,
          "tier": "pass",
          "failure_stage": "pass"
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
        "comparison_reasons": {}
      }
    }
  ]
}
```
