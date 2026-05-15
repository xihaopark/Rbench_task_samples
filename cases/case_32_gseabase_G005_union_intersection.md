# Case 32 - `gseabase/G005_union_intersection`
**Track:** `omics_core`  **Package:** `gseabase`  **Function:** `GSEABase::GeneSet`  **Level:** `L2`  **Agent sample:** Biomni `sample_00`  **Evaluation status:** `FAIL`
**Evaluation message:** Failed at case_01_seed_1000
**Sample status counts:** `{"FAIL": 5}`

## Task Prompt

```text
Write R code to compare the two largest gene sets in a GMT file using GSEABase. At the beginning, load the required packages: library(GSEABase). The goal is to understand how much overlap exists between the strongest gene signatures in your collection, since substantial intersection between large sets in inputs/signature.gmt can indicate that nominally distinct pathways or experimental signatures share a common biological core. Use GSEABase functions such as getGmt, GeneSet, and geneIds to load all gene sets, determine their sizes, identify the two largest sets, then compute their gene union, their intersection, and the genes unique to each set, relying only on GSEABase and its documented helpers rather than adding other toolkits. Save the full union of genes to outputs/union_genes.txt, the overlapping genes to outputs/intersection_genes.txt, and a concise comparison table (including set names, sizes, unique gene counts, and intersection size) to outputs/comparison_summary.csv, and finish with a quick quality check to confirm these files exist, that set sizes and overlaps are biologically plausible, and that there are no obvious NA or empty-gene issues.
```

## Input Files

**`inputs/signature.gmt`**

