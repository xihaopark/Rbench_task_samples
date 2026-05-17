# Sample 41: pharmaverse/admiral/derive_var_trtdurd

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/admiral/derive_var_trtdurd`
- package/function: `admiral` / `derive_var_trtdurd`
- expected_artifacts: `outputs/result.csv`
- current_status: `TIMEOUT` tier=`exec_fail`
- simple_status: `TIMEOUT` tier=`exec_fail`

## Reference Prompt
```text
Derive **treatment duration** (`TRTDURD`). Load `library(admiral)`.

**Inputs:** `inputs/datase.tsv`, `inputs/start_date.tsv`, `inputs/end_date.tsv` — the reference parses dates, assigns **`TRTSDT`** / **`TRTEDT`** on the dataset, then calls **`admiral::derive_var_trtdurd(datase)`** with default start/end column resolution as in admiral.

**Required outputs for grading (exact paths):**
- `outputs/result.csv`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
The reference may also emit `outputs/summary.csv` when the long template is used; follow `solution.R` if present.

```

## Current Prompt
```text
Write R code to derive total treatment duration (days) using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/datase.tsv, inputs/start_date.tsv, inputs/end_date.tsv). **Note:** This is a wrapper function for the more generic `derive_vars_duration()`. Additional details: start to end date plus one. Use admiral's derive_var_trtdurd function with the following parameters: datase (t `r roxygen_param_dataset(expected_vars = c("start_date", "end_date"))`), start_date (The start date A date or date-time object is expected.), end_date (The end date A date or date-time object is expected.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with `TRTDURD` added. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.

## Inputs preview (no reference answers)

### datase.tsv (578 bytes)
USUBJID	STUDYID	SUBJID	TRTA	TRTAN	TRTSDT	TRTEDT	AGE	SEX	SAFFL	FASFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	1015	Placebo	0	2019-03-15	2019-09-14	74	F	Y	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	1023	Low Dose	1	2019-04-15	2019-10-14	31	F	Y	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	1028	High Dose	2	2019-05-15	2019-11-14	74	F	Y	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	1033	Placebo	0	2019-06-15	2019-12-14	43	M	Y	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	1034	Low Dose	1	2019-07-15	2019-13-14	67	F	Y	Y
CDISCPILOT01-01-701-1047	CDISCPILOT01	1047	High Dose	2	2019-08-15	2019-14-14	48	M	Y	Y

### end_date.tsv (75 bytes)
end_date
2020-01-10
2020-01-10
2022-09-14
2020-06-30
2020-06-30
2021-02-18

### end_date_df.tsv (86 bytes)
end_date
2020-01-10
2020-06-30
2019-03-15
2019-03-15
2020-06-30
2021-02-18
2019-07-22

### start_date.tsv (66 bytes)
start_date
2019-07-22
2022-09-14
2020-01-10
2021-02-18
2019-03-15

### start_date_df.tsv (66 bytes)
start_date
2021-11-05
2022-04-27
2020-06-30
2022-04-27
2019-07-22

```

## Simple Prompt
```text
Create R script to perform derive var trtdurd using the admiral clinical task contract.

Input: datase.tsv, end_date.tsv, end_date_df.tsv, start_date.tsv, start_date_df.tsv
Output: result.csv

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### datase.tsv (578 bytes)
USUBJID	STUDYID	SUBJID	TRTA	TRTAN	TRTSDT	TRTEDT	AGE	SEX	SAFFL	FASFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	1015	Placebo	0	2019-03-15	2019-09-14	74	F	Y	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	1023	Low Dose	1	2019-04-15	2019-10-14	31	F	Y	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	1028	High Dose	2	2019-05-15	2019-11-14	74	F	Y	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	1033	Placebo	0	2019-06-15	2019-12-14	43	M	Y	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	1034	Low Dose	1	2019-07-15	2019-13-14	67	F	Y	Y
CDISCPILOT01-01-701-1047	CDISCPILOT01	1047	High Dose	2	2019-08-15	2019-14-14	48	M	Y	Y

