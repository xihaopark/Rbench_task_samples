# Sample 36: pharmaverse/aNCA/get_halflife_plots_single

- task_dir: `tasks/releases/rbiobench_stable_v1/tracks/clinical_pilot/tasks/aNCA/get_halflife_plots_single`
- package/function: `aNCA` / `get_halflife_plots_single`
- expected_artifacts: `outputs/result.csv, outputs/result.rds`
- current_status: `FAIL` tier=`output_bad`
- simple_status: `FAIL` tier=`output_bad`

## Reference Prompt
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

## Current Prompt
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

## Simple Prompt
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

## Current Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(0, 1) vs llm=(54, 17) | summary.csv: match=False reason=File not generated"
}
```

## Simple Evaluation
```text
{
  "case": "case_embedded",
  "case_status": "FAIL",
  "tier": "output_bad",
  "message": "",
  "returncode": 0,
  "stderr": "",
  "comparison": "result.csv: match=False reason=Shape mismatch: ref=(0, 1) vs llm=(3, 11) | summary.csv: match=False reason=File not generated"
}
```

## Reference Solution Head
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
text <- read.delim(text_path, check.nam
```

## Current Solution
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

## Simple Solution
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

## Current Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for get halflife plots single. The available input files are `inputs/add_annotations.tsv`, `inputs/color.tsv`, `inputs/conc_col.tsv`, `inputs/fit_line_data.tsv`, `inputs/group_vars.tsv`, `inputs/plot_data.tsv`, `inputs/subtitle.tsv`, `inputs/symbol.tsv`, `inputs/text.tsv`, `inputs/time_col.tsv`, `inputs/title.tsv`, `inputs/xlab.tsv`, `inputs/ylab.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```

## Simple Candidate Prompt File
```text
I am preparing an aNCA clinical pharmacokinetic support task for get halflife plots single. The available input files are `inputs/add_annotations.tsv`, `inputs/color.tsv`, `inputs/conc_col.tsv`, `inputs/fit_line_data.tsv`, `inputs/group_vars.tsv`, `inputs/plot_data.tsv`, `inputs/subtitle.tsv`, `inputs/symbol.tsv`, `inputs/text.tsv`, `inputs/time_col.tsv`, `inputs/title.tsv`, `inputs/xlab.tsv`, `inputs/ylab.tsv`. Create an R script that reads each TSV with header preservation, treats one-row tables as scalar arguments when appropriate, and preserves row alignment across vector or table inputs. Required grading outputs are `outputs/result.csv`, `outputs/result.rds`. This benchmark helper should be implemented as the equivalent data transformation directly, using aNCA-compatible data conventions where useful. Keep the CSV output compact and inspectable; when an RDS artifact is required, write the full result object there as well. Create the outputs directory before writing files.
```