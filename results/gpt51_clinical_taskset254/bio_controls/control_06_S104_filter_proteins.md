# Control 06 - `transpror/S104_filter_proteins`

**Task ID in `task.json`:** `rbench/transpror/S104`  
**Package:** `transpror`  **Level:** `L1`  **Selected sample:** `0`

**5-sample strict result:** `FAIL=5`  
**Selected sample status:** `FAIL` - Failed 1/1 test cases

## Why This Is a Control

LLM-error control: prompt/reference contract is coherent, but every sample fails because the model invented an unavailable JSON config.

This is the clearest negative control: the prompt and reference solution both ask for a simple `counts.tsv` missingness filter, but the generated solution looks for `inputs/filter_proteins.json`, which is not part of the task contract.

## Task Prompt From `task.json`

```text
Write R code to filter a protein expression matrix using standard R. Read inputs/counts.tsv, compute missing_pct = rowMeans(is.na(data)), keep rows with missing_pct < 0.3, and write the filtered table to outputs/filtered_proteins.tsv using write.table with sep='	', row.names=TRUE, quote=FALSE.
```

## Expected Artifact Contract

```json
{
  "reference_mode": "dynamic",
  "artifacts": [
    {
      "type": "tsv",
      "path": "outputs/filtered_proteins.tsv"
    }
  ],
  "checks": [
    {
      "type": "file_exists",
      "target": "outputs/filtered_proteins.tsv"
    }
  ]
}
```

## Dynamic Input Contract

`input_factory`: `transpror.filter_proteins_input`

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
  "description": "Schema for S104_filter_proteins (transpror)",
  "parameters": {
    "n_proteins": {
      "min": 50,
      "max": 200
    },
    "n_samples": {
      "min": 20,
      "max": 50
    },
    "filename": "proteins.tsv",
    "needs_clinical": false
  },
  "seed_dependent": true
}
```

## Reference Code

**`solution.R`**

```r
#!/usr/bin/env Rscript
# Filter proteins based on missing value threshold
# Removes proteins with too many missing values across samples

# Read protein expression data from input file
protein_expr <- read.table('inputs/counts.tsv', header = TRUE, sep = '\t', row.names = 1, check.names = FALSE)

# Calculate percentage of missing values for each protein
missing_pct <- rowMeans(is.na(protein_expr))

# Filter: keep only proteins detected in >70% of samples (missing < 30%)
# This ensures sufficient data for downstream analysis
filtered_proteins <- protein_expr[missing_pct < 0.3, ]

# Save filtered protein expression data
write.table(filtered_proteins, 'outputs/filtered_proteins.tsv', sep = "\t", row.names = TRUE, quote = FALSE)

```

## GPT-5.1 Generated Code

**`sample_00/generated_solution.R`**

```r
#!/usr/bin/env Rscript

## Filter protein expression matrix using rules from inputs/filter_proteins.json
## and write outputs/filtered_proteins.tsv

## -------------------------
## Helper / setup
## -------------------------

# Simple null-coalescing helper
`%||%` <- function(a, b) {
  if (!is.null(a)) a else b
}

# Paths
counts_file  <- "inputs/counts.tsv"
config_file  <- "inputs/filter_proteins.json"
output_file  <- "outputs/filtered_proteins.tsv"

# Ensure needed package is available
if (!requireNamespace("jsonlite", quietly = TRUE)) {
  stop("The 'jsonlite' package is required. Install it with: install.packages('jsonlite')")
}

# Ensure output directory exists
out_dir <- dirname(output_file)
if (!dir.exists(out_dir)) {
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
}

## -------------------------
## Read configuration
## -------------------------

config <- jsonlite::fromJSON(config_file)

# Allow either:
# {
#   "filters": { ... }
# }
# or directly:
# {
#   "min_non_missing_per_protein": ...,
#   ...
# }
filters <- config$filters %||% config

## Expected/typical fields (all optional; only applied if present):
##   min_non_missing_per_protein       (integer)
##   max_missing_fraction_per_protein  (0–1)
##   min_mean_abundance                (numeric)
##   expression_threshold              (numeric)
##   min_samples_above_threshold       (integer)

## -------------------------
## Read protein expression matrix
## -------------------------

if (!file.exists(counts_file)) {
  stop("Counts file not found: ", counts_file)
}

# Assumes first column is protein ID, remaining columns are samples
expr <- read.table(
  counts_file,
  header = TRUE,
  sep = "\t",
  stringsAsFactors = FALSE,
  check.names = FALSE,
  na.strings = c("NA", "NaN", "", "null", "NULL")
)

if (ncol(expr) < 2) {
  stop("counts.tsv should have at least one ID column and one expression column.")
}

# Set rownames to the first column (protein IDs)
rownames(expr) <- expr[[1]]
expr <- expr[, -1, drop = FALSE]

