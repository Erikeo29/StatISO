"""Traductions francaises pour StatISO."""

STRINGS: dict[str, str] = {
    # ──────────────────────────────────────────────
    # General / Home
    # ──────────────────────────────────────────────
    "app.title": "StatISO",
    "app.subtitle": "Analyses statistiques selon les normes ISO",
    "app.version": "v1.0",
    "nav.home": "Accueil",
    "nav.ci": "Intervalle de confiance",
    "nav.ti": "Intervalle de tolérance",
    "nav.capability": "Capabilité process",
    "nav.comparison": "Comparaison IC / IT",
    "nav.simulations": "Simulations",
    "nav.documentation": "Documentation",
    # ──────────────────────────────────────────────
    # Sidebar / data
    # ──────────────────────────────────────────────
    "sidebar.language": "Langue",
    "sidebar.data_source": "Source de données",
    "sidebar.upload_file": "Importer un fichier CSV ou Excel",
    "sidebar.use_sample": "Utiliser les données exemple",
    "sidebar.sample_loaded": "Données exemple chargées",
    "sidebar.manual_input": "Saisie manuelle",
    "sidebar.manual_placeholder": "Une valeur par ligne",
    "sidebar.validate": "Valider",
    "sidebar.data_loaded": "{n} valeurs chargées",
    "sidebar.no_data": "Aucune donnée chargée",
    "sidebar.column_select": "Colonne à analyser",
    "sidebar.confidence": "Niveau de confiance",
    "sidebar.coverage": "Proportion de couverture",
    # ──────────────────────────────────────────────
    # Descriptive statistics
    # ──────────────────────────────────────────────
    "stats.n": "Taille (n)",
    "stats.mean": "Moyenne",
    "stats.std": "Écart-type",
    "stats.se": "Erreur standard",
    "stats.cv": "CV%",
    "stats.min": "Minimum",
    "stats.max": "Maximum",
    "stats.median": "Médiane",
    "stats.q1": "Q1 (25%)",
    "stats.q3": "Q3 (75%)",
    "stats.iqr": "IQR",
    "stats.variance": "Variance",
    "stats.df": "Degrés de liberté",
    # ──────────────────────────────────────────────
    # Page 1 — Confidence Interval (ISO 2602)
    # ──────────────────────────────────────────────
    "ci.title": "Intervalle de confiance pour la moyenne (ISO 2602)",
    "ci.type": "Type d'intervalle",
    "ci.bilateral": "Bilatéral",
    "ci.unilateral": "Unilatéral",
    "ci.side": "Côté",
    "ci.lower": "Inférieur",
    "ci.upper": "Supérieur",
    "ci.calculate": "Calculer",
    "ci.results": "Résultats",
    "ci.lower_bound": "Limite inférieure",
    "ci.upper_bound": "Limite supérieure",
    "ci.margin": "Marge d'erreur",
    "ci.t_value": "Valeur t",
    "ci.interpretation": (
        "Nous sommes confiants à {conf}% que la vraie moyenne "
        "se situe entre {lower} et {upper}."
    ),
    "ci.interpretation_lower": (
        "Nous sommes confiants à {conf}% que la vraie moyenne "
        "est supérieure à {bound}."
    ),
    "ci.interpretation_upper": (
        "Nous sommes confiants à {conf}% que la vraie moyenne "
        "est inférieure à {bound}."
    ),
    "ci.details": "Détails du calcul",
    "ci.export": "Exporter les résultats",
    # ──────────────────────────────────────────────
    # Page 2 — Tolerance Interval (ISO 16269-6)
    # ──────────────────────────────────────────────
    "ti.title": "Intervalle de tolérance statistique (ISO 16269-6)",
    "ti.type": "Type d'intervalle",
    "ti.bilateral": "Bilatéral",
    "ti.unilateral": "Unilatéral",
    "ti.side": "Côté",
    "ti.lower": "Inférieur",
    "ti.upper": "Supérieur",
    "ti.calculate": "Calculer",
    "ti.results": "Résultats",
    "ti.lower_bound": "Limite inférieure",
    "ti.upper_bound": "Limite supérieure",
    "ti.k_factor": "Facteur k",
    "ti.interpretation": (
        "Nous sommes confiants à {conf}% que {cov}% de la population "
        "se situe dans cet intervalle."
    ),
    "ti.normality": "Tests de normalité",
    "ti.shapiro": "Shapiro-Wilk",
    "ti.anderson": "Anderson-Darling",
    "ti.ks_test": "Kolmogorov-Smirnov",
    "ti.jb_test": "Jarque-Bera",
    "ti.is_normal": "Distribution normale (p > 0.05)",
    "ti.not_normal": "Distribution non normale (p ≤ 0.05)",
    "ti.outliers": "Détection de valeurs aberrantes",
    "ti.n_outliers": "{n} valeur(s) aberrante(s) détectée(s)",
    "ti.no_outliers": "Aucune valeur aberrante détectée",
    "ti.details": "Détails du calcul",
    "ti.export": "Exporter les résultats",
    # ──────────────────────────────────────────────
    # Page 3 — Process Capability
    # ──────────────────────────────────────────────
    "cap.title": "Analyse de capabilité process",
    "cap.lsl": "Limite inférieure de spécification (LSL)",
    "cap.usl": "Limite supérieure de spécification (USL)",
    "cap.calculate": "Analyser",
    "cap.results": "Résultats",
    "cap.cp": "Cp (capabilité potentielle)",
    "cap.cpk": "Cpk (capabilité réelle)",
    "cap.cpu": "Cpu",
    "cap.cpl": "Cpl",
    "cap.pct_out": "% hors spécifications",
    "cap.excellent": "Excellent (Cpk > 1.67)",
    "cap.capable": "Capable (Cpk > 1.33)",
    "cap.marginal": "Marginal (1.0 < Cpk ≤ 1.33)",
    "cap.incapable": "Non capable (Cpk ≤ 1.0)",
    "cap.interpretation_capable": (
        "Le processus est capable. La variabilité est bien contenue "
        "dans les spécifications."
    ),
    "cap.interpretation_incapable": (
        "Le processus n'est pas capable. Actions correctives nécessaires : "
        "réduire la variabilité ou recentrer le processus."
    ),
    # ──────────────────────────────────────────────
    # Page 4 — Comparison CI vs TI
    # ──────────────────────────────────────────────
    "comp.title": "Comparaison IC vs IT",
    "comp.calculate": "Calculer les deux intervalles",
    "comp.results": "Résultats comparatifs",
    "comp.type": "Type",
    "comp.lower": "Limite inf.",
    "comp.upper": "Limite sup.",
    "comp.width": "Largeur",
    "comp.ci_label": "Intervalle de confiance (IC)",
    "comp.ti_label": "Intervalle de tolérance (IT)",
    "comp.help_title": "Aide à la décision",
    "comp.q_objective": "Quel est votre objectif ?",
    "comp.obj_mean": "Estimer la moyenne d'un processus",
    "comp.obj_specs": "Définir des limites de spécification",
    "comp.obj_lot": "Valider un lot de production",
    "comp.obj_capability": "Évaluer la capabilité",
    "comp.rec_ci": "Recommandation : Intervalle de confiance (ISO 2602)",
    "comp.rec_ti": "Recommandation : Intervalle de tolérance (ISO 16269-6)",
    "comp.rec_both": "Recommandation : Les deux méthodes",
    "comp.key_differences": "Différences clés",
    "comp.aspect": "Aspect",
    "comp.objective": "Objectif",
    "comp.ci_objective": "Estimer la moyenne",
    "comp.ti_objective": "Contenir la population",
    "comp.formula": "Formule",
    "comp.ci_formula": "x̄ ± t × s/√n",
    "comp.ti_formula": "x̄ ± k × s",
    "comp.typical_use": "Usage typique",
    "comp.ci_use": "Validation, comparaison",
    "comp.ti_use": "Spécifications, capabilité",
    # ──────────────────────────────────────────────
    # Page 5 — Simulations
    # ──────────────────────────────────────────────
    "sim.title": "Simulations interactives",
    "sim.select": "Choisir une simulation",
    "sim.ic_vs_it": "IC vs IT — comparaison visuelle",
    "sim.sample_size": "Impact de la taille d'échantillon",
    "sim.capability": "Analyse de capabilité",
    "sim.coverage": "Couverture des intervalles de confiance",
    "sim.run": "Simuler",
    "sim.n": "Taille de l'échantillon",
    "sim.confidence": "Niveau de confiance",
    "sim.coverage_prop": "Proportion IT",
    "sim.process_mean": "Moyenne du processus",
    "sim.process_std": "Écart-type du processus",
    "sim.lsl": "LSL",
    "sim.usl": "USL",
    "sim.obs_ic_it": (
        "L'IT est toujours plus large que l'IC. L'IC estime la position "
        "de la moyenne, l'IT contient une proportion de la population."
    ),
    "sim.obs_sample": (
        "L'IC diminue rapidement avec √n. L'IT diminue lentement. "
        "Pour n > 100, l'amélioration est marginale."
    ),
    "sim.obs_coverage": (
        "Sur 100 intervalles à 95%, environ 95 contiennent "
        "la vraie moyenne μ."
    ),
    "sim.launch_coverage": "Lancer 100 simulations",
    "sim.coverage_result": "Intervalles contenant μ : {n}/100",
    # ──────────────────────────────────────────────
    # Page 6 — Documentation
    # ──────────────────────────────────────────────
    "doc.title": "Documentation et formules",
    "doc.select": "Section",
    "doc.iso2602": "ISO 2602:1980 — intervalles de confiance",
    "doc.iso16269": "ISO 16269-6:2014 — intervalles de tolérance",
    "doc.comparison": "Comparaison IC vs IT",
    "doc.glossary": "Glossaire",
    "doc.methodology": "Méthodologie",
    "doc.principle": "Principe",
    "doc.formulas": "Formules",
    "doc.ci_principle": (
        "L'intervalle de confiance estime la plage dans laquelle se trouve "
        "la vraie moyenne de la population avec un certain niveau de confiance."
    ),
    "doc.ti_principle": (
        "L'intervalle de tolérance contient une proportion spécifiée "
        "de la population avec un certain niveau de confiance."
    ),
    "doc.case_sigma_known": "Cas 1 : σ connu",
    "doc.case_sigma_unknown": "Cas 2 : σ inconnu (Student)",
    "doc.where": "Où :",
    # ──────────────────────────────────────────────
    # Common / errors
    # ──────────────────────────────────────────────
    "common.error": "Erreur",
    "common.warning": "Attention",
    "common.success": "Succès",
    "common.no_data": "Veuillez d'abord charger des données.",
    "common.min_samples": "Au moins {n} observations requises.",
    "common.download": "Télécharger",
    "common.plot": "Graphique",
    "common.table": "Tableau",
    "common.interpretation": "Interprétation",
    "common.distribution_plot": "Distribution des données",
    "common.normal_curve": "Courbe normale",
    "common.data_points": "Données",
    # ──────────────────────────────────────────────
    # Glossary
    # ──────────────────────────────────────────────
    "glossary.confidence_level": "Niveau de confiance",
    "glossary.confidence_level_def": (
        "Probabilité que l'intervalle contienne le paramètre vrai."
    ),
    "glossary.coverage": "Proportion de couverture",
    "glossary.coverage_def": (
        "Pourcentage de la population contenu dans l'intervalle de tolérance."
    ),
    "glossary.cp": "Capabilité (Cp)",
    "glossary.cp_def": (
        "Ratio entre tolérance spécifiée et variabilité du processus."
    ),
    "glossary.cpk": "Capabilité (Cpk)",
    "glossary.cpk_def": (
        "Capabilité tenant compte du centrage du processus."
    ),
    "glossary.lsl": "LSL",
    "glossary.lsl_def": "Limite inférieure de spécification.",
    "glossary.usl": "USL",
    "glossary.usl_def": "Limite supérieure de spécification.",
    "glossary.df": "Degré de liberté",
    "glossary.df_def": "n − 1 pour un échantillon.",
    "glossary.se": "Erreur standard",
    "glossary.se_def": (
        "Écart-type de la distribution d'échantillonnage de la moyenne."
    ),
    "glossary.k_factor": "Facteur k",
    "glossary.k_factor_def": (
        "Facteur multiplicatif tabulé pour le calcul "
        "d'intervalles de tolérance."
    ),
    "glossary.t_value": "Valeur t",
    "glossary.t_value_def": (
        "Valeur critique de la loi de Student utilisée "
        "pour les intervalles de confiance."
    ),
    "glossary.normality": "Normalité",
    "glossary.normality_def": (
        "Hypothèse que les données suivent une distribution gaussienne."
    ),
    "glossary.outlier": "Valeur aberrante",
    "glossary.outlier_def": (
        "Observation anormalement éloignée du reste des données."
    ),
}
