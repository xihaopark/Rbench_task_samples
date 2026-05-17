# Control 05 - `transpror/S109_correlation_proteomics`

**Task ID in `task.json`:** `rbench/transpror/S109`  
**Package:** `transpror`  **Level:** `L1`  **Selected sample:** `3`

**5-sample strict result:** `FAIL=1, PASS=4`  
**Selected sample status:** `FAIL` - Failed 1/5 test cases

## Why This Is a Control

Mixed control: 4/5 samples passed; selected sample shows how extra QC logic can drop one protein and fail exact schema matching.

The selected failure is not a prompt/reference mismatch. The model inserted an extra zero-variance filtering step, which removed one protein and caused a column mismatch in one generated case.

## Task Prompt From `task.json`

```text
Write R code to compute the protein-protein correlation matrix. Read inputs/counts.tsv, compute cor(t(data), method='pearson', use='pairwise.complete.obs'), and write the matrix to outputs/protein_correlation_matrix.tsv using write.table with sep='	', row.names=TRUE, quote=FALSE.
```

## Expected Artifact Contract

```json
{
  "reference_mode": "dynamic",
  "artifacts": [
    {
      "type": "tsv",
      "path": "outputs/protein_correlation_matrix.tsv"
    }
  ],
  "checks": [
    {
      "type": "file_exists",
      "target": "outputs/protein_correlation_matrix.tsv"
    }
  ]
}
```

## Dynamic Input Contract

`input_factory`: `transpror.correlation_proteomics_input`

The selected proteomics tasks use generated expression matrices. The archive for this GPT-5.1 run does not include the concrete `inputs/counts.tsv` files, but the factory contract is stable: it writes `inputs/counts.tsv` and `inputs/expression.tsv` from a biologically shaped expression matrix.

**Factory registration excerpt**

```python
def _register_transpror_factories(self):
        """Register transpror (proteomics) factories"""
        expr_factory = ExpressionMatrixFactory()
        clinical_factory = ClinicalDataFactory()

        # Basic preprocessing tasks (only need counts.tsv)
        self._factories['transpror.prep_limma_input'] = expr_factory
        self._factories['transpror.log_transform_proteomics_input'] = expr_factory
        self._factories['transpror.normalize_proteomics_input'] = expr_factory
        self._factories['transpror.filter_proteins_input'] = expr_factory
        self._factories['transpror.impute_missing_input'] = expr_factory
        # limma_analysis needs clinical data
        expr_clinical_factory = CompositeFactory([expr_factory, clinical_factory])
        self._factories['transpror.limma_analysis_input'] = expr_clinical_factory
        self._factories['transpror.correlation_proteomics_input'] = expr_factory
        self._factories['transpror.PCA_proteomics_input'] = expr_factory
        
        # Tasks requiring clinical data (need both counts.tsv and clinical.tsv)
        expr_clinical_factory = CompositeFactory([expr_factory, clinical_factory])
        self._factories['transpror.feature_selection_input'] = expr_clinical_factory
        self._factories['transpror.classification_model_input'] = expr_clinical_factory
        self._factories['transpror.cross_validation_input'] = expr_clinical_factory
        self._factories['transpror.ROC_analysis_input'] = expr_clinical_factory
        self._factories['transpror.biomarker_discovery_input'] = expr_clinical_factory
        self._factories['transpror.t_test_proteomics_input'] = expr_clinical_factory
        self._factories['transpror.ANOVA_proteomics_input'] = expr_clinical_factory

```

**Expression matrix factory excerpt**

```python
class ExpressionMatrixFactory(InputFactory):
    """Generate biologically-realistic RNA-seq expression matrices

    Features:
    - Negative binomial distribution (over-dispersion)
    - Log-normal expression levels
    - Stable housekeeping genes (CV < 0.3)
    - Realistic dynamic range
    """

    HOUSEKEEPING_GENES = [
        "ACTB", "GAPDH", "HPRT1", "B2M", "YWHAZ",
        "TBP", "RPLP0", "RPL13A", "PGK1", "PPIA"
    ]

    def generate(
        self,
        work_dir: Path,
        schema_path: Optional[Path] = None,
        seed: Optional[int] = None,
        log_file: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Generate RNA-seq expression matrix"""

        rng = np.random.default_rng(seed)
        schema = self.load_schema(schema_path)
        params = schema.get("parameters", {})

        # Parameters
        n_genes = rng.integers(
            params.get("n_genes", {}).get("min", 100),
            params.get("n_genes", {}).get("max", 500) + 1
        )
        n_samples = rng.integers(
            params.get("n_samples", {}).get("min", 20),
            params.get("n_samples", {}).get("max", 100) + 1
        )

        # Import vocabulary
        import sys
        vocab_path = Path(__file__).parent.parent.parent / "data" / "rbench_data"
        sys.path.insert(0, str(vocab_path))
        from common_vocab import get_random_genes, get_random_samples

        gene_names = get_random_genes(n_genes, rng, include_housekeeping=True)
        sample_names = get_random_samples(n_samples, rng, sample_type="01")

        # Generate log-normal expression levels
        mu_values = self._generate_lognormal_expression(n_genes, rng)

        # Generate negative binomial counts
        counts = np.zeros((n_genes, n_samples), dtype=int)
        for i in range(n_genes):
            dispersion = rng.uniform(0.1, 5)
            size = dispersion
            prob = size / (size + mu_values[i])
            counts[i, :] = rng.negative_binomial(size, prob, n_samples)

        # Enforce housekeeping gene stability
        counts = self._enforce_housekeeping_stability(counts, gene_names, n_samples, rng)

        # Create DataFrame
        expr_df = pd.DataFrame(counts, index=gene_names, columns=sample_names)

        # Save
        inputs_dir = work_dir / "inputs"
        inputs_dir.mkdir(parents=True, exist_ok=True)
        expr_path = inputs_dir / "counts.tsv"
        expr_df.to_csv(expr_path, sep="\t")
        # Also provide an expression.tsv alias for packages expecting that name
        expr_alias_path = inputs_dir / "expression.tsv"
        expr_df.to_csv(expr_alias_path, sep="\t")

        generated_files = [
            {"name": "counts.tsv", "path": expr_path},
            {"name": "expression.tsv", "path": expr_alias_path},
        ]
        self._log_generated_files(generated_files, log_file=log_file)
        return generated_files

    def _generate_lognormal_expression(self, n_genes: int, rng) -> np.ndarray:
        """Generate log-normal distributed expression levels"""

        # Low expression (80%)
        n_low = int(n_genes * 0.8)
        expr_low = rng.lognormal(mean=3, sigma=1.5, size=n_low)

        # Medium expression (15%)
        n_medium = int(n_genes * 0.15)
        expr_medium = rng.lognormal(mean=6, sigma=1, size=n_medium)

        # High expression (5%)
        n_high = n_genes - n_low - n_medium
        expr_high = rng.lognormal(mean=9, sigma=0.5, size=n_high)

        expr = np.concatenate([expr_low, expr_medium, expr_high])
        rng.shuffle(expr)

        return expr

    def _enforce_housekeeping_stability(
        self,
        counts: np.ndarray,
        gene_names: List[str],
        n_samples: int,
        rng
    ) -> np.ndarray:
        """Ensure housekeeping genes are stable and highly expressed"""

        for hk_gene in self.HOUSEKEEPING_GENES:
            if hk_gene in gene_names:
                idx = gene_names.index(hk_gene)

                mean_expr = rng.uniform(5000, 15000)
                cv = 0.15
                std_expr = mean_expr * cv

                counts[idx, :] = rng.normal(mean_expr, std_expr, n_samples)
                counts[idx, :] = np.maximum(counts[idx, :], 0).astype(int)

        return counts

    def validate(self, files: List[Dict[str, Any]]) -> bool:
        """Validate expression matrix with biological QC"""

        expr_path = next((f["path"] for f in files if f["name"] == "counts.tsv"), None)
        if expr_path is None:
            raise ValueError("counts.tsv not found")

        expr_df = pd.read_csv(expr_path, sep="\t", index_col=0)

        if expr_df.shape[0] == 0 or expr_df.shape[1] == 0:
            raise ValueError("Empty expression matrix")

        # Check all values are numeric
        if not expr_df.applymap(lambda x: isinstance(x, (int, float, np.number))).all().all():
            raise ValueError("Non-numeric values in expression matrix")

        # Biological QC
        qc = BiologicalQC()
        qc.add_check(self._validate_overdispersion, expr_df, level="error")
        qc.add_check(self._validate_lognormal, expr_df, level="warning")
        qc.add_check(self._validate_housekeeping, expr_df, level="warning")

        self.qc_report = qc.report()

        if self.qc_report["status"] == "FAIL":
            raise ValueError(f"Biological QC failed: {self.qc_report['errors']}")

        return True

    @staticmethod
    def _validate_overdispersion(expr_df: pd.DataFrame):
        """Validate over-dispersion (Var > Mean)"""
        gene_means = expr_df.mean(axis=1)
        gene_vars = expr_df.var(axis=1)

        # Avoid division by zero
        valid_genes = gene_means > 0
        dispersion_ratio = gene_vars[valid_genes] / gene_means[valid_genes]

        median_ratio = np.median(dispersion_ratio)
        assert median_ratio > 1.5, \
            f"Median dispersion ratio={median_ratio:.2f} too low (should >1.5 for RNA-seq)"

    @staticmethod
    def _validate_lognormal(expr_df: pd.Da

... [truncated]
```