# Coerce to numeric where possible (if some columns are character)
expr[] <- lapply(expr, function(col) {
  if (is.factor(col)) col <- as.character(col)
  suppressWarnings(as.numeric(col))
})

# Convert back to matrix for efficient processing
expr_mat <- as.matrix(expr)

## -------------------------
## Apply filtering rules
## -------------------------

filter_proteins <- function(mat, cfg) {
  n_proteins <- nrow(mat)
  if (n_proteins == 0L) return(mat)

  keep <- rep(TRUE, n_proteins)

  # 1) Minimum number of non-missing values per protein
  if (!is.null(cfg$min_non_missing_per_protein)) {
    nonmiss <- rowSums(!is.na(mat))
    keep <- keep & (nonmiss >= cfg$min_non_missing_per_protein)
  }

  # 2) Maximum fraction of missing values per protein
  if (!is.null(cfg$max_missing_fraction_per_protein)) {
    miss_frac <- rowMeans(is.na(mat))
    keep <- keep & (miss_frac <= cfg$max_missing_fraction_per_protein)
  }

  # 3) Minimum mean abundance across samples
  if (!is.null(cfg$min_mean_abundance)) {
    mean_abund <- rowMeans(mat, na.rm = TRUE)
    keep <- keep & (mean_abund >= cfg$min_mean_abundance)
  }

  # 4) Minimum number of samples above a given expression threshold
  if (!is.null(cfg$expression_threshold) &&
      !is.null(cfg$min_samples_above_threshold)) {

    above <- mat > cfg$expression_threshold
    above[is.na(above)] <- FALSE
    n_above <- rowSums(above)
    keep <- keep & (n_above >= cfg$min_samples_above_threshold)
  }

  mat[keep, , drop = FALSE]
}

n_before <- nrow(expr_mat)
filtered_mat <- filter_proteins(expr_mat, filters)
n_after  <- nrow(filtered_mat)

## -------------------------
## Write filtered results
## -------------------------

# Reattach protein IDs as the first column for output
filtered_df <- data.frame(
  protein_id = rownames(filtered_mat),
  filtered_mat,
  check.names = FALSE,
  row.names = NULL
)

write.table(
  filtered_df,
  file = output_file,
  sep = "\t",
  quote = FALSE,
  row.names = FALSE
)

## -------------------------
## Post-filter checks / summaries
## -------------------------

# Confirm file creation
if (!file.exists(output_file)) {
  stop("Filtered output file was not created: ", output_file)
}

cat("Filtered protein expression written to:", output_file, "\n")
cat("Number of proteins before filtering:", n_before, "\n")
cat("Number of proteins after filtering: ", n_after,  "\n")
if (n_before > 0) {
  cat("Retention ratio:", round(n_after / n_before, 3), "\n")
}

# Check for unexpected NAs or anomalies
any_na   <- anyNA(filtered_mat)
rows_all_na <- sum(rowSums(is.na(filtered_mat)) == ncol(filtered_mat))
cols_all_na <- sum(colSums(is.na(filtered_mat)) == nrow(filtered_mat))

cat("Any NA values in filtered data?:", any_na, "\n")
cat("Proteins with all values NA:", rows_all_na, "\n")
cat("Samples with all values NA: ", cols_all_na, "\n")

# Basic numeric summaries (ignoring NAs)
if (n_after > 0) {
  vals <- as.numeric(filtered_mat)
  vals <- vals[!is.na(vals)]
  if (length(vals) > 0) {
    cat("Expression summary (non-NA values):\n")
    print(summary(vals))
  } else {
    cat("Warning: All values in filtered matrix are NA.\n")
  }
} else {
  cat("Warning: No proteins retained after filtering.\n")
}

```

## Selected Sample Evaluation Record

```json
{
  "task_id": "transpror/S104_filter_proteins",
  "sample_idx": 0,
  "status": "FAIL",
  "message": "Failed 1/1 test cases",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-01-18T10:07:45.194891",
  "test_cases": [
    {
      "case": "case_01_seed_1004",
      "status": "NO_OUTPUT",
      "message": "No output files created",
      "stderr": "Error: lexical error: invalid char in json text.\n                                       inputs/filter_proteins.json\n                     (right here) ------^\nExecution halted\n",
      "stdout": "",
      "returncode": 1
    }
  ]
}
```

## Case Comparisons and Archived Outputs

No per-case comparison files were found in the archive for this sample.
## Task-Level `all_cases_comparison.json`

```json
[
  {
    "case": "case_01_seed_1004",
    "status": "NO_OUTPUT",
    "message": "No output files created",
    "stderr": "Error: lexical error: invalid char in json text.\n                                       inputs/filter_proteins.json\n                     (right here) ------^\nExecution halted\n",
    "stdout": "",
    "returncode": 1
  }
]
```

