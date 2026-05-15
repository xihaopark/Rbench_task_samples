# Clinical Shortlist

This shortlist is for discussion and handoff. It separates tasks that are worth turning into full cases from tasks that should not be shown because the failure is mostly a benchmark artifact.

Source context:

- Release: `rbiobench_stable_v1`
- Track: `clinical_pilot`
- Primary failure evidence: GPT-5.1 direct LLM pass5 artifacts
- Secondary evidence where useful: Biomni agent re-evaluation artifacts

## Five Admiral Candidates

| # | Task ID | Level | Why It Is Useful | Capability Boundary |
|---|---|---:|---|---|
| 1 | `pharmaverse/admiral/derive_var_ontrtfl` | L3 | On-treatment flag from analysis date and treatment window; clinically interpretable boundary cases. | The model generated the wrong row/column shape and missed the exact flag contract. |
| 2 | `pharmaverse/admiral/derive_var_trtemfl` | L3 | Treatment-emergent AE flag using treatment dates, AE dates, toxicity grades, and subject keys. | The model added an extra AE row and failed to reproduce the canonical TEAE structure. |
| 3 | `pharmaverse/admiral/create_period_dataset` | L3 | One-row-per-subject-per-period construction from `APxxSDT` / `APxxEDT`; directly relevant to ADaM period structure. | The model failed to understand the `APxx` wide-to-long period pattern. |
| 4 | `pharmaverse/admiral/derive_vars_joined` | L3 | Joined derivation pattern used in ADaM workflows; good test of join semantics and tidy-eval. | The model passed symbols where filter conditions or `exprs()` lists were required. |
| 5 | `pharmaverse/admiral/derive_vars_transposed` | L3 | Multi-input transposed derivation with `by_vars`, `id_vars`, `key_var`, and `value_var`. | The model failed on rlang symbol conversion and variable mapping. |

## Fifteen Additional Clinical Candidates

| # | Task ID | Package | Level | Why It Is Useful | Capability Boundary |
|---|---|---|---:|---|---|
| 1 | `pharmaverse/aNCA/PKNCA_impute_method_start_c1` | aNCA | L2 | PK/NCA start-time imputation with a concrete concentration-time table. | Rule reconstruction and output shape. |
| 2 | `pharmaverse/aNCA/add_f_to_pknca_results` | aNCA | L1 | Adds `f` rows to a PKNCA-style result object. | Object structure, `bind_rows()`, CSV/RDS serialization. |
| 3 | `pharmaverse/aNCA/create_metabfl` | aNCA | L1 | Derives metabolite flags from `PARAM` and a metabolite list. | Column selection and vectorized flag derivation. |
| 4 | `pharmaverse/aNCA/dose_profile_duplicates` | aNCA | L3 | Detects dose-profile duplicates in a PK workflow. | Internal helper use and fixture interpretation. |
| 5 | `pharmaverse/aNCA/format_pkncadata_intervals` | aNCA | L2 | Builds and formats PKNCA interval data. | `PKNCAdata` object construction and interval schema. |
| 6 | `pharmaverse/aNCA/generate_tooltip_text` | aNCA | L2 | Generates tooltip text from multiple data fields. | Strict output schema and text assembly. |
| 7 | `pharmaverse/aNCA/get_conversion_factor` | aNCA | L1 | Converts between units with the `units` package. | Unit parsing and preserving the required `result` column. |
| 8 | `pharmaverse/aNCA/parse_annotation` | aNCA | L1 | Expands annotation strings with data-aware placeholders. | `glue`, labels, and fallback behavior. |
| 9 | `pharmaverse/aNCA/read_pk` | aNCA | L1 | Reads a PK dataset through an internal reader with fallback behavior. | File path handling, fallback temp data, and RDS output. |
| 10 | `pharmaverse/aNCA/simplify_unit` | aNCA | L2 | Simplifies unit expressions and handles `unitless` / NA cases. | Unit object vs string handling and value-level matching. |
| 11 | `pharmaverse/admiraldev/process_set_values_to` | admiraldev | L2 | Processes `set_values_to` expressions used by admiral derivations. | Quosures, expression lists, and expected type handling. |
| 12 | `pharmaverse/metatools/create_subgrps` | metatools | L2 | Creates subgroup labels from numeric range definitions. | Range parsing, expression evaluation, and exclusivity checks. |
| 13 | `pharmaverse/tidytlg/add_indent` | tidytlg | L2 | Computes indentation for TLG row types. | Reporting rules and exact tabular output. |
| 14 | `pharmaverse/gridify/get_layouts` | gridify | L1 | Serializes available reporting layouts. | List/data-frame serialization and strict columns. |
| 15 | `pharmaverse/ggsurvfit/scale_ggsurvfit` | ggsurvfit | L1 | Useful contrast case: GPT-5.1 passes, but agent runs can fail. | Distinguishes direct LLM ability from agent execution issues. |

## Explicitly Excluded Examples

| Task ID | Reason |
|---|---|
| `pharmaverse/admiral/derive_vars_dt` | The archived output depends on a current-date fallback. This is not a good public example. |
| `pharmaverse/admiral/compute_dtf` | Placeholder `item*` DTC values collapse the clinical meaning into mostly NA output. |
| `pharmaverse/aNCA/apply_labels` | Failure can be dominated by missing `summary.csv` even when `result.csv` matches. |
| `pharmaverse/tidytlg/replace_na_with_blank` | Same `summary.csv` false-failure issue. |
| `pharmaverse/logrx/parse_log` | Prompt/interface is too weak around non-exported behavior. |
| `pharmaverse/admiralci/hello_admiral` | Smoke test; not useful for discussing clinical coding ability. |
| `pharmaverse/sdtmchecks/pass` | Trivial wrapper; failure is mostly output shape. |