```text
Signature_1	NA	JAK2_142	SMAD3	ATM_179	MAX_74	GATA6	RHOA	BRCA1_42	STAT5A	CDH2_107	FLCN	CTNNB1
Signature_2	NA	BRAF_48	CTNNA1_90	DNMT3A	PRKAA2	FOXO1_26	FH	RB1_103	TSC2_77	JAK3_153	ABL1_78	RAD51_112	GATA6
Signature_3	NA	STAT5A	CCND1	MSH2_194	U2AF1_170	MSH6	FOXO3_104	ESR1	BAP1_23	NF2_163	MAX_64	RB1_60	ABL1_134	SHMT2_188	SETD2_37	MAX_74	FADD_75	NF1_15	RBL2_8	ARID1A_159	MITF	ATM_97	ARID1A_105	IDH1_192	PDX1_65	KEAP1_172	ERBB2_115	BAX	RAC1	E2F3_124	FOS_122	STAT5B	CUL3	MAP2K1	CCND2_156	ASXL1
Signature_4	NA	U2AF1_89	RB1_60	SDHD	TGFBR1_49	KMT2A	CDK6	SDHB	PTPN11	ARID1A_131	BTK	GATA4	CTNNA1_90	CDH2_164	STK11_32	STK11_110	ERBB2_115	IDH2	BCL2L11	KRAS_17	MSH2_136	MAX_64	APC	DICER1	PHGDH	IDH1_192	PTEN	KEAP1_147	CDC42_102	BRAF_57	CCNE1	DNMT3A	CUL3	SRC_39	FOXA1_121	ARID1A_62	SRSF2	ATM_97	SHMT1_137	CCND2_156	MITF	PDX1_65
Signature_5	NA	DCC	RB1_103	FOS_122	FADD_155	PTEN	CDC42_53	IDH1_192	SDHD	SMAD3	CDK6	PSAT1	U2AF1_89	TSC2_168	NF1_15	TGFBR1_1	MTOR_123	CASP9_88	PRKAA2	BRIP1	FOXP1	PAX8	U2AF1_63
Signature_6	NA	AXIN1	MYCN	MSH2_136	JUN	MAX_64	RB1_103	SHMT2_150	ESR1	PAX8	ABL1_134	FANCF_111	MSH2_133	MDM2	KIT	TSC1_166	ARID1A_131	PHGDH	FANCF_138	BRCA1_27	IDH1_181	DICER1	CDH2_164	FOXO1_26	TGFBR1_1	ACVR1B_35	WT1
Signature_7	NA	BRCA1_42	POLE	JAK2_143	HNF1A_38	MAPK1	ARID2	BAP1_23	NOTCH2	ATM_179	U2AF1_89	FANCF_138	FOS_180	RHOA	STK11_6	MTHFD1_87	MSH6	HNF1B_197	MSH2_133	JAK3_174	RBL1	ALK_189	PSPH	ZRSR2	FANCF_111	E2F3_124	MTHFD1_145	U2AF1_170	MAX_74	STK11_32	MAX_41	NF2_24	TSC1_166	FOXO3_104	AXIN1	FADD_155	SHMT2_188	MAP2K1	DCC	RB1_103
Signature_8	NA	FOXP1	HNF1A_38	SHMT2_150	FLCN	MAP3K1	CASP9_79	ARID1A_105	FOXO3_51	PMS2	FOXO3_104	SOX2	CASP8	FOS_180	PTPN11	FANCA	FANCF_138	RHOA	ERBB2_115	MAX_41	CCND2_7
Signature_9	NA	AKT2	CASP8	SHMT1_43	MDM2	TITF1	AKT1	U2AF1_170	CDC42_53	SOX2	BRAF_48	JAK3_174	SRC_39	KIT	ASXL1	SHMT1_58	SMAD4	FOXO3_104	FOXO1_130	FADD_75	RBL2_8	PTEN	BAX
Signature_10	NA	SDHB	STAT5A	TGFBR1_1	SOX2	CCND2_156	STK11_110	BRCA1_27	SOX9	RAD51_84	MAPK1	NF2_163	RBL2_8	FLT3	E2F3_124	NF1_116
Signature_11	NA	PMS2	MSH2_136	BAP1_23	MTHFD1_145	DCC	SHMT1_58	U2AF1_170	ABL1_134	CASP9_88	AR	AKT2	SOX2	PRKAA2	FOXA1_121
Signature_12	NA	KEAP1_172	ACVR1B_91	ARID1A_131	RAD51_84	TITF1	MSH2_133	MDM2	GATA6	PSPH	APC	TSC1_173	MTOR_4	DNMT3A	IDH1_192	CTNNB1	CUL3	HNF1B_33	RHOA	BRAF_57	RBL2_178	CASP9_88	JAK2_143	ATM_97	PTPN11	FOXA1_191	KEAP1_147	FADD_75	SOX9
Signature_13	NA	CASP9_79	KMT2A	FANCA	ACVR1B_135	NOTCH1	BCL2L11	DCC	ACVR1B_35	BAP1_99	MAPK1
Signature_14	NA	BCL2L11	TGFBR1_1	RBL2_178	TP53	CCNE1	ARID1A_62	ALK_146	ATM_69	E2F3_108	PMS2	CTNNA1_90	GATA4	SRSF2	U2AF1_170	BRCA1_113	SOX9	POLD1	FANCA
Signature_15	NA	NF1_116	ATM_69	BAP1_99	BCL2L11	FOXO3_51	SDHD	PRKAA2	CUL3	POLE	CCND2_156	MTHFD1_145	NOTCH2	SRC_39	SHMT1_43	PTEN	CTNNB1	ARID1A_159	ARID1A_131	PSPH	RBL2_178	SDHB	ATM_179	AXIN2	BAP1_23	NF1_15	ACVR1B_135	MSH2_133	NF2_128	KMT2A	FANCA	ERBB2_141	RB1_60	FOXP2	MTOR_4	ACVR1B_94	TSC1_173	FGFR2_59	SMAD3	SMAD4	CTNNA1_56	PSAT1	FOXA1_191
Signature_16	NA	STAT5B	FADD_75	NF1_118	MSH2_136	FGFR2_29	FOXO1_26	PSPH	ERBB2_115	FOXO3_104	SHMT1_160	PDX1_152
```

**`inputs/signatures.tsv`**

