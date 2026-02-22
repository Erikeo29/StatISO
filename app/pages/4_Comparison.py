"""Page 4 -- CI vs TI comparison and decision helper."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import streamlit as st

from core.iso2602 import ConfidenceInterval
from core.iso16269 import ToleranceInterval
from data.report import ReportGenerator
from i18n import t

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------

if not st.session_state.get("authentication_status"):
    st.warning("Please log in from the Home page.")
    st.stop()

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------

st.title(t("comp.title"))

# ---------------------------------------------------------------------------
# Data check
# ---------------------------------------------------------------------------

if "data" not in st.session_state or st.session_state["data"] is None:
    st.warning(t("common.no_data"))
    st.stop()

data: np.ndarray = st.session_state["data"]

if len(data) < 2:
    st.warning(t("common.min_samples").format(n=2))
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar parameters
# ---------------------------------------------------------------------------

with st.sidebar:
    st.subheader(t("comp.title"))

    confidence = st.select_slider(
        t("sidebar.confidence"),
        options=[0.90, 0.95, 0.99],
        value=0.95,
        key="comp_confidence",
    )

    coverage = st.select_slider(
        t("sidebar.coverage"),
        options=[0.90, 0.95, 0.99],
        value=0.95,
        key="comp_coverage",
    )

# ---------------------------------------------------------------------------
# Calculate both intervals
# ---------------------------------------------------------------------------

if st.button(t("comp.calculate"), type="primary"):
    try:
        ci = ConfidenceInterval(data, confidence=confidence)
        ci_lo, ci_hi = ci.bilateral_interval()

        ti = ToleranceInterval(data, confidence=confidence, coverage=coverage)
        ti_lo, ti_hi = ti.bilateral_interval()

        mean_val = float(np.mean(data))
        ci_width = ci_hi - ci_lo
        ti_width = ti_hi - ti_lo

        # -- Store results in session for display below the button --
        st.session_state["comp_results"] = {
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
            "ti_lo": ti_lo,
            "ti_hi": ti_hi,
            "mean": mean_val,
            "ci_width": ci_width,
            "ti_width": ti_width,
        }
    except Exception as exc:
        st.error(f"{t('common.error')}: {exc}")

# ---------------------------------------------------------------------------
# Display results
# ---------------------------------------------------------------------------

if "comp_results" in st.session_state:
    res = st.session_state["comp_results"]

    st.subheader(t("comp.results"))

    # -- Two-column layout: CI left, TI right --
    col_ci, col_ti = st.columns(2)

    with col_ci:
        st.markdown(f"**{t('comp.ci_label')}**")
        st.metric(t("comp.lower"), f"{res['ci_lo']:.4f}")
        st.metric(t("comp.upper"), f"{res['ci_hi']:.4f}")
        st.metric(t("comp.width"), f"{res['ci_width']:.4f}")

    with col_ti:
        st.markdown(f"**{t('comp.ti_label')}**")
        st.metric(t("comp.lower"), f"{res['ti_lo']:.4f}")
        st.metric(t("comp.upper"), f"{res['ti_hi']:.4f}")
        st.metric(t("comp.width"), f"{res['ti_width']:.4f}")

    # -- Comparative table --
    st.markdown("---")

    comp_df = pd.DataFrame(
        {
            t("comp.type"): [t("comp.ci_label"), t("comp.ti_label")],
            t("comp.lower"): [
                f"{res['ci_lo']:.4f}",
                f"{res['ti_lo']:.4f}",
            ],
            t("stats.mean"): [
                f"{res['mean']:.4f}",
                f"{res['mean']:.4f}",
            ],
            t("comp.upper"): [
                f"{res['ci_hi']:.4f}",
                f"{res['ti_hi']:.4f}",
            ],
            t("comp.width"): [
                f"{res['ci_width']:.4f}",
                f"{res['ti_width']:.4f}",
            ],
        }
    )
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # -- Comparison plot --
    fig = ReportGenerator.comparison_plot(
        ci_lower=res["ci_lo"],
        ci_upper=res["ci_hi"],
        ti_lower=res["ti_lo"],
        ti_upper=res["ti_hi"],
        mean=res["mean"],
        data=data,
        ci_label=t("comp.ci_label"),
        ti_label=t("comp.ti_label"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # -- Key differences table --
    st.markdown("---")
    st.subheader(t("comp.key_differences"))

    diff_df = pd.DataFrame(
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
    st.table(diff_df)

# ---------------------------------------------------------------------------
# Decision helper
# ---------------------------------------------------------------------------

st.markdown("---")
st.subheader(t("comp.help_title"))

objective = st.radio(
    t("comp.q_objective"),
    options=[
        t("comp.obj_mean"),
        t("comp.obj_specs"),
        t("comp.obj_lot"),
        t("comp.obj_capability"),
    ],
    key="comp_objective_radio",
)

# Map selection to recommendation
if objective == t("comp.obj_mean"):
    st.success(t("comp.rec_ci"))
elif objective == t("comp.obj_specs"):
    st.success(t("comp.rec_ti"))
elif objective == t("comp.obj_lot"):
    st.success(t("comp.rec_both"))
elif objective == t("comp.obj_capability"):
    st.success(t("comp.rec_ti"))
