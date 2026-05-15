# Case 04 - `admiral/compute_bmi`

**Task ID:** `pharmaverse/admiral/compute_bmi`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L1
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This maps to the ADSL skill's baseline body-measure derivation family. In a full ADSL workflow, height and weight records are often merged first, then BMI is computed. This microtask isolates the computation primitive and the benchmark's file contract.

## Task Prompt

```text
Write R code to implement the **Compute BMI** workflow using the `admiral` package. Load `library(admiral)`.

**Inputs:** `inputs/height.tsv`, `inputs/weight.tsv`. Each file is a TSV with a header row. Read with `read.delim(file.path("inputs", ...), check.names = FALSE, stringsAsFactors = FALSE)`. Use the first column or a column named `height` / `weight`, coerce to numeric, then call `admiral::compute_bmi(height = height_vec, weight = weight_vec)`.

**Required outputs for grading:** `outputs/result.csv`
```

## Input

**`inputs/height.tsv`**

```tsv
height
"test_value"
```

**`inputs/weight.tsv`**

```tsv
weight
"test_value"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

height <- read.delim(file.path("inputs", "height.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
weight <- read.delim(file.path("inputs", "weight.tsv"), check.names = FALSE, stringsAsFactors = FALSE)

height_vec <- as.numeric(if ("height" %in% names(height)) height$height else height[[1]])
weight_vec <- as.numeric(if ("weight" %in% names(weight)) weight$weight else weight[[1]])

result <- admiral::compute_bmi(height = height_vec, weight = weight_vec)
result_df <- data.frame(id = seq_along(result), result = result, stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE)
write.csv(result_df, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

```csv
"id","result"
1,NA
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

height <- read.delim(file.path("inputs", "height.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
weight <- read.delim(file.path("inputs", "weight.tsv"), check.names = FALSE, stringsAsFactors = FALSE)

if (!"USUBJID" %in% names(height)) {
  stop("height.tsv must contain a USUBJID column")
}
if (!"USUBJID" %in% names(weight)) {
  stop("weight.tsv must contain a USUBJID column")
}

if (!"HEIGHT" %in% names(height)) {
  stop("height.tsv must contain a HEIGHT column with height in cm (or adjust code).")
}
if (!"WEIGHT" %in% names(weight)) {
  stop("weight.tsv must contain a WEIGHT column with weight in kg (or adjust code).")
}

dat <- merge(height[, c("USUBJID", "HEIGHT")], weight[, c("USUBJID", "WEIGHT")], by = "USUBJID", all = TRUE)
dat$BMI <- admiral::compute_bmi(height = dat$HEIGHT, weight = dat$WEIGHT)

write.csv(dat, file.path("outputs", "result.csv"), row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error: height.tsv must contain a USUBJID column
Execution halted
```

**Failure point:** the model imposed a realistic clinical merge schema (`USUBJID`, `HEIGHT`, `WEIGHT`) that the prompt did not require. The benchmark expected direct argument extraction from the provided files.