## Input Schema

```json
{
  "type": "protein_expression",
  "description": "Schema for S109_correlation_proteomics (transpror)",
  "parameters": {
    "n_proteins": {
      "min": 50,
      "max": 200
    },
    "n_samples": {
      "min": 20,
      "max": 50
    },
    "filename": "protein_expression.tsv",
    "needs_clinical": false
  },
  "seed_dependent": true
}
```

## Reference Code

**`solution.R`**

```r
#!/usr/bin/env Rscript
# Calculate protein-protein correlation matrix
# Identifies co-regulated proteins across samples

# Read protein expression data from input file
protein_expr <- read.table('inputs/counts.tsv', header = TRUE, sep = '\t', row.names = 1, check.names = FALSE)

# Calculate Pearson correlation between all protein pairs
# Transpose so proteins are rows, samples are columns
# use = "pairwise.complete.obs" handles missing values
cor_matrix <- cor(t(protein_expr), method = "pearson", use = "pairwise.complete.obs")

# Save protein-protein correlation matrix
write.table(cor_matrix, 'outputs/protein_correlation_matrix.tsv', sep = "\t", row.names = TRUE, quote = FALSE)

```

## GPT-5.1 Generated Code

**`sample_03/generated_solution.R`**

```r
#!/usr/bin/env Rscript

## Correlation proteomics analysis in base R
## - Input:  inputs/counts.tsv
## - Output: outputs/protein_correlation_matrix.tsv

## -----------------------
## 1. Setup and I/O paths
## -----------------------

input_file  <- "inputs/counts.tsv"
output_dir  <- "outputs"
output_file <- file.path(output_dir, "protein_correlation_matrix.tsv")

if (!file.exists(input_file)) {
  stop("Input file not found: ", input_file)
}

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
}

## -----------------------
## 2. Read expression data
## -----------------------
## Assumes:
##   - First column: protein IDs
##   - Remaining columns: samples
##   - Rows: proteins, columns: samples

expr <- read.table(
  input_file,
  header = TRUE,
  sep = "\t",
  row.names = 1,
  check.names = FALSE,
  comment.char = "",
  quote = ""
)

## Keep only numeric columns (in case of any metadata columns)
is_num_col <- vapply(expr, is.numeric, logical(1))
if (!all(is_num_col)) {
  warning("Non-numeric columns detected; keeping only numeric columns.")
  expr <- expr[, is_num_col, drop = FALSE]
}

if (nrow(expr) < 2 || ncol(expr) < 2) {
  stop("Expression matrix must have at least 2 proteins and 2 samples.")
}

## Optionally remove proteins with zero variance across samples
var_per_protein <- apply(expr, 1, var, na.rm = TRUE)
zero_var <- which(var_per_protein == 0 | is.na(var_per_protein))
if (length(zero_var) > 0) {
  warning("Removing ", length(zero_var),
          " proteins with zero or undefined variance across samples.")
  expr <- expr[-zero_var, , drop = FALSE]
}

## -----------------------------------------
## 3. Compute protein–protein correlation
## -----------------------------------------
## Use Pearson correlation, pairwise complete observations

cor_mat <- cor(
  t(as.matrix(expr)),       # transpose so that proteins are columns
  use   = "pairwise.complete.obs",
  method = "pearson"
)

## -----------------------------------------
## 4. Save correlation matrix
## -----------------------------------------

write.table(
  cor_mat,
  file      = output_file,
  sep       = "\t",
  quote     = FALSE,
  col.names = NA
)

## -----------------------------------------
## 5. Quick checks / sanity diagnostics
## -----------------------------------------

cat("Correlation matrix written to:", output_file, "\n")

## Confirm file creation
if (!file.exists(output_file)) {
  stop("Output file was not created correctly: ", output_file)
} else {
  cat("Confirmed: output file exists.\n")
}

## Extract non-diagonal correlation values
upper_vals <- cor_mat[upper.tri(cor_mat, diag = FALSE)]

## Basic distribution summary
cat("\nSummary of non-diagonal correlation values:\n")
print(summary(upper_vals))

## Range of correlations (excluding NAs)
non_na_vals <- upper_vals[!is.na(upper_vals)]
if (length(non_na_vals) > 0) {
  cat("\nRange of correlations (excluding NAs):\n")
  cat("Min:", min(non_na_vals), " Max:", max(non_na_vals), "\n")

  ## Quick check of extreme correlations
  high_pos <- mean(non_na_vals > 0.9)
  high_neg <- mean(non_na_vals < -0.9)
  cat("Fraction of correlations > 0.9:", round(high_pos, 4), "\n")
  cat("Fraction of correlations < -0.9:", round(high_neg, 4), "\n")
} else {
  warning("All correlation values are NA.")
}

## NA diagnostics
na_total <- sum(is.na(upper_vals))
na_frac  <- mean(is.na(upper_vals))
cat("\nNA diagnostics (non-diagonal entries):\n")
cat("Total NAs:", na_total, "\n")
cat("Fraction NAs:", round(na_frac, 4), "\n")

## Check for rows/columns heavily affected by NAs
na_row_frac <- rowMeans(is.na(cor_mat))
na_col_frac <- colMeans(is.na(cor_mat))  # same as rowMeans, symmetric matrix

high_na_rows <- names(na_row_frac)[na_row_frac > 0.5]
if (length(high_na_rows) > 0) {
  warning("Proteins with >50% NA correlations (possible anomalies):\n",
          paste(head(high_na_rows, 20), collapse = ", "),
          if (length(high_na_rows) > 20) " ... (truncated)" else "")
} else {
  cat("No proteins with >50% NA correlations.\n")
}

cat("\nCorrelation proteomics analysis complete.\n")

```

