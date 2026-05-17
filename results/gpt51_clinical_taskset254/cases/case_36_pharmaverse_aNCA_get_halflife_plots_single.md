# Case 36 - `pharmaverse/aNCA/get_halflife_plots_single`

**Package:** `aNCA`  **Function:** `get_halflife_plots_single`  **Expected artifacts:** `outputs/result.csv, outputs/result.rds`

**Current prompt status:** `FAIL` / tier `output_bad`  
**Simple prompt status:** `FAIL` / tier `output_bad`  
**Audit root cause:** `prompt_wrong`  **Confidence:** `medium`

## Audit Evidence

Reference prompt says use internal `aNCA:::get_halflife_plots_single`; current prompt says implement an equivalent data transformation directly. Outputs are data dumps (`(54, 17)` and `(3, 11)`) while reference CSV is empty-shaped `(0, 1)`.

## Task Prompt From `task.json`

```text
Write R code to implement the **Get halflife plots single** workflow using the `aNCA` package.
At the beginning, load required packages: library(aNCA).

**Inputs:**
- `inputs/add_annotations.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'add_annotations.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/color.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'color.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/conc_col.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'conc_col.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/fit_line_data.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'fit_line_data.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/group_vars.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'group_vars.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/plot_data.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'plot_data.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/subtitle.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'subtitle.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/symbol.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'symbol.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/text.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'text.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/time_col.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'time_col.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/title.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'title.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/xlab.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'xlab.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).
- `inputs/ylab.tsv`: tab-separated values with a **header row**. Read with `read.delim(file.path('inputs', 'ylab.tsv'), check.names=FALSE, stringsAsFactors=FALSE)` and map columns to the arguments expected by `aNCA:::get_halflife_plots_single` (numeric vectors are often stored in a column named like the parameter).

**Required outputs for grading (exact paths):**
- `outputs/result.csv`
- `outputs/result.rds`

Create `outputs/` with `dir.create('outputs', showWarnings=FALSE)` if needed.
For CSV use `write.csv(..., row.names=FALSE)` unless you must preserve row names to match the reference.
For RDS use `saveRDS()`.
When both `outputs/result.csv` and `outputs/result.rds` are required, write the full object to the RDS file and a sensible tabular summary to the CSV.