```tsv
Signature_1	JAK2_142
Signature_1	SMAD3
Signature_1	ATM_179
Signature_1	MAX_74
Signature_1	GATA6
Signature_1	RHOA
Signature_1	BRCA1_42
Signature_1	STAT5A
Signature_1	CDH2_107
Signature_1	FLCN
Signature_1	CTNNB1
Signature_2	BRAF_48
Signature_2	CTNNA1_90
Signature_2	DNMT3A
Signature_2	PRKAA2
Signature_2	FOXO1_26
Signature_2	FH
Signature_2	RB1_103
Signature_2	TSC2_77
Signature_2	JAK3_153
Signature_2	ABL1_78
Signature_2	RAD51_112
Signature_2	GATA6
Signature_3	STAT5A
Signature_3	CCND1
Signature_3	MSH2_194
Signature_3	U2AF1_170
Signature_3	MSH6
Signature_3	FOXO3_104
Signature_3	ESR1
Signature_3	BAP1_23
Signature_3	NF2_163
Signature_3	MAX_64
Signature_3	RB1_60
Signature_3	ABL1_134
Signature_3	SHMT2_188
Signature_3	SETD2_37
Signature_3	MAX_74
Signature_3	FADD_75
Signature_3	NF1_15
Signature_3	RBL2_8
Signature_3	ARID1A_159
Signature_3	MITF
Signature_3	ATM_97
Signature_3	ARID1A_105
Signature_3	IDH1_192
Signature_3	PDX1_65
Signature_3	KEAP1_172
Signature_3	ERBB2_115
Signature_3	BAX
Signature_3	RAC1
Signature_3	E2F3_124
Signature_3	FOS_122
Signature_3	STAT5B
Signature_3	CUL3
Signature_3	MAP2K1
Signature_3	CCND2_156
Signature_3	ASXL1
Signature_4	U2AF1_89
Signature_4	RB1_60
Signature_4	SDHD
Signature_4	TGFBR1_49
Signature_4	KMT2A
Signature_4	CDK6
Signature_4	SDHB
Signature_4	PTPN11
Signature_4	ARID1A_131
Signature_4	BTK
Signature_4	GATA4
Signature_4	CTNNA1_90
Signature_4	CDH2_164
Signature_4	STK11_32
Signature_4	STK11_110
Signature_4	ERBB2_115
Signature_4	IDH2
Signature_4	BCL2L11
Signature_4	KRAS_17
Signature_4	MSH2_136
Signature_4	MAX_64
Signature_4	APC
Signature_4	DICER1
Signature_4	PHGDH
Signature_4	IDH1_192
Signature_4	PTEN
Signature_4	KEAP1_147
Signature_4	CDC42_102
Signature_4	BRAF_57
Signature_4	CCNE1
Signature_4	DNMT3A
Signature_4	CUL3
Signature_4	SRC_39
Signature_4	FOXA1_121
Signature_4	ARID1A_62
Signature_4	SRSF2
Signature_4	ATM_97
Signature_4	SHMT1_137
Signature_4	CCND2_156
Signature_4	MITF
Signature_4	PDX1_65
Signature_5	DCC
Signature_5	RB1_103
Signature_5	FOS_122
Signature_5	FADD_155
Signature_5	PTEN
Signature_5	CDC42_53
Signature_5	IDH1_192
Signature_5	SDHD
Signature_5	SMAD3
Signature_5	CDK6
Signature_5	PSAT1
Signature_5	U2AF1_89
Signature_5	TSC2_168
Signature_5	NF1_15
Signature_5	TGFBR1_1
Signature_5	MTOR_123
Signature_5	CASP9_88
Signature_5	PRKAA2
Signature_5	BRIP1
Signature_5	FOXP1
Signature_5	PAX8
Signature_5	U2AF1_63
Signature_6	AXIN1
Signature_6	MYCN
Signature_6	MSH2_136
Signature_6	JUN
Signature_6	MAX_64
Signature_6	RB1_103
Signature_6	SHMT2_150
Signature_6	ESR1
Signature_6	PAX8
Signature_6	ABL1_134
Signature_6	FANCF_111
Signature_6	MSH2_133
Signature_6	MDM2
Signature_6	KIT
Signature_6	TSC1_166
Signature_6	ARID1A_131
Signature_6	PHGDH
Signature_6	FANCF_138
Signature_6	BRCA1_27
Signature_6	IDH1_181
Signature_6	DICER1
Signature_6	CDH2_164
Signature_6	FOXO1_26
Signature_6	TGFBR1_1
Signature_6	ACVR1B_35
Signature_6	WT1
Signature_7	BRCA1_42
Signature_7	POLE
Signature_7	JAK2_143
Signature_7	HNF1A_38
Signature_7	MAPK1
Signature_7	ARID2
Signature_7	BAP1_23
Signature_7	NOTCH2
Signature_7	ATM_179
Signature_7	U2AF1_89
Signature_7	FANCF_138
Signature_7	FOS_180
Signature_7	RHOA
Signature_7	STK11_6
Signature_7	MTHFD1_87
Signature_7	MSH6
Signature_7	HNF1B_197
Signature_7	MSH2_133
Signature_7	JAK3_174
Signature_7	RBL1
Signature_7	ALK_189
Signature_7	PSPH
Signature_7	ZRSR2
Signature_7	FANCF_111
Signature_7	E2F3_124
Signature_7	MTHFD1_145
Signature_7	U2AF1_170
Signature_7	MAX_74
Signature_7	STK11_32
Signature_7	MAX_41
Signature_7	NF2_24
Signature_7	TSC1_166
Signature_7	FOXO3_104
Signature_7	AXIN1
Signature_7	FADD_155
Signature_7	SHMT2_188
Signature_7	MAP2K1
Signature_7	DCC
Signature_7	RB1_103
Signature_8	FOXP1
Signature_8	HNF1A_38
Signature_8	SHMT2_150
Signature_8	FLCN
Signature_8	MAP3K1
Signature_8	CASP9_79
Signature_8	ARID1A_105
Signature_8	FOXO3_51
Signature_8	PMS2
Signature_8	FOXO3_104
Signature_8	SOX2
Signature_8	CASP8
Signature_8	FOS_180
Signature_8	PTPN11
Signature_8	FANCA
Signature_8	FANCF_138
Signature_8	RHOA
Signature_8	ERBB2_115
Signature_8	MAX_41
Signature_8	CCND2_7
Signature_9	AKT2
Signature_9	CASP8
Signature_9	SHMT1_43
Signature_9	MDM2
Signature_9	TITF1
Signature_9	AKT1
Signature_9	U2AF1_170
Signature_9	CDC42_53
Signature_9	SOX2
Signature_9	BRAF_48
Signature_9	JAK3_174
Signature_9	SRC_39
Signature_9	KIT
Signature_9	ASXL1
Signature_9	SHMT1_58
Signature_9	SMAD4
Signature_9	FOXO3_104
Signature_9	FOXO1_130
Signature_9	FADD_75
Signature_9	RBL2_8
Signature_9	PTEN
Signature_9	BAX
Signature_10	SDHB
Signature_10	STAT5A
Signature_10	TGFBR1_1
Signature_10	SOX2
Signature_10	CCND2_156
Signature_10	STK11_110
Signature_10	BRCA1_27
Signature_10	SOX9
Signature_10	RAD51_84
Signature_10	MAPK1
Signature_10	NF2_163
Signature_10	RBL2_8
Signature_10	FLT3
Signature_10	E2F3_124
Signature_10	NF1_116
Signature_11	PMS2
Signature_11	MSH2_136
Signature_11	BAP1_23
Signature_11	MTHFD1_145
Signature_11	DCC
Signature_11	SHMT1_58
Signature_11	U2AF1_170
Signature_11	ABL1_134
Signature_11	CASP9_88
Signature_11	AR
Signature_11	AKT2
Signature_11	SOX2
Signature_11	PRKAA2
Signature_11	FOXA1_121
Signature_12	KEAP1_172
Signature_12	ACVR1B_91
Signature_12	ARID1A_131
Signature_12	RAD51_84
Signature_12	TITF1
Signature_12	MSH2_133
Signature_12	MDM2
Signature_12	GATA6
Signature_12	PSPH
Signature_12	APC
Signature_12	TSC1_173
Signature_12	MTOR_4
Signature_12	DNMT3A
Signature_12	IDH1_192
Signature_12	CTNNB1
Signature_12	CUL3
Signature_12	HNF1B_33
Signature_12	RHOA
Signature_12	BRAF_57
Signature_12	RBL2_178
Signature_12	CASP9_88
Signature_12	JAK2_143
Signature_12	ATM_97
Signature_12	PTPN11
Signature_12	FOXA1_191
Signature_12	KEAP1_147
Signature_12	FADD_75
Signature_12	SOX9
Signature_13	CASP9_79
Signature_13	KMT2A
Signature_13	FANCA
Signature_13	ACVR1B_135
Signature_13	NOTCH1
Signature_13	BCL2L11
Signature_13	DCC
Signature_13	ACVR1B_35
Signature_13	BAP1_99
Signature_13	MAPK1
Signature_14	BCL2L11
Signature_14	TGFBR1_1
Signature_14	RBL2_178
Signature_14	TP53
Signature_14	CCNE1
Signature_14	ARID1A_62
Signature_14	ALK_146
Signature_14	ATM_69
Signature_14	E2F3_108
Signature_14	PMS2
Signature_14	CTNNA1_90
Signature_14	GATA4
Signature_14	SRSF2
Signature_14	U2AF1_170
Signature_14	BRCA1_113
Signature_14	SOX9
Signature_14	POLD1
Signature_14	FANCA
Signature_15	NF1_116
Signature_15	ATM_69
Signature_15	BAP1_99
Signature_15	BCL2L11
Signature_15	FOXO3_51
Signature_15	SDHD
Signature_15	PRKAA2
Signature_15	CUL3
Signature_15	POLE
Signature_15	CCND2_156
Signature_15	MTHFD1_145
Signature_15	NOTCH2
Signature_15	SRC_39
Signature_15	SHMT1_43
Signature_15	PTEN
Signature_15	CTNNB1
Signature_15	ARID1A_159
Signature_15	ARID1A_131
Signature_15	PSPH
Signature_15	RBL2_178
Signature_15	SDHB
Signature_15	ATM_179
Signature_15	AXIN2
Signature_15	BAP1_23
Signature_15	NF1_15
Signature_15	ACVR1B_135
Signature_15	MSH2_133
Signature_15	NF2_128
Signature_15	KMT2A
Signature_15	FANCA
Signature_15	ERBB2_141
Signature_15	RB1_60
Signature_15	FOXP2
Signature_15	MTOR_4
Signature_15	ACVR1B_94
Signature_15	TSC1_173
Signature_15	FGFR2_59
Signature_15	SMAD3
Signature_15	SMAD4
Signature_15	CTNNA1_56
Signature_15	PSAT1
Signature_15	FOXA1_191
Signature_16	STAT5B
Signature_16	FADD_75
Signature_16	NF1_118
Signature_16	MSH2_136
Signature_16	FGFR2_29
Signature_16	FOXO1_26
Signature_16	PSPH
Signature_16	ERBB2_115
Signature_16	FOXO3_104
Signature_16	SHMT1_160
Signature_16	PDX1_152
```

