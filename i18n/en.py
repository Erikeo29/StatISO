"""English translations for StatISO."""

STRINGS: dict[str, str] = {
    # ──────────────────────────────────────────────
    # General / Home
    # ──────────────────────────────────────────────
    "app.title": "StatISO",
    "app.subtitle": "Statistical analysis according to ISO standards",
    "app.version": "v2.0",
    "nav.home": "Home",
    "nav.ci": "Confidence Interval",
    "nav.ti": "Tolerance Interval",
    "nav.capability": "Process Capability",
    "nav.comparison": "CI / TI Comparison",
    "nav.simulations": "Simulations",
    "nav.documentation": "Documentation",
    # ──────────────────────────────────────────────
    # Sidebar / data
    # ──────────────────────────────────────────────
    "sidebar.language": "Language",
    "sidebar.data_source": "Data source",
    "sidebar.upload_file": "Upload a CSV or Excel file",
    "sidebar.use_sample": "Use sample data",
    "sidebar.sample_loaded": "Sample data loaded",
    "sidebar.manual_input": "Manual input",
    "sidebar.manual_placeholder": "One value per line",
    "sidebar.validate": "Validate",
    "sidebar.data_loaded": "{n} values loaded",
    "sidebar.no_data": "No data loaded",
    "sidebar.column_select": "Column to analyse",
    "sidebar.confidence": "Confidence level",
    "sidebar.coverage": "Coverage proportion",
    # ──────────────────────────────────────────────
    # Descriptive statistics
    # ──────────────────────────────────────────────
    "stats.n": "Sample size (n)",
    "stats.mean": "Mean",
    "stats.std": "Standard deviation",
    "stats.se": "Standard error",
    "stats.cv": "CV%",
    "stats.min": "Minimum",
    "stats.max": "Maximum",
    "stats.median": "Median",
    "stats.q1": "Q1 (25%)",
    "stats.q3": "Q3 (75%)",
    "stats.iqr": "IQR",
    "stats.variance": "Variance",
    "stats.df": "Degrees of freedom",
    # ──────────────────────────────────────────────
    # Page 1 — Confidence Interval (ISO 2602)
    # ──────────────────────────────────────────────
    "ci.title": "Confidence interval for the mean (ISO 2602)",
    "ci.type": "Interval type",
    "ci.bilateral": "Two-sided",
    "ci.unilateral": "One-sided",
    "ci.side": "Side",
    "ci.lower": "Lower",
    "ci.upper": "Upper",
    "ci.calculate": "Calculate",
    "ci.results": "Results",
    "ci.lower_bound": "Lower bound",
    "ci.upper_bound": "Upper bound",
    "ci.margin": "Margin of error",
    "ci.t_value": "t-value",
    "ci.interpretation": (
        "We are {conf}% confident that the true mean "
        "lies between {lower} and {upper}."
    ),
    "ci.interpretation_lower": (
        "We are {conf}% confident that the true mean "
        "is greater than {bound}."
    ),
    "ci.interpretation_upper": (
        "We are {conf}% confident that the true mean "
        "is less than {bound}."
    ),
    "ci.details": "Calculation details",
    "ci.export": "Export results",
    # ──────────────────────────────────────────────
    # Page 2 — Tolerance Interval (ISO 16269-6)
    # ──────────────────────────────────────────────
    "ti.title": "Statistical tolerance interval (ISO 16269-6)",
    "ti.type": "Interval type",
    "ti.bilateral": "Two-sided",
    "ti.unilateral": "One-sided",
    "ti.side": "Side",
    "ti.lower": "Lower",
    "ti.upper": "Upper",
    "ti.calculate": "Calculate",
    "ti.results": "Results",
    "ti.lower_bound": "Lower bound",
    "ti.upper_bound": "Upper bound",
    "ti.k_factor": "k-factor",
    "ti.interpretation": (
        "We are {conf}% confident that {cov}% of the population "
        "falls within this interval."
    ),
    "ti.normality": "Normality tests",
    "ti.shapiro": "Shapiro-Wilk",
    "ti.anderson": "Anderson-Darling",
    "ti.ks_test": "Kolmogorov-Smirnov",
    "ti.jb_test": "Jarque-Bera",
    "ti.is_normal": "Normal distribution (p > 0.05)",
    "ti.not_normal": "Non-normal distribution (p ≤ 0.05)",
    "ti.outliers": "Outlier detection",
    "ti.n_outliers": "{n} outlier(s) detected",
    "ti.no_outliers": "No outliers detected",
    "ti.details": "Calculation details",
    "ti.export": "Export results",
    # ──────────────────────────────────────────────
    # Page 3 — Process Capability
    # ──────────────────────────────────────────────
    "cap.title": "Process capability analysis",
    "cap.lsl": "Lower specification limit (LSL)",
    "cap.usl": "Upper specification limit (USL)",
    "cap.calculate": "Analyse",
    "cap.results": "Results",
    "cap.cp": "Cp (potential capability)",
    "cap.cpk": "Cpk (actual capability)",
    "cap.cpu": "Cpu",
    "cap.cpl": "Cpl",
    "cap.pct_out": "% out of specification",
    "cap.excellent": "Excellent (Cpk > 1.67)",
    "cap.capable": "Capable (Cpk > 1.33)",
    "cap.marginal": "Marginal (1.0 < Cpk ≤ 1.33)",
    "cap.incapable": "Not capable (Cpk ≤ 1.0)",
    "cap.interpretation_capable": (
        "The process is capable. Variability is well contained "
        "within the specifications."
    ),
    "cap.interpretation_incapable": (
        "The process is not capable. Corrective actions required: "
        "reduce variability or re-centre the process."
    ),
    # ──────────────────────────────────────────────
    # Page 4 — Comparison CI vs TI
    # ──────────────────────────────────────────────
    "comp.title": "CI vs TI Comparison",
    "comp.calculate": "Calculate both intervals",
    "comp.results": "Comparative results",
    "comp.type": "Type",
    "comp.lower": "Lower bound",
    "comp.upper": "Upper bound",
    "comp.width": "Width",
    "comp.ci_label": "Confidence Interval (CI)",
    "comp.ti_label": "Tolerance Interval (TI)",
    "comp.help_title": "Decision guide",
    "comp.q_objective": "What is your objective?",
    "comp.obj_mean": "Estimate a process mean",
    "comp.obj_specs": "Define specification limits",
    "comp.obj_lot": "Validate a production batch",
    "comp.obj_capability": "Assess capability",
    "comp.rec_ci": "Recommendation: Confidence Interval (ISO 2602)",
    "comp.rec_ti": "Recommendation: Tolerance Interval (ISO 16269-6)",
    "comp.rec_both": "Recommendation: Both methods",
    "comp.key_differences": "Key differences",
    "comp.aspect": "Aspect",
    "comp.objective": "Objective",
    "comp.ci_objective": "Estimate the mean",
    "comp.ti_objective": "Contain the population",
    "comp.formula": "Formula",
    "comp.ci_formula": "x̄ ± t × s/√n",
    "comp.ti_formula": "x̄ ± k × s",
    "comp.typical_use": "Typical use",
    "comp.ci_use": "Validation, comparison",
    "comp.ti_use": "Specifications, capability",
    # ──────────────────────────────────────────────
    # Page 5 — Simulations
    # ──────────────────────────────────────────────
    "sim.title": "Interactive simulations",
    "sim.select": "Choose a simulation",
    "sim.ic_vs_it": "CI vs TI — visual comparison",
    "sim.sample_size": "Sample size impact",
    "sim.capability": "Capability analysis",
    "sim.coverage": "Confidence interval coverage",
    "sim.run": "Simulate",
    "sim.n": "Sample size",
    "sim.confidence": "Confidence level",
    "sim.coverage_prop": "TI proportion",
    "sim.process_mean": "Process mean",
    "sim.process_std": "Process standard deviation",
    "sim.lsl": "LSL",
    "sim.usl": "USL",
    "sim.obs_ic_it": (
        "The TI is always wider than the CI. The CI estimates the position "
        "of the mean, the TI contains a proportion of the population."
    ),
    "sim.obs_sample": (
        "The CI decreases rapidly with √n. The TI decreases slowly. "
        "For n > 100, the improvement is marginal."
    ),
    "sim.obs_coverage": (
        "Out of 100 intervals at 95%, approximately 95 contain "
        "the true mean μ."
    ),
    "sim.launch_coverage": "Run 100 simulations",
    "sim.coverage_result": "Intervals containing μ: {n}/100",
    # ──────────────────────────────────────────────
    # Page 6 — Documentation
    # ──────────────────────────────────────────────
    "doc.title": "Documentation and formulas",
    "doc.select": "Section",
    "doc.iso2602": "ISO 2602:1980 — confidence intervals",
    "doc.iso16269": "ISO 16269-6:2014 — tolerance intervals",
    "doc.comparison": "CI vs TI comparison",
    "doc.glossary": "Glossary",
    "doc.methodology": "Methodology",
    "doc.principle": "Principle",
    "doc.formulas": "Formulas",
    "doc.ci_principle": (
        "The confidence interval estimates the range within which the true "
        "population mean lies at a given confidence level."
    ),
    "doc.ti_principle": (
        "The tolerance interval contains a specified proportion "
        "of the population at a given confidence level."
    ),
    "doc.case_sigma_known": "Case 1: σ known",
    "doc.case_sigma_unknown": "Case 2: σ unknown (Student)",
    "doc.where": "Where:",
    # ──────────────────────────────────────────────
    # Common / errors
    # ──────────────────────────────────────────────
    "common.error": "Error",
    "common.warning": "Warning",
    "common.success": "Success",
    "common.no_data": "Please load data first.",
    "common.min_samples": "At least {n} observations required.",
    "common.download": "Download",
    "common.plot": "Plot",
    "common.table": "Table",
    "common.interpretation": "Interpretation",
    "common.distribution_plot": "Data distribution",
    "common.normal_curve": "Normal curve",
    "common.data_points": "Data points",
    # ──────────────────────────────────────────────
    # Glossary
    # ──────────────────────────────────────────────
    "glossary.confidence_level": "Confidence level",
    "glossary.confidence_level_def": (
        "Probability that the interval contains the true parameter."
    ),
    "glossary.coverage": "Coverage proportion",
    "glossary.coverage_def": (
        "Percentage of the population contained in the tolerance interval."
    ),
    "glossary.cp": "Capability (Cp)",
    "glossary.cp_def": (
        "Ratio of specified tolerance to process variability."
    ),
    "glossary.cpk": "Capability (Cpk)",
    "glossary.cpk_def": (
        "Capability accounting for process centring."
    ),
    "glossary.lsl": "LSL",
    "glossary.lsl_def": "Lower specification limit.",
    "glossary.usl": "USL",
    "glossary.usl_def": "Upper specification limit.",
    "glossary.df": "Degrees of freedom",
    "glossary.df_def": "n − 1 for a sample.",
    "glossary.se": "Standard error",
    "glossary.se_def": (
        "Standard deviation of the sampling distribution of the mean."
    ),
    "glossary.k_factor": "k-factor",
    "glossary.k_factor_def": (
        "Tabulated multiplicative factor for tolerance interval calculation."
    ),
    "glossary.t_value": "t-value",
    "glossary.t_value_def": (
        "Critical value from Student's t-distribution used "
        "for confidence intervals."
    ),
    "glossary.normality": "Normality",
    "glossary.normality_def": (
        "Assumption that the data follow a Gaussian distribution."
    ),
    "glossary.outlier": "Outlier",
    "glossary.outlier_def": (
        "Observation abnormally far from the rest of the data."
    ),
}