Use the internal function `aNCA:::get_halflife_plots_single` when it is the correct public API for this task; otherwise reproduce the same computational result as the reference using the given inputs.
```

## Current Generated Prompt

```text
I am preparing an aNCA clinical pharmacokinetic support task for get halflife plots single. The available input files are `inputs/add_annotations.tsv`, `inputs/color.tsv`, `inputs/conc_col.tsv`, `inputs/fit_line_data.tsv`, `inputs/group_vars.tsv`, `inputs/plot_data.tsv`, `inputs/subtitle.tsv`, `inputs/symbol.tsv`, `inputs/text.tsv`, `inputs/time_col.tsv`, `inputs/title.tsv`, `inputs/xlab.tsv`, `inputs/ylab.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.

## Inputs preview (no reference answers)

### add_annotations.tsv (37 bytes)
add_annotations
AVAL
AVISITN
USUBJID

### color.tsv (27 bytes)
color
AVAL
AVISITN
USUBJID

### conc_col.tsv (30 bytes)
conc_col
AVAL
AVISITN
USUBJID

### fit_line_data.tsv (5948 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.61	0	Baseline	2020-01-15	Y	99.59	1.02	1.0274	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	98.26	4	Week 4	2020-02-15	Y	99.59	-1.33	-1.3323	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.94	12	Week 12	2020-04-15	Y	99.59	0.35	0.3546	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	69.69	0	Baseline	2020-01-15	Y	69.88	-0.19	-0.2772	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	70.66	4	Week 4	2020-02-15	Y	69.88	0.78	1.1108	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	69.62	12	Week 12	2020-04-15	Y	69.88	-0.26	-0.3774	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	66.22	0	Baseline	2020-01-15	Y	68.75	-2.53	-3.6807	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	64.57	4	Week 4	2020-02-15	Y	68.75	-4.18	-6.0807	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	69.59	12	Week 12	2020-04-15	Y	68.75	0.84	1.2211	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	124.45	0	Baseline	2020-01-15	Y	124.93	-0.48	-0.3843	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.62	4	Week 4	2020-02-15	Y	124.93	0.69	0.5522	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.94	12	Week 12	2020-04-15	Y	124.93	-0.99	-0.7926	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.95	0	Baseline	2020-01-15	Y	75.38	-0.43	-0.5706	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	73.81	4	Week 4	2020-02-15	Y	75.38	-1.57	-2.0829	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.14	12	Week 12	2020-04-15	Y	75.38	-1.24	-1.6451	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	83.02	0	Baseline	2020-01-15	Y	82.76	0.26	0.3177	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	81.95	4	Week 4	2020-02-15	Y	82.76	-0.81	-0.9752	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	82.91	12	Week 12	2020-04-15	Y	82.76	0.15	0.1848	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	107.49	0	Baseline	2020-01-15	Y	110.85	-3.36	-3.0299	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	109.72	4	Week 4	2020-02-15	Y	110.85	-1.13	-1.0182	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.34	12	Week 12	2020-04-15	Y	110.85	0.49	0.4433	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	76.14	0	Baseline	2020-01-15	Y	77.0	-0.86	-1.1232	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	77.59	4	Week 4	2020-02-15	Y	77.0	0.59	0.7598	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	78.73	12	Week 12	2020-04-15	Y	77.0	1.73	2.2403	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	94.07	0	Baseline	2020-01-15	Y	91.34	2.73	2.9914	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	91.36	4	Week 4	2020-02-15	Y	91.34	0.02	0.0244	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	90.28	12	Week 12	2020-04-15	Y	91.34	-1.06	-1.158	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.59	0	Baseline	2020-01-15	Y	111.17	0.42	0.3735	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	112.18	4	Week 4	2020-02-15	Y	111.17	1.01	0.9042	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.94	12	Week 12	2020-04-15	Y	111.17	0.77	0.6883	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	84.69	0	Baseline	2020-01-15	Y	84.88	-0.19	-0.2194	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	83.09	4	Week 4	2020-02-15	Y	84.88	-1.79	-2.1045	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	85.55	12	Week 12	2020-04-15	Y	84.88	0.67	0.7939	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	99.21	0	Baseline	2020-01-15	Y	98.42	0.79	0.8034	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	100.33	4	Week 4	2020-02-15	Y	98.42	1.91	1.9414	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	96.72	12	Week 12	2020-04-15	Y	98.42	-1.7	-1.7266	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	106.3	0	Baseline	2020-01-15	Y	104.07	2.23	2.1381	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.53	4	Week 4	2020-02-15	Y	104.07	-2.54	-2.4452	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.81	12	Week 12	2020-04-15	Y	104.07	-2.26	-2.1761	
... [15 more lines omitted]

### group_vars.tsv (32 bytes)
group_vars
AVAL
AVISITN
USUBJID

### plot_data.tsv (5941 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	106.72	0	Baseline	2020-01-15	Y	104.64	2.08	1.988	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.46	4	Week 4	2020-02-15	Y	104.64	0.82	0.7838	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.92	12	Week 12	2020-04-15	Y	104.64	-1.72	-1.6435	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	59.41	0	Baseline	2020-01-15	Y	61.19	-1.78	-2.9077	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	61.02	4	Week 4	2020-02-15	Y	61.19	-0.17	-0.2765	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	61.6	12	Week 12	2020-04-15	Y	61.19	0.41	0.6714	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	90.63	0	Baseline	2020-01-15	Y	89.43	1.2	1.3452	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	88.96	4	Week 4	2020-02-15	Y	89.43	-0.47	-0.5222	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	89.17	12	Week 12	2020-04-15	Y	89.43	-0.26	-0.2874	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.85	0	Baseline	2020-01-15	Y	128.76	-2.91	-2.258	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.47	4	Week 4	2020-02-15	Y	128.76	1.71	1.3301	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	131.24	12	Week 12	2020-04-15	Y	128.76	2.48	1.9282	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	71.62	0	Baseline	2020-01-15	Y	71.64	-0.02	-0.0246	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	72.15	4	Week 4	2020-02-15	Y	71.64	0.51	0.7152	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	69.31	12	Week 12	2020-04-15	Y	71.64	-2.33	-3.2492	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	69.04	0	Baseline	2020-01-15	Y	67.19	1.85	2.7592	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	65.17	4	Week 4	2020-02-15	Y	67.19	-2.02	-3.0009	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	71.64	12	Week 12	2020-04-15	Y	67.19	4.45	6.6291	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.83	0	Baseline	2020-01-15	Y	102.22	-1.39	-1.3583	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.43	4	Week 4	2020-02-15	Y	102.22	-0.79	-0.7713	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.31	12	Week 12	2020-04-15	Y	102.22	2.09	2.0462	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	61.97	0	Baseline	2020-01-15	Y	62.87	-0.9	-1.4264	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	63.86	4	Week 4	2020-02-15	Y	62.87	0.99	1.5799	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	62.68	12	Week 12	2020-04-15	Y	62.87	-0.19	-0.2971	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	103.4	0	Baseline	2020-01-15	Y	99.95	3.45	3.4553	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	99.48	4	Week 4	2020-02-15	Y	99.95	-0.47	-0.4668	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	98.79	12	Week 12	2020-04-15	Y	99.95	-1.16	-1.1571	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.42	0	Baseline	2020-01-15	Y	100.64	1.78	1.7638	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.22	4	Week 4	2020-02-15	Y	100.64	1.58	1.5651	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.61	12	Week 12	2020-04-15	Y	100.64	-1.03	-1.0282	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	67.48	0	Baseline	2020-01-15	Y	67.54	-0.06	-0.09	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	68.25	4	Week 4	2020-02-15	Y	67.54	0.71	1.0501	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	67.27	12	Week 12	2020-04-15	Y	67.54	-0.27	-0.4009	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	82.46	0	Baseline	2020-01-15	Y	80.26	2.2	2.7414	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	82.63	4	Week 4	2020-02-15	Y	80.26	2.37	2.9532	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	84.2	12	Week 12	2020-04-15	Y	80.26	3.94	4.9093	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	119.5	0	Baseline	2020-01-15	Y	118.53	0.97	0.815	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.07	4	Week 4	2020-02-15	Y	118.53	-0.46	-0.3914	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	121.01	12	Week 12	2020-04-15	Y	118.53	2.48	2.0889	
... [15 more lines omitted]

### subtitle.tsv (30 bytes)
subtitle
AVAL
AVISITN
USUBJID

### symbol.tsv (28 bytes)
symbol
AVAL
AVISITN
USUBJID

### text.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### time_col.tsv (30 bytes)
time_col
AVAL
AVISITN
USUBJID

### title.tsv (27 bytes)
title
AVAL
AVISITN
USUBJID

### xlab.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### ylab.tsv (26 bytes)
ylab
AVAL
AVISITN
USUBJID

```

## Simple Generated Prompt

