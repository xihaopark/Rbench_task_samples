# Case 03 - `admiral/derive_vars_dy`

**Task ID:** `pharmaverse/admiral/derive_vars_dy`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L2
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

This is a direct overlap with the `admiral-adsl` skill at the function-idiom level. The skill tells agents to use `derive_vars_dy()` for ADaM study-day variables instead of hand-coding date subtraction.

## Task Prompt

```text
Derive **study day** (`*DY`) relative to a reference date. Load `library(admiral)`.

**Inputs:** `datase.tsv` - reference assigns `TRTSDT` and `ASTDT`.

**Computation:** `admiral::derive_vars_dy(datase, reference_date = TRTSDT, source_vars = admiral::exprs(TRTSDT, ASTDT))`.

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

The reference adds `TRTSDT <- Sys.Date()` and `ASTDT <- Sys.Date() + 7` before calling admiral.

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

datase <- read.delim(file.path("inputs", "datase.tsv"), check.names = FALSE, stringsAsFactors = FALSE)
datase$TRTSDT <- Sys.Date()
datase$ASTDT <- Sys.Date() + 7

result <- admiral::derive_vars_dy(datase, reference_date = TRTSDT, source_vars = admiral::exprs(TRTSDT, ASTDT))
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

Run-date dependent. Archived reference run:

```csv
"id","value","group","category","TRTSDT","ASTDT","TRTSDY","ASTDY"
1,10.5,"A","Type1",2026-03-17,2026-03-24,1,8
2,20.3,"B","Type2",2026-03-17,2026-03-24,1,8
3,30.7,"A","Type1",2026-03-17,2026-03-24,1,8
4,40.2,"B","Type2",2026-03-17,2026-03-24,1,8
5,50.9,"A","Type1",2026-03-17,2026-03-24,1,8
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

datase <- read.table("datase.tsv", header = TRUE, sep = "\t", stringsAsFactors = FALSE, na.strings = c("", "NA"))

date_vars <- c("TRTSDT", "ASTDT")
for (v in date_vars) {
  if (!inherits(datase[[v]], "Date")) datase[[v]] <- as.Date(datase[[v]])
}

datase <- derive_vars_dy(datase, reference_date = TRTSDT, source_vars = exprs(TRTSDT, ASTDT))
write.csv(datase, "outputs/result.csv", row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in file(file, "rt") : cannot open the connection
Calls: read.table -> file
In addition: Warning message:
In file(file, "rt") :
  cannot open file 'datase.tsv': No such file or directory
Execution halted
```

**Failure point:** the model missed `inputs/datase.tsv` and did not reproduce the reference's creation of `TRTSDT` and `ASTDT`.
