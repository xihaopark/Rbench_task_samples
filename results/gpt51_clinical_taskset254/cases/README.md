# Rich Case Review Index

These pages expand the 50 sampled audit cases with actual task inputs, reference outputs, generated code, execution logs, generated output files, and compact evaluation records.

| # | task | current | simple | root cause | page |
|---:|---|---|---|---|---|
| 01 | `pharmaverse/aNCA/get_conversion_factor` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_01_pharmaverse_aNCA_get_conversion_factor.md) |
| 02 | `pharmaverse/aNCA/g_pkcg03_log` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_02_pharmaverse_aNCA_g_pkcg03_log.md) |
| 03 | `pharmaverse/admiral/convert_special_cases` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_03_pharmaverse_admiral_convert_special_cases.md) |
| 04 | `pharmaverse/tidytlg/check_file` | `NO_OUTPUT/exec_fail` | `NO_OUTPUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_04_pharmaverse_tidytlg_check_file.md) |
| 05 | `pharmaverse/tidytlg/check_req_arg` | `NO_OUTPUT/exec_fail` | `NO_OUTPUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_05_pharmaverse_tidytlg_check_req_arg.md) |
| 06 | `pharmaverse/admiral/count_vals` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `data_or_fixture_issue` | [case](./case_06_pharmaverse_admiral_count_vals.md) |
| 07 | `pharmaverse/admiral/compute_age_years` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_wrong` | [case](./case_07_pharmaverse_admiral_compute_age_years.md) |
| 08 | `pharmaverse/admiral/derive_vars_joined` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_08_pharmaverse_admiral_derive_vars_joined.md) |
| 09 | `pharmaverse/metatools/dash_to_eq` | `NO_OUTPUT/exec_fail` | `NO_OUTPUT/exec_fail` | `prompt_wrong` | [case](./case_09_pharmaverse_metatools_dash_to_eq.md) |
| 10 | `pharmaverse/aNCA/add_exclusion_reasons` | `FAIL/output_bad` | `TIMEOUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_10_pharmaverse_aNCA_add_exclusion_reasons.md) |
| 11 | `pharmaverse/aNCA/check_valid_pknca_data` | `FAIL/output_bad` | `NO_OUTPUT/exec_fail` | `prompt_wrong` | [case](./case_11_pharmaverse_aNCA_check_valid_pknca_data.md) |
| 12 | `pharmaverse/admiral/call_derivation` | `NO_OUTPUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_wrong` | [case](./case_12_pharmaverse_admiral_call_derivation.md) |
| 13 | `pharmaverse/aNCA/add_qmd_plot` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_13_pharmaverse_aNCA_add_qmd_plot.md) |
| 14 | `pharmaverse/admiral/print_named_list` | `TIMEOUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_14_pharmaverse_admiral_print_named_list.md) |
| 15 | `pharmaverse/aNCA/dose_profile_duplicates` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_reference_mismatch` | [case](./case_15_pharmaverse_aNCA_dose_profile_duplicates.md) |
| 16 | `pharmaverse/tidytlg/replace_na_with_blank` | `FAIL/output_bad` | `NO_OUTPUT/exec_fail` | `llm_wrong` | [case](./case_16_pharmaverse_tidytlg_replace_na_with_blank.md) |
| 17 | `pharmaverse/aNCA/error_plot` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_17_pharmaverse_aNCA_error_plot.md) |
| 18 | `pharmaverse/sdtm.oak/str_to_anycase` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `llm_wrong` | [case](./case_18_pharmaverse_sdtm_oak_str_to_anycase.md) |
| 19 | `pharmaverse/aNCA/add_qmd_sl_plottabletable` | `NO_OUTPUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_wrong` | [case](./case_19_pharmaverse_aNCA_add_qmd_sl_plottabletable.md) |
| 20 | `pharmaverse/aNCA/create_html_dose_slides` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_20_pharmaverse_aNCA_create_html_dose_slides.md) |
| 21 | `pharmaverse/admiral/extract_unit` | `TIMEOUT/exec_fail` | `FAIL/output_bad` | `llm_wrong` | [case](./case_21_pharmaverse_admiral_extract_unit.md) |
| 22 | `pharmaverse/admiraldev/get_source_vars` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_22_pharmaverse_admiraldev_get_source_vars.md) |
| 23 | `pharmaverse/admiraldev/squote` | `FAIL/output_bad` | `NO_OUTPUT/exec_fail` | `llm_wrong` | [case](./case_23_pharmaverse_admiraldev_squote.md) |
| 24 | `pharmaverse/aNCA/translate_terms` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_24_pharmaverse_aNCA_translate_terms.md) |
| 25 | `pharmaverse/admiral/restrict_imputed_dtc_dtm` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_25_pharmaverse_admiral_restrict_imputed_dtc_dtm.md) |
| 26 | `pharmaverse/admiral/get_imputation_target_date` | `NO_OUTPUT/exec_fail` | `NO_OUTPUT/exec_fail` | `prompt_wrong` | [case](./case_26_pharmaverse_admiral_get_imputation_target_date.md) |
| 27 | `pharmaverse/admiraldiscovery/admiral_pkg_versions` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_27_pharmaverse_admiraldiscovery_admiral_pkg_versions.md) |
| 28 | `pharmaverse/sdtm.oak/problems` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_28_pharmaverse_sdtm_oak_problems.md) |
| 29 | `pharmaverse/aNCA/add_qmd_sl_plot` | `TIMEOUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_29_pharmaverse_aNCA_add_qmd_sl_plot.md) |
| 30 | `pharmaverse/admiral/convert_predose_patterns` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `unclear_needs_rerun` | [case](./case_30_pharmaverse_admiral_convert_predose_patterns.md) |
| 31 | `pharmaverse/aNCA/g_pkcg01_log` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_31_pharmaverse_aNCA_g_pkcg01_log.md) |
| 32 | `pharmaverse/admiral/derive_param_rr` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `data_or_fixture_issue` | [case](./case_32_pharmaverse_admiral_derive_param_rr.md) |
| 33 | `pharmaverse/admiral/slice_derivation` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_reference_mismatch` | [case](./case_33_pharmaverse_admiral_slice_derivation.md) |
| 34 | `pharmaverse/gridify/gpar_args` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `data_or_fixture_issue` | [case](./case_34_pharmaverse_gridify_gpar_args.md) |
| 35 | `pharmaverse/ggsurvfit/scale_ggsurvfit` | `FAIL/output_bad` | `FAIL/output_bad` | `llm_wrong` | [case](./case_35_pharmaverse_ggsurvfit_scale_ggsurvfit.md) |
| 36 | `pharmaverse/aNCA/get_halflife_plots_single` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_36_pharmaverse_aNCA_get_halflife_plots_single.md) |
| 37 | `pharmaverse/logrx/parse_log` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `data_or_fixture_issue` | [case](./case_37_pharmaverse_logrx_parse_log.md) |
| 38 | `pharmaverse/aNCA/g_pkcg02_lin` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_38_pharmaverse_aNCA_g_pkcg02_lin.md) |
| 39 | `pharmaverse/admiral/get_imputation_targets` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_reference_mismatch` | [case](./case_39_pharmaverse_admiral_get_imputation_targets.md) |
| 40 | `pharmaverse/aNCA/create_pptx_doc` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_40_pharmaverse_aNCA_create_pptx_doc.md) |
| 41 | `pharmaverse/admiral/derive_var_trtdurd` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_wrong` | [case](./case_41_pharmaverse_admiral_derive_var_trtdurd.md) |
| 42 | `pharmaverse/admiral/assert_valid_queries` | `TIMEOUT/exec_fail` | `NO_OUTPUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_42_pharmaverse_admiral_assert_valid_queries.md) |
| 43 | `pharmaverse/admiraldev/assert_same_type` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_reference_mismatch` | [case](./case_43_pharmaverse_admiraldev_assert_same_type.md) |
| 44 | `pharmaverse/admiraldev/assert_expr` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_44_pharmaverse_admiraldev_assert_expr.md) |
| 45 | `pharmaverse/admiraldev/assert_unit` | `FAIL/output_bad` | `NO_OUTPUT/exec_fail` | `data_or_fixture_issue` | [case](./case_45_pharmaverse_admiraldev_assert_unit.md) |
| 46 | `pharmaverse/aNCA/calculate_f` | `NO_OUTPUT/exec_fail` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_46_pharmaverse_aNCA_calculate_f.md) |
| 47 | `pharmaverse/admiral/derive_vars_atc` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_wrong` | [case](./case_47_pharmaverse_admiral_derive_vars_atc.md) |
| 48 | `pharmaverse/admiral/dthcaus_source` | `TIMEOUT/exec_fail` | `TIMEOUT/exec_fail` | `prompt_reference_mismatch` | [case](./case_48_pharmaverse_admiral_dthcaus_source.md) |
| 49 | `pharmaverse/aNCA/create_qmd_doc` | `FAIL/output_bad` | `FAIL/output_bad` | `prompt_wrong` | [case](./case_49_pharmaverse_aNCA_create_qmd_doc.md) |
| 50 | `pharmaverse/tidytlg/add_indent` | `FAIL/output_bad` | `FAIL/output_bad` | `data_or_fixture_issue` | [case](./case_50_pharmaverse_tidytlg_add_indent.md) |