```text
Create R script to perform get halflife plots single using the aNCA clinical task contract.

Input: add_annotations.tsv, color.tsv, conc_col.tsv, fit_line_data.tsv, group_vars.tsv, plot_data.tsv, subtitle.tsv, symbol.tsv, text.tsv, time_col.tsv, title.tsv, xlab.tsv, ylab.tsv
Output: result.csv, result.rds

Read files from inputs/ and write the required files under outputs/.

## Inputs preview (no reference answers)

### add_annotations.tsv (37 bytes)
add_annotations
AVAL
AVISITN
USUBJID

### color.tsv (27 bytes)
color
AVAL
AVISITN
USUBJID

### conc_col.tsv (30 bytes)
conc_col
AVAL
AVISITN
USUBJID

### fit_line_data.tsv (5948 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.61	0	Baseline	2020-01-15	Y	99.59	1.02	1.0274	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	98.26	4	Week 4	2020-02-15	Y	99.59	-1.33	-1.3323	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.94	12	Week 12	2020-04-15	Y	99.59	0.35	0.3546	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	69.69	0	Baseline	2020-01-15	Y	69.88	-0.19	-0.2772	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	70.66	4	Week 4	2020-02-15	Y	69.88	0.78	1.1108	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	69.62	12	Week 12	2020-04-15	Y	69.88	-0.26	-0.3774	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	66.22	0	Baseline	2020-01-15	Y	68.75	-2.53	-3.6807	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	64.57	4	Week 4	2020-02-15	Y	68.75	-4.18	-6.0807	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	69.59	12	Week 12	2020-04-15	Y	68.75	0.84	1.2211	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	124.45	0	Baseline	2020-01-15	Y	124.93	-0.48	-0.3843	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.62	4	Week 4	2020-02-15	Y	124.93	0.69	0.5522	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	123.94	12	Week 12	2020-04-15	Y	124.93	-0.99	-0.7926	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.95	0	Baseline	2020-01-15	Y	75.38	-0.43	-0.5706	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	73.81	4	Week 4	2020-02-15	Y	75.38	-1.57	-2.0829	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	74.14	12	Week 12	2020-04-15	Y	75.38	-1.24	-1.6451	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	83.02	0	Baseline	2020-01-15	Y	82.76	0.26	0.3177	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	81.95	4	Week 4	2020-02-15	Y	82.76	-0.81	-0.9752	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	82.91	12	Week 12	2020-04-15	Y	82.76	0.15	0.1848	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	107.49	0	Baseline	2020-01-15	Y	110.85	-3.36	-3.0299	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	109.72	4	Week 4	2020-02-15	Y	110.85	-1.13	-1.0182	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.34	12	Week 12	2020-04-15	Y	110.85	0.49	0.4433	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	76.14	0	Baseline	2020-01-15	Y	77.0	-0.86	-1.1232	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	77.59	4	Week 4	2020-02-15	Y	77.0	0.59	0.7598	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	78.73	12	Week 12	2020-04-15	Y	77.0	1.73	2.2403	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	94.07	0	Baseline	2020-01-15	Y	91.34	2.73	2.9914	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	91.36	4	Week 4	2020-02-15	Y	91.34	0.02	0.0244	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	90.28	12	Week 12	2020-04-15	Y	91.34	-1.06	-1.158	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.59	0	Baseline	2020-01-15	Y	111.17	0.42	0.3735	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	112.18	4	Week 4	2020-02-15	Y	111.17	1.01	0.9042	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	111.94	12	Week 12	2020-04-15	Y	111.17	0.77	0.6883	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	84.69	0	Baseline	2020-01-15	Y	84.88	-0.19	-0.2194	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	83.09	4	Week 4	2020-02-15	Y	84.88	-1.79	-2.1045	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	85.55	12	Week 12	2020-04-15	Y	84.88	0.67	0.7939	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	99.21	0	Baseline	2020-01-15	Y	98.42	0.79	0.8034	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	100.33	4	Week 4	2020-02-15	Y	98.42	1.91	1.9414	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	96.72	12	Week 12	2020-04-15	Y	98.42	-1.7	-1.7266	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	106.3	0	Baseline	2020-01-15	Y	104.07	2.23	2.1381	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.53	4	Week 4	2020-02-15	Y	104.07	-2.54	-2.4452	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.81	12	Week 12	2020-04-15	Y	104.07	-2.26	-2.1761	
... [15 more lines omitted]

### group_vars.tsv (32 bytes)
group_vars
AVAL
AVISITN
USUBJID

### plot_data.tsv (5941 bytes)
USUBJID	STUDYID	PARAMCD	PARAM	AVAL	AVISITN	AVISIT	ADT	ANL01FL	BASE	CHG	PCHG	ABLFL
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	106.72	0	Baseline	2020-01-15	Y	104.64	2.08	1.988	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	105.46	4	Week 4	2020-02-15	Y	104.64	0.82	0.7838	
CDISCPILOT01-01-701-1015	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.92	12	Week 12	2020-04-15	Y	104.64	-1.72	-1.6435	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	59.41	0	Baseline	2020-01-15	Y	61.19	-1.78	-2.9077	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	61.02	4	Week 4	2020-02-15	Y	61.19	-0.17	-0.2765	
CDISCPILOT01-01-701-1015	CDISCPILOT01	DIABP	DIABP (mmHg)	61.6	12	Week 12	2020-04-15	Y	61.19	0.41	0.6714	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	90.63	0	Baseline	2020-01-15	Y	89.43	1.2	1.3452	Y
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	88.96	4	Week 4	2020-02-15	Y	89.43	-0.47	-0.5222	
CDISCPILOT01-01-701-1015	CDISCPILOT01	PULSE	PULSE (beats/min)	89.17	12	Week 12	2020-04-15	Y	89.43	-0.26	-0.2874	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	125.85	0	Baseline	2020-01-15	Y	128.76	-2.91	-2.258	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	130.47	4	Week 4	2020-02-15	Y	128.76	1.71	1.3301	
CDISCPILOT01-01-701-1023	CDISCPILOT01	SYSBP	SYSBP (mmHg)	131.24	12	Week 12	2020-04-15	Y	128.76	2.48	1.9282	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	71.62	0	Baseline	2020-01-15	Y	71.64	-0.02	-0.0246	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	72.15	4	Week 4	2020-02-15	Y	71.64	0.51	0.7152	
CDISCPILOT01-01-701-1023	CDISCPILOT01	DIABP	DIABP (mmHg)	69.31	12	Week 12	2020-04-15	Y	71.64	-2.33	-3.2492	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	69.04	0	Baseline	2020-01-15	Y	67.19	1.85	2.7592	Y
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	65.17	4	Week 4	2020-02-15	Y	67.19	-2.02	-3.0009	
CDISCPILOT01-01-701-1023	CDISCPILOT01	PULSE	PULSE (beats/min)	71.64	12	Week 12	2020-04-15	Y	67.19	4.45	6.6291	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	100.83	0	Baseline	2020-01-15	Y	102.22	-1.39	-1.3583	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	101.43	4	Week 4	2020-02-15	Y	102.22	-0.79	-0.7713	
CDISCPILOT01-01-701-1028	CDISCPILOT01	SYSBP	SYSBP (mmHg)	104.31	12	Week 12	2020-04-15	Y	102.22	2.09	2.0462	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	61.97	0	Baseline	2020-01-15	Y	62.87	-0.9	-1.4264	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	63.86	4	Week 4	2020-02-15	Y	62.87	0.99	1.5799	
CDISCPILOT01-01-701-1028	CDISCPILOT01	DIABP	DIABP (mmHg)	62.68	12	Week 12	2020-04-15	Y	62.87	-0.19	-0.2971	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	103.4	0	Baseline	2020-01-15	Y	99.95	3.45	3.4553	Y
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	99.48	4	Week 4	2020-02-15	Y	99.95	-0.47	-0.4668	
CDISCPILOT01-01-701-1028	CDISCPILOT01	PULSE	PULSE (beats/min)	98.79	12	Week 12	2020-04-15	Y	99.95	-1.16	-1.1571	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.42	0	Baseline	2020-01-15	Y	100.64	1.78	1.7638	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	102.22	4	Week 4	2020-02-15	Y	100.64	1.58	1.5651	
CDISCPILOT01-01-701-1033	CDISCPILOT01	SYSBP	SYSBP (mmHg)	99.61	12	Week 12	2020-04-15	Y	100.64	-1.03	-1.0282	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	67.48	0	Baseline	2020-01-15	Y	67.54	-0.06	-0.09	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	68.25	4	Week 4	2020-02-15	Y	67.54	0.71	1.0501	
CDISCPILOT01-01-701-1033	CDISCPILOT01	DIABP	DIABP (mmHg)	67.27	12	Week 12	2020-04-15	Y	67.54	-0.27	-0.4009	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	82.46	0	Baseline	2020-01-15	Y	80.26	2.2	2.7414	Y
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	82.63	4	Week 4	2020-02-15	Y	80.26	2.37	2.9532	
CDISCPILOT01-01-701-1033	CDISCPILOT01	PULSE	PULSE (beats/min)	84.2	12	Week 12	2020-04-15	Y	80.26	3.94	4.9093	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	119.5	0	Baseline	2020-01-15	Y	118.53	0.97	0.815	Y
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	118.07	4	Week 4	2020-02-15	Y	118.53	-0.46	-0.3914	
CDISCPILOT01-01-701-1034	CDISCPILOT01	SYSBP	SYSBP (mmHg)	121.01	12	Week 12	2020-04-15	Y	118.53	2.48	2.0889	
... [15 more lines omitted]

### subtitle.tsv (30 bytes)
subtitle
AVAL
AVISITN
USUBJID

### symbol.tsv (28 bytes)
symbol
AVAL
AVISITN
USUBJID

### text.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### time_col.tsv (30 bytes)
time_col
AVAL
AVISITN
USUBJID

### title.tsv (27 bytes)
title
AVAL
AVISITN
USUBJID

### xlab.tsv (34 bytes)
x
SYSBP
DIABP
PULSE
WEIGHT
HEIGHT

### ylab.tsv (26 bytes)
ylab
AVAL
AVISITN
USUBJID

```