## Selected Sample Evaluation Record

```json
{
  "task_id": "transpror/S109_correlation_proteomics",
  "sample_idx": 3,
  "status": "FAIL",
  "message": "Failed 1/5 test cases",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-01-18T10:50:48.716567",
  "test_cases": [
    {
      "case": "case_01_seed_1004",
      "status": "PASS",
      "message": "All outputs match reference",
      "comparison": {
        "protein_correlation_matrix.tsv": {
          "match": true,
          "reason": "All columns match within tolerance"
        }
      }
    },
    {
      "case": "case_01_seed_1002",
      "status": "PASS",
      "message": "All outputs match reference",
      "comparison": {
        "protein_correlation_matrix.tsv": {
          "match": true,
          "reason": "All columns match within tolerance"
        }
      }
    },
    {
      "case": "case_01_seed_1001",
      "status": "PASS",
      "message": "All outputs match reference",
      "comparison": {
        "protein_correlation_matrix.tsv": {
          "match": true,
          "reason": "All columns match within tolerance"
        }
      }
    },
    {
      "case": "case_01_seed_1003",
      "status": "PASS",
      "message": "All outputs match reference",
      "comparison": {
        "protein_correlation_matrix.tsv": {
          "match": true,
          "reason": "All columns match within tolerance"
        }
      }
    },
    {
      "case": "case_01_seed_1000",
      "status": "FAIL",
      "message": "Outputs do not match reference",
      "comparison": {
        "protein_correlation_matrix.tsv": {
          "match": false,
          "reason": "Column mismatch. Expected: ['JAK2', 'PTPN11', 'KEAP1', 'PDX1', 'MTOR', 'U2AF1', 'PRKAR1A', 'BRAF', 'MDM2', 'DEPTOR', 'FADD', 'FLT3', 'FOXP2', 'POLD1', 'BRIP1', 'ARID2', 'CDK6', 'HNF1A', 'KAT6A', 'TP53', 'AR', 'RBL2', 'GATA2', 'E2F3', 'ESR1', 'SETD2', 'CTNNA1', 'CDKN2B', 'RB1', 'BAX', 'NF2', 'GATA4', 'CTNND1', 'MYB', 'MDM4', 'FANCD2', 'FOXP1', 'SHMT2', 'PDGFRB', 'PPIA', 'AKT2', 'FGFR3', 'TGFBR1', 'EP300', 'ARID1B', 'STAT3', 'CHEK2', 'PALB2', 'CUL3', 'ERBB3', 'PTEN', 'CDH1', 'NCOR1', 'YWHAZ', 'EZH2', 'MTHFD1', 'CDH2', 'NFKB1', 'EGFR', 'ERBB2', 'BRCA1', 'PHGDH', 'MYCN', 'TTF1', 'KMT2A', 'B2M', 'CDK4', 'HNF1B', 'RBL1', 'KIT', 'ACVR1B', 'DICER1', 'PSPH', 'NRAS', 'PMS2', 'TSC2', 'BCL2', 'FAS', 'MITF', 'BMPR1A', 'ATM', 'BRCA2', 'STAT5A', 'NOTCH2', 'PDGFRA', 'NKX2-1', 'RHEB', 'AXIN1', 'NF1', 'FBXW7', 'SOX2', 'RELA', 'MET', 'SDHD', 'BAK1', 'DCC', 'CREBBP', 'RHOA', 'ROS1', 'ARID1A', 'CASP9', 'SMAD4', 'APC', 'RPLP0', 'SDHB', 'JAK1', 'UBC', 'HMBS', 'CCNE1', 'FOS', 'FGFR1', 'SMAD3', 'TUBB', 'MTHFD2', 'NCOR2', 'KMT2D', 'CCND3', 'E2F1', 'SMARCA4', 'MYC', 'ALK', 'KDM6A', 'HPRT1', 'FH', 'ZRSR2', 'BAP1', 'GATA3', 'MLH1', 'ABL1', 'MAX', 'SPOP', 'ACTB', 'IDH1', 'MSH6', 'SDHA', 'KRAS', 'NOTCH1', 'FGFR2', 'MAPK1', 'CDKN2A', 'SF3B1', 'FOXO1', 'RPL13A', 'TFRC', 'GATA6', 'TITF1', 'SMAD2', 'PAX8', 'GUSB', 'TGFBR2', 'FANCF', 'FOXA1', 'RAC1', 'HRAS', 'TET2', 'NFE2L2', 'MAP2K1', 'SRSF2', 'PGK1', 'RUNX1', 'JAK3', 'BTK', 'PBRM1', 'TBP', 'GAPDH', 'MAP2K2', 'WT1', 'AKT1', 'TSC1', 'ASXL1', 'SMARCB1', 'PRKAA1', 'PRKAA2', 'CDC42', 'PSAT1', 'SOX9', 'MUTYH', 'POLE', 'JUN', 'SHMT1', 'STK11'], Got: ['JAK2', 'PTPN11', 'KEAP1', 'PDX1', 'MTOR', 'U2AF1', 'PRKAR1A', 'BRAF', 'MDM2', 'DEPTOR', 'FADD', 'FLT3', 'FOXP2', 'POLD1', 'BRIP1', 'ARID2', 'CDK6', 'HNF1A', 'KAT6A', 'TP53', 'AR', 'RBL2', 'GATA2', 'E2F3', 'ESR1', 'SETD2', 'CTNNA1', 'CDKN2B', 'RB1', 'BAX', 'NF2', 'GATA4', 'CTNND1', 'MYB', 'MDM4', 'FANCD2', 'FOXP1', 'SHMT2', 'PDGFRB', 'PPIA', 'AKT2', 'FGFR3', 'TGFBR1', 'EP300', 'ARID1B', 'STAT3', 'CHEK2', 'PALB2', 'CUL3', 'ERBB3', 'PTEN', 'CDH1', 'NCOR1', 'YWHAZ', 'EZH2', 'MTHFD1', 'CDH2', 'NFKB1', 'EGFR', 'ERBB2', 'BRCA1', 'PHGDH', 'MYCN', 'TTF1', 'KMT2A', 'B2M', 'HNF1B', 'RBL1', 'KIT', 'ACVR1B', 'DICER1', 'PSPH', 'NRAS', 'PMS2', 'TSC2', 'BCL2', 'FAS', 'MITF', 'BMPR1A', 'ATM', 'BRCA2', 'STAT5A', 'NOTCH2', 'PDGFRA', 'NKX2-1', 'RHEB', 'AXIN1', 'NF1', 'FBXW7', 'SOX2', 'RELA', 'MET', 'SDHD', 'BAK1', 'DCC', 'CREBBP', 'RHOA', 'ROS1', 'ARID1A', 'CASP9', 'SMAD4', 'APC', 'RPLP0', 'SDHB', 'JAK1', 'UBC', 'HMBS', 'CCNE1', 'FOS', 'FGFR1', 'SMAD3', 'TUBB', 'MTHFD2', 'NCOR2', 'KMT2D', 'CCND3', 'E2F1', 'SMARCA4', 'MYC', 'ALK', 'KDM6A', 'HPRT1', 'FH', 'ZRSR2', 'BAP1', 'GATA3', 'MLH1', 'ABL1', 'MAX', 'SPOP', 'ACTB', 'IDH1', 'MSH6', 'SDHA', 'KRAS', 'NOTCH1', 'FGFR2', 'MAPK1', 'CDKN2A', 'SF3B1', 'FOXO1', 'RPL13A', 'TFRC', 'GATA6', 'TITF1', 'SMAD2', 'PAX8', 'GUSB', 'TGFBR2', 'FANCF', 'FOXA1', 'RAC1', 'HRAS', 'TET2', 'NFE2L2', 'MAP2K1', 'SRSF2', 'PGK1', 'RUNX1', 'JAK3', 'BTK', 'PBRM1', 'TBP', 'GAPDH', 'MAP2K2', 'WT1', 'AKT1', 'TSC1', 'ASXL1', 'SMARCB1', 'PRKAA1', 'PRKAA2', 'CDC42', 'PSAT1', 'SOX9', 'MUTYH', 'POLE', 'JUN', 'SHMT1', 'STK11']"
        }
      }
    }
  ]
}
```

