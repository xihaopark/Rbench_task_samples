# Control 04 - `transpror/S101_prep_limma`

**Task ID in `task.json`:** `rbench/transpror/S101`  
**Package:** `transpror`  **Level:** `L1`  **Selected sample:** `1`

**5-sample strict result:** `FAIL=1, PASS=4`  
**Selected sample status:** `FAIL` - Failed 1/5 test cases

## Why This Is a Control

Mixed control: 4/5 samples passed; the selected sample fails only one generated case, useful for seeing small exactness drift.

The selected failure is narrow: most generated cases match, but one case has a row-count mismatch, showing exactness drift rather than a broad benchmark contract defect.

## Task Prompt From `task.json`

```text
Write R code to prepare limma-ready proteomics data using limma. At the beginning, load the required packages: library(limma). Read the protein expression data from inputs/counts.tsv, apply log2(x + 1), normalize with limma::normalizeBetweenArrays, and write the final processed data as a tab-separated file to outputs/limma_prepared.tsv using write.table with sep='	', row.names=TRUE, quote=FALSE.
```

## Expected Artifact Contract

```json
{
  "reference_mode": "dynamic",
  "artifacts": [
    {
      "type": "tsv",
      "path": "outputs/limma_prepared.tsv"
    }
  ],
  "checks": [
    {
      "type": "file_exists",
      "target": "outputs/limma_prepared.tsv"
    }
  ]
}
```

## Dynamic Input Contract

`input_factory`: `transpror.prep_limma_input`

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
  "description": "Schema for S101_prep_limma (transpror)",
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
library(limma)

# Read protein expression data
protein_expr <- read.table('inputs/counts.tsv', header = TRUE, sep = '\t', row.names = 1, check.names = FALSE)

# Prepare data for limma analysis (log transform and normalize)
log_expr <- log2(protein_expr + 1)
norm_expr <- normalizeBetweenArrays(log_expr)

# Save prepared data
write.table(norm_expr, 'outputs/limma_prepared.tsv', sep = "\t", row.names = TRUE, quote = FALSE)

```

## GPT-5.1 Generated Code

**`sample_01/generated_solution.R`**

```r
## Load required package
library(limma)

##---------------------------
## 1. Read raw protein data
##---------------------------
# Adjust working directory as needed before running this script
# setwd("path/to/project")

# Read counts; assumes first column is protein ID
counts <- read.delim(
  "inputs/counts.tsv",
  header = TRUE,
  row.names = 1,
  check.names = FALSE
)

# Keep only numeric columns (in case there are annotation columns)
is_num <- vapply(counts, is.numeric, logical(1))
expr_raw <- as.matrix(counts[, is_num, drop = FALSE])

##---------------------------
## 2. Basic filtering
##---------------------------
# Remove rows that are all NA or all zero
keep <- rowSums(!is.na(expr_raw)) > 0 & rowSums(expr_raw, na.rm = TRUE) > 0
expr_raw <- expr_raw[keep, , drop = FALSE]

##---------------------------
## 3. Log2 transform
##---------------------------
expr_log <- log2(expr_raw + 1)

##---------------------------
## 4. Between-array normalization
##---------------------------
# Quantile normalization across samples
expr_norm <- normalizeBetweenArrays(expr_log, method = "quantile")

##---------------------------
## 5. Write limma-ready data
##---------------------------
if (!dir.exists("outputs")) {
  dir.create("outputs", recursive = TRUE)
}

out_file <- "outputs/limma_prepared.tsv"

write.table(
  expr_norm,
  file      = out_file,
  sep       = "\t",
  quote     = FALSE,
  col.names = NA
)

##---------------------------
## 6. Basic checks / QC
##---------------------------

# Confirm file creation
file.exists(out_file)

# Inspect first few rows and columns
head(expr_norm[, 1:min(6, ncol(expr_norm)), drop = FALSE])

# Summary statistics of all values
summary(as.vector(expr_norm))