## Actual Input Files

**`add_annotations.tsv`**

```tsv
add_annotations
FALSE

```

**`color.tsv`**

```tsv
color
"test_value"

```

**`conc_col.tsv`**

```tsv
conc_col
"yes"
"no"
"true"
"false"
"active"

```

**`fit_line_data.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

```

**`group_vars.tsv`**

```tsv
group_vars
"item1"
"item2"
"item3"
"item4"
"item5"

```

**`plot_data.tsv`**

```tsv
id	value	group	category
1	10.5	A	Type1
2	20.3	B	Type2
3	30.7	A	Type1
4	40.2	B	Type2
5	50.9	A	Type1

```

**`subtitle.tsv`**

```tsv
subtitle
"yes"
"no"
"true"
"false"
"active"

```

**`symbol.tsv`**

```tsv
symbol
"test_value"

```

**`text.tsv`**

```tsv
text
"test_value"

```

**`time_col.tsv`**

```tsv
time_col
"yes"
"no"
"true"
"false"
"active"

```

**`title.tsv`**

```tsv
title
"yes"
"no"
"true"
"false"
"active"

```

**`xlab.tsv`**

```tsv
xlab
"test_value"

```

_Omitted 1 additional files._

## Reference Output Files

**`result.csv`**

```csv
""

```

**`summary.csv`**

```csv
"n_rows","n_cols","col_names"
0,0,""

```

## Reference Code

**`solution.R`**

