# Control 02 - `transpror/S103_normalize_proteomics`

**Task ID in `task.json`:** `rbench/transpror/S103`  
**Package:** `transpror`  **Level:** `L1`  **Selected sample:** `0`

**5-sample strict result:** `PASS=5`  
**Selected sample status:** `PASS` - Passed all 5/5 test cases

## Why This Is a Control

Clean PASS control with required Bioconductor-style package usage: limma quantile normalization, 5/5 samples passed.

This page is a positive control: the task has a direct input/output contract and GPT-5.1 produced code that matched the dynamic reference across all five samples.

## Task Prompt From `task.json`

```text
Write R code to normalize proteomics expression data using limma. At the beginning, load the required packages: library(limma). Read inputs/counts.tsv, apply limma::normalizeBetweenArrays with method='quantile', and write the normalized matrix to outputs/normalized_proteomics.tsv using write.table with sep='	', row.names=TRUE, quote=FALSE.
```

## Expected Artifact Contract

```json
{
  "reference_mode": "dynamic",
  "artifacts": [
    {
      "type": "tsv",
      "path": "outputs/normalized_proteomics.tsv"
    }
  ],
  "checks": [
    {
      "type": "file_exists",
      "target": "outputs/normalized_proteomics.tsv"
    }
  ]
}
```

## Dynamic Input Contract

`input_factory`: `transpror.normalize_proteomics_input`

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
  "description": "Schema for S103_normalize_proteomics (transpror)",
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
library(limma)

# Read protein expression data
protein_expr <- read.table('inputs/counts.tsv', header = TRUE, sep = '\t', row.names = 1, check.names = FALSE)

# Quantile normalization
norm_protein_expr <- normalizeBetweenArrays(protein_expr, method = "quantile")

# Save normalized data
write.table(norm_protein_expr, 'outputs/normalized_proteomics.tsv', sep = "\t", row.names = TRUE, quote = FALSE)

```

## GPT-5.1 Generated Code

**`sample_00/generated_solution.R`**

```r
## Load required package
library(limma)

## Create output directory if needed
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

## 1. Read protein expression data
# Assumes first column is feature/protein IDs and samples are in columns
counts <- read.table(
  "inputs/counts.tsv",
  header = TRUE,
  sep = "\t",
  row.names = 1,
  check.names = FALSE
)

# Convert to matrix for limma
expr_mat <- as.matrix(counts)

## 2. Quantile normalization
norm_mat <- normalizeBetweenArrays(expr_mat, method = "quantile")

## 3. Write normalized matrix to file
out_file <- "outputs/normalized_proteomics.tsv"
write.table(
  norm_mat,
  file = out_file,
  sep = "\t",
  quote = FALSE,
  col.names = NA
)

## 4. Quick checks after normalization

# 4a. Confirm file creation
if (file.exists(out_file)) {
  message("Normalized file created: ", out_file)
} else {
  stop("ERROR: Normalized file was not created.")
}

# 4b. Basic summary statistics
message("\nDimensions of normalized matrix:")
print(dim(norm_mat))

message("\nSummary of all normalized values:")
print(summary(as.numeric(norm_mat)))

# Per-sample summaries (first few)
message("\nPer-sample mean (first 10):")
print(head(colMeans(norm_mat, na.rm = TRUE), 10))

message("\nPer-sample median (first 10):")
print(head(apply(norm_mat, 2, median, na.rm = TRUE), 10))

# 4c. Check for NAs
na_count <- sum(is.na(norm_mat))
message("\nTotal NA count in normalized matrix: ", na_count)

# 4d. Check range for extreme outliers
rng <- range(norm_mat, na.rm = TRUE, finite = TRUE)
message("\nRange of normalized values (min, max):")
print(rng)

# Optional: simple outlier check using IQR across all values
vals <- as.numeric(norm_mat)
vals <- vals[is.finite(vals)]
q <- quantile(vals, probs = c(0.25, 0.5, 0.75), na.rm = TRUE)
iqr <- q[3] - q[1]
upper_fence <- q[3] + 3 * iqr
lower_fence <- q[1] - 3 * iqr

