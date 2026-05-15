# Case 04 - `admiral/derive_var_trtdurd`

**Task ID:** `pharmaverse/admiral/derive_var_trtdurd`
**Package:** admiral | **Track:** clinical_pilot | **Level:** L2
**Sample chosen:** GPT-5.1 direct LLM pass5, `sample_00`

## Why This Case Matters

Treatment duration is a normal ADSL endpoint once treatment start and end dates exist. The `admiral-adsl` skill covers the surrounding ADSL workflow; RBioBench isolates the admiral primitive and the fixture-specific date preparation required before calling it.

## Task Prompt

```text
Derive **treatment duration** (`TRTDURD`). Load `library(admiral)`.

**Inputs:** `inputs/datase.tsv`, `inputs/start_date.tsv`, `inputs/end_date.tsv`.

**Computation:** The reference parses dates, assigns `TRTSDT` and `TRTEDT`, then calls `admiral::derive_var_trtdurd(datase)`.

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

**`inputs/start_date.tsv`** and **`inputs/end_date.tsv`** contain one generic string column (`item_a` through `item_e`); the reference falls back to run-date defaults when parsing fails.

## Reference Code

```r
suppressPackageStartupMessages(library(admiral))

datase <- read.delim(file.path("inputs", "datase.tsv"), check.names = FALSE, stringsAsFactors = FALSE)

parse_date <- function(path, default) {
  if (!file.exists(path)) return(default)
  df <- read.delim(path, check.names = FALSE, stringsAsFactors = FALSE)
  value <- as.character(df[[ncol(df)]][1])
  parsed <- suppressWarnings(as.Date(value, tryFormats = c("%Y-%m-%d", "%Y/%m/%d", "%d%b%Y")))
  if (is.na(parsed)) default else parsed
}

datase$TRTSDT <- parse_date(file.path("inputs", "start_date.tsv"), Sys.Date())
datase$TRTEDT <- parse_date(file.path("inputs", "end_date.tsv"), Sys.Date() + 30)

result <- admiral::derive_var_trtdurd(datase)
dir.create("outputs", showWarnings = FALSE)
write.csv(result, file.path("outputs", "result.csv"), row.names = FALSE)
```

## Reference Output

Run-date dependent. Archived reference run:

```csv
"id","value","group","category","TRTSDT","TRTEDT","TRTDURD"
1,10.5,"A","Type1",2026-03-17,2026-04-16,31
2,20.3,"B","Type2",2026-03-17,2026-04-16,31
3,30.7,"A","Type1",2026-03-17,2026-04-16,31
4,40.2,"B","Type2",2026-03-17,2026-04-16,31
5,50.9,"A","Type1",2026-03-17,2026-04-16,31
```

## LLM Code

```r
library(admiral)

dir.create("outputs", showWarnings = FALSE)

datase <- read.delim("inputs/datase.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
start_date <- read.delim("inputs/start_date.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
end_date <- read.delim("inputs/end_date.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

datase <- datase |>
  dplyr::left_join(start_date, by = c("STUDYID", "USUBJID")) |>
  dplyr::left_join(end_date, by = c("STUDYID", "USUBJID"))

datase <- derive_var_trtdurd(datase)
write.csv(datase, "outputs/result.csv", row.names = FALSE)
```

## LLM Output

**stdout:** empty

**stderr:**

```text
Error in `dplyr::left_join()`:
! Join columns in `x` must be present in the data.
x Problem with `STUDYID` and `USUBJID`.
```

**Failure point:** the model assumed realistic SDTM subject keys, but the benchmark fixture is intentionally generic.