## Case Comparisons and Archived Outputs

### `case_01` - `PASS`

**comparison.json**

```json
{
  "protein_correlation_matrix.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
Correlation matrix written to: outputs/protein_correlation_matrix.tsv 
Confirmed: output file exists.

Summary of non-diagonal correlation values:
      Min.    1st Qu.     Median       Mean    3rd Qu.       Max. 
-0.7874385 -0.1657659 -0.0138349 -0.0002239  0.1542255  0.8408660 

Range of correlations (excluding NAs):
Min: -0.7874385  Max: 0.840866 
Fraction of correlations > 0.9: 0 
Fraction of correlations < -0.9: 0 

NA diagnostics (non-diagonal entries):
Total NAs: 0 
Fraction NAs: 0 
No proteins with >50% NA correlations.

Correlation proteomics analysis complete.

```

**Archived LLM output excerpt: `protein_correlation_matrix.tsv`**

```tsv
	MAPK1_0	ABL1_1	MUTYH	APC	KEAP1_4	CDC42_5	SRSF2	SDHD	PRKAA2	AKT1_9	SOX2_10	PDGFRA	SETD2	FBXW7_13	BRAF_14	BAX_15	PALB2_16	NFE2L2_17	FOXO3_18	CTNNB1_19	PSAT1_20	TTF1	FGFR3_22	ACTB_23	MTHFD2_24	MTHFD2_25	GNAS_26	BRIP1_27	BCL2L1	CDKN2A_29	PAX8_30	GATA2_31	CDK6	KEAP1_33	FOXP1_34	KRAS_35	PALB2_36	BCL2_37	PHGDH_38	POLE_39	ESR1_40	SMARCA4_41	STK11_42	PRKAR1A_43	HNF1A_44	IDH2_45	AXIN1_46	TGFBR2_47	MAP2K1	ERBB2	NFKB1	CUL3_51	GATA2_52	B2M_53	RET_54	ASXL1_55	ZRSR2_56	HNF1B	NCOR2_58	TBP_59	SMARCA4_60	MTOR_61	RB1_62	AKT2_63	BTK_64	PHGDH_65	PSPH_66	RET_67	PAX5_68	RBL1_69	IDH1_70	RUNX1	KMT2D_72	RAD51_73	KIT	FANCF_75	BAX_76	GUSB_77	SDHA_78	MET_79	VHL_80	RPLP0_81	GAPDH_82	ARID1A_83	BCL2_84	RHEB_85	FOXL2_86	PDX1_87	WT1_88	GATA6_89	PALB2_90	HPRT1_91	RB1_92	TFRC_93	EP300_94	PTPN11_95	MITF_96	CCND2_97	FOXL2_98	MDM2	MTHFD2_100	BRAF_101	GATA2_102	PAX5_103	ERBB3_104	AKT1_105	PIK3CA_106	SMAD3	FANCF_108	EZH2	ARID1A_110	CDH1	ASXL1_112	MSH2_113	SHMT2	TFRC_115	CCND2_116	DNMT3A_117	ESR1_118	AXIN2_119	U2AF1_120	B2M_121	ARID1A_122	CDK4_123	CDKN2A_124	GATA6_125	TGFBR1_126	CDKN2A_127	MTOR_128	PAX8_129	PSAT1_130	YWHAZ_131	BMPR1A_132	PDX1_133	BRCA2_134	E2F3_135	E2F1	FBXW7_137	GUSB_138	GATA4_139	UBC_140	FLT3	NOTCH2	DNMT3A_143	HNF1A_144	FGFR2_145	TGFBR2_146	GATA4_147	GATA4_148	MTOR_149	ATM_150	ZRSR2_151	SDHA_152	EP300_153	SRC_154	MTHFD1_155	PRKAR1A_156	ASXL1_157	NCOR1_158	ERBB3_159	PSAT1_160	MET_161	TSC2_162	CDH2	CUL3_164	ARID1B	PAX5_166	TBP_167	ACTB_168	FBXW7_169	E2F3_170	MET_171	U2AF1_172	ASXL1_173	PIK3CA_174	E2F3_175	CHEK2_176	FOXP1_177	PTPN11_178	CHEK2_179	HPRT1_180	CDKN2A_181	SPOP_182	NCOR1_183	CREBBP_184	SMAD2_185	TFRC_186	ABL1_187	GUSB_188	MSH2_189	B2M_190	RELA_191	CTNNA1	MAP2K2	BRCA1_194	ATM_195	GATA3	RELA_197	DICER1_198	GUSB_199	SF3B1	STK11_201	FOS_202	BAX_203	GNAS_204	MAX_205	BRCA1_206	NRAS	TBP_208	IDH2_209	TSC1_210	PAX5_211	PMS2_212	SMAD4	SOX2_214	TFRC_215	AKT2_216	STAT3_217	SPOP_218	FANCF_219	ZRSR2_220	MTHFD1_221	ALK_222	GATA6_223	MAX_224	WT1_225	SMARCB1_226	NFE2L2_227	KEAP1_228	RHOA	NOTCH1_230	PHGDH_231	PRKAR1A_232	AXIN1_233	POLE_234	HRAS	HNF1A_236	HMBS	PTEN	PSPH_239	BRCA1_240	KAT6A_241	TITF1	UBC_243	PSAT1_244	FH_245	RBL1_246	GAPDH_247	FBXW7_248	CREBBP_249	CDKN2B	TSC2_251	BRCA2_252	ALK_2

... [truncated, original 2869455 chars]
```