### end_date.tsv (75 bytes)
end_date
2020-01-10
2020-01-10
2022-09-14
2020-06-30
2020-06-30
2021-02-18

### end_date_df.tsv (86 bytes)
end_date
2020-01-10
2020-06-30
2019-03-15
2019-03-15
2020-06-30
2021-02-18
2019-07-22

### start_date.tsv (66 bytes)
start_date
2019-07-22
2022-09-14
2020-01-10
2021-02-18
2019-03-15

### start_date_df.tsv (66 bytes)
start_date
2021-11-05
2022-04-27
2020-06-30
2022-04-27
2019-07-22

```

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "message": "Timeout after 120s",
  "returncode": "",
  "stderr": "",
  "comparison": ""
}
```

## Simple Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "TIMEOUT",
  "tier": "exec_fail",
  "message": "Timeout after 120s",
  "returncode": "",
  "stderr": "",
  "comparison": ""
}
```

## Reference Solution Head
```r
suppressPackageStartupMessages(library(admiral))

# 1. 读取输入数据
datase_path <- file.path("inputs", "datase.tsv")
if (!file.exists(datase_path)) stop("datase.tsv is required input")
datase <- read.delim(datase_path, check.names = FALSE, stringsAsFactors = FALSE)

start_date_path <- file.path("inputs", "start_date.tsv")
if (!file.exists(start_date_path)) stop("start_date.tsv is required input")
start_date_df <- read.delim(start_date_path, check.names = FALSE, stringsAsFactors = FALSE)
start_date_val <- as.character(start_date_df[[ncol(start_date_df)]][1])

end_date_path <- file.path("inputs", "end_date.tsv")
if (!file.exists(end_date_path)) stop("end_date.tsv is required input")
end_date_df <- read.delim(end_date_path, check.names = FALSE, stringsAsFactors = FALSE)
end_date_val <- as.character(end_date_df[[ncol(end_date_df)]][1])

# 2. 解析日期
start_dt <- tryCatch(as.Date(start_date_val, tryFormats = c("%Y-%m-%d", "%Y/%m/%d")), error = function(e) Sys.Date())
end_dt <- tryCatch(as.Date(end_date_val, tryFormats = c("%Y-%m-%d", "%Y/%m/%d")), error = function(e) Sys.Date() + 30)

# 3. 构建数据集 (需 TRTSDT, TRTEDT)
datase$TRTSDT <- start_dt
datase$TRTEDT <- end_dt

# 4. 执行函数 (默认 start_date=TRTSDT, end_date=TRTEDT)
result <- admiral::derive_var_trtdurd(datase)

# 5. 保存输出
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)

```

## Current Solution
```r
library(admiral)
library(readr)
library(dplyr)
library(purrr)
library(lubridate)

#-----------------------------
# Helper: safe date parser
#-----------------------------
parse_date_safe <- function(x, col_name) {
  d <- suppressWarnings(ymd(x))
  if (any(is.na(d) & !is.na(x))) {
    warning(
      sprintf(
        "Some values in '%s' could not be parsed as dates:\n%s",
        col_name,
        paste(unique(x[is.na(d) & !is.na(x)]), collapse = ", ")
      )
    )
  }
  d
}

#-----------------------------
# Read & validate input data
#-----------------------------
# Main dataset
datase_path <- file.path("inputs", "datase.tsv")
datase <- read_tsv(datase_path, show_col_types = FALSE)

# Basic validation
req_vars <- c("TRTSDT", "TRTEDT")
missing_vars <- setdiff(req_vars, names(datase))
if (length(missing_vars) > 0) {
  stop("datase is missing required variables: ", paste(missing_vars, collapse = ", "))
}

# Parse TRTSDT/TRTEDT as dates
datase <- datase %>%
  mutate(
    start_date = parse_date_safe(TRTSDT, "TRTSDT"),
    end_date   = parse_date_safe(TRTEDT, "TRTEDT")
  )