## Reference Code

```r
#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(GSEABase))

gmt_path <- file.path('inputs', 'signature.gmt')
if (!file.exists(gmt_path)) stop('signature.gmt input is missing.')

gsc <- getGmt(gmt_path)
sizes <- vapply(gsc, function(gs) length(geneIds(gs)), integer(1))
if (length(sizes) < 2) stop('Need at least two gene sets to compare.')

order_idx <- order(sizes, decreasing = TRUE)
set_a <- gsc[[order_idx[1]]]
set_b <- gsc[[order_idx[2]]]

genes_a <- geneIds(set_a)
genes_b <- geneIds(set_b)

union_genes <- sort(unique(c(genes_a, genes_b)))
intersection_genes <- sort(intersect(genes_a, genes_b))
unique_a <- setdiff(genes_a, genes_b)
unique_b <- setdiff(genes_b, genes_a)

dir.create('outputs', showWarnings = FALSE, recursive = TRUE)
writeLines(union_genes, con = file.path('outputs', 'union_genes.txt'))
writeLines(intersection_genes, con = file.path('outputs', 'intersection_genes.txt'))

summary_df <- data.frame(
  set_name = c(names(gsc)[order_idx[1]], names(gsc)[order_idx[2]]),
  size = c(length(genes_a), length(genes_b)),
  unique_genes = c(length(unique_a), length(unique_b)),
  intersection_size = length(intersection_genes),
  stringsAsFactors = FALSE
)
write.csv(summary_df, file.path('outputs', 'comparison_summary.csv'), row.names = FALSE)
```