### `case_02` - `PASS`

**comparison.json**

```json
{
  "protein_correlation_matrix.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
Correlation matrix written to: outputs/protein_correlation_matrix.tsv 
Confirmed: output file exists.

Summary of non-diagonal correlation values:
      Min.    1st Qu.     Median       Mean    3rd Qu.       Max. 
-0.6789368 -0.1303282 -0.0118812 -0.0008585  0.1198417  0.7554764 

Range of correlations (excluding NAs):
Min: -0.6789368  Max: 0.7554764 
Fraction of correlations > 0.9: 0 
Fraction of correlations < -0.9: 0 

NA diagnostics (non-diagonal entries):
Total NAs: 0 
Fraction NAs: 0 
No proteins with >50% NA correlations.

Correlation proteomics analysis complete.

```

**Archived LLM output excerpt: `protein_correlation_matrix.tsv`**

```tsv
	SMARCB1	CASP9_1	KIT_2	ARID1B_3	FGFR1_4	DICER1_5	CTNNB1_6	SHMT1	GNAS	U2AF1_9	CASP9_10	JAK1	TUBB_12	WT1_13	E2F3_14	RHOA_15	CDKN2B	BCL2_17	BAK1	IDH1_19	FOXO3_20	DNMT3A_21	TBP	MAX	PMS2	AXIN2	PAX8_26	FH_27	JAK3_28	ASXL1_29	RBL1	YWHAZ_31	TTF1_32	GAPDH_33	AR_34	GUSB_35	ACTB_36	MITF_37	CASP9_38	BTK_39	POLD1_40	CREBBP_41	DNMT3A_42	BMPR1A_43	RHOA_44	GATA4_45	RBL2_46	MET_47	PALB2	PSPH_49	ROS1_50	GATA4_51	MDM2_52	GATA6_53	E2F3_54	FOS_55	ROS1_56	RB1_57	AKT1	ARID2	TUBB_60	IDH1_61	FGFR2	RAD51_63	RB1_64	BCL2_65	NOTCH2_66	BCL2L11_67	RBL2_68	FOS_69	EZH2_70	FADD_71	ACVR1B	ARID1B_73	EGFR_74	NCOR1_75	SMARCA4_76	DNMT3A_77	ROS1_78	EZH2_79	PBRM1_80	SRSF2_81	PBRM1_82	TP53_83	NRAS_84	JAK3_85	JAK3_86	PAX8_87	STK11_88	NCOR1_89	MET_90	GUSB_91	FANCD2_92	FOXL2_93	MITF_94	BAX_95	DICER1_96	PDGFRB_97	MET_98	GUSB_99	ASXL1_100	ACTB_101	TET2_102	SDHD_103	HMBS_104	DNMT3A_105	IDH1_106	MLH1_107	NOTCH2_108	ALK	TGFBR2	MAP3K1	CTNND1_112	FANCF_113	PRKAR1A	PPIA_115	JAK2_116	FOXO1_117	DEPTOR	FLCN_119	ASXL1_120	CDC42	POLE	GATA2_123	E2F3_124	YWHAZ_125	SRC	NOTCH1_127	FOXO3_128	BRCA2	FANCD2_130	FOXO1_131	PDX1_132	MTHFD2_133	AKT2_134	PBRM1_135	KMT2D	NF1	KEAP1_138	FOXL2_139	MSH2_140	E2F3_141	ACTB_142	RAC1_143	RPLP0_144	RUNX1_145	TP53_146	KDM6A	BTK_148	NOTCH1_149	STAT3	TGFBR1	NCOR1_152	SOX2	CTNNB1_154	MAP2K2	FOXL2_156	SMAD2	MET_158	MYB_159	ESR1_160	VHL_161	CDKN2A_162	ESR1_163	YWHAZ_164	RHOA_165	NCOR2_166	SHMT2	KMT2A_168	STK11_169	EGFR_170	PDGFRA	KEAP1_172	CASP8_173	CCND3_174	PPIA_175	IDH1_176	SDHD_177	TSC1_178	CTNNB1_179	JUN_180	TSC1_181	JUN_182	FLCN_183	MTHFD1_184	MLH1_185	RPLP0_186	FOXO3_187	HPRT1_188	NF2_189	KEAP1_190	TSC2	CDH1	CHEK2	DNMT3A_194	RB1_195	CUL3	BRAF_197	MSH2_198	PIK3CA_199	MYC	TUBB_201	CASP9_202	SRSF2_203	BAP1	WT1_205	GAPDH_206	MUTYH	KEAP1_208	CTNND1_209	SETD2	NCOR2_211	JAK3_212	POLD1_213	TET2_214	SMAD3	KMT2A_216	JAK2_217	HNF1A_218	FLCN_219	PHGDH_220	ASXL1_221	JUP	BRAF_223	ERBB2_224	KAT6A_225	BMPR1A_226	MTHFD2_227	ARID1A_228	PTPN11	HRAS	PRKAA1_231	U2AF1_232	AKT2_233	ERBB2_234	PDX1_235	BCL2_236	DNMT3A_237	AR_238	NFE2L2	NOTCH2_240	ATM_241	STK11_242	RET	HNF1A_244	GATA4_245	HPRT1_246	JAK2_247	CASP9_248	ATM_249	ACTB_250	JAK2_251	MTHFD1_252	FLCN_253	HMBS_254	NRAS_255	CDK4_256	BRAF_257	NCOR2_258	E2F1_259

... [truncated, original 2206677 chars]
```

### `case_03` - `PASS`

**comparison.json**

```json
{
  "protein_correlation_matrix.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
Correlation matrix written to: outputs/protein_correlation_matrix.tsv 
Confirmed: output file exists.

Summary of non-diagonal correlation values:
      Min.    1st Qu.     Median       Mean    3rd Qu.       Max. 
-0.6129867 -0.1163004 -0.0077329  0.0001693  0.1093629  0.8159573 

Range of correlations (excluding NAs):
Min: -0.6129867  Max: 0.8159573 
Fraction of correlations > 0.9: 0 
Fraction of correlations < -0.9: 0 

NA diagnostics (non-diagonal entries):
Total NAs: 0 
Fraction NAs: 0 
No proteins with >50% NA correlations.

Correlation proteomics analysis complete.

```

**Archived LLM output excerpt: `protein_correlation_matrix.tsv`**