# Check for missing or inverted dates
if (any(is.na(datase$start_date))) {
  warning("Some start_date values are NA after parsing.")
}
if (any(is.na(datase$end_date))) {
  warning("Some end_date values are NA after parsing.")
}
if (any(datase$end_date < datase$start_date, na.rm = TRUE)) {
  warning("Some records have end_date < start_date; TRTDURD may be negative.")
}

#-----------------------------
# Optional: load standalone start/end tables
# (for validation / alignment checks)
#-----------------------------
start_date_tbl_path     <- file.path("inputs", "start_date.tsv")
end_date_tbl_path       <- file.path("inputs", "end_date.tsv")
start_date_df_tbl_path  <- file.path("inputs", "start_date_df.tsv")
end_date_df_tbl_path    <- file.path("inputs", "end_date_df.tsv")

start_date_tbl    <- read_tsv(start_date_tbl_path, show_col_types = FALSE)
end_date_tbl      <- read_tsv(end_date_tbl_path, show_col_types = FALSE)
start_date_df_tbl <- read_tsv(start_date_df_tbl_path, show_col_types = FALSE)
end_date_df_tbl   <- read_tsv(end_date_df_tbl_path, show_col_types = FALSE)

start_date_tbl <- start_date_tbl %>%
  mutate(start_date = parse_date_safe(start_date, "start_date"))
end_date_tbl <- end_date_tbl %>%
  mutate(end_date = parse_date_safe(end_date, "end_date"))
start_date_df_tbl <- start_date_df_tbl %>%
  mutate(start_date = parse_date_safe(start_date, "start_date"))
end_date_df_tbl <- end_date_df_tbl %>%
  mutate(end_date = parse_date_safe(end_date, "end_date"))

# Simple alignment checks (no join key provided, so only length checks)
if (nrow(start_date_tbl) != nrow(end_date_tbl)) {
  warning("start_date.tsv and end_date.tsv have different row counts; potential misalignment.")
}
if (nrow(start_date_df_tbl) != nrow(end_date_df_tbl)) {
  warning("start_date_df.tsv and end_date_df.tsv have different row counts; potential misalignment.")
}

#-----------------------------
# Wrapper: derive_var_trtdurd
#-----------------------------
#' Derive Treatment Duration (Days)
#'
#' Wrapper around `derive_vars_duration()` to derive TRTDURD
#' as (end_date - start_date + 1) in days.
#'
#' @param datase `r roxygen_param_dataset(expected_vars = c("start_date", "end_date"))`
#' @param start_date The start date. A date or date-time object is expected.
#' @param end_date   The end date. A date or date-time object is expected.
#'
#' @return The input dataset with `TRTDURD` added.
derive_var_trtdurd <- function(datase,
                               start_date,
                               end_date) {
  if (!all(c("start_date", "end_date") %in% names(datase))) {
    stop("datase must contain 'start_date' and 'end_date' variables.")
  }

  datase %>%
    derive_vars_duration(
      new_var        = TRTDURD,
      start_date     = {{ start_date }},
      end_date       = {{ end_date }},
      out_unit       = "days",
      add_one        = TRUE
    )
}

#-----------------------------
# Apply wrapper to datase
#-----------------------------
datase_trt <- derive_var_trtdurd(
  datase    = datase,
  start_date = start_date,
  end_date   = end_date
)

#-----------------------------
# Basic post-derivation checks
#-----------------------------
if (!"TRTDURD" %in% names(datase_trt)) {
  stop("TRTDURD was not created in datase_trt.")
}

if (any(is.na(datase_trt$TRTDURD) & !is.na(datase_trt$start_date) & !is.na(datase_trt$end_date))) {
  warning("Some TRTDURD values are NA despite non-missing start_date and end_date.")
}

if (any(datase_trt$TRTDURD <= 0, na.rm = TRUE)) {
  warning("Some TRTDURD values are non-positive; check for date issues.")
}

#-----------------------------
# Write outputs
#-----------------------------
dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

