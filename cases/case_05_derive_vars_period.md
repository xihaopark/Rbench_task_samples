# Case 05 - `admiral/derive_vars_period`

**Task ID:** `pharmaverse/admiral/derive_vars_period`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L2
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This is ADSL-adjacent because analysis-period start/end variables are subject-level attributes that often feed downstream ADaM derivations. The revised prompt makes the `inputs/` path and minimal-column normalization explicit, avoiding the earlier hidden-reference problem.

## Task Prompt

```text
Add **analysis period** start/end columns by joining subject-level period bounds. Load `library(admiral)`.

**Inputs:** `inputs/dataset.tsv`, `inputs/dataset_ref.tsv`. Read both from `inputs/`. If `USUBJID` or `STUDYID` is missing, create it as in the reference. Ensure `dataset_ref` has `APERIOD`, `APERSDT`, and `APEREDT`; if absent, create default period 1 with run-date start and run-date + 30 end. Then call `admiral::derive_vars_period(dataset, dataset_ref = dataset_ref, new_vars = admiral::exprs(APxxSDT = APERSDT, APxxEDT = APEREDT))`.

**Required outputs for grading:** `outputs/result.csv`
```

## Input

**`inputs/dataset.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

**`inputs/dataset_ref.tsv`**

```tsv
new_vars	subject_keys
1	1
2	2
3	3
4	4
5	5
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

dataset <- read.delim(file.path("inputs", "dataset.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
dataset_ref <- read.delim(file.path("inputs", "dataset_ref.tsv"), check.names = FALSE, stringsAsFactors = FALSE)

id_col <- if ("USUBJID" %in% names(dataset)) "USUBJID" else if ("id" %in% names(dataset)) "id" else names(dataset)[1]
if (id_col != "USUBJID") dataset$USUBJID <- as.character(dataset[[id_col]])
if (!"STUDYID" %in% names(dataset)) dataset$STUDYID <- "STUDY1"
if (!"USUBJID" %in% names(dataset_ref)) dataset_ref$USUBJID <- as.character(dataset_ref[[names(dataset_ref)[1]]])
if (!"STUDYID" %in% names(dataset_ref)) dataset_ref$STUDYID <- "STUDY1"

if (!"APERIOD" %in% names(dataset_ref)) dataset_ref$APERIOD <- 1L
if (!"APERSDT" %in% names(dataset_ref)) dataset_ref$APERSDT <- Sys.Date()
if (!"APEREDT" %in% names(dataset_ref)) dataset_ref$APEREDT <- Sys.Date() + 30

dataset_ref$APERSDT <- as.Date(dataset_ref$APERSDT)
dataset_ref$APEREDT <- as.Date(dataset_ref$APEREDT)

result <- admiral::derive_vars_period(
  dataset,
  dataset_ref = dataset_ref,
  new_vars = admiral::exprs(APxxSDT = APERSDT, APxxEDT = APEREDT)
)

dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

Run-date dependent. Archived reference run:

```csv
"id","value","group","category","USUBJID","STUDYID","AP01SDT","AP01EDT"
1,10.5,"A","Type1","1","STUDY1",2026-03-17,2026-04-16
2,20.3,"B","Type2","2","STUDY1",2026-03-17,2026-04-16
3,30.7,"A","Type1","3","STUDY1",2026-03-17,2026-04-16
4,40.2,"B","Type2","4","STUDY1",2026-03-17,2026-04-16
5,50.9,"A","Type1","5","STUDY1",2026-03-17,2026-04-16
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

dataset     <- read.delim("dataset.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
dataset_ref <- read.delim("dataset_ref.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

required_ref <- c("USUBJID", "APERIOD", "APERSDT", "APEREDT")
missing_ref  <- setdiff(required_ref, names(dataset_ref))
if (length(missing_ref) > 0) {
  stop("Missing required columns in dataset_ref: ", paste(missing_ref, collapse = ", "))
}

result <- admiral::derive_vars_period(
  dataset,
  dataset_ref = dataset_ref,
  new_vars = admiral::exprs(APxxSDT = APERSDT, APxxEDT = APEREDT)
)

write.csv(result, file = "outputs/result.csv", row.names = FALSE)
saveRDS(result, file = "outputs/result.rds")
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in file(file, "rt") : cannot open the connection
Calls: read.delim -> read.table -> file
In addition: Warning message:
In file(file, "rt") :
  cannot open file 'dataset.tsv': No such file or directory
Execution halted
```

**Failure point:** the model missed the `inputs/` path and treated `dataset_ref` as if it already had all ADaM period columns, instead of following the reference's explicit normalization step.