## Reference Output

**`outputs/comparison_summary.csv`**

```csv
"set_name","size","unique_genes","intersection_size"
"Signature_15",42,32,10
"Signature_4",41,31,10
```

**`outputs/intersection_genes.txt`**

```text
ARID1A_131
BCL2L11
CCND2_156
CUL3
KMT2A
PTEN
RB1_60
SDHB
SDHD
SRC_39
```

**`outputs/union_genes.txt`**

```text
ACVR1B_135
ACVR1B_94
APC
ARID1A_131
ARID1A_159
ARID1A_62
ATM_179
ATM_69
ATM_97
AXIN2
BAP1_23
BAP1_99
BCL2L11
BRAF_57
BTK
CCND2_156
CCNE1
CDC42_102
CDH2_164
CDK6
CTNNA1_56
CTNNA1_90
CTNNB1
CUL3
DICER1
DNMT3A
ERBB2_115
ERBB2_141
FANCA
FGFR2_59
FOXA1_121
FOXA1_191
FOXO3_51
FOXP2
GATA4
IDH1_192
IDH2
KEAP1_147
KMT2A
KRAS_17
MAX_64
MITF
MSH2_133
MSH2_136
MTHFD1_145
MTOR_4
NF1_116
NF1_15
NF2_128
NOTCH2
PDX1_65
PHGDH
POLE
PRKAA2
PSAT1
PSPH
PTEN
PTPN11
RB1_60
RBL2_178
SDHB
SDHD
SHMT1_137
SHMT1_43
SMAD3
SMAD4
SRC_39
SRSF2
STK11_110
STK11_32
TGFBR1_49
TSC1_173
U2AF1_89
```