datase_csv_path <- file.path("outputs", "datase_trt.csv")
datase_rds_path <- file.path("outputs", "datase_trt.rds")

write_csv(datase_trt, datase_csv_path, na = "")
saveRDS(datase_trt, datase_rd
```

## Simple Solution
```r
#!/usr/bin/env Rscript

library(admiral)
library(dplyr)
library(readr)
library(lubridate)

# Create outputs directory if it doesn't exist
if (!dir.exists("outputs")) dir.create("outputs", recursive = TRUE)

# Read input datasets
adsl <- read_tsv(
  file = file.path("inputs", "datase.tsv"),
  col_types = cols(
    USUBJID = col_character(),
    STUDYID = col_character(),
    SUBJID  = col_character(),
    TRTA    = col_character(),
    TRTAN   = col_double(),
    TRTSDT  = col_character(),
    TRTEDT  = col_character(),
    AGE     = col_double(),
    SEX     = col_character(),
    SAFFL   = col_character(),
    FASFL   = col_character()
  )
) %>%
  mutate(
    TRTSDT = ymd(TRTSDT),
    TRTEDT = ymd(TRTEDT)
  )

end_date <- read_tsv(
  file = file.path("inputs", "end_date.tsv"),
  col_types = cols(
    end_date = col_character()
  )
) %>%
  mutate(end_date = ymd(end_date))

end_date_df <- read_tsv(
  file = file.path("inputs", "end_date_df.tsv"),
  col_types = cols(
    end_date = col_character()
  )
) %>%
  mutate(end_date = ymd(end_date))

start_date <- read_tsv(
  file = file.path("inputs", "start_date.tsv"),
  col_types = cols(
    start_date = col_character()
  )
) %>%
  mutate(start_date = ymd(start_date))

start_date_df <- read_tsv(
  file = file.path("inputs", "start_date_df.tsv"),
  col_types = cols(
    start_date = col_character()
  )
) %>%
  mutate(start_date = ymd(start_date))

# For this script, use ADSL treatment start/end as reference for TRTDURD
# TRTDURD = (TRTEDT - TRTSDT) + 1, as per common ADaM convention
result <- adsl %>%
  derive_var_trtdurd(
    start_date = TRTSDT,
    end_date   = TRTEDT
  )

# Write result
write_csv(result, file.path("outputs", "result.csv"), na = "")
```

## Current Candidate Prompt File
```text
Write R code to derive total treatment duration (days) using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/datase.tsv, inputs/start_date.tsv, inputs/end_date.tsv). **Note:** This is a wrapper function for the more generic `derive_vars_duration()`. Additional details: start to end date plus one. Use admiral's derive_var_trtdurd function with the following parameters: datase (t `r roxygen_param_dataset(expected_vars = c("start_date", "end_date"))`), start_date (The start date A date or date-time object is expected.), end_date (The end date A date or date-time object is expected.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with `TRTDURD` added. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```

## Simple Candidate Prompt File
```text
Write R code to derive total treatment duration (days) using admiral. At the beginning, load the required packages: library(admiral). The input data files are stored in inputs/ directory (inputs/datase.tsv, inputs/start_date.tsv, inputs/end_date.tsv). **Note:** This is a wrapper function for the more generic `derive_vars_duration()`. Additional details: start to end date plus one. Use admiral's derive_var_trtdurd function with the following parameters: datase (t `r roxygen_param_dataset(expected_vars = c("start_date", "end_date"))`), start_date (The start date A date or date-time object is expected.), end_date (The end date A date or date-time object is expected.). Ensure that you carefully read and process the input data according to the parameter requirements. The function returns: The input dataset with `TRTDURD` added. After calling the function, save the result to outputs/ directory as appropriate file format (CSV for data frames, RDS for complex objects). Before finishing, confirm that the output files were written correctly and check for any unexpected patterns or errors that might indicate data misalignment or parsing issues. Ensure proper error handling and data validation throughout the code.
```