```r
suppressPackageStartupMessages(library(aNCA))

# 1. 读取输入数据 / Read input data
fit_line_data_path <- file.path("inputs", "fit_line_data.tsv")
if (!file.exists(fit_line_data_path)) {
  stop("fit_line_data.tsv is required input")
}
fit_line_data <- read.delim(fit_line_data_path, check.names = FALSE, stringsAsFactors = FALSE)
plot_data_path <- file.path("inputs", "plot_data.tsv")
if (!file.exists(plot_data_path)) {
  stop("plot_data.tsv is required input")
}
plot_data <- read.delim(plot_data_path, check.names = FALSE, stringsAsFactors = FALSE)
time_col_path <- file.path("inputs", "time_col.tsv")
if (!file.exists(time_col_path)) {
  stop("time_col.tsv is required input")
}
time_col_df <- read.delim(time_col_path, check.names = FALSE, stringsAsFactors = FALSE)
time_col <- time_col_df$time_col
conc_col_path <- file.path("inputs", "conc_col.tsv")
if (!file.exists(conc_col_path)) {
  stop("conc_col.tsv is required input")
}
conc_col_df <- read.delim(conc_col_path, check.names = FALSE, stringsAsFactors = FALSE)
conc_col <- conc_col_df$conc_col
title_path <- file.path("inputs", "title.tsv")
if (!file.exists(title_path)) {
  stop("title.tsv is required input")
}
title <- read.delim(title_path, check.names = FALSE, stringsAsFactors = FALSE)
xlab_path <- file.path("inputs", "xlab.tsv")
if (!file.exists(xlab_path)) {
  stop("xlab.tsv is required input")
}
xlab <- read.delim(xlab_path, check.names = FALSE, stringsAsFactors = FALSE)
ylab_path <- file.path("inputs", "ylab.tsv")
if (!file.exists(ylab_path)) {
  stop("ylab.tsv is required input")
}
ylab <- read.delim(ylab_path, check.names = FALSE, stringsAsFactors = FALSE)
subtitle_path <- file.path("inputs", "subtitle.tsv")
if (!file.exists(subtitle_path)) {
  stop("subtitle.tsv is required input")
}
subtitle <- read.delim(subtitle_path, check.names = FALSE, stringsAsFactors = FALSE)
color_path <- file.path("inputs", "color.tsv")
if (!file.exists(color_path)) {
  stop("color.tsv is required input")
}
color <- read.delim(color_path, check.names = FALSE, stringsAsFactors = FALSE)
symbol_path <- file.path("inputs", "symbol.tsv")
if (!file.exists(symbol_path)) {
  stop("symbol.tsv is required input")
}
symbol <- read.delim(symbol_path, check.names = FALSE, stringsAsFactors = FALSE)
group_vars_path <- file.path("inputs", "group_vars.tsv")
if (!file.exists(group_vars_path)) {
  stop("group_vars.tsv is required input")
}
group_vars_df <- read.delim(group_vars_path, check.names = FALSE, stringsAsFactors = FALSE)
group_vars <- group_vars_df$group_vars
add_annotations_path <- file.path("inputs", "add_annotations.tsv")
if (!file.exists(add_annotations_path)) {
  stop("add_annotations.tsv is required input")
}
add_annotations_df <- read.delim(add_annotations_path, check.names = FALSE, stringsAsFactors = FALSE)
add_annotations <- as.logical(add_annotations_df$add_annotations)
text_path <- file.path("inputs", "text.tsv")
if (!file.exists(text_path)) {
  stop("text.tsv is required input")
}
text <- read.delim(text_path, check.names = FALSE, stringsAsFactors = FALSE)

# 2. 数据验证 / Data validation
# 检查数据框的基本结构

# 2. 数据验证 / Data validation
# 检查数据框的基本结构
for (df_name in c("fit_line_data", "plot_data")) {
  df <- get(df_name)
  if (nrow(df) == 0) {
    stop(paste("Data frame", df_name, "is empty"))
  }
  if (ncol(df) == 0) {
    stop(paste("Data frame", df_name, "has no columns"))
  }
}

# 提取标量参数
if (is.data.frame(title) && ncol(title) > 0 && nrow(title) > 0) {
  title <- title[[1]][1]
} else if (is.character(title)) {
  title <- title[1]
}
if (is.data.frame(xlab) && ncol(xlab) > 0 && nrow(xlab) > 0) {
  xlab <- xlab[[1]][1]
} else if (is.character(xlab)) {
  xlab <- xlab[1]
}
if (is.data.frame(ylab) && ncol(ylab) > 0 && nrow(ylab) > 0) {
  ylab <- ylab[[1]][1]
} else if (is.character(ylab)) {
  ylab <- ylab[1]
}
if (is.data.frame(subtitle) && ncol(subtitle) > 0 && nrow(subtitle) > 0) {
  subtitle <- subtitle[[1]][1]
} else if (is.character(subtitle)) {
  subtitle <- subtitle[1]
}
if (is.data.frame(color) && ncol(color) > 0 && nrow(color) > 0) {
  color <- color[[1]][1]
} else if (is.character(color)) {
  color <- color[1]
}
if (is.data.frame(symbol) && ncol(symbol) > 0 && nrow(symbol) > 0) {
  symbol <- symbol[[1]][1]
} else if (is.character(symbol)) {
  symbol <- symbol[1]
}
if (is.data.frame(text) && ncol(text) > 0 && nrow(text) > 0) {
  text <- text[[1]][1]
} else if (is.character(text)) {
  text <- text[1]
}

# 3. 执行函数实现 / Execute function implementation
result <- tryCatch({
  aNCA:::get_halflife_plots_single(
    fit_line_data = fit_line_data,
    plot_data = plot_data,
    time_col = time_col,
    conc_col = conc_col,
    title = title,
    xlab = xlab,
    ylab = ylab,
    subtitle = subtitle,
    color = color,
    symbol = symbol,
    group_vars = group_vars,
    add_annotations = add_annotations,
    text = text
  )
}, error = function(e) {
  # 如果函数调用失败，返回NULL
  NULL
})


# 4. 创建结果数据框 / Create result dataframe
# 将函数结果与输入数据合并（如果可能）
if (is.vector(result) || is.numeric(result) || is.character(result)) {
  result_df <- data.frame(
    time_col = time_col, conc_col = conc_col,
    result = result,
    stringsAsFactors = FALSE)
  } else if (is.data.frame(result)) {
  result_df <- result
} else {
  result_df <- data.frame(result = result, stringsAsFactors = FALSE)
}

# 5. 生成汇总统计 / Generate summary statistics
if (is.data.frame(result_df)) {
  summary_stats <- data.frame(
    n_rows = nrow(result_df),
    n_cols = ncol(result_df),
    col_names = paste(colnames(result_df), collapse = ", "),
    stringsAsFactors = FALSE)
  } else if (is.vector(result) || is.numeric(result)) {
  summary_stats <- data.frame(
    n_values = length(result),
    mean_value = mean(result, na.rm = TRUE),
    min_value = min(result, na.rm = TRUE),
    max_value = max(result, na.rm = TRUE),
    median_value = median(result, na.rm = TRUE),
    stringsAsFactors = FALSE)
  } else {
  summary_stats <- data.frame(
    result_type = class(result)[1],
    stringsAsFactors = FALSE
  )
}

# 7. 保存输出 / Save outputs
outputs_dir <- "outputs"
dir.create(outputs_dir, showWarnings = FALSE)
if (exists("result_df") && is.data.frame(result_df)) {
  write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (exists("result")) {
  if (is.data.frame(result)) {
    write.csv(result, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else if (is.list(result)) {
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  } else if (is.vector(result) || is.numeric(result) || is.character(result)) {
    result_df <- data.frame(result = result, stringsAsFactors = FALSE)
    write.csv(result_df, file.path(outputs_dir, "result.csv"), row.names = FALSE)
  } else {
    saveRDS(result, file.path(outputs_dir, "result.rds"))
  }
} else {
  stop("No result variable found. Function implementation may not have returned a value.")
}
if (exists("summary_stats")) {
  write.csv(summary_stats, file.path(outputs_dir, "summary.csv"), row.names = FALSE)
}
```

## Current Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(purrr)
})

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

read_tsv_scalar <- function(path) {
  df <- read_tsv(path, col_types = cols(), show_col_types = FALSE)
  if (nrow(df) == 1L && ncol(df) == 1L) {
    df[[1, 1]]
  } else {
    df
  }
}

add_annotations <- read_tsv("inputs/add_annotations.tsv",
                            col_types = cols(),
                            show_col_types = FALSE)