message("\nApproximate extreme outlier fences (all values pooled):")
message("Lower fence: ", lower_fence, "  Upper fence: ", upper_fence)

extreme_low  <- sum(vals < lower_fence)
extreme_high <- sum(vals > upper_fence)
message("Count of values below lower fence: ", extreme_low)
message("Count of values above upper fence: ", extreme_high)

```

## Selected Sample Evaluation Record

```json
{
  "task_id": "transpror/S103_normalize_proteomics",
  "sample_idx": 0,
  "status": "PASS",
  "message": "Passed all 5/5 test cases",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-01-18T09:56:39.110051",
  "test_cases": [
    {
      "case": "case_01_seed_1004",
      "status": "PASS",
      "message": "All outputs match reference",
      "comparison": {
        "normalized_proteomics.tsv": {
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
        "normalized_proteomics.tsv": {
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
        "normalized_proteomics.tsv": {
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
        "normalized_proteomics.tsv": {
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
        "normalized_proteomics.tsv": {
          "match": true,
          "reason": "All columns match within tolerance"
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
  "normalized_proteomics.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] 391  20
    Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    0.00     6.65    29.60   707.42   144.09 50177.95 
TCGA-FG-7608-01 TCGA-04-5840-01 TCGA-A7-3116-01 TCGA-07-5190-01 TCGA-07-9110-01 
       707.4020        707.4139        707.4304        707.4031        707.4084 
TCGA-02-1841-01 TCGA-A2-8417-01 TCGA-04-2354-01 TCGA-FG-5284-01 TCGA-A7-3974-01 
       707.4141        707.4121        707.3941        707.4225        707.4354 
TCGA-FG-7608-01 TCGA-04-5840-01 TCGA-A7-3116-01 TCGA-07-5190-01 TCGA-07-9110-01 
         29.325          30.000          30.200          30.100          29.800 
TCGA-02-1841-01 TCGA-A2-8417-01 TCGA-04-2354-01 TCGA-FG-5284-01 TCGA-A7-3974-01 
         28.825          29.325          29.600          28.600          29.050 
[1]     0.00 50177.95

```

**stderr excerpt**

```text
Normalized file created: outputs/normalized_proteomics.tsv

Dimensions of normalized matrix:

Summary of all normalized values:

Per-sample mean (first 10):

Per-sample median (first 10):

Total NA count in normalized matrix: 0

Range of normalized values (min, max):

Approximate extreme outlier fences (all values pooled):
Lower fence: -405.68125  Upper fence: 556.425
Count of values below lower fence: 0
Count of values above upper fence: 921

```

**Archived LLM output excerpt: `normalized_proteomics.tsv`**

```tsv
	TCGA-FG-7608-01	TCGA-04-5840-01	TCGA-A7-3116-01	TCGA-07-5190-01	TCGA-07-9110-01	TCGA-02-1841-01	TCGA-A2-8417-01	TCGA-04-2354-01	TCGA-FG-5284-01	TCGA-A7-3974-01	TCGA-B6-4255-01	TCGA-GM-5832-01	TCGA-E2-2473-01	TCGA-FG-7979-01	TCGA-03-9682-01	TCGA-07-1640-01	TCGA-10-2136-01	TCGA-08-3258-01	TCGA-01-6447-01	TCGA-07-6047-01
PRKAR1A_0	50	19.8	45.55	14.5	72.55	43.9	5.9	40.675	47.125	26.1	40.175	22.55	30	35.375	38.7	74.75	43.5	37.9	102.25	25
BAX_1	169.2	340.9	84.675	63.45	202.875	64.45	73.15	200.35	155.95	43.5	142	31.9	9.65	70.6	292.45	210.5	12.1	225.25	225.25	85.25
FGFR1	78.8	86.85	64	120.85	96	12.65	69.55	32.55	14.5	8.975	45.9	10.6	207.95	31.075	12.6	93.225	8.275	46.15	15.3	2
PSAT1	5.25	8.725	0.9	10.2	3.2	4.375	4.725	18.55	3.2	2.9	4.65	6.05	15.8	9.75	6.525	5.125	7.35	10.3	2.25	11.75
FOXL2_4	0	1.85	0	0	0	0	0	0.1	0.9	2.9	0	1.85	0	0	0.0500000000000001	0	0.55	0	0	0
TTF1_5	98.5	20.3	88.4	65.45	33.075	56.725	48.3	101.35	41.8	23.725	95.25	33.15	19.15	50.875	95.25	73.15	84.675	70.6	14.675	44.25
ESR1	20.475	10.8	12.45	7.35	26.4	10.1	19.3	13.4	12.65	15.45	4.65	6.05	12.15	6.4	12.6	15.7	7.35	16.6	10.475	15.975
VHL	136.95	17.35	76.05	45.9	56.45	0	18.7	60.65	96	29.05	232.1	163.35	0	6.4	30.5	0.95	11	10.3	377.45	95.25
GATA4	7.95	5.5	7.75	2.975	4.65	11.075	7.875	6.9	6.65	1.8	2.325	4.675	5.275	6.4	4.45	2.7	6.35	9.15	0.95	5.375
BRCA1_9	19	14.9	15.45	18.85	11.9	28.825	50.875	22.75	11.45	20.475	35.5	33.15	14.9	49.65	44.25	26.4	45.2	31.9	32.775	50.875
NF1_10	24.85	20.3	11.15	11	33.75	11.9	13.4	30.2	38.7	14.55	56.45	27.525	14.2	28.2	12.6	8.2	32.3	9.15	7.3	30
PALB2	12.65	0.9	16.15	37.25	5.45	8.725	16.6	16.525	27.275	12.4	0	14.55	4.4	43.1	4.45	22.25	20.95	32.775	20.8	20.95
SOX2	21.7	9.7	2.45	1.05	6.6	2.45	3.35	13.4	3.2	6.35	6.65	17.75	10.925	0.9	7.7	2.7	3.45	3.8	10.475	11.75
NCOR1_13	1146.6	463.3	809.9	225.25	155.95	361.75	171.1	25.85	554.2	340.9	998	1266.85	19.15	130.55	504.65	537.9	286.75	473.6	95.25	81.3
RELA_14	0.95	7	0.9	5.75	7.8	2.45	3.35	6.9	8.375	2.9	1.05	2.9	0.9	0	0.0500000000000001	0	0	0	0	5.375
CDKN2B_15	504.65	155.95	2018.1	734.9	1146.6	554.2	758.225	165.65	437.55	432.65	2018.1	2928	372.95	1872.1	597.95	299.25	381.95	1062.6	153.95	1364.9
TSC1_16	20.475	310.9	0	9.15	0	0	89.375	0.1

... [truncated, original 48023 chars]
```

### `case_02` - `PASS`

**comparison.json**

```json
{
  "normalized_proteomics.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] 342  31
     Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
    0.000     5.129    23.129   693.263   113.548 32915.419 
TCGA-05-9916-01 TCGA-GM-8196-01 TCGA-05-8021-01 TCGA-E2-1539-01 TCGA-FG-1497-01 
       693.2653        693.2596        693.2818        693.2671        693.2670 
TCGA-D8-5287-01 TCGA-05-9243-01 TCGA-A7-9846-01 TCGA-A1-5924-01 TCGA-08-2656-01 
       693.2716        693.2548        693.2708        693.2633        693.2518 
TCGA-05-9916-01 TCGA-GM-8196-01 TCGA-05-8021-01 TCGA-E2-1539-01 TCGA-FG-1497-01 
       23.12903        22.93548        23.28226        22.93548        23.12903 
TCGA-D8-5287-01 TCGA-05-9243-01 TCGA-A7-9846-01 TCGA-A1-5924-01 TCGA-08-2656-01 
       23.07258        23.22581        23.28226        23.12903        23.12903 
[1]     0.00 32915.42

```

**stderr excerpt**

```text
Normalized file created: outputs/normalized_proteomics.tsv

Dimensions of normalized matrix:

Summary of all normalized values:

Per-sample mean (first 10):

Per-sample median (first 10):

Total NA count in normalized matrix: 0

Range of normalized values (min, max):

Approximate extreme outlier fences (all values pooled):
Lower fence: -320.129032258065  Upper fence: 438.806451612903
Count of values below lower fence: 0
Count of values above upper fence: 1364

```

**Archived LLM output excerpt: `normalized_proteomics.tsv`**

```tsv
	TCGA-05-9916-01	TCGA-GM-8196-01	TCGA-05-8021-01	TCGA-E2-1539-01	TCGA-FG-1497-01	TCGA-D8-5287-01	TCGA-05-9243-01	TCGA-A7-9846-01	TCGA-A1-5924-01	TCGA-08-2656-01	TCGA-EW-2217-01	TCGA-BT-6461-01	TCGA-08-1928-01	TCGA-D8-6045-01	TCGA-D8-8491-01	TCGA-EW-6511-01	TCGA-A7-6511-01	TCGA-04-4500-01	TCGA-D8-5713-01	TCGA-A2-4134-01	TCGA-08-8570-01	TCGA-06-3360-01	TCGA-01-7005-01	TCGA-06-6654-01	TCGA-02-5417-01	TCGA-A7-2533-01	TCGA-B6-4730-01	TCGA-03-6410-01	TCGA-04-4549-01	TCGA-07-2889-01	TCGA-FG-3750-01
HRAS	3.37096774193548	0	4.09677419354839	0.870967741935484	4.01612903225806	3.03225806451613	7.12903225806452	17.8387096774194	11.6129032258065	2.38709677419355	3.2258064516129	2.06451612903226	9.79032258064516	2.16129032258065	1.01612903225806	3.93548387096774	1.25806451612903	2.06451612903226	12.6774193548387	3.04838709677419	1.37096774193548	1.04838709677419	4.90322580645161	2.06451612903226	6.90322580645161	2.90322580645161	6.43548387096774	1.30645161290323	1.64516129032258	2.16129032258065	1.54838709677419
SMAD3_1	12.0161290322581	11.8064516129032	0	8.45161290322581	16.2258064516129	0	7.12903225806452	3.14516129032258	3	10.6451612903226	16.2258064516129	2.06451612903226	13.2741935483871	2.16129032258065	5.25806451612903	2.90322580645161	5.04838709677419	4.09677419354839	10	21.741935483871	6.80645161290323	23.1290322580645	1.37096774193548	0	2.03225806451613	3.67741935483871	0	0	0.82258064516129	2.16129032258065	0
YWHAZ_2	55.5645161290323	28.5483870967742	37.9193548387097	32.3870967741936	24.1290322580645	49.3225806451613	42.0322580645161	21.1290322580645	31.0967741935484	34.2903225806452	38.9032258064516	24.8709677419355	33.6451612903226	30.0967741935484	37.5806451612903	77.8548387096774	47.6935483870968	27.5806451612903	46.9677419354839	27.5806451612903	57.1290322580645	44.1129032258064	36.3225806451613	22.7096774193548	66.4516129032258	44.4516129032258	21.3870967741935	24.7096774193548	21.8225806451613	30.8387096774194	24.5483870967742
NCOR2_3	0	0	0.967741935483871	1.35483870967742	2.09677419354839	1.98387096774194	1.24193548387097	11.4193548387097	7.74193548387097	2.38709677419355	12.0322580645161	1	15.0806451612903	8.24193548387097	6.09677419354839	2.90322580645161

... [truncated, original 167354 chars]
```

### `case_03` - `PASS`

**comparison.json**

```json
{
  "normalized_proteomics.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] 462  38
     Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
    0.000     4.829    23.158   688.094   115.000 44435.158 
TCGA-D8-9652-01 TCGA-B6-8960-01 TCGA-08-6812-01 TCGA-04-3704-01 TCGA-08-3279-01 
       688.1024        688.0996        688.0995        688.0858        688.0915 
TCGA-A1-9099-01 TCGA-A1-1771-01 TCGA-FG-6975-01 TCGA-05-3181-01 TCGA-FG-9096-01 
       688.1155        688.1037        688.1130        688.0894        688.1061 
TCGA-D8-9652-01 TCGA-B6-8960-01 TCGA-08-6812-01 TCGA-04-3704-01 TCGA-08-3279-01 
       23.73684        23.46053        23.00000        23.14474        23.05921 
TCGA-A1-9099-01 TCGA-A1-1771-01 TCGA-FG-6975-01 TCGA-05-3181-01 TCGA-FG-9096-01 
       23.15789        23.73684        23.60526        23.15789        23.31579 
[1]     0.00 44435.16

```

**stderr excerpt**

```text
Normalized file created: outputs/normalized_proteomics.tsv

Dimensions of normalized matrix:

Summary of all normalized values:

Per-sample mean (first 10):

Per-sample median (first 10):

Total NA count in normalized matrix: 0

Range of normalized values (min, max):

Approximate extreme outlier fences (all values pooled):
Lower fence: -325.684210526316  Upper fence: 445.513157894737
Count of values below lower fence: 0
Count of values above upper fence: 2241

```

**Archived LLM output excerpt: `normalized_proteomics.tsv`**

```tsv
	TCGA-D8-9652-01	TCGA-B6-8960-01	TCGA-08-6812-01	TCGA-04-3704-01	TCGA-08-3279-01	TCGA-A1-9099-01	TCGA-A1-1771-01	TCGA-FG-6975-01	TCGA-05-3181-01	TCGA-FG-9096-01	TCGA-10-1234-01	TCGA-A1-4471-01	TCGA-03-2353-01	TCGA-B6-4596-01	TCGA-BT-3218-01	TCGA-06-5889-01	TCGA-04-9112-01	TCGA-EW-4428-01	TCGA-09-5688-01	TCGA-03-9321-01	TCGA-06-2566-01	TCGA-B6-4023-01	TCGA-01-9218-01	TCGA-02-2361-01	TCGA-E2-7473-01	TCGA-GM-1204-01	TCGA-08-4790-01	TCGA-EW-3979-01	TCGA-09-2664-01	TCGA-05-1024-01	TCGA-09-7316-01	TCGA-FG-9827-01	TCGA-A2-7788-01	TCGA-A1-6562-01	TCGA-FG-8266-01	TCGA-10-1305-01	TCGA-E2-5322-01	TCGA-04-8543-01
STAT5A_0	9.39473684210526	2.5921052631579	6.42105263157895	8.31578947368421	0	8.8421052631579	0.921052631578947	6.36842105263158	3.73684210526316	2.88157894736842	2.28947368421053	3.88157894736842	2.93421052631579	9.13157894736842	11.8026315789474	1.98684210526316	5.34210526315789	1	13.9342105263158	2.38157894736842	13.4605263157895	17.3947368421053	7.46052631578947	5.55263157894737	8.8421052631579	10.4473684210526	1.07894736842105	1.94736842105263	3.65789473684211	2.1578947368421	4.71052631578947	3.65789473684211	6.71052631578947	11.3947368421053	5.73684210526316	8.19736842105263	15.2894736842105	2.80263157894737
RPLP0_1	251.184210526316	679.526315789474	75.2105263157895	423.473684210526	312.657894736842	227.131578947368	409.473684210526	153.605263157895	168.657894736842	245.394736842105	187	232.631578947368	494.539473684211	382.763157894737	254.355263157895	210.710526315789	321.552631578947	606.605263157895	199.605263157895	222.289473684211	277.263157894737	321.552631578947	396.605263157895	277.263157894737	450.421052631579	159.921052631579	123.236842105263	423.473684210526	195.184210526316	416.473684210526	115	517.210526315789	312.657894736842	641.407894736842	303.578947368421	360.815789473684	344.131578947368	232.631578947368
ALK_2	12.6052631578947	44.7763157894737	33.1184210526316	24.7105263157895	22.6578947368421	35.3947368421053	38.3289473684211	37.9342105263158	29.7894736842105	24.7105263157895	16.1184210526316	111.144736842105	8.36842105263158	25.6842105263158	23.6052631578947	21.2894736842105	23.3157894736842	31.3947368421053	43.4736842105263	32.644736842

... [truncated, original 269287 chars]
```

### `case_04` - `PASS`

**comparison.json**

```json
{
  "normalized_proteomics.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] 219  25
    Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
    0.00     5.99    27.68   697.29   129.08 30931.48 
TCGA-05-4160-01 TCGA-01-5806-01 TCGA-01-2940-01 TCGA-FG-4406-01 TCGA-06-3367-01 
       697.2970        697.3008        697.2889        697.2754        697.2866 
TCGA-EW-3683-01 TCGA-07-4382-01 TCGA-02-1437-01 TCGA-A2-2703-01 TCGA-09-5189-01 
       697.2853        697.3050        697.2818        697.2968        697.3003 
TCGA-05-4160-01 TCGA-01-5806-01 TCGA-01-2940-01 TCGA-FG-4406-01 TCGA-06-3367-01 
          27.34           27.34           29.00           27.34           27.68 
TCGA-EW-3683-01 TCGA-07-4382-01 TCGA-02-1437-01 TCGA-A2-2703-01 TCGA-09-5189-01 
          27.34           27.00           27.68           28.10           27.68 
[1]     0.00 30931.48

```

**stderr excerpt**

```text
Normalized file created: outputs/normalized_proteomics.tsv

Dimensions of normalized matrix:

Summary of all normalized values:

Per-sample mean (first 10):

Per-sample median (first 10):

Total NA count in normalized matrix: 0

Range of normalized values (min, max):

Approximate extreme outlier fences (all values pooled):
Lower fence: -363.28  Upper fence: 498.35
Count of values below lower fence: 0
Count of values above upper fence: 575

```

**Archived LLM output excerpt: `normalized_proteomics.tsv`**

```tsv
	TCGA-05-4160-01	TCGA-01-5806-01	TCGA-01-2940-01	TCGA-FG-4406-01	TCGA-06-3367-01	TCGA-EW-3683-01	TCGA-07-4382-01	TCGA-02-1437-01	TCGA-A2-2703-01	TCGA-09-5189-01	TCGA-04-3394-01	TCGA-05-3400-01	TCGA-GM-4635-01	TCGA-07-2991-01	TCGA-06-3213-01	TCGA-08-6761-01	TCGA-A2-5223-01	TCGA-03-2736-01	TCGA-09-9138-01	TCGA-EW-7903-01	TCGA-A2-3137-01	TCGA-B6-8152-01	TCGA-EW-9453-01	TCGA-06-4489-01	TCGA-08-2946-01
FLCN_0	77.08	76.34	40.38	23.12	77.08	61.44	28.52	69.24	28.1	47.48	32	72.88	66.52	35.6	44.76	92.46	36.48	102.92	22.56	77.08	46.24	55.12	24.4	78.3	69.24
SHMT2_1	7.14	24.12	8.92	6.08	13.36	3.26	21.54	19.86	23.56	58.32	6.08	10.38	8.92	4.08	19.86	27.68	11.02	21.2	27	28.1	17.84	5.96	19.34	10.74	25.42
CDH2_2	231	0	0.88	56.36	0	130.44	0	1.02	75.6	0	163.04	3.6	0	1.8	0.04	0	0.02	156.2	51.96	965.8	2015.16	261.24	0	1.02	0
FH	52.88	105.92	11.92	36.48	42.76	30.32	14.88	52.88	129.08	58.32	25.72	37.4	55.12	33.28	71.12	39.18	53.8	67.52	89.04	38.68	24.12	44.34	9.2	45.5	15.92
FANCF_4	0	8.24	5.24	0	5.36	3.26	0.84	10.74	10.92	4.76	1.58	0	10.04	4.08	3.26	0.86	9.44	3.66	5.66	0.74	5.66	0	0	9.2	6.68
SMAD3_5	0.84	0.86	4.36	0	19.34	2.18	15.92	2.18	51.96	15.12	9.72	6.44	1.2	22.22	0.04	0	2.3	2.3	9.12	6.26	4.36	2.2	10.04	17.84	8.24
NKX2-1_6	0	48.36	26.24	0	23.34	8.92	25.42	5.36	0	49.88	283.4	131.8	0	41.96	47.48	25.98	3.66	10.38	64.36	149.68	0	105.92	14.12	0	7.4
FBXW7_7	41.08	0.86	29	41.08	13.36	102.92	36.04	179.88	17.7	0	20.08	1.48	0	59.08	0.04	78.3	34.64	1.08	39.18	14.58	298.88	0.88	53.8	121.52	11.02
PGK1_8	6799.24	4850.44	30931.48	30931.48	9372.04	16382.48	16382.48	4064.96	9372.04	4064.96	4850.44	16382.48	8320.4	30931.48	10691.88	13944.68	30931.48	13944.68	13944.68	30931.48	4064.96	30931.48	2517.2	2517.2	8320.4
PRKAA1_9	5.24	0	22.84	21.2	0	0.56	0	5.36	0	4.76	7.4	6.44	8.92	0.2	0.04	0	2.3	0	0	4.36	0	0	34.22	9.2	0
CUL3	11.44	66.52	35.6	96.64	0	149.68	411.76	37.4	6.52	35.12	431.92	93.64	33.28	24.26	67.52	12.08	129.08	61.44	25.12	39.68	75.6	238.68	0	38.04	39.18
MAP3K1_11	98.08	118.2	125.88	62.2	79.52	59.08	86.28	92.46	246.84	96.64	83.84	184.84	179.88	53.8	135.92	125.88	118.2	113.24	215.24	56.96	72.88	197.68	44.76	55.12	79.52
SOX2_12	7.14	40.38	11.92	18.7	13.36	7.88	3.2	43.34	19.64	27.68	14.2	18.7	15.5

... [truncated, original 33314 chars]
```

### `case_05` - `PASS`

**comparison.json**

```json
{
  "normalized_proteomics.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] 181  36
     Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
    0.000     8.208    32.556   987.368   179.917 25129.167 
TCGA-D8-3746-01 TCGA-A2-1091-01 TCGA-FG-6163-01 TCGA-A7-3012-01 TCGA-BT-5121-01 
       987.3646        987.3617        987.3795        987.3780        987.3591 
TCGA-A1-3479-01 TCGA-07-2049-01 TCGA-08-8034-01 TCGA-A1-9167-01 TCGA-FG-9482-01 
       987.3755        987.3757        987.3697        987.3752        987.3689 
TCGA-D8-3746-01 TCGA-A2-1091-01 TCGA-FG-6163-01 TCGA-A7-3012-01 TCGA-BT-5121-01 
       32.55556        33.09722        33.09722        32.22222        33.09722 
TCGA-A1-3479-01 TCGA-07-2049-01 TCGA-08-8034-01 TCGA-A1-9167-01 TCGA-FG-9482-01 
       32.55556        31.88889        32.22222        33.63889        31.88889 
[1]     0.00 25129.17

```

**stderr excerpt**

```text
Normalized file created: outputs/normalized_proteomics.tsv

Dimensions of normalized matrix:

Summary of all normalized values:

Per-sample mean (first 10):

Per-sample median (first 10):

Total NA count in normalized matrix: 0

Range of normalized values (min, max):

Approximate extreme outlier fences (all values pooled):
Lower fence: -506.916666666667  Upper fence: 695.041666666667
Count of values below lower fence: 0
Count of values above upper fence: 756

```

**Archived LLM output excerpt: `normalized_proteomics.tsv`**

```tsv
	TCGA-D8-3746-01	TCGA-A2-1091-01	TCGA-FG-6163-01	TCGA-A7-3012-01	TCGA-BT-5121-01	TCGA-A1-3479-01	TCGA-07-2049-01	TCGA-08-8034-01	TCGA-A1-9167-01	TCGA-FG-9482-01	TCGA-D8-5224-01	TCGA-09-8409-01	TCGA-E2-1726-01	TCGA-BT-5207-01	TCGA-A2-4150-01	TCGA-B6-3480-01	TCGA-04-6729-01	TCGA-02-3923-01	TCGA-02-2846-01	TCGA-05-6588-01	TCGA-GM-1945-01	TCGA-B6-5589-01	TCGA-08-9649-01	TCGA-10-7683-01	TCGA-BT-4761-01	TCGA-04-4649-01	TCGA-D8-3284-01	TCGA-FG-2149-01	TCGA-A1-6009-01	TCGA-04-9826-01	TCGA-A1-1421-01	TCGA-05-8094-01	TCGA-FG-6219-01	TCGA-10-6555-01	TCGA-07-5500-01	TCGA-BT-7097-01
PDGFRA	360.416666666667	381.027777777778	152.083333333333	319.680555555556	170.861111111111	212.583333333333	104.430555555556	202.583333333333	179.916666666667	91.5	120.736111111111	360.416666666667	433.805555555556	402.388888888889	98.6666666666667	693.333333333333	304.013888888889	334.513888888889	146.083333333333	12.4722222222222	295	158.5	158.5	191.458333333333	146.083333333333	76.1944444444444	146.083333333333	152.083333333333	164.694444444444	128.194444444444	243.861111111111	123.194444444444	64.4722222222222	313.027777777778	265.666666666667	158.5
DEPTOR	48.9722222222222	43.4166666666667	57.6111111111111	26.375	64.4722222222222	82.2222222222222	146.083333333333	94.8888888888889	66.8888888888889	62	68.1111111111111	128.194444444444	110.333333333333	72.4722222222222	230.972222222222	91.5	164.694444444444	179.916666666667	68.1111111111111	48.9722222222222	128.194444444444	118.277777777778	64.4722222222222	53.1388888888889	22.8888888888889	34.1666666666667	53.1388888888889	60.1944444444444	146.083333333333	66.8888888888889	51.0277777777778	57.6111111111111	48.9722222222222	123.194444444444	84.9722222222222	82.2222222222222
FAS	22.1666666666667	14.5555555555556	22.1666666666667	13.1388888888889	3.61111111111111	13.3055555555556	13.9444444444444	31.0555555555556	13.4722222222222	23.7916666666667	28.875	51.0277777777778	21.1527777777778	14.7222222222222	15.9027777777778	8.38888888888889	5.52777777777778	13.7083333333333	30.5277777777778	10.6944444444444	15.9027777777778	4.58333333333333	0.861111111111111	19.8611111111111	25.3055555555556	6.08333333333333	22.1666666666667	20.5277777777778	28.875	2

... [truncated, original 105200 chars]
```

## Task-Level `all_cases_comparison.json`

```json
[
  {
    "case": "case_01_seed_1004",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "normalized_proteomics.tsv": {
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
      "normalized_proteomics.tsv": {
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
      "normalized_proteomics.tsv": {
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
      "normalized_proteomics.tsv": {
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
      "normalized_proteomics.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  }
]
```