# Check for NAs
total_NA  <- sum(is.na(expr_norm))
prop_NA   <- mean(is.na(expr_norm))
cat("Total NAs:", total_NA, "\nProportion NAs:", prop_NA, "\n")

# Simple check for obvious outliers via boxplot of sample distributions
# (visually inspect when running interactively)
boxplot(
  expr_norm,
  outline = TRUE,
  las     = 2,
  main    = "Normalized log2 protein expression",
  ylab    = "log2(intensity + 1)"
)

## expr_norm is now ready to be used as the expression matrix in limma

```

## Selected Sample Evaluation Record

```json
{
  "task_id": "transpror/S101_prep_limma",
  "sample_idx": 1,
  "status": "FAIL",
  "message": "Failed 1/5 test cases",
  "model": "openai/gpt-5.1",
  "timestamp": "2026-01-18T09:36:04.209382",
  "test_cases": [
    {
      "case": "case_01_seed_1004",
      "status": "PASS",
      "message": "All outputs match reference",
      "comparison": {
        "limma_prepared.tsv": {
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
        "limma_prepared.tsv": {
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
        "limma_prepared.tsv": {
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
        "limma_prepared.tsv": {
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
        "limma_prepared.tsv": {
          "match": false,
          "reason": "Row count mismatch. Expected: 181, Got: 180"
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
  "limma_prepared.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] TRUE
         TCGA-FG-7608-01 TCGA-04-5840-01 TCGA-A7-3116-01 TCGA-07-5190-01
GUSB_0          5.670406        4.357914        5.537870        3.955193
IDH2_1          7.405867        8.369388        6.416530        6.007578
EZH2            6.315010        6.451967        6.019968        6.921377
MDM2            2.632977        3.247381        0.925000        3.473387
TGFBR1_4        0.000000        1.482594        0.000000        0.000000
SDHB_5          6.630325        4.400013        6.476900        6.051668
         TCGA-07-9110-01 TCGA-02-1841-01
GUSB_0          6.197428        5.485277
IDH2_1          7.661098        6.029845
EZH2            6.593471        3.759972
MDM2            2.080482        2.427142
TGFBR1_4        0.000000        0.000000
SDHB_5          5.086557        5.848783
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
  0.000   2.919   4.900   5.263   7.149  15.303 
Total NAs: 0 
Proportion NAs: 0 

```

**Archived LLM output excerpt: `limma_prepared.tsv`**

```tsv
	TCGA-FG-7608-01	TCGA-04-5840-01	TCGA-A7-3116-01	TCGA-07-5190-01	TCGA-07-9110-01	TCGA-02-1841-01	TCGA-A2-8417-01	TCGA-04-2354-01	TCGA-FG-5284-01	TCGA-A7-3974-01	TCGA-B6-4255-01	TCGA-GM-5832-01	TCGA-E2-2473-01	TCGA-FG-7979-01	TCGA-03-9682-01	TCGA-07-1640-01	TCGA-10-2136-01	TCGA-08-3258-01	TCGA-01-6447-01	TCGA-07-6047-01
GUSB_0	5.67040560323738	4.35791438682669	5.53787040537306	3.95519282465466	6.19742822381546	5.48527744548956	2.78879846514227	5.37709037757228	5.58625769444815	4.75225886531705	5.36064121977267	4.54945308843943	4.94992455407537	5.19519692509731	5.30810873184213	6.23919260520825	5.47235634618233	5.2760308423811	6.68274913933564	4.69321174888494
IDH2_1	7.40586749461935	8.36938769933665	6.41652971635237	6.00757787423706	7.66109761347837	6.02984474170584	6.20867083021524	7.64361155296046	7.2836105120965	5.47235634618233	7.14880568856884	5.03016950256947	3.40563460622084	6.15952135417423	8.19620552732277	7.71545350483499	3.71782591186056	7.8105112703867	7.8105112703867	6.42613321618534
EZH2	6.31500980014561	6.45196724611339	6.01996773188029	6.92137723520152	6.59347085573301	3.75997228870438	6.13797523717972	5.06556592780971	3.95519282465466	3.332459047297	5.54880493093968	3.54675416224351	7.69701858941564	5.02027445459514	3.73275626289319	6.55216942445779	3.20244338853468	5.55653910008577	4.03622345105032	1.57646625064904
MDM2	2.63297694121096	3.24738057313159	0.925	3.47338686844535	2.08048202372184	2.42714185722088	2.51968346173395	4.26755757771064	2.06438561897747	1.9330889048886	2.47771663916277	2.82916621124515	4.05846312937163	3.42083491556534	2.86414982848697	2.61222506624702	3.06300970672733	3.51108715363386	1.68872187554087	3.68018055495879
TGFBR1_4	0	1.48259406309495	0	0	0	0	0	0.1	0.9	1.9330889048886	0	1.49721812561298	0	0	0.0500000000000001	0	0.6	0	0	0
SDHB_5	6.63032543168805	4.40001345616764	6.47690033392353	6.05166755809257	5.0865572446991	5.84878261719754	5.62123302866339	6.67043515069985	5.41651953161018	4.61672441264038	6.5823078977745	5.08859095819613	4.32162772890394	5.6947097312843	6.5823078977745	6.20867083021524	6.41652971635237	6.15952135417423	3.97756348683119	5.49648514504731
STAT5A	4.41522859406553	3.5276764620193	3.754198427833

... [truncated, original 127471 chars]
```

### `case_02` - `PASS`

**comparison.json**

```json
{
  "limma_prepared.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] TRUE
          TCGA-05-9916-01 TCGA-GM-8196-01 TCGA-05-8021-01 TCGA-E2-1539-01
UBC              2.124617       0.0000000       2.3459261       0.8709677
CDKN2B_1         3.672522       3.6814638       0.0000000       3.2855856
YWHAZ_2          5.808856       4.8766265       5.2947523       5.0729031
TSC2_3           0.000000       0.0000000       0.9677419       1.2075673
PMS2_4           1.037740       0.9516129       2.0073812       2.0348450
PRKAR1A_5        4.864492       3.8200127       4.1500331       2.0348450
          TCGA-FG-1497-01 TCGA-D8-5287-01
UBC              2.313379        2.007381
CDKN2B_1         4.118916        0.000000
YWHAZ_2          4.658695        5.672108
TSC2_3           1.619646        1.549648
PMS2_4           4.237882        1.018870
PRKAR1A_5        3.061765        3.384226
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
  0.000   2.632   4.632   5.066   6.938  14.790 
Total NAs: 0 
Proportion NAs: 0 

```

**Archived LLM output excerpt: `limma_prepared.tsv`**

```tsv
	TCGA-05-9916-01	TCGA-GM-8196-01	TCGA-05-8021-01	TCGA-E2-1539-01	TCGA-FG-1497-01	TCGA-D8-5287-01	TCGA-05-9243-01	TCGA-A7-9846-01	TCGA-A1-5924-01	TCGA-08-2656-01	TCGA-EW-2217-01	TCGA-BT-6461-01	TCGA-08-1928-01	TCGA-D8-6045-01	TCGA-D8-8491-01	TCGA-EW-6511-01	TCGA-A7-6511-01	TCGA-04-4500-01	TCGA-D8-5713-01	TCGA-A2-4134-01	TCGA-08-8570-01	TCGA-06-3360-01	TCGA-01-7005-01	TCGA-06-6654-01	TCGA-02-5417-01	TCGA-A7-2533-01	TCGA-B6-4730-01	TCGA-03-6410-01	TCGA-04-4549-01	TCGA-07-2889-01	TCGA-FG-3750-01
UBC	2.12461732705317	0	2.34592613854083	0.870967741935484	2.31337901099249	2.00738124808051	3.0088467312366	4.22636273547578	3.62331023197398	1.69206895214795	2.10384777254431	1.63577500060484	3.44732292244409	1.65859818607708	0.983870967741935	2.29545915111525	1.18869758087779	1.600776210259	3.78486379264211	2.00068709486634	1.19813245992168	1.03773951617556	2.60386228443131	1.63577500060484	2.95716016959195	1.95382802236711	2.89741197354927	1.16982782279001	1.33965564558003	1.65190403286291	1.28304637131669
CDKN2B_1	3.67252231972602	3.6814638387726	0	3.28558560700586	4.11891638318602	0	3.0088467312366	2.02815080258937	1.97391048200964	3.51793703749325	4.11891638318602	1.63577500060484	3.82001274028796	1.65859818607708	2.64008346984374	1.95382802236711	2.60386228443131	2.33129887086973	3.46851663493711	4.47081898171194	2.89741197354927	4.56796392543571	1.24530685514113	0	1.61964596834678	2.18692599057976	0	0	0.758064516129032	1.65190403286291	0
YWHAZ_2	5.80885585859172	4.87662645494435	5.29475230024122	5.07290314170886	4.65869466070738	5.672107682212	5.43595705219804	4.46386091094551	4.99408335630644	5.13366985317421	5.305451653609	4.70293491856348	5.12607054251823	4.97236612940435	5.25430394274711	6.29280059757896	5.59681585086398	4.87662645494435	5.59681585086398	4.80466798000523	5.85139812808371	5.48424663763916	5.234755715721	4.56047460865999	6.06602823726302	5.49818365235231	4.47081898171194	4.65869466070738	4.48069830837293	5.00113491114777	4.6396169188638
TSC2_3	0	0	0.967741935483871	1.20756733896557	1.61964596834678	1.54964838765509	1.16982782279001	3.58881968859483	3.10881711452968	1.69206895214795	3.71514560097654	1	4.00152484981049	3.18742278162362	2.832276281837

... [truncated, original 171188 chars]
```

### `case_03` - `PASS`

**comparison.json**

```json
{
  "limma_prepared.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] TRUE
        TCGA-D8-9652-01 TCGA-B6-8960-01 TCGA-08-6812-01 TCGA-04-3704-01
EZH2_0         3.360143        1.839180        2.902297        3.214207
CCND3_1        7.966010        9.400021        6.191019        8.721252
CCND1_2        3.754462        5.495988        5.056898        4.674521
E2F1           6.642653        7.025206        7.472694        7.130116
NOTCH1         2.252604        3.649535        4.048860        1.585952
SPOP_5        10.172814       10.246403        9.290624       10.108287
        TCGA-08-3279-01 TCGA-A1-9099-01
EZH2_0         0.000000        3.286853
CCND3_1        8.280449        7.788325
CCND1_2        4.571471        5.169082
E2F1           6.242872        9.127923
NOTCH1         2.692454        2.746482
SPOP_5        10.561395       10.881151
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
  0.000   2.536   4.600   4.952   6.822  15.230 
Total NAs: 0 
Proportion NAs: 0 

```

**Archived LLM output excerpt: `limma_prepared.tsv`**

```tsv
	TCGA-D8-9652-01	TCGA-B6-8960-01	TCGA-08-6812-01	TCGA-04-3704-01	TCGA-08-3279-01	TCGA-A1-9099-01	TCGA-A1-1771-01	TCGA-FG-6975-01	TCGA-05-3181-01	TCGA-FG-9096-01	TCGA-10-1234-01	TCGA-A1-4471-01	TCGA-03-2353-01	TCGA-B6-4596-01	TCGA-BT-3218-01	TCGA-06-5889-01	TCGA-04-9112-01	TCGA-EW-4428-01	TCGA-09-5688-01	TCGA-03-9321-01	TCGA-06-2566-01	TCGA-B6-4023-01	TCGA-01-9218-01	TCGA-02-2361-01	TCGA-E2-7473-01	TCGA-GM-1204-01	TCGA-08-4790-01	TCGA-EW-3979-01	TCGA-09-2664-01	TCGA-05-1024-01	TCGA-09-7316-01	TCGA-FG-9827-01	TCGA-A2-7788-01	TCGA-A1-6562-01	TCGA-FG-8266-01	TCGA-10-1305-01	TCGA-E2-5322-01	TCGA-04-8543-01
EZH2_0	3.36014273206573	1.83918018042277	2.90229673945264	3.21420680053347	0	3.28685348027027	0.907894736842105	2.88768581425982	2.2356603412577	1.95386159469719	1.70510493472293	2.26799767521812	1.97024465387925	3.31634140406642	3.66260048603667	1.5727939151474	2.66304849867841	1	3.90346292859606	1.74210694907241	3.83373706343436	4.20223417129879	3.0635049985695	2.71454181127466	3.29247203475638	3.51452725327681	1.04618125005693	1.55740016512842	2.21024496534554	1.65595575717675	2.51360386842293	2.21024496534554	2.94105990771682	3.61162850848138	2.7464821261748	3.20373496785952	4.03022807263443	1.92109547633307
CCND3_1	7.96601038866985	9.40002070336267	6.1910190149743	8.72125227781267	8.28044900391551	7.78832522466188	8.67344854071329	7.25445456739555	7.34997265684452	7.96601038866985	7.5421190454194	7.86080194953519	8.94206350759123	8.57732747295984	7.98437711049974	7.71671486265639	8.31967932957137	9.23674080906978	7.68262429544582	7.82551714411742	8.11220008857876	8.31967932957137	8.62584217479628	8.11220008857876	8.8087351560266	7.34997265684452	6.97367536194776	8.72125227781267	7.63755875162494	8.69735040926298	6.84771839071811	9.00871399033992	8.31967932957137	9.31881865843389	8.28044900391551	8.48966666769491	8.4529572805343	7.89729328153735
CCND1_2	3.75446192803346	5.49598787364993	5.05689849555941	4.67452142002701	4.57147108347685	5.16908207047156	5.28159208379726	5.28159208379726	4.93055248262596	4.70811165969939	4.10059343988496	6.81091361249164	3.21420680053347	4.72386872023218	4.60813875577796	4.48566338375121	4.60813875577796	5.00338190686561	5.47420

... [truncated, original 279653 chars]
```

### `case_04` - `PASS`

**comparison.json**

```json
{
  "limma_prepared.tsv": {
    "match": true,
    "reason": "All columns match within tolerance"
  }
}
```

**stdout excerpt**

```text
[1] TRUE
        TCGA-05-4160-01 TCGA-01-5806-01 TCGA-01-2940-01 TCGA-FG-4406-01
APC_0          6.272828        6.254631        5.406406        4.572340
IDH2_1         3.017575        4.632871        3.302261        2.841344
RHOA_2         7.849750        0.000000        0.880000        5.846897
FANCA          5.705682        6.726653        3.684318        5.220758
KDM6A_4        0.000000        3.189779        2.662791        0.020000
IDH1_5         0.760000        0.840000        2.476132        0.020000
        TCGA-06-3367-01 TCGA-EW-3683-01
APC_0          6.309159        5.941270
IDH2_1         3.880423        2.061513
RHOA_2         0.000000        7.024133
FANCA          5.484621        4.930379
KDM6A_4        2.662791        2.061513
IDH1_5         4.367491        1.661173
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
  0.000   2.799   4.843   5.164   7.040  14.732 
Total NAs: 0 
Proportion NAs: 0 

```

**Archived LLM output excerpt: `limma_prepared.tsv`**

```tsv
	TCGA-05-4160-01	TCGA-01-5806-01	TCGA-01-2940-01	TCGA-FG-4406-01	TCGA-06-3367-01	TCGA-EW-3683-01	TCGA-07-4382-01	TCGA-02-1437-01	TCGA-A2-2703-01	TCGA-09-5189-01	TCGA-04-3394-01	TCGA-05-3400-01	TCGA-GM-4635-01	TCGA-07-2991-01	TCGA-06-3213-01	TCGA-08-6761-01	TCGA-A2-5223-01	TCGA-03-2736-01	TCGA-09-9138-01	TCGA-EW-7903-01	TCGA-A2-3137-01	TCGA-B6-8152-01	TCGA-EW-9453-01	TCGA-06-4489-01	TCGA-08-2946-01
APC_0	6.27282812230998	6.25463066403757	5.40640592743459	4.57234017741993	6.30915926915051	5.94126953089958	4.87403033089357	6.11232239096485	4.85872832054162	5.59471648059421	5.04149666916246	6.18448140486401	6.05560951991428	5.18280827930346	5.5201606531591	6.53039103493494	5.25958057267009	6.68570964546582	4.54313722734895	6.27282812230998	5.5201606531591	5.78595558558935	4.65456479954281	6.29099369573024	6.11232239096485
IDH2_1	3.01757502005096	4.63287064373261	3.3022607698674	2.84134418169767	3.88042290689434	2.06151324043607	4.47961438709851	4.36749076995024	4.60708543669458	5.91328894330006	2.79924548490191	3.46166772192864	3.3022607698674	2.3417134857767	4.36749076995024	4.84342631018966	3.60472593545615	4.45802270323221	4.79389045085321	4.85872832054162	4.22741778143472	2.76441680557971	4.31232449911339	3.54392602928641	4.70822127914116
RHOA_2	7.84974987930083	0	0.88	5.84689693095101	0	7.02413336948716	0	0.978496250072116	6.23643320576516	0	7.34701219271804	2.22707673319462	0	1.39777450049039	0.1	0	0.1	7.28230486745396	5.73272453959498	9.86154177845505	10.8538801388778	8.01631714666499	0	1.05359400011538	0
FANCA	5.7056821805367	6.72665291506471	3.68431811040853	5.22075750141354	5.48462140060307	4.93037900401839	3.97359634600131	5.75934006259217	7.00801974657515	5.91328894330006	4.72380888948939	5.22075750141354	5.78595558558935	5.09545949603024	6.18448140486401	5.32473289968318	5.82341548761711	6.07502863131224	6.47876693120973	5.30545161034566	4.63287064373261	5.50239102688109	3.3108009726863	5.54013532842459	4.06447616074166
KDM6A_4	0	3.18977867666517	2.66279112619981	0.02	2.66279112619981	2.06151324043607	0.7	3.50023529216833	3.56693973156996	2.50643582894801	1.26908275033173	0	3.46166772192864	2.3417134857767	2.01915749287393	0.86	3.42095866928245	2.167402

... [truncated, original 88095 chars]
```

### `case_05` - `FAIL`

**comparison.json**

```json
{
  "limma_prepared.tsv": {
    "match": false,
    "reason": "Row count mismatch. Expected: 181, Got: 180"
  }
}
```

**stdout excerpt**

```text
[1] TRUE
      TCGA-D8-3746-01 TCGA-A2-1091-01 TCGA-FG-6163-01 TCGA-A7-3012-01
PHGDH        8.465990        8.625432        7.274249        8.123041
TP53         5.728748        5.436776        5.942878        4.785740
SHMT2        4.582169        4.017248        4.530278        3.797842
MYCN         7.762935        7.448175        6.969329        8.315441
EP300        3.842611        3.645340        3.697948        3.046165
CASP9       14.592386       13.562873       13.562873       13.842189
      TCGA-BT-5121-01 TCGA-A1-3479-01
PHGDH        7.388825        7.702762
TP53         5.998742        6.333910
SHMT2        2.130234        3.820226
MYCN         7.247837        7.762935
EP300        3.069546        4.186429
CASP9       14.592386       14.592386
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
  0.000   3.298   5.126   5.657   7.548  14.592 
Total NAs: 0 
Proportion NAs: 0 

```

**Archived LLM output excerpt: `limma_prepared.tsv`**

```tsv
	TCGA-D8-3746-01	TCGA-A2-1091-01	TCGA-FG-6163-01	TCGA-A7-3012-01	TCGA-BT-5121-01	TCGA-A1-3479-01	TCGA-07-2049-01	TCGA-08-8034-01	TCGA-A1-9167-01	TCGA-FG-9482-01	TCGA-D8-5224-01	TCGA-09-8409-01	TCGA-E2-1726-01	TCGA-BT-5207-01	TCGA-A2-4150-01	TCGA-B6-3480-01	TCGA-04-6729-01	TCGA-02-3923-01	TCGA-02-2846-01	TCGA-05-6588-01	TCGA-GM-1945-01	TCGA-B6-5589-01	TCGA-08-9649-01	TCGA-10-7683-01	TCGA-BT-4761-01	TCGA-04-4649-01	TCGA-D8-3284-01	TCGA-FG-2149-01	TCGA-A1-6009-01	TCGA-04-9826-01	TCGA-A1-1421-01	TCGA-05-8094-01	TCGA-FG-6219-01	TCGA-10-6555-01	TCGA-07-5500-01	TCGA-BT-7097-01
PHGDH	8.46598973497115	8.62543211976667	7.27424893378367	8.12304071946217	7.38882466287254	7.70276194382931	6.64152011761391	7.63532075689925	7.51976305337694	6.48540658419248	6.94075595438211	8.31544076889883	8.62543211976667	8.53459732455537	6.6649271431721	9.44415581075883	8.27275402447703	8.50029352976326	7.2214256407551	3.6589234397307	8.23006728005522	7.27424893378367	7.27424893378367	7.60593778532951	7.2214256407551	6.22481232505339	7.2214256407551	7.32054996217956	7.38882466287254	6.96932869523764	7.95215987840184	6.96932869523764	6.10469043451204	8.17086541115583	8.07521602776851	7.2214256407551
TP53	5.72874824400882	5.43677578565383	5.9428781031204	4.78573979308476	5.99874227353006	6.33391049320497	7.08406615318307	6.61811309205572	5.99874227353006	5.9428781031204	6.07807940036082	6.96932869523764	6.80876275752809	6.27679474231588	7.88777005086413	6.5427248974621	7.38882466287254	7.44817548327681	6.07807940036082	5.57070153031851	6.91218321352658	6.85362940051429	5.99874227353006	5.78241781481121	4.62916841666427	5.16926557479359	5.67834490497539	5.9428781031204	7.2214256407551	5.99874227353006	5.72874824400882	5.83682292143063	5.72874824400882	6.91218321352658	6.39235440549413	6.39235440549413
SHMT2	4.58216865034409	4.01724823104067	4.53027751521832	3.79784240908138	2.13023372135287	3.82022645740672	3.91665356334275	4.99423517891354	3.78033939023129	4.61270613304584	4.80597598006952	5.62254343846707	4.51221145671007	4.08185047617167	4.01724823104067	3.18673091454677	2.68997361076405	3.8612938800017	4.92224191266788	3.42968142214173	4.03835329389051	2.41599502116124	0.814995833413462	4.

... [truncated, original 111993 chars]
```

## Task-Level `all_cases_comparison.json`

```json
[
  {
    "case": "case_01_seed_1004",
    "status": "PASS",
    "message": "All outputs match reference",
    "comparison": {
      "limma_prepared.tsv": {
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
      "limma_prepared.tsv": {
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
      "limma_prepared.tsv": {
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
      "limma_prepared.tsv": {
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
      "limma_prepared.tsv": {
        "match": true,
        "reason": "All columns match within tolerance"
      }
    }
  }
]
```