color         <- read_tsv("inputs/color.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
conc_col      <- read_tsv("inputs/conc_col.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
group_vars    <- read_tsv("inputs/group_vars.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
subtitle      <- read_tsv("inputs/subtitle.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
symbol        <- read_tsv("inputs/symbol.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
time_col      <- read_tsv("inputs/time_col.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
title_tbl     <- read_tsv("inputs/title.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
ylab_tbl      <- read_tsv("inputs/ylab.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)

text_tbl  <- read_tsv("inputs/text.tsv",
                      col_types = cols(),
                      show_col_types = FALSE)
xlab_tbl  <- read_tsv("inputs/xlab.tsv",
                      col_types = cols(),
                      show_col_types = FALSE)

fit_line_data <- read_tsv("inputs/fit_line_data.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)
plot_data     <- read_tsv("inputs/plot_data.tsv",
                          col_types = cols(),
                          show_col_types = FALSE)

# Build a compact, inspectable summary that preserves alignment between
# plot_data and fit_line_data by joining on key aNCA-like variables
key_vars <- c("USUBJID", "STUDYID", "PARAMCD", "PARAM", "AVISITN", "AVISIT", "ADT")

result <- plot_data %>%
  rename(within_AVAL = AVAL,
         within_BASE = BASE,
         within_CHG  = CHG,
         within_PCHG = PCHG,
         within_ABLFL = ABLFL) %>%
  left_join(
    fit_line_data %>%
      rename(fit_AVAL = AVAL,
             fit_BASE = BASE,
             fit_CHG  = CHG,
             fit_PCHG = PCHG,
             fit_ABLFL = ABLFL),
    by = key_vars,
    suffix = c("", "")
  ) %>%
  select(
    USUBJID, STUDYID, PARAMCD, PARAM, AVISITN, AVISIT, ADT,
    within_AVAL, fit_AVAL,
    within_BASE, fit_BASE,
    within_CHG,  fit_CHG,
    within_PCHG, fit_PCHG,
    within_ABLFL, fit_ABLFL
  )

write_csv(result, "outputs/result.csv")

saveRDS(
  list(
    result        = result,
    add_annotations = add_annotations,
    color           = color,
    conc_col        = conc_col,
    group_vars      = group_vars,
    subtitle        = subtitle,
    symbol          = symbol,
    time_col        = time_col,
    title           = title_tbl,
    ylab            = ylab_tbl,
    text            = text_tbl,
    xlab            = xlab_tbl,
    plot_data       = plot_data,
    fit_line_data   = fit_line_data
  ),
  file = "outputs/result.rds"
)
```

## Current Prompt Execution Logs

**`stderr.txt`**

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

```

**`stdout.txt`**

```text

```

## Current Prompt Output Files

**`result.csv`**

```csv
USUBJID,STUDYID,PARAMCD,PARAM,AVISITN,AVISIT,ADT,within_AVAL,fit_AVAL,within_BASE,fit_BASE,within_CHG,fit_CHG,within_PCHG,fit_PCHG,within_ABLFL,fit_ABLFL
CDISCPILOT01-01-701-1015,CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,2020-01-15,106.72,100.61,104.64,99.59,2.08,1.02,1.988,1.0274,Y,Y
CDISCPILOT01-01-701-1015,CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,2020-02-15,105.46,98.26,104.64,99.59,0.82,-1.33,0.7838,-1.3323,NA,NA
CDISCPILOT01-01-701-1015,CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,2020-04-15,102.92,99.94,104.64,99.59,-1.72,0.35,-1.6435,0.3546,NA,NA
CDISCPILOT01-01-701-1015,CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,2020-01-15,59.41,69.69,61.19,69.88,-1.78,-0.19,-2.9077,-0.2772,Y,Y
CDISCPILOT01-01-701-1015,CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,2020-02-15,61.02,70.66,61.19,69.88,-0.17,0.78,-0.2765,1.1108,NA,NA
CDISCPILOT01-01-701-1015,CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,2020-04-15,61.6,69.62,61.19,69.88,0.41,-0.26,0.6714,-0.3774,NA,NA
CDISCPILOT01-01-701-1015,CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,2020-01-15,90.63,66.22,89.43,68.75,1.2,-2.53,1.3452,-3.6807,Y,Y
CDISCPILOT01-01-701-1015,CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,2020-02-15,88.96,64.57,89.43,68.75,-0.47,-4.18,-0.5222,-6.0807,NA,NA
CDISCPILOT01-01-701-1015,CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,2020-04-15,89.17,69.59,89.43,68.75,-0.26,0.84,-0.2874,1.2211,NA,NA
CDISCPILOT01-01-701-1023,CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,2020-01-15,125.85,124.45,128.76,124.93,-2.91,-0.48,-2.258,-0.3843,Y,Y
CDISCPILOT01-01-701-1023,CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,2020-02-15,130.47,125.62,128.76,124.93,1.71,0.69,1.3301,0.5522,NA,NA
CDISCPILOT01-01-701-1023,CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,2020-04-15,131.24,123.94,128.76,124.93,2.48,-0.99,1.9282,-0.7926,NA,NA
CDISCPILOT01-01-701-1023,CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,2020-01-15,71.62,74.95,71.64,75.38,-0.02,-0.43,-0.0246,-0.5706,Y,Y
CDISCPILOT01-01-701-1023,CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,2020-02-15,72.15,73.81,71.64,75.38,0.51,-1.57,0.7152,-2.0829,NA,NA
CDISCPILOT01-01-701-1023,CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,2020-04-15,69.31,74.14,71.64,75.38,-2.33,-1.24,-3.2492,-1.6451,NA,NA
CDISCPILOT01-01-701-1023,CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,2020-01-15,69.04,83.02,67.19,82.76,1.85,0.26,2.7592,0.3177,Y,Y
CDISCPILOT01-01-701-1023,CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,2020-02-15,65.17,81.95,67.19,82.76,-2.02,-0.81,-3.0009,-0.9752,NA,NA
CDISCPILOT01-01-701-1023,CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,2020-04-15,71.64,82.91,67.19,82.76,4.45,0.15,6.6291,0.1848,NA,NA
CDISCPILOT01-01-701-1028,CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,2020-01-15,100.83,107.49,102.22,110.85,-1.39,-3.36,-1.3583,-3.0299,Y,Y
CDISCPILOT01-01-701-1028,CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,2020-02-15,101.43,109.72,102.22,110.85,-0.79,-1.13,-0.7713,-1.0182,NA,NA
CDISCPILOT01-01-701-1028,CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,2020-04-15,104.31,111.34,102.22,110.85,2.09,0.49,2.0462,0.4433,NA,NA
CDISCPILOT01-01-701-1028,CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,2020-01-15,61.97,76.14,62.87,77,-0.9,-0.86,-1.4264,-1.1232,Y,Y
CDISCPILOT01-01-701-1028,CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,2020-02-15,63.86,77.59,62.87,77,0.99,0.59,1.5799,0.7598,NA,NA
CDISCPILOT01-01-701-1028,CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,2020-04-15,62.68,78.73,62.87,77,-0.19,1.73,-0.2971,2.2403,NA,NA
CDISCPILOT01-01-701-1028,CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,2020-01-15,103.4,94.07,99.95,91.34,3.45,2.73,3.4553,2.9914,Y,Y
CDISCPILOT01-01-701-1028,CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,2020-02-15,99.48,91.36,99.95,91.34,-0.47,0.02,-0.4668,0.0244,NA,NA
CDISCPILOT01-01-701-1028,CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,2020-04-15,98.79,90.28,99.95,91.34,-1.16,-1.06,-1.1571,-1.158,NA,NA
CDISCPILOT01-01-701-1033,CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,2020-01-15,102.42,111.59,100.64,111.17,1.78,0.42,1.7638,0.3735,Y,Y
CDISCPILOT01-01-701-1033,CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,2020-02-15,102.22,112.18,100.64,111.17,1.58,1.01,1.5651,0.9042,NA,NA
CDISCPILOT01-01-701-1033,CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,2020-04-15,99.61,111.94,100.64,111.17,-1.03,0.77,-1.0282,0.6883,NA,NA
CDISCPILOT01-01-701-1033,CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,2020-01-15,67.48,84.69,67.54,84.88,-0.06,-0.19,-0.09,-0.2194,Y,Y
CDISCPILOT01-01-701-1033,CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,2020-02-15,68.25,83.09,67.54,84.88,0.71,-1.79,1.0501,-2.1045,NA,NA
CDISCPILOT01-01-701-1033,CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,2020-04-15,67.27,85.55,67.54,84.88,-0.27,0.67,-0.4009,0.7939,NA,NA
CDISCPILOT01-01-701-1033,CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,2020-01-15,82.46,99.21,80.26,98.42,2.2,0.79,2.7414,0.8034,Y,Y
CDISCPILOT01-01-701-1033,CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,2020-02-15,82.63,100.33,80.26,98.42,2.37,1.91,2.9532,1.9414,NA,NA
CDISCPILOT01-01-701-1033,CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,2020-04-15,84.2,96.72,80.26,98.42,3.94,-1.7,4.9093,-1.7266,NA,NA
CDISCPILOT01-01-701-1034,CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,2020-01-15,119.5,106.3,118.53,104.07,0.97,2.23,0.815,2.1381,Y,Y
CDISCPILOT01-01-701-1034,CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,2020-02-15,118.07,101.53,118.53,104.07,-0.46,-2.54,-0.3914,-2.4452,NA,NA
CDISCPILOT01-01-701-1034,CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,2020-04-15,121.01,101.81,118.53,104.07,2.48,-2.26,2.0889,-2.1761,NA,NA
CDISCPILOT01-01-701-1034,CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,2020-01-15,78.5,62.8,78,63.4,0.5,-0.6,0.6472,-0.9479,Y,Y
CDISCPILOT01-01-701-1034,CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,2020-02-15,78.25,62.85,78,63.4,0.25,-0.55,0.3267,-0.8691,NA,NA
CDISCPILOT01-01-701-1034,CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,2020-04-15,79.06,62.96,78,63.4,1.06,-0.44,1.3652,-0.6956,NA,NA
CDISCPILOT01-01-701-1034,CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,2020-01-15,83.81,80.15,84.69,79.7,-0.88,0.45,-1.0437,0.5683,Y,Y
CDISCPILOT01-01-701-1034,CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,2020-02-15,86.15,77.35,84.69,79.7,1.46,-2.35,1.7192,-2.945,NA,NA
CDISCPILOT01-01-701-1034,CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,2020-04-15,86.57,81.51,84.69,79.7,1.88,1.81,2.2151,2.2748,NA,NA
CDISCPILOT01-01-701-1047,CDISCPILOT01,SYSBP,SYSBP (mmHg),0,Baseline,2020-01-15,103.61,104.89,102.57,101.89,1.04,3,1.0183,2.9485,Y,Y
CDISCPILOT01-01-701-1047,CDISCPILOT01,SYSBP,SYSBP (mmHg),4,Week 4,2020-02-15,102.67,102.24,102.57,101.89,0.1,0.35,0.1019,0.3476,NA,NA
CDISCPILOT01-01-701-1047,CDISCPILOT01,SYSBP,SYSBP (mmHg),12,Week 12,2020-04-15,105.96,100.82,102.57,101.89,3.39,-1.07,3.3096,-1.0462,NA,NA
CDISCPILOT01-01-701-1047,CDISCPILOT01,DIABP,DIABP (mmHg),0,Baseline,2020-01-15,68.49,78.61,68.65,78.47,-0.16,0.14,-0.2369,0.1838,Y,Y
CDISCPILOT01-01-701-1047,CDISCPILOT01,DIABP,DIABP (mmHg),4,Week 4,2020-02-15,70.83,78.42,68.65,78.47,2.18,-0.05,3.1715,-0.0583,NA,NA
CDISCPILOT01-01-701-1047,CDISCPILOT01,DIABP,DIABP (mmHg),12,Week 12,2020-04-15,68.57,80.19,68.65,78.47,-0.08,1.72,-0.1204,2.1975,NA,NA
CDISCPILOT01-01-701-1047,CDISCPILOT01,PULSE,PULSE (beats/min),0,Baseline,2020-01-15,83.39,71.96,83.4,73.67,-0.01,-1.71,-0.0098,-2.3206,Y,Y
CDISCPILOT01-01-701-1047,CDISCPILOT01,PULSE,PULSE (beats/min),4,Week 4,2020-02-15,83.23,77.28,83.4,73.67,-0.17,3.61,-0.2016,4.9008,NA,NA
CDISCPILOT01-01-701-1047,CDISCPILOT01,PULSE,PULSE (beats/min),12,Week 12,2020-04-15,82.8,75.72,83.4,73.67,-0.6,2.05,-0.7172,2.7832,NA,NA

```

**`result.rds`**

```text
[binary artifact: result.rds, 3180 bytes]
```

## Simple Prompt LLM Code

```r
#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(purrr)
})

in_dir  <- "inputs"
out_dir <- "outputs"

dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

read_single_col <- function(fname) {
  fpath <- file.path(in_dir, fname)
  if (!file.exists(fpath)) return(NULL)
  df <- suppressMessages(read_tsv(fpath, show_col_types = FALSE))
  if (ncol(df) == 0) return(NULL)
  as.character(df[[1]])
}

add_annotations <- read_single_col("add_annotations.tsv")
color_vec      <- read_single_col("color.tsv")
conc_col       <- read_single_col("conc_col.tsv")
group_vars     <- read_single_col("group_vars.tsv")
subtitle_vec   <- read_single_col("subtitle.tsv")
symbol_vec     <- read_single_col("symbol.tsv")
time_col       <- read_single_col("time_col.tsv")
title_vec      <- read_single_col("title.tsv")
ylab_vec       <- read_single_col("ylab.tsv")

text_df <- suppressMessages(read_tsv(file.path(in_dir, "text.tsv"),
                                     show_col_types = FALSE))
xlab_df <- suppressMessages(read_tsv(file.path(in_dir, "xlab.tsv"),
                                     show_col_types = FALSE))

fit_line_data <- suppressMessages(
  read_tsv(file.path(in_dir, "fit_line_data.tsv"), show_col_types = FALSE)
)
plot_data <- suppressMessages(
  read_tsv(file.path(in_dir, "plot_data.tsv"), show_col_types = FALSE)
)

# Basic single “halflife-like” summary per PARAM: simple exponential decay fit
# AVAL vs AVISITN for each PARAM using all subjects, then derive pseudo half-life

# Ensure numeric time and concentration columns
if (!"AVISITN" %in% names(plot_data) || !"AVAL" %in% names(plot_data)) {
  stop("Required columns AVAL and AVISITN not found in plot_data.")
}

plot_data <- plot_data %>%
  mutate(
    AVISITN = suppressWarnings(as.numeric(AVISITN)),
    AVAL    = suppressWarnings(as.numeric(AVAL))
  ) %>%
  filter(!is.na(AVISITN), !is.na(AVAL))

# Exponential model: AVAL = A0 * exp(-k * time)
# Linearize: log(AVAL) = log(A0) - k * time
halflife_results <- plot_data %>%
  group_by(PARAMCD, PARAM) %>%
  filter(all(AVAL > 0, na.rm = TRUE)) %>%
  mutate(logAVAL = log(AVAL)) %>%
  do({
    df <- .
    if (n_distinct(df$AVISITN) < 2L) {
      return(tibble(
        A0        = NA_real_,
        k         = NA_real_,
        halflife  = NA_real_,
        n_points  = nrow(df)
      ))
    }
    fit <- try(lm(logAVAL ~ AVISITN, data = df), silent = TRUE)
    if (inherits(fit, "try-error")) {
      tibble(
        A0        = NA_real_,
        k         = NA_real_,
        halflife  = NA_real_,
        n_points  = nrow(df)
      )
    } else {
      coef_fit <- coef(fit)
      intercept <- unname(coef_fit[1])
      slope     <- unname(coef_fit[2])
      k <- -slope
      hl <- if (!is.na(k) && k > 0) log(2) / k else NA_real_
      tibble(
        A0        = exp(intercept),
        k         = k,
        halflife  = hl,
        n_points  = nrow(df)
      )
    }
  }) %>%
  ungroup()

# Attach some annotations from side tables where they make sense
# Title / subtitle / ylab as simple concatenated strings
title_str    <- if (!is.null(title_vec)) paste(title_vec, collapse = " | ") else NA_character_
subtitle_str <- if (!is.null(subtitle_vec)) paste(subtitle_vec, collapse = " | ") else NA_character_
ylab_str     <- if (!is.null(ylab_vec))   paste(ylab_vec, collapse = " | ") else NA_character_

text_str  <- if ("x" %in% names(text_df))  paste(text_df$x,  collapse = " | ") else NA_character_
xlab_str  <- if ("x" %in% names(xlab_df))  paste(xlab_df$x,  collapse = " | ") else NA_character_

meta_cols <- tibble(
  title    = title_str,
  subtitle = subtitle_str,
  ylab     = ylab_str,
  xlab     = xlab_str,
  text     = text_str
)

# Combine meta with each PARAM row
result_tbl <- halflife_results %>%
  mutate(tmp = 1L) %>%
  left_join(meta_cols %>% mutate(tmp = 1L), by = "tmp") %>%
  select(-tmp)

# Write outputs
write_csv(result_tbl, file.path(out_dir, "result.csv"))
saveRDS(result_tbl, file.path(out_dir, "result.rds"))
```

## Simple Prompt Execution Logs

**`stderr.txt`**

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

```

**`stdout.txt`**

```text

```

## Simple Prompt Output Files

**`result.csv`**

```csv
PARAMCD,PARAM,A0,k,halflife,n_points,title,subtitle,ylab,xlab,text
DIABP,DIABP (mmHg),68.10882917853932,1.809732619025531e-5,38301.08234072597,18,AVAL | AVISITN | USUBJID,AVAL | AVISITN | USUBJID,AVAL | AVISITN | USUBJID,SYSBP | DIABP | PULSE | WEIGHT | HEIGHT,SYSBP | DIABP | PULSE | WEIGHT | HEIGHT
PULSE,PULSE (beats/min),84.26825789727872,-5.766665966335077e-4,NA,18,AVAL | AVISITN | USUBJID,AVAL | AVISITN | USUBJID,AVAL | AVISITN | USUBJID,SYSBP | DIABP | PULSE | WEIGHT | HEIGHT,SYSBP | DIABP | PULSE | WEIGHT | HEIGHT
SYSBP,SYSBP (mmHg),109.3639102109427,-6.752468071269525e-4,NA,18,AVAL | AVISITN | USUBJID,AVAL | AVISITN | USUBJID,AVAL | AVISITN | USUBJID,SYSBP | DIABP | PULSE | WEIGHT | HEIGHT,SYSBP | DIABP | PULSE | WEIGHT | HEIGHT

```

**`result.rds`**

```text
[binary artifact: result.rds, 396 bytes]
```

## Evaluation Records

### Current Prompt

```json
{
  "task_id": "pharmaverse/aNCA/get_halflife_plots_single",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "returncode": 0,
  "comparison": {
    "result.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "Shape mismatch: ref=(0, 1) vs llm=(54, 17)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    }
  },
  "normalizations": []
}
```

### Simple Prompt

```json
{
  "task_id": "pharmaverse/aNCA/get_halflife_plots_single",
  "status": "FAIL",
  "pass": false,
  "score": 0.0,
  "message": "Failed at case_embedded",
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "returncode": 0,
  "comparison": {
    "result.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "Shape mismatch: ref=(0, 1) vs llm=(3, 11)"
    },
    "summary.csv": {
      "match": false,
      "tier": "output_bad",
      "reason": "File not generated"
    }
  },
  "normalizations": []
}
```
