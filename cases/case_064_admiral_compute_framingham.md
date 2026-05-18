# Case 064: pharmaverse/admiral/compute_framingham

## Case Metadata

- Task ID: `pharmaverse/admiral/compute_framingham`
- Package: `admiral`
- Track: `clinical_pilot`
- Model: `openai/gpt-5.1`
- Prompt type: `simple_prompt_plus_inputs`
- Status: `FAIL`
- Failure stage: `value_mismatch`
- Attribution bucket: `mixed_needs_review`
- Attribution note: value semantics likely package-specific; need inspect prompt/reference before blaming model

## Prompt

```text
Write an R script to perform compute framingham using the admiral clinical task contract.

Input: age.tsv, chol.tsv, cholhdl.tsv, diabetfl.tsv, sex.tsv, smokefl.tsv, sysbp.tsv, trthypfl.tsv
Output: result.csv


Required columns for result.csv: age, sex, sysbp, chol, cholhdl, smokefl, diabetfl, trthypfl, result
Read input files from inputs/ using relative paths. Write only the required output file(s) under outputs/. Create outputs/ if needed. Do not write alternative filenames.

## Input preview

### age.tsv (13 bytes)
age
45
60
72

### chol.tsv (17 bytes)
chol
180
220
260

### cholhdl.tsv (20 bytes)
cholhdl
3.5
4.2
5.0

### diabetfl.tsv (15 bytes)
diabetfl
N
N
Y

### sex.tsv (10 bytes)
sex
F
M
F

### smokefl.tsv (14 bytes)
smokefl
N
Y
N

### sysbp.tsv (18 bytes)
sysbp
118
142
155

### trthypfl.tsv (15 bytes)
trthypfl
N
Y
Y
```

## Input Data

### `age.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/age.tsv`
- Size: 13 bytes

```text
age
45
60
72
```

### `chol.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/chol.tsv`
- Size: 17 bytes

```text
chol
180
220
260
```

### `cholhdl.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/cholhdl.tsv`
- Size: 20 bytes

```text
cholhdl
3.5
4.2
5.0
```

### `diabetfl.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/diabetfl.tsv`
- Size: 15 bytes

```text
diabetfl
N
N
Y
```

### `sex.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/sex.tsv`
- Size: 10 bytes

```text
sex
F
M
F
```

### `smokefl.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/smokefl.tsv`
- Size: 14 bytes

```text
smokefl
N
Y
N
```

### `sysbp.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/sysbp.tsv`
- Size: 18 bytes

```text
sysbp
118
142
155
```

### `trthypfl.tsv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/inputs/trthypfl.tsv`
- Size: 15 bytes

```text
trthypfl
N
Y
Y
```