```tsv
	CCND2_0	KMT2A_1	MTOR_2	SDHB	PSPH	BRIP1_5	ACVR1B_6	MTHFD2_7	PDX1_8	BAP1_9	SMAD4_10	WT1_11	FLT3	GATA6_13	ESR1_14	JAK1_15	TSC1_16	ACVR1B_17	CCND1_18	PRKAA1_19	RBL1_20	FOXO3_21	BCL2L1_22	BTK	PDGFRA_24	FH_25	TSC1_26	UBC	GAPDH_28	HMBS_29	PAX5_30	MET_31	FH_32	POLD1_33	MITF_34	RHOA_35	ABL1_36	BAP1_37	ESR1_38	TP53_39	EGFR_40	SMAD2	FAS_42	KAT6A	HNF1B_44	PMS2_45	ARID1B_46	BRCA2	GUSB_48	MSH6_49	GUSB_50	NFKB1_51	TBP	RAD51_53	CASP9_54	JUP_55	FOXA1_56	GAPDH_57	MTHFD1_58	VHL_59	CASP8_60	MSH6_61	KEAP1_62	VHL_63	NOTCH1_64	CDC42	FANCA	MET_67	FH_68	NF2_69	FOXL2_70	KMT2D	NF1_72	RAC1	HRAS_74	CDKN2A_75	PRKAA2_76	SDHD	CASP9_78	BAP1_79	FANCD2_80	MAP3K1_81	CCND3_82	SDHA	CCND1_84	PDX1_85	GUSB_86	MTOR_87	DCC_88	FOS	RHEB_90	CDH1_91	FOXO3_92	SF3B1_93	VHL_94	FOXL2_95	CCND3_96	CDKN2A_97	STAT5B_98	RPL13A_99	BRCA1_100	GATA6_101	BAX_102	PDX1_103	PIK3CA_104	TSC1_105	MTHFD1_106	ARID2_107	EP300_108	ABL1_109	PPIA	HNF1A_111	PTEN_112	CDKN2A_113	KDM6A_114	HRAS_115	ACTB	BAK1_117	CCND1_118	TTF1_119	RELA_120	CASP9_121	MTHFD2_122	CTNNB1_123	CUL3_124	AR_125	NF2_126	MET_127	RBL2_128	CHEK2_129	ARID1A_130	KDM6A_131	SMARCB1	PTPN11_133	NKX2-1_134	ARID1B_135	CDKN2A_136	RBL1_137	SHMT2_138	RUNX1_139	E2F3_140	SOX2_141	RHEB_142	CREBBP_143	PBRM1_144	MLH1_145	MITF_146	CTNNA1_147	MUTYH	MTOR_149	CTNNB1_150	SRC_151	MSH6_152	KEAP1_153	RET_154	ARID1B_155	IDH1_156	JUN_157	TFRC	FGFR3_159	HNF1B_160	NFKB1_161	E2F3_162	JAK2_163	JAK3_164	FADD_165	TTF1_166	BAX_167	SF3B1_168	KRAS_169	SRSF2_170	IDH1_171	CASP9_172	FGFR1_173	CDKN2B	FBXW7_175	TTF1_176	CCND2_177	GATA2_178	GATA6_179	CCND2_180	GATA3_181	YWHAZ	FOXL2_183	PRKAA2_184	PRKAA2_185	AKT1_186	CTNND1_187	CCND3_188	TP53_189	RPL13A_190	TGFBR2	FGFR1_192	FLCN_193	HNF1A_194	PSAT1_195	PRKAA1_196	BAX_197	ZRSR2_198	PBRM1_199	CDKN2A_200	RHOA_201	SMAD3_202	STK11	NFKB1_204	MTHFD1_205	CTNNA1_206	BCL2L11_207	MDM2	CDK4_209	RBL2_210	CASP9_211	CHEK2_212	ZRSR2_213	PAX5_214	CTNND1_215	ERBB2_216	STAT5A	SMAD3_218	TET2	ABL1_220	RPLP0_221	MITF_222	CCND3_223	PALB2	FOXP2_225	RPL13A_226	MTHFD2_227	E2F1_228	KEAP1_229	EP300_230	FADD_231	FLCN_232	MET_233	TUBB_234	PMS2_235	MAPK1_236	ARID1B_237	CCND2_238	BCL2L1_239	JAK2_240	RET_241	MAPK1_242	EP300_243	ROS1	AKT1_245	NFKB1_246	PGK1_247	STAT5B_248	BRCA1_249	MET_250

... [truncated, original 4036073 chars]
```

### `case_04` - `PASS`

**comparison.json**

```json
{
  "protein_correlation_matrix.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
Correlation matrix written to: outputs/protein_correlation_matrix.tsv 
Confirmed: output file exists.

Summary of non-diagonal correlation values:
     Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
-0.674449 -0.147082 -0.014190 -0.001052  0.131634  0.786834 

Range of correlations (excluding NAs):
Min: -0.6744489  Max: 0.7868337 
Fraction of correlations > 0.9: 0 
Fraction of correlations < -0.9: 0 

NA diagnostics (non-diagonal entries):
Total NAs: 0 
Fraction NAs: 0 
No proteins with >50% NA correlations.

Correlation proteomics analysis complete.

```

**Archived LLM output excerpt: `protein_correlation_matrix.tsv`**

