# Case 05 - `admiral/derive_vars_computed`

**Task ID:** `pharmaverse/admiral/derive_vars_computed`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L3
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This is the closest RBioBench case to the baseline-value derivation style used in `admiral-adsl`, for example deriving BMI from height and weight records. The important overlap is the admiral pattern of joining parameterized records and computing a new variable with expression objects.

## Task Prompt

```text
Write R code to implement the **Derive Vars Computed** workflow using the `admiral` package.
At the beginning, load required packages: library(admiral).

Read input TSVs including `datase.tsv`, `dataset_add.tsv`, `by_vars.tsv`,
`constant_by_vars.tsv`, `constant_parameters.tsv`, `filter_add.tsv`,
`new_vars.tsv`, and `parameters.tsv`.

Use `admiral::derive_vars_computed` when it is the correct public API for this task.

Required output: `outputs/result.csv`
```

## Input

**`inputs/datase.tsv`**

```tsv
by_vars
1
2
3
4
5
```

**`inputs/dataset_add.tsv`**

```tsv
by_vars
1
2
3
4
5
```

Other fixtures are intentionally generic: `by_vars.tsv`, `constant_by_vars.tsv`, `constant_parameters.tsv`, `filter_add.tsv`, `new_vars.tsv`, and `parameters.tsv`.

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(rlang))

datase <- read.delim(file.path("inputs", "datase.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dataset_add <- read.delim(file.path("inputs", "dataset_add.tsv"), check.names = FALSE, stringsAsFactors = FALSE)

by_cols <- intersect(names(datase), names(dataset_add))
if (length(by_cols) == 0) by_cols <- "id"
if (!"id" %in% names(datase)) datase$id <- seq_len(nrow(datase))
if (!"id" %in% names(dataset_add)) dataset_add$id <- rep(seq_len(max(1, nrow(datase) %/% 2)), length.out = nrow(dataset_add))

if (!"PARAMCD" %in% names(dataset_add)) dataset_add$PARAMCD <- rep(c("WEIGHT", "HEIGHT"), length.out = nrow(dataset_add))
if (!"AVAL" %in% names(dataset_add)) dataset_add$AVAL <- dataset_add[[names(dataset_add)[sapply(dataset_add, is.numeric)][1]]]
if (!"ABLFL" %in% names(dataset_add)) dataset_add$ABLFL <- c("Y", "N")[((seq_len(nrow(dataset_add)) - 1) %% 2) + 1]

by_vars <- exprs(!!!syms(by_cols))
parameters <- c("WEIGHT", "HEIGHT")
new_vars <- exprs(BMIBL = compute_bmi(height = AVAL.HEIGHT, weight = AVAL.WEIGHT))
filter_add <- expr(ABLFL == "Y")

result <- admiral::derive_vars_computed(dataset = datase, dataset_add = dataset_add, by_vars = by_vars, parameters = parameters, new_vars = new_vars, filter_add = !!filter_add)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

```csv
"by_vars","id","BMIBL"
1,1,NA
2,2,NA
3,3,NA
4,4,NA
5,5,NA
```

## LLM Code

```r
library(admiral)
library(dplyr)
library(rlang)

dir.create("outputs", showWarnings = FALSE)

datase <- read.delim("inputs/datase.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
dataset_add <- read.delim("inputs/dataset_add.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
by_vars_df <- read.delim("inputs/by_vars.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
constant_by_vars_df <- read.delim("inputs/constant_by_vars.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
constant_parameters_df <- read.delim("inputs/constant_parameters.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
filter_add_df <- read.delim("inputs/filter_add.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
new_vars_df <- read.delim("inputs/new_vars.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)
parameters_df <- read.delim("inputs/parameters.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE, check.names = FALSE)

by_vars <- rlang::quos(!!!rlang::syms(names(by_vars_df)))
constant_by_vars <- rlang::quos(!!!rlang::syms(names(constant_by_vars_df)))
parameters_expr <- as.character(parameters_df[[1]])
constant_parameters_expr <- as.character(constant_parameters_df[[1]])
new_vars_list <- as.list(as.character(new_vars_df[[1]]))
dataset_add_list <- dataset_add
filter_add_expr <- rlang::sym(as.character(filter_add_df[[1]][1]))

result <- derive_vars_computed(dataset = datase, by_vars = by_vars, constant_by_vars = constant_by_vars, parameters = parameters_expr, constant_parameters = constant_parameters_expr, new_vars = new_vars_list, dataset_add = dataset_add_list, filter_add = filter_add_expr)
write.csv(result, file = "outputs/result.csv", row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in `derive_vars_computed()`:
! Argument `filter_add` must be a filter condition, but is a symbol
```

**Failure point:** the model treated fixture text as literal API arguments. The admiral API requires expression objects for `by_vars`, `new_vars`, and `filter_add`.
