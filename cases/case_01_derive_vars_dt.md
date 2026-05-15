# Case 01 - `admiral/derive_vars_dt`

**Task ID:** `pharmaverse/admiral/derive_vars_dt`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L2
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This maps directly to the `admiral-adsl` skill's date-derivation layer. In an ADSL workflow, the skill expects agents to create analysis date variables such as treatment start/end dates from SDTM character dates. RBioBench isolates the lower-level API contract: `admiral::derive_vars_dt(dataset, new_vars_prefix = ..., dtc = !!rlang::sym(dtc_col))`.

## Task Prompt

```text
Derive **imputed Date** variables (`*DT`) from partial-date character `*DTC`. Load `library(admiral)` and `library(rlang)`.

**Inputs:** `inputs/datase.tsv`, optional `inputs/new_vars_prefix.tsv`, optional `inputs/flag_imputation.tsv`.

**Computation:** Read from the `inputs/` directory. Pick an existing `*DTC` column (`ASTDTC`, `AESTDTC`, `MHSTDTC`, `EXSTDTC`), or create fallback `ASTDTC <- format(Sys.Date(), "%Y-%m-%d")`. Then call `admiral::derive_vars_dt(datase, new_vars_prefix = ..., dtc = !!rlang::sym(dtc_col), flag_imputation = ...)`. Treat invalid `flag_imputation` fixture values as the reference default `"auto"`.

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

**`inputs/new_vars_prefix.tsv`**

```tsv
new_vars_prefix
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

**`inputs/flag_imputation.tsv`**

```tsv
flag_imputation
"item_a"
"item_b"
"item_c"
"item_d"
"item_e"
```

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))
suppressPackageStartupMessages(library(rlang))

datase_path <- file.path("inputs", "datase.tsv")
if (!file.exists(datase_path)) stop("datase.tsv is required input")
datase <- read.delim(datase_path, check.names = FALSE, stringsAsFactors = FALSE)

new_vars_prefix <- "AST"
if (file.exists(file.path("inputs", "new_vars_prefix.tsv"))) {
  df <- read.delim(file.path("inputs", "new_vars_prefix.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
  new_vars_prefix <- as.character(df[[ncol(df)]][1])
}

flag_imputation <- "auto"
if (file.exists(file.path("inputs", "flag_imputation.tsv"))) {
  df <- read.delim(file.path("inputs", "flag_imputation.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
  v <- as.character(df[[ncol(df)]][1])
  if (v %in% c("auto", "date", "none")) flag_imputation <- v
}

dtc_col <- NULL
for (c in c("ASTDTC", "AESTDTC", "MHSTDTC", "EXSTDTC")) {
  if (c %in% names(datase)) { dtc_col <- c; break }
}
if (is.null(dtc_col)) { datase$ASTDTC <- format(Sys.Date(), "%Y-%m-%d"); dtc_col <- "ASTDTC" }

result <- admiral::derive_vars_dt(datase, new_vars_prefix = new_vars_prefix, dtc = !!rlang::sym(dtc_col), flag_imputation = flag_imputation)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

Run-date dependent. Archived reference run:

```csv
"id","value","group","category","ASTDTC","item_aDT"
1,10.5,"A","Type1","2026-03-17",2026-03-17
2,20.3,"B","Type2","2026-03-17",2026-03-17
3,30.7,"A","Type1","2026-03-17",2026-03-17
4,40.2,"B","Type2","2026-03-17",2026-03-17
5,50.9,"A","Type1","2026-03-17",2026-03-17
```

## LLM Code

```r
library(admiral)
library(rlang)

dir.create("outputs", showWarnings = FALSE)

datase <- read.delim("datase.tsv", sep = "\t", stringsAsFactors = FALSE, check.names = FALSE)

if (file.exists("new_vars_prefix.tsv")) {
  nvp_df <- read.delim("new_vars_prefix.tsv", sep = "\t", stringsAsFactors = FALSE, header = FALSE)
  new_vars_prefix <- nvp_df[[1]][1]
} else {
  new_vars_prefix <- "IMPUTED_"
}

if (file.exists("flag_imputation.tsv")) {
  fi_df <- read.delim("flag_imputation.tsv", sep = "\t", stringsAsFactors = FALSE, header = FALSE)
  flag_imputation <- fi_df[[1]][1]
} else {
  flag_imputation <- "Y"
}

dtc_cols <- grep("DTC$", names(datase), value = TRUE)
if (length(dtc_cols) == 0) { datase$ASTDTC <- NA_character_; dtc_col <- "ASTDTC" } else { dtc_col <- dtc_cols[1] }

result <- derive_vars_dt(datase, new_vars_prefix = new_vars_prefix, dtc = !!sym(dtc_col), flag_imputation = flag_imputation)
write.csv(result, file = "outputs/result.csv", row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in file(file, "rt") : cannot open the connection
Calls: read.delim -> read.table -> file
In addition: Warning message:
In file(file, "rt") :
  cannot open file 'datase.tsv': No such file or directory
Execution halted
```

**Failure point:** the model knew the admiral function, but missed the benchmark file contract (`inputs/datase.tsv`) and invented unsafe defaults.
