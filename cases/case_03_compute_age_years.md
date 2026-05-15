# Case 03 - `admiral/compute_age_years`

**Task ID:** `pharmaverse/admiral/compute_age_years`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L2
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This is a cleaner ADSL-adjacent primitive than the previous study-day example. ADSL derivations often need age variables standardized to years before or during subject-level age derivation. The prompt explicitly names the input paths, valid age units, and invalid-unit fallback.

## Task Prompt

```text
Write R code to convert age to **years** for ADaM. Load `library(admiral)`.

**Inputs:** `inputs/age.tsv`, `inputs/age_unit.tsv` - numeric age and a unit string (`years`, `months`, `weeks`, `days`, `hours`, `minutes`, `seconds`); invalid units fall back to `years` in the reference.

**Computation:** `admiral::compute_age_years(age, age_unit)`.

**Required outputs for grading:** `outputs/result.csv`
```

## Input

**`inputs/age.tsv`**

```tsv
age
0.1
1.5
10.0
100.0
1000.0
```

**`inputs/age_unit.tsv`**

```tsv
age_unit
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

age_df <- read.delim(file.path("inputs", "age.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
age <- suppressWarnings(as.numeric(as.character(age_df[[1]])))

age_unit_df <- read.delim(file.path("inputs", "age_unit.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
age_unit <- tolower(as.character(age_unit_df[[1]][1]))
valid_units <- c("years", "months", "weeks", "days", "hours", "minutes", "seconds")
if (!age_unit %in% valid_units) age_unit <- "years"

result <- admiral::compute_age_years(age, age_unit)
result_df <- data.frame(age = age, age_unit = age_unit, result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

```csv
"age","age_unit","result"
0.1,"years",0.1
1.5,"years",1.5
10,"years",10
100,"years",100
1000,"years",1000
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

age_df <- read.table("inputs/age.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
age_unit_df <- read.table("inputs/age_unit.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE)

df <- cbind(age_df, age_unit_df)

df$AGE_Y <- compute_age_years(df[[1]], df[[2]])

write.csv(df, "outputs/result.csv", row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in `compute_age_years()`:
! Argument `unique(tolower(age_unit))` must be <character> with values
  NA, "years", "months", "weeks", "days", "hours", "minutes", and "seconds".
```

**Failure point:** the prompt says invalid units fall back to `years`, but the model passed `test_value` directly into admiral instead of applying that reference fallback.
