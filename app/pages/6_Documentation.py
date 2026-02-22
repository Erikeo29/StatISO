"""Page 6 -- Documentation with formulas and glossary."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import streamlit as st

from i18n import t, get_lang

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------

if not st.session_state.get("authentication_status"):
    st.warning("Please log in from the Home page.")
    st.stop()

# ---------------------------------------------------------------------------
# Collect glossary term keys dynamically
# ---------------------------------------------------------------------------
# Glossary keys follow the pattern glossary.<term> / glossary.<term>_def.
# We import the raw dict for the current language to discover all term keys.

from i18n import fr as _fr, en as _en

_GLOSSARY_SOURCES = {"fr": _fr.STRINGS, "en": _en.STRINGS}


def _get_glossary_terms() -> list[tuple[str, str]]:
    """Return sorted list of (term, definition) from glossary.* keys."""
    strings = _GLOSSARY_SOURCES.get(get_lang(), _GLOSSARY_SOURCES["fr"])
    terms: list[tuple[str, str]] = []
    seen: set[str] = set()

    for key in strings:
        if key.startswith("glossary.") and not key.endswith("_def"):
            base = key  # e.g. "glossary.cp"
            def_key = f"{base}_def"
            if base not in seen:
                seen.add(base)
                term_text = t(base)
                def_text = t(def_key)
                terms.append((term_text, def_text))

    terms.sort(key=lambda x: x[0].lower())
    return terms


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------

st.title(t("doc.title"))

# ---------------------------------------------------------------------------
# Section selector
# ---------------------------------------------------------------------------

section = st.selectbox(
    t("doc.select"),
    options=[
        t("doc.iso2602"),
        t("doc.iso16269"),
        t("doc.comparison"),
        t("doc.glossary"),
    ],
    key="doc_section",
)

# ===================================================================
# ISO 2602 -- confidence intervals
# ===================================================================

if section == t("doc.iso2602"):
    st.subheader(t("doc.principle"))
    st.write(t("doc.ci_principle"))

    st.markdown("---")
    st.subheader(t("doc.formulas"))

    # Case 1 -- sigma known
    st.markdown(f"**{t('doc.case_sigma_known')}**")
    st.latex(r"\bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}")

    # Case 2 -- sigma unknown
    st.markdown(f"**{t('doc.case_sigma_unknown')}**")
    st.latex(r"\bar{x} \pm t_{n-1,\;\alpha/2} \cdot \frac{s}{\sqrt{n}}")

    # Where section
    st.markdown(f"**{t('doc.where')}**")
    st.markdown(
        f"- $\\bar{{x}}$ : {t('stats.mean')}\n"
        f"- $s$ : {t('stats.std')}\n"
        f"- $n$ : {t('stats.n')}\n"
        f"- $t_{{n-1,\\;\\alpha/2}}$ : {t('glossary.t_value')}\n"
        f"- $z_{{\\alpha/2}}$ : {t('glossary.confidence_level')}\n"
        f"- $\\sigma$ : {t('stats.std')}\n"
    )

# ===================================================================
# ISO 16269-6 -- tolerance intervals
# ===================================================================

elif section == t("doc.iso16269"):
    st.subheader(t("doc.principle"))
    st.write(t("doc.ti_principle"))

    st.markdown("---")
    st.subheader(t("doc.formulas"))

    st.latex(r"\bar{x} \pm k(n,\;p,\;1-\alpha) \cdot s")

    # Where section
    st.markdown(f"**{t('doc.where')}**")
    st.markdown(
        f"- $\\bar{{x}}$ : {t('stats.mean')}\n"
        f"- $s$ : {t('stats.std')}\n"
        f"- $n$ : {t('stats.n')}\n"
        f"- $k$ : {t('glossary.k_factor')} -- {t('glossary.k_factor_def')}\n"
        f"- $p$ : {t('glossary.coverage')} -- {t('glossary.coverage_def')}\n"
        f"- $1 - \\alpha$ : {t('glossary.confidence_level')}\n"
    )

# ===================================================================
# Comparison CI vs TI
# ===================================================================

elif section == t("doc.comparison"):
    st.subheader(t("comp.key_differences"))

    comp_df = pd.DataFrame(
        {
            t("comp.aspect"): [
                t("comp.objective"),
                t("comp.formula"),
                t("comp.typical_use"),
            ],
            t("comp.ci_label"): [
                t("comp.ci_objective"),
                t("comp.ci_formula"),
                t("comp.ci_use"),
            ],
            t("comp.ti_label"): [
                t("comp.ti_objective"),
                t("comp.ti_formula"),
                t("comp.ti_use"),
            ],
        }
    )
    st.table(comp_df)

    st.markdown("---")

    # CI formula
    st.markdown(f"**{t('comp.ci_label')}**")
    st.latex(r"\bar{x} \pm t_{n-1,\;\alpha/2} \cdot \frac{s}{\sqrt{n}}")

    # TI formula
    st.markdown(f"**{t('comp.ti_label')}**")
    st.latex(r"\bar{x} \pm k(n,\;p,\;1-\alpha) \cdot s")

# ===================================================================
# Glossary
# ===================================================================

elif section == t("doc.glossary"):
    terms = _get_glossary_terms()

    if terms:
        glossary_df = pd.DataFrame(
            terms,
            columns=[t("comp.aspect"), t("common.interpretation")],
        )
        st.table(glossary_df)
    else:
        st.info(t("common.no_data"))
