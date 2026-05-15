# Case 02 - `admiral/derive_vars_dtm`

**Task ID:** `pharmaverse/admiral/derive_vars_dtm`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L2
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This is the datetime companion to Case 01. The `admiral-adsl` skill needs this idiom whenever SDTM `--DTC` values must become ADaM datetime variables. RBioBench tests the `derive_vars_dtm()` API plus a sparse fixture that lacks a DTC column.

## Task Prompt

```text
Derive **datetime** variables (`*DTM`) from ISO-like `*DTC` strings. Load `library(admiral)` and `library(rlang)`.

**Inputs:** `inputs/datase.tsv`.

**Computation:** Select an existing `*DTC` column (`ASTDTC`, `AESTDTC`, `LBDTC`). If none exists, first create fallback `ASTDTC <- format(Sys.time(), "%Y-%m-%dT%H:%M")`, then call `admiral::derive_vars_dtm(datase, new_vars_prefix = "AST", dtc = !!rlang::sym(dtc_col))`.

**Required outputs for grading:** `outputs/result.csv`
```

## Input

**`inputs/datase.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1
```

Additional fixtures exist (`dtc.tsv`, `flag_imputation.tsv`, `mhdt.tsv`, `new_vars_prefix.tsv`), but the reference solution only needs `inputs/datase.tsv` here.

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

datase <- read.delim(file.path("inputs", "datase.tsv"), check.names = FALSE, stringsAsFactors = FALSE)

dtc_col <- NULL
for (c in c("ASTDTC", "AESTDTC", "LBDTC")) {
  if (c %in% names(datase)) { dtc_col <- c; break }
}
if (is.null(dtc_col)) { datase$ASTDTC <- format(Sys.time(), "%Y-%m-%dT%H:%M"); dtc_col <- "ASTDTC" }

result <- admiral::derive_vars_dtm(datase, new_vars_prefix = "AST", dtc = !!rlang::sym(dtc_col))
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

Run-time dependent. Archived reference run:

```csv
"id","value","group","category","ASTDTC","ASTDTM","ASTTMF"
1,10.5,"A","Type1","2026-03-17T21:52",2026-03-17 21:52:00,NA
2,20.3,"B","Type2","2026-03-17T21:52",2026-03-17 21:52:00,NA
3,30.7,"A","Type1","2026-03-17T21:52",2026-03-17 21:52:00,NA
4,40.2,"B","Type2","2026-03-17T21:52",2026-03-17 21:52:00,NA
5,50.9,"A","Type1","2026-03-17T21:52",2026-03-17 21:52:00,NA
```

## LLM Code

```r
library(admiral)
library(rlang)

dir.create("outputs", showWarnings = FALSE)

datase <- read.delim("inputs/datase.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

dtc_priority <- c("ASTDTC", "AENDTC", "TRTDTC", "TRTSDTC", "TRTEDTC")
dtc_col <- dtc_priority[dtc_priority %in% names(datase)][1]
if (is.na(dtc_col)) dtc_col <- "ASTDTC"

datase <- derive_vars_dtm(datase, new_vars_prefix = "AST", dtc = !!sym(dtc_col))
write.csv(datase, "outputs/result.csv", row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in `derive_vars_dtm()`:
! Required variable `ASTDTC` is missing in `dataset`
```

**Failure point:** the model selected a default column name but did not create the fallback `ASTDTC` value before calling admiral.