## Biomni Code

```r
#!/usr/bin/env Rscript

# Load required package
library(GSEABase)

# Create outputs directory
dir.create('outputs', showWarnings = FALSE)

# Define file paths
gmt_file <- 'inputs/signature.gmt'
union_file <- 'outputs/union_genes.txt'
intersection_file <- 'outputs/intersection_genes.txt'
summary_file <- 'outputs/comparison_summary.csv'

# Check if input file exists
if (!file.exists(gmt_file)) {
  stop(paste("Input GMT file not found:", gmt_file))
}

cat("Loading GMT file:", gmt_file, "\n")

# Load all gene sets from GMT file
tryCatch({
  gene_sets <- getGmt(gmt_file)
  cat("Successfully loaded", length(gene_sets), "gene sets\n")
}, error = function(e) {
  stop(paste("Error loading GMT file:", e$message))
})

# Check if we have at least 2 gene sets
if (length(gene_sets) < 2) {
  stop(paste("Need at least 2 gene sets for comparison, found only", length(gene_sets)))
}

# Get gene set sizes
set_sizes <- sapply(gene_sets, function(gs) length(geneIds(gs)))
set_names <- names(gene_sets)

# Create a data frame with set information
set_info <- data.frame(
  SetName = set_names,
  Size = set_sizes,
  stringsAsFactors = FALSE
)

# Order by size (descending)
set_info <- set_info[order(-set_info$Size), ]

cat("\nTop 5 largest gene sets:\n")
print(head(set_info, 5))

# Identify the two largest sets
largest_set_name <- set_info$SetName[1]
second_largest_set_name <- set_info$SetName[2]

cat("\nTwo largest gene sets:\n")
cat("1.", largest_set_name, "(size:", set_info$Size[1], "genes)\n")
cat("2.", second_largest_set_name, "(size:", set_info$Size[2], "genes)\n")

# Extract the two largest gene sets
largest_set <- gene_sets[[largest_set_name]]
second_largest_set <- gene_sets[[second_largest_set_name]]

# Get gene IDs for each set
genes_largest <- geneIds(largest_set)
genes_second <- geneIds(second_largest_set)

# Remove any NA or empty values (quality check)
genes_largest <- genes_largest[!is.na(genes_largest) & genes_largest != ""]
genes_second <- genes_second[!is.na(genes_second) & genes_second != ""]

cat("\nQuality check - removing NA/empty genes:\n")
cat("  Largest set:", length(genes_largest), "genes after cleaning\n")
cat("  Second largest set:", length(genes_second), "genes after cleaning\n")

# Compute union and intersection
union_genes <- union(genes_largest, genes_second)
intersection_genes <- intersect(genes_largest, genes_second)

# Compute genes unique to each set
unique_to_largest <- setdiff(genes_largest, genes_second)
unique_to_second <- setdiff(genes_second, genes_largest)

# Save union genes
cat("\nSaving union genes to:", union_file, "\n")
writeLines(union_genes, union_file)

# Save intersection genes
cat("Saving intersection genes to:", intersection_file, "\n")
writeLines(intersection_genes, intersection_file)

# Create comparison summary
comparison_summary <- data.frame(
  SetName = c(largest_set_name, second_largest_set_name, "Comparison"),
  Size = c(length(genes_largest), length(genes_second), NA),
  UniqueGenes = c(length(unique_to_largest), length(unique_to_second), NA),
  IntersectionSize = c(NA, NA, length(intersection_genes)),
  UnionSize = c(NA, NA, length(union_genes)),
  JaccardIndex = c(NA, NA, length(intersection_genes) / length(union_genes)),
  stringsAsFactors = FALSE
)

# Save comparison summary
cat("Saving comparison summary to:", summary_file, "\n")
write.csv(comparison_summary, summary_file, row.names = FALSE)

# Print summary
cat("\n=== COMPARISON SUMMARY ===\n")
cat("Set 1:", largest_set_name, "\n")
cat("  Size:", length(genes_largest), "genes\n")
cat("  Unique genes:", length(unique_to_largest), "\n")
cat("\nSet 2:", second_largest_set_name, "\n")
cat("  Size:", length(genes_second), "genes\n")
cat("  Unique genes:", length(unique_to_second), "\n")
cat("\nIntersection:", length(intersection_genes), "genes\n")
cat("Union:", length(union_genes), "genes\n")
cat("Jaccard Index (intersection/union):", 
    round(length(intersection_genes) / length(union_genes), 3), "\n")

# Final quality checks
cat("\n=== FINAL QUALITY CHECKS ===\n")

# Check if output files exist
output_files <- c(union_file, intersection_file, summary_file)
for (file in output_files) {
  if (file.exists(file)) {
    cat("✓ File exists:", file, "\n")
  } else {
    cat("✗ File missing:", file, "\n")
  }
}

# Check for biologically plausible sizes
cat("\nBiological plausibility checks:\n")
if (length(genes_largest) > 0 && length(genes_second) > 0) {
  cat("✓ Both gene sets contain genes\n")
} else {
  cat("✗ One or both gene sets are empty\n")
}

if (length(intersection_genes) <= min(length(genes_largest), length(genes_second))) {
  cat("✓ Intersection size is plausible\n")
} else {
  cat("✗ Intersection size exceeds smallest set - check for errors\n")
}

if (length(union_genes) >= max(length(genes_largest), length(genes_second))) {
  cat("✓ Union size is plausible\n")
} else {
  cat("✗ Union size smaller than largest set - check for errors\n")
}

# Check for NA values
cat("\nNA value checks:\n")
if (any(is.na(union_genes))) {
  cat("✗ NA values found in union genes\n")
} else {
  cat("✓ No NA values in union genes\n")
}

if (any(is.na(intersection_genes))) {
  cat("✗ NA values found in intersection genes\n")
} else {
  cat("✓ No NA values in intersection genes\n")
}

cat("\nAnalysis complete!\n")
```

