"""Page 1 -- Confidence interval for the mean (ISO 2602:1980)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats as sp_stats

from core.constants import get_t_value
from core.iso2602 import ConfidenceInterval
from data.handler import DataHandler
from data.report import ReportGenerator
from i18n import t

# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------

if not st.session_state.get("authentication_status"):
    st.warning("Please log in from the Home page.")
    st.stop()

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.set_page_config(page_title=t("nav.ci"), page_icon="\U0001F4CA", layout="wide")
st.title(t("ci.title"))

# ---------------------------------------------------------------------------
# Data guard
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
    confidence_level = st.selectbox(
        t("sidebar.confidence"),
        options=[0.90, 0.95, 0.99],
        index=1,
        format_func=lambda x: f"{int(x * 100)} %",
    )

    interval_type = st.radio(
        t("ci.type"),
        options=[t("ci.bilateral"), t("ci.unilateral")],
    )

    side = "lower"
    if interval_type == t("ci.unilateral"):
        side_label = st.radio(
            t("ci.side"),
            options=[t("ci.lower"), t("ci.upper")],
        )
        side = "lower" if side_label == t("ci.lower") else "upper"

# ---------------------------------------------------------------------------
# Calculation
# ---------------------------------------------------------------------------

if st.button(t("ci.calculate"), type="primary"):
    ci = ConfidenceInterval(data, confidence=confidence_level)
    stats_dict = ci.get_statistics()

    # Resolve the t-value used for display
    is_bilateral = interval_type == t("ci.bilateral")
    t_val = get_t_value(ci.df, confidence_level, bilateral=is_bilateral)
    if t_val is None:
        if is_bilateral:
            t_val = float(sp_stats.t.ppf((1 + confidence_level) / 2, ci.df))
        else:
            t_val = float(sp_stats.t.ppf(confidence_level, ci.df))

    # -------------------------------------------------------------------
    # Results
    # -------------------------------------------------------------------

    st.subheader(t("ci.results"))

    if is_bilateral:
        lower, upper = ci.bilateral_interval()
        margin = t_val * ci.se

        col_a, col_b, col_c = st.columns(3)
        col_a.metric(t("ci.lower_bound"), f"{lower:.4f}")
        col_b.metric(t("ci.upper_bound"), f"{upper:.4f}")
        col_c.metric(t("ci.margin"), f"{margin:.4f}")

        # Interpretation
        st.info(
            t("ci.interpretation").format(
                conf=int(confidence_level * 100),
                lower=f"{lower:.4f}",
                upper=f"{upper:.4f}",
            )
        )

        # Distribution plot with CI bounds
        fig = ReportGenerator.distribution_plot(
            data,
            ci.mean,
            ci.std,
            lower=lower,
            upper=upper,
            title=t("ci.title"),
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        bound = ci.unilateral_interval(side=side)
        margin = t_val * ci.se

        col_a, col_b = st.columns(2)
        if side == "lower":
            col_a.metric(t("ci.lower_bound"), f"{bound:.4f}")
            col_b.metric(t("ci.margin"), f"{margin:.4f}")
            st.info(
                t("ci.interpretation_lower").format(
                    conf=int(confidence_level * 100),
                    bound=f"{bound:.4f}",
                )
            )
            fig = ReportGenerator.distribution_plot(
                data,
                ci.mean,
                ci.std,
                lower=bound,
                title=t("ci.title"),
            )
        else:
            col_a.metric(t("ci.upper_bound"), f"{bound:.4f}")
            col_b.metric(t("ci.margin"), f"{margin:.4f}")
            st.info(
                t("ci.interpretation_upper").format(
                    conf=int(confidence_level * 100),
                    bound=f"{bound:.4f}",
                )
            )
            fig = ReportGenerator.distribution_plot(
                data,
                ci.mean,
                ci.std,
                upper=bound,
                title=t("ci.title"),
            )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------
    # Calculation details
    # -------------------------------------------------------------------

    with st.expander(t("ci.details")):
        details = {
            t("stats.n"): ci.n,
            t("stats.mean"): f"{ci.mean:.6f}",
            t("stats.std"): f"{ci.std:.6f}",
            t("stats.se"): f"{ci.se:.6f}",
            t("stats.df"): ci.df,
            t("ci.t_value"): f"{t_val:.4f}",
            t("ci.margin"): f"{margin:.6f}",
            t("sidebar.confidence"): f"{int(confidence_level * 100)} %",
        }
        df_details = pd.DataFrame(
            list(details.items()),
            columns=["Parameter", "Value"],
        )
        st.dataframe(df_details, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------
    # Export
    # -------------------------------------------------------------------

    results_export = {
        "n": ci.n,
        "mean": ci.mean,
        "std": ci.std,
        "se": ci.se,
        "df": ci.df,
        "confidence": confidence_level,
        "t_value": t_val,
        "margin": margin,
    }
    if is_bilateral:
        results_export["lower_bound"] = lower
        results_export["upper_bound"] = upper
    else:
        results_export["bound"] = bound
        results_export["side"] = side

    excel_buf = DataHandler.export_to_excel(results_export, data)
    st.download_button(
        t("ci.export"),
        data=excel_buf,
        file_name="ci_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