```tsv
	MSH2_0	ZRSR2_1	CREBBP_2	GNAS	WT1_4	ALK_5	FOXL2_6	MAP2K2_7	EP300_8	JAK2_9	FANCF	MAPK1_11	HNF1B_12	TBP_13	SF3B1	RPL13A_15	FGFR2	CCND1_17	KMT2A	TET2	BMPR1A_20	DCC	MDM4_22	CCND1_23	CDKN2A_24	CCND3_25	EGFR_26	BMPR1A_27	ACVR1B_28	RELA	ARID1B_30	MDM4_31	ARID1A_32	RPLP0_33	ASXL1_34	BRIP1_35	TBP_36	AKT1	STK11_38	RPL13A_39	JUP	TGFBR2_41	PDGFRA_42	MLH1	PSAT1_44	KIT_45	KMT2D_46	BCL2L1_47	BAK1	SMARCB1_49	IDH1_50	FADD_51	RAD51_52	NFE2L2_53	TGFBR1_54	PSPH	PDX1_56	KEAP1_57	SMARCB1_58	RUNX1	FOXL2_60	FAS	ERBB2_62	PTPN11	ERBB3_64	STAT3	KAT6A_66	GUSB_67	BMPR1A_68	MYB_69	NOTCH1	ARID1B_71	CCND3_72	SOX9_73	PAX8	CCND1_75	MYCN	IDH2	U2AF1_78	HRAS	FOS	ABL1	PDX1_82	BAX_83	DEPTOR_84	ARID1B_85	FOXL2_86	SMAD2	GATA2	PHGDH_89	RET	FOXP1	PIK3CA	JUN_93	RB1	MAP2K2_95	PTEN_96	TGFBR1_97	RAD51_98	ARID1A_99	BCL2L1_100	ZRSR2_101	CDK6_102	FOXO1	ATM	ALK_105	FOXO3	NRAS_107	SHMT2_108	JUN_109	KEAP1_110	PHGDH_111	KRAS	RAD51_113	NRAS_114	PTEN_115	FGFR3	TFRC_117	ASXL1_118	EZH2	JAK2_120	ALK_121	PPIA	FADD_123	SDHD	PRKAA2	MYB_126	KEAP1_127	NCOR1	MAPK1_129	FOXP2	MSH2_131	SOX2	BRAF	PALB2_134	MYB_135	BMPR1A_136	ACTB	SOX9_138	BAX_139	E2F3	ERBB2_141	ESR1	KDM6A	ALK_144	PSAT1_145	HNF1B_146	TFRC_147	PMS2	MUTYH	FLT3_150	DNMT3A	BCL2	ERBB3_153	RAC1_154	EP300_155	PDGFRA_156	DEPTOR_157	PALB2_158	NF1	FLT3_160	JUN_161	PALB2_162	ACVR1B_163	MAX	FBXW7_165	TP53	PDX1_167	AXIN1_168	CTNND1_169	SHMT2_170	MDM2	PAX5	CTNND1_173	NFE2L2_174	CDKN2A_175	NF2	RPLP0_177	EGFR_178	PDGFRB	RAC1_180	AXIN1_181	TBP_182	BRIP1_183	PGK1_184	TITF1	PRKAR1A	GUSB_187	MYB_188	CTNNA1	FANCD2	MTOR	KAT6A_192	CREBBP_193	TFRC_194	STAT5B	APC	GATA4	KMT2D_198	PHGDH_199	U2AF1_200	STK11_201	TGFBR2_202	PGK1_203	AXIN1_204	FBXW7_205	SOX9_206	HPRT1	CDK6_208	TSC1	WT1_210	JAK3	KIT_212	ARID1B_213	CDKN2B	ERBB2_215	IDH1_216	FBXW7_217	ALK_218
MSH2_0	1	0.0754625922814277	-0.0654968073554273	0.0564657656396162	-0.0200842621572912	-0.317519192577594	0.00724835922390144	-0.178304237057064	-0.163599309016128	-0.349851165733475	-0.225228668897052	-0.00340341772739887	0.20567637704451	0.321385312290937	-0.0166469159717121	-0.339707613482112	0.337049164105812	-0.294642615181939	-0.00584095074716229	-0.244541722881673	0.435252220228196	0.0348886387778734	-0.00569969096932386	0.206789698446

... [truncated, original 902711 chars]
```

### `case_05` - `FAIL`

**comparison.json**

```json
{
  "protein_correlation_matrix.tsv": {
    "match": false,
    "reason": "Column mismatch. Expected: ['JAK2', 'PTPN11', 'KEAP1', 'PDX1', 'MTOR', 'U2AF1', 'PRKAR1A', 'BRAF', 'MDM2', 'DEPTOR', 'FADD', 'FLT3', 'FOXP2', 'POLD1', 'BRIP1', 'ARID2', 'CDK6', 'HNF1A', 'KAT6A', 'TP53', 'AR', 'RBL2', 'GATA2', 'E2F3', 'ESR1', 'SETD2', 'CTNNA1', 'CDKN2B', 'RB1', 'BAX', 'NF2', 'GATA4', 'CTNND1', 'MYB', 'MDM4', 'FANCD2', 'FOXP1', 'SHMT2', 'PDGFRB', 'PPIA', 'AKT2', 'FGFR3', 'TGFBR1', 'EP300', 'ARID1B', 'STAT3', 'CHEK2', 'PALB2', 'CUL3', 'ERBB3', 'PTEN', 'CDH1', 'NCOR1', 'YWHAZ', 'EZH2', 'MTHFD1', 'CDH2', 'NFKB1', 'EGFR', 'ERBB2', 'BRCA1', 'PHGDH', 'MYCN', 'TTF1', 'KMT2A', 'B2M', 'CDK4', 'HNF1B', 'RBL1', 'KIT', 'ACVR1B', 'DICER1', 'PSPH', 'NRAS', 'PMS2', 'TSC2', 'BCL2', 'FAS', 'MITF', 'BMPR1A', 'ATM', 'BRCA2', 'STAT5A', 'NOTCH2', 'PDGFRA', 'NKX2-1', 'RHEB', 'AXIN1', 'NF1', 'FBXW7', 'SOX2', 'RELA', 'MET', 'SDHD', 'BAK1', 'DCC', 'CREBBP', 'RHOA', 'ROS1', 'ARID1A', 'CASP9', 'SMAD4', 'APC', 'RPLP0', 'SDHB', 'JAK1', 'UBC', 'HMBS', 'CCNE1', 'FOS', 'FGFR1', 'SMAD3', 'TUBB', 'MTHFD2', 'NCOR2', 'KMT2D', 'CCND3', 'E2F1', 'SMARCA4', 'MYC', 'ALK', 'KDM6A', 'HPRT1', 'FH', 'ZRSR2', 'BAP1', 'GATA3', 'MLH1', 'ABL1', 'MAX', 'SPOP', 'ACTB', 'IDH1', 'MSH6', 'SDHA', 'KRAS', 'NOTCH1', 'FGFR2', 'MAPK1', 'CDKN2A', 'SF3B1', 'FOXO1', 'RPL13A', 'TFRC', 'GATA6', 'TITF1', 'SMAD2', 'PAX8', 'GUSB', 'TGFBR2', 'FANCF', 'FOXA1', 'RAC1', 'HRAS', 'TET2', 'NFE2L2', 'MAP2K1', 'SRSF2', 'PGK1', 'RUNX1', 'JAK3', 'BTK', 'PBRM1', 'TBP', 'GAPDH', 'MAP2K2', 'WT1', 'AKT1', 'TSC1', 'ASXL1', 'SMARCB1', 'PRKAA1', 'PRKAA2', 'CDC42', 'PSAT1', 'SOX9', 'MUTYH', 'POLE', 'JUN', 'SHMT1', 'STK11'], Got: ['JAK2', 'PTPN11', 'KEAP1', 'PDX1', 'MTOR', 'U2AF1', 'PRKAR1A', 'BRAF', 'MDM2', 'DEPTOR', 'FADD', 'FLT3', 'FOXP2', 'POLD1', 'BRIP1', 'ARID2', 'CDK6', 'HNF1A', 'KAT6A', 'TP53', 'AR', 'RBL2', 'GATA2', 'E2F3', 'ESR1', 'SETD2', 'CTNNA1', 'CDKN2B', 'RB1', 'BAX', 'NF2', 'GATA4', 'CTNND1', 'MYB', 'MDM4', 'FANCD2', 'FOXP1', 'SHMT2', 'PDGFRB', 'PPIA', 'AKT2', 'FGFR3', 'TGFBR1', 'EP300', 'ARID1B', 'STAT3', 'CHEK2', 'PALB2', 'CUL3', 'ERBB3', 'PTEN', 'CDH1', 'NCOR1', 'YWHAZ', 'EZH2', 'MTHFD1', 'CDH2', 'NFKB1', 'EGFR', 'ERBB2', 'BRCA1', 'PHGDH', 'MYCN', 'TTF1', 'KMT2A', 'B2M', 'HNF1B', 'RBL1', 'KIT', 'ACVR1B', 'DICER1', 'PSPH', 'NRAS', 'PMS2', 'TSC2', 'BCL2', 'FAS', 'MITF', 'BMPR1A', 'ATM', 'BRCA2', 'STAT5A', 'NOTCH2', 'PDGFRA', 'NKX2-1', 'RHEB', 'AXIN1', 'NF1', 'FBXW7', 'SOX2', 'RELA', 'MET', 'SDHD', 'BAK1', 'DCC', 'CREBBP', 'RHOA', 'ROS1', 'ARID1A', 'CASP9', 'SMAD4', 'APC', 'RPLP0', 'SDHB', 'JAK1', 'UBC', 'HMBS', 'CCNE1', 'FOS', 'FGFR1', 'SMAD3', 'TUBB', 'MTHFD2', 'NCOR2', 'KMT2D', 'CCND3', 'E2F1', 'SMARCA4', 'MYC', 'ALK', 'KDM6A', 'HPRT1', 'FH', 'ZRSR2', 'BAP1', 'GATA3', 'MLH1', 'ABL1', 'MAX', 'SPOP', 'ACTB', 'IDH1', 'MSH6', 'SDHA', 'KRAS', 'NOTCH1', 'FGFR2', 'MAPK1', 'CDKN2A', 'SF3B1', 'FOXO1', 'RPL13A', 'TFRC', 'GATA6', 'TITF1', 'SMAD2', 'PAX8', 'GUSB', 'TGFBR2', 'FANCF', 'FOXA1', 'RAC1', 'HRAS', 'TET2', 'NFE2L2', 'MAP2K1', 'SRSF2', 'PGK1', 'RUNX1', 'JAK3', 'BTK', 'PBRM1', 'TBP', 'GAPDH', 'MAP2K2', 'WT1', 'AKT1', 'TSC1', 'ASXL1', 'SMARCB1', 'PRKAA1', 'PRKAA2', 'CDC42', 'PSAT1', 'SOX9', 'MUTYH', 'POLE', 'JUN', 'SHMT1', 'STK11']"
  }
}
```