## Biomni Execution Output

**`stdout.txt`**

```text
Loading GMT file: inputs/signature.gmt 
Successfully loaded 16 gene sets

Top 5 largest gene sets:
        SetName Size
15 Signature_15   42
4   Signature_4   41
7   Signature_7   39
3   Signature_3   35
12 Signature_12   28

Two largest gene sets:
1. Signature_15 (size: 42 genes)
2. Signature_4 (size: 41 genes)

Quality check - removing NA/empty genes:
  Largest set: 42 genes after cleaning
  Second largest set: 41 genes after cleaning

Saving union genes to: outputs/union_genes.txt 
Saving intersection genes to: outputs/intersection_genes.txt 
Saving comparison summary to: outputs/comparison_summary.csv 

=== COMPARISON SUMMARY ===
Set 1: Signature_15 
  Size: 42 genes
  Unique genes: 32 

Set 2: Signature_4 
  Size: 41 genes
  Unique genes: 31 

Intersection: 10 genes
Union: 73 genes
Jaccard Index (intersection/union): 0.137 

=== FINAL QUALITY CHECKS ===
✓ File exists: outputs/union_genes.txt 
✓ File exists: outputs/intersection_genes.txt 
✓ File exists: outputs/comparison_summary.csv 

Biological plausibility checks:
✓ Both gene sets contain genes
✓ Intersection size is plausible
✓ Union size is plausible

NA value checks:
✓ No NA values in union genes
✓ No NA values in intersection genes

Analysis complete!
```

**`stderr.txt`**