## Reference Code

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/solution.R`
- Size: 959 bytes

```r
read_col <- function(name) read.delim(file.path("inputs", paste0(name, ".tsv")), check.names = FALSE, stringsAsFactors = FALSE)[[name]]
age <- as.numeric(read_col("age"))
sex <- as.character(read_col("sex"))
sysbp <- as.numeric(read_col("sysbp"))
chol <- as.numeric(read_col("chol"))
cholhdl <- as.numeric(read_col("cholhdl"))
smokefl <- as.character(read_col("smokefl"))
diabetfl <- as.character(read_col("diabetfl"))
trthypfl <- as.character(read_col("trthypfl"))
flag <- function(x) ifelse(toupper(x) == "Y", 1, 0)
result <- 0.1 * age + 0.02 * sysbp + 0.01 * chol + 0.5 * cholhdl + 2 * flag(smokefl) + 2 * flag(diabetfl) + flag(trthypfl)
result_df <- data.frame(age = age, sex = sex, sysbp = sysbp, chol = chol, cholhdl = cholhdl, smokefl = smokefl, diabetfl = diabetfl, trthypfl = trthypfl, result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

### `result.csv`

- Path: `public/releases/rbiobench_stable_v1_fair/tracks/clinical_pilot/tasks/admiral/compute_framingham/outputs/result.csv`
- Size: 186 bytes

```csv
"age","sex","sysbp","chol","cholhdl","smokefl","diabetfl","trthypfl","result"
45,"F",118,180,3.5,"N","N","N",10.41
60,"M",142,220,4.2,"Y","N","Y",16.14
72,"F",155,260,5,"N","Y","Y",18.4
```

## LLM Generated Code

```r
#!/usr/bin/env Rscript

library(dplyr)
library(readr)

dir.create("outputs", showWarnings = FALSE)

age      <- read_tsv("inputs/age.tsv", col_types = cols())
chol     <- read_tsv("inputs/chol.tsv", col_types = cols())
cholhdl  <- read_tsv("inputs/cholhdl.tsv", col_types = cols())
diabetfl <- read_tsv("inputs/diabetfl.tsv", col_types = cols())
sex      <- read_tsv("inputs/sex.tsv", col_types = cols())
smokefl  <- read_tsv("inputs/smokefl.tsv", col_types = cols())
sysbp    <- read_tsv("inputs/sysbp.tsv", col_types = cols())
trthypfl <- read_tsv("inputs/trthypfl.tsv", col_types = cols())

df <- bind_cols(
  age,
  sex,
  sysbp,
  chol,
  cholhdl,
  smokefl,
  diabetfl,
  trthypfl
)

# Example Framingham-like risk score (placeholder implementation)
# Scores are illustrative only, not for clinical use.
df <- df %>%
  mutate(
    age_score = case_when(
      age < 45 ~ 0,
      age < 55 ~ 2,
      age < 65 ~ 4,
      age < 75 ~ 6,
      TRUE     ~ 8
    ),
    chol_score = case_when(
      chol < 160 ~ 0,
      chol < 200 ~ 1,
      chol < 240 ~ 2,
      chol < 280 ~ 3,
      TRUE       ~ 4
    ),
    hdl_score = case_when(
      cholhdl < 3.0 ~ -1,
      cholhdl < 4.0 ~ 0,
      cholhdl < 5.0 ~ 1,
      TRUE          ~ 2
    ),
    bp_score = case_when(
      sysbp < 120 ~ 0,
      sysbp < 130 ~ 1,
      sysbp < 140 ~ 2,
      sysbp < 160 ~ 3,
      TRUE        ~ 4
    ),
    smoke_score = if_else(smokefl == "Y", 2, 0),
    diab_score  = if_else(diabetfl == "Y", 3, 0),
    trt_score   = if_else(trthypfl == "Y", 2, 0),
    total_score = age_score + chol_score + hdl_score +
      bp_score + smoke_score + diab_score + trt_score,
    result = pmin(pmax(1 + total_score, 1), 30)
  ) %>%
  select(age, sex, sysbp, chol, cholhdl, smokefl, diabetfl, trthypfl, result)

write_csv(df, "outputs/result.csv")
```

## LLM Output

### `result.csv`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_framingham/sample_00/case_01/llm_outputs/result.csv`
- Size: 135 bytes

```csv
age,sex,sysbp,chol,cholhdl,smokefl,diabetfl,trthypfl,result
45,F,118,180,3.5,N,N,N,4
60,M,142,220,4.2,Y,N,Y,15
72,F,155,260,5,N,Y,Y,20
```

### `case_01/stderr.txt`

- Path: `analysis/clinical_clean_benchmark/task_cards_gpt51_eval_artifacts/artifacts/pharmaverse__admiral__compute_framingham/sample_00/case_01/stderr.txt`
- Size: 1333 bytes

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

Attaching package: ‘dplyr’

The following objects are masked from ‘package:stats’:

    filter, lag

The following objects are masked from ‘package:base’:

    intersect, setdiff, setequal, union
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
          "reason": "Numeric mismatch in column: result"
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
            "reason": "Numeric mismatch in column: result"
          }
        }
      }
    }
  ]
}
```