**stdout excerpt**

```text
Correlation matrix written to: outputs/protein_correlation_matrix.tsv 
Confirmed: output file exists.

Summary of non-diagonal correlation values:
     Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
-0.589295 -0.120971 -0.008694 -0.002135  0.108854  0.662924 

Range of correlations (excluding NAs):
Min: -0.5892945  Max: 0.6629243 
Fraction of correlations > 0.9: 0 
Fraction of correlations < -0.9: 0 

NA diagnostics (non-diagonal entries):
Total NAs: 0 
Fraction NAs: 0 
No proteins with >50% NA correlations.

Correlation proteomics analysis complete.

```

**stderr excerpt**

```text
Warning message:
Removing 1 proteins with zero or undefined variance across samples. 

```

**Archived LLM output excerpt: `protein_correlation_matrix.tsv`**

```tsv
	JAK2	PTPN11	KEAP1	PDX1	MTOR	U2AF1	PRKAR1A	BRAF	MDM2	DEPTOR	FADD	FLT3	FOXP2	POLD1	BRIP1	ARID2	CDK6	HNF1A	KAT6A	TP53	AR	RBL2	GATA2	E2F3	ESR1	SETD2	CTNNA1	CDKN2B	RB1	BAX	NF2	GATA4	CTNND1	MYB	MDM4	FANCD2	FOXP1	SHMT2	PDGFRB	PPIA	AKT2	FGFR3	TGFBR1	EP300	ARID1B	STAT3	CHEK2	PALB2	CUL3	ERBB3	PTEN	CDH1	NCOR1	YWHAZ	EZH2	MTHFD1	CDH2	NFKB1	EGFR	ERBB2	BRCA1	PHGDH	MYCN	TTF1	KMT2A	B2M	HNF1B	RBL1	KIT	ACVR1B	DICER1	PSPH	NRAS	PMS2	TSC2	BCL2	FAS	MITF	BMPR1A	ATM	BRCA2	STAT5A	NOTCH2	PDGFRA	NKX2-1	RHEB	AXIN1	NF1	FBXW7	SOX2	RELA	MET	SDHD	BAK1	DCC	CREBBP	RHOA	ROS1	ARID1A	CASP9	SMAD4	APC	RPLP0	SDHB	JAK1	UBC	HMBS	CCNE1	FOS	FGFR1	SMAD3	TUBB	MTHFD2	NCOR2	KMT2D	CCND3	E2F1	SMARCA4	MYC	ALK	KDM6A	HPRT1	FH	ZRSR2	BAP1	GATA3	MLH1	ABL1	MAX	SPOP	ACTB	IDH1	MSH6	SDHA	KRAS	NOTCH1	FGFR2	MAPK1	CDKN2A	SF3B1	FOXO1	RPL13A	TFRC	GATA6	TITF1	SMAD2	PAX8	GUSB	TGFBR2	FANCF	FOXA1	RAC1	HRAS	TET2	NFE2L2	MAP2K1	SRSF2	PGK1	RUNX1	JAK3	BTK	PBRM1	TBP	GAPDH	MAP2K2	WT1	AKT1	TSC1	ASXL1	SMARCB1	PRKAA1	PRKAA2	CDC42	PSAT1	SOX9	MUTYH	POLE	JUN	SHMT1	STK11
JAK2	1	0.235568656834549	0.0487561807116452	-0.18110942580933	-0.0290472418378634	0.107216309353678	0.200732397115161	-0.0961086279436062	-0.155526419104966	0.300113713427798	-0.326908729818349	0.342662032907175	0.0245751278366908	0.036165316033374	0.0759127386318502	0.114533610593124	0.303453783877265	0.20606473279652	-0.0167878324553917	0.0281756897655916	-0.00987507646098335	0.0396829024219008	-0.0439618103366566	0.158808592771058	0.0776914988152954	0.170244777890747	0.142605730009924	-0.101262064323932	0.181174686660281	-0.380312236563817	-0.246935805928579	0.22949930849818	0.191321259867567	0.087857555836953	0.0383549500775322	-0.021662124604107	-0.186919486069666	-0.0371664062222835	0.286492679740364	0.159681083876173	0.353077174602059	0.269379652864443	0.251859561863468	0.0211161491815337	-0.277534547035857	0.236246929496021	0.0244651072287821	-0.333441180204795	-0.0738503249725849	0.0754152068814746	0.0027089197966448	-0.281413144053932	0.0761764700983743	0.0653109605806788	-0.0966824404877672	-0.257403597623524	-0.00979801640779749	0.0136210207659707	-0.156127213792341	0.189923195592538	-0.253145591856326	-0.270180066402683	-0.172565919396761	-0.017808601325719	0.0375

... [truncated, original 611243 chars]
```

## Task-Level `all_cases_comparison.json`

```json
[
  {
    "case": "case_01_seed_1004",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "protein_correlation_matrix.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  },
  {
    "case": "case_01_seed_1002",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "protein_correlation_matrix.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  },
  {
    "case": "case_01_seed_1001",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "protein_correlation_matrix.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  },
  {
    "case": "case_01_seed_1003",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "protein_correlation_matrix.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  },
  {
    "case": "case_01_seed_1000",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "protein_correlation_matrix.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  }
]
```