```text
Loading required package: BiocGenerics
Loading required package: generics

Attaching package: ‘generics’

The following objects are masked from ‘package:base’:

    as.difftime, as.factor, as.ordered, intersect, is.element, setdiff,
    setequal, union


Attaching package: ‘BiocGenerics’

The following objects are masked from ‘package:stats’:

    IQR, mad, sd, var, xtabs

The following objects are masked from ‘package:base’:

    anyDuplicated, aperm, append, as.data.frame, basename, cbind,
    colnames, dirname, do.call, duplicated, eval, evalq, Filter, Find,
    get, grep, grepl, is.unsorted, lapply, Map, mapply, match, mget,
    order, paste, pmax, pmax.int, pmin, pmin.int, Position, rank,
    rbind, Reduce, rownames, sapply, saveRDS, table, tapply, unique,
    unsplit, which.max, which.min

Loading required package: Biobase
Welcome to Bioconductor

    Vignettes contain introductory material; view with
    'browseVignettes()'. To cite Bioconductor, see
    'citation("Biobase")', and for packages 'citation("pkgname")'.

Loading required package: annotate
Loading required package: AnnotationDbi
Loading required package: stats4
Loading required package: IRanges
Loading required package: S4Vectors

Attaching package: ‘S4Vectors’

The following object is masked from ‘package:utils’:

    findMatches

The following objects are masked from ‘package:base’:

    expand.grid, I, unname

Loading required package: XML
Loading required package: graph

Attaching package: ‘graph’

The following object is masked from ‘package:XML’:

    addNode

```

## Biomni Output Files

**`outputs/comparison_summary.csv`**

```csv
"SetName","Size","UniqueGenes","IntersectionSize","UnionSize","JaccardIndex"
"Signature_15",42,32,NA,NA,NA
"Signature_4",41,31,NA,NA,NA
"Comparison",NA,NA,10,73,0.136986301369863
```

**`outputs/intersection_genes.txt`**

```text
BCL2L11
SDHD
CUL3
CCND2_156
SRC_39
PTEN
ARID1A_131
SDHB
KMT2A
RB1_60
```

**`outputs/union_genes.txt`**

```text
NF1_116
ATM_69
BAP1_99
BCL2L11
FOXO3_51
SDHD
PRKAA2
CUL3
POLE
CCND2_156
MTHFD1_145
NOTCH2
SRC_39
SHMT1_43
PTEN
CTNNB1
ARID1A_159
ARID1A_131
PSPH
RBL2_178
SDHB
ATM_179
AXIN2
BAP1_23
NF1_15
ACVR1B_135
MSH2_133
NF2_128
KMT2A
FANCA
ERBB2_141
RB1_60
FOXP2
MTOR_4
ACVR1B_94
TSC1_173
FGFR2_59
SMAD3
SMAD4
CTNNA1_56
PSAT1
FOXA1_191
U2AF1_89
TGFBR1_49
CDK6
PTPN11
BTK
GATA4
CTNNA1_90
CDH2_164
STK11_32
STK11_110
ERBB2_115
IDH2
KRAS_17
MSH2_136
MAX_64
APC
DICER1
PHGDH
IDH1_192
KEAP1_147
CDC42_102
BRAF_57
CCNE1
DNMT3A
FOXA1_121
ARID1A_62
SRSF2
ATM_97
SHMT1_137
MITF
PDX1_65
```

## Biomni Metadata

```json
{
  "task_id": "gseabase/G005_union_intersection",
  "package": "gseabase",
  "track_id": "omics_core",
  "content_tag_id": "omics",
  "flow_tag_id": "report",
  "scoring_mode_id": "strict",
  "code_sha256": "77ddbca7a7a8e4fbb74b263090057aebb7139e7371eca1f64c2cc80139965d39",
  "agent": "biomni",
  "model": "deepseek/deepseek-v3.2-exp",
  "temperature": 1.0,
  "timestamp": "2026-04-02T16:31:34.438678",
  "raw_response": "",
  "token_usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  },
  "gen_time_seconds": 99.33
}
```

## Evaluation Record

```json
{
  "task_id": "gseabase/G005_union_intersection",
  "sample_idx": 0,
  "agent": "biomni",
  "status": "FAIL",
  "message": "Failed at case_01_seed_1000",
  "timestamp": "2026-02-14T14:40:55.971525",
  "gen_time": 47.29,
  "docker_time": 11.26,
  "test_cases": [
    {
      "case": "case_01_seed_1000",
      "status": "FAIL",
      "comparison": {
        "intersection_genes.txt": {
          "match": false,
          "reason": "Binary mismatch (ref=69B, llm=69B)"
        },
        "union_genes.txt": {
          "match": false,
          "reason": "Binary mismatch (ref=565B, llm=565B)"
        },
        "comparison_summary.csv": {
          "match": false,
          "reason": "Shape mismatch: ref=(2, 4) vs llm=(3, 4)"
        }
      },
      "returncode": 0
    }
  ]
}
```
