"""Page 2 -- Statistical tolerance interval (ISO 16269-6:2014)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import streamlit as st

from core.constants import get_k_factor
from core.iso16269 import ToleranceInterval
from core.normality import check_normality, remove_outliers
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

st.set_page_config(page_title=t("nav.ti"), page_icon="\U0001F4CA", layout="wide")
st.title(t("ti.title"))

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
        key="ti_confidence",
    )

    coverage_level = st.selectbox(
        t("sidebar.coverage"),
        options=[0.90, 0.95, 0.99],
        index=1,
        format_func=lambda x: f"{int(x * 100)} %",
        key="ti_coverage",
    )

    interval_type = st.radio(
        t("ti.type"),
        options=[t("ti.bilateral"), t("ti.unilateral")],
        key="ti_type",
    )

    side = "lower"
    if interval_type == t("ti.unilateral"):
        side_label = st.radio(
            t("ti.side"),
            options=[t("ti.lower"), t("ti.upper")],
            key="ti_side",
        )
        side = "lower" if side_label == t("ti.lower") else "upper"

# ---------------------------------------------------------------------------
# Normality tests (always displayed)
# ---------------------------------------------------------------------------

st.subheader(t("ti.normality"))

normality_results = check_normality(data)

# Build a summary table from the normality test results
norm_rows = []

if "shapiro" in normality_results:
    res = normality_results["shapiro"]
    norm_rows.append({
        t("common.table"): t("ti.shapiro"),
        "Statistic": f"{res['statistic']:.4f}",
        "p-value": f"{res['p_value']:.4f}",
        "Verdict": t("ti.is_normal") if res["is_normal"] else t("ti.not_normal"),
    })

if "anderson" in normality_results:
    res = normality_results["anderson"]
    cv_5 = res["critical_values"].get("5%", "N/A")
    norm_rows.append({
        t("common.table"): t("ti.anderson"),
        "Statistic": f"{res['statistic']:.4f}",
        "p-value": f"cv(5%)={cv_5}",
        "Verdict": t("ti.is_normal") if res["is_normal"] else t("ti.not_normal"),
    })

if "ks" in normality_results:
    res = normality_results["ks"]
    norm_rows.append({
        t("common.table"): t("ti.ks_test"),
        "Statistic": f"{res['statistic']:.4f}",
        "p-value": f"{res['p_value']:.4f}",
        "Verdict": t("ti.is_normal") if res["is_normal"] else t("ti.not_normal"),
    })

if "jarque_bera" in normality_results:
    res = normality_results["jarque_bera"]
    norm_rows.append({
        t("common.table"): t("ti.jb_test"),
        "Statistic": f"{res['statistic']:.4f}",
        "p-value": f"{res['p_value']:.4f}",
        "Verdict": t("ti.is_normal") if res["is_normal"] else t("ti.not_normal"),
    })

if norm_rows:
    st.dataframe(
        pd.DataFrame(norm_rows),
        use_container_width=True,
        hide_index=True,
    )

# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

st.subheader(t("ti.outliers"))

cleaned_data, outlier_indices = remove_outliers(data, method="iqr", threshold=1.5)

if len(outlier_indices) > 0:
    st.warning(t("ti.n_outliers").format(n=len(outlier_indices)))
    outlier_values = data[outlier_indices]
    st.dataframe(
        pd.DataFrame({
            "Index": outlier_indices,
            "Value": outlier_values,
        }),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.success(t("ti.no_outliers"))

# ---------------------------------------------------------------------------
# Calculate button
# ---------------------------------------------------------------------------

st.markdown("---")

if st.button(t("ti.calculate"), type="primary"):
    is_bilateral = interval_type == t("ti.bilateral")

    try:
        ti = ToleranceInterval(
            data,
            confidence=confidence_level,
            coverage=coverage_level,
        )
    except ValueError as exc:
        st.error(f"{t('common.error')}: {exc}")
        st.stop()

    # Resolve k-factor for display
    k_val = get_k_factor(
        ti.n,
        confidence_level,
        coverage_level,
        bilateral=is_bilateral,
    )
    if k_val is None:
        st.error(
            f"{t('common.error')}: k-factor not available for n={ti.n}, "
            f"confidence={confidence_level}, coverage={coverage_level}"
        )
        st.stop()

    # -------------------------------------------------------------------
    # Results
    # -------------------------------------------------------------------

    st.subheader(t("ti.results"))

    if is_bilateral:
        lower, upper = ti.bilateral_interval()

        col_a, col_b, col_c = st.columns(3)
        col_a.metric(t("ti.lower_bound"), f"{lower:.4f}")
        col_b.metric(t("ti.upper_bound"), f"{upper:.4f}")
        col_c.metric(t("ti.k_factor"), f"{k_val:.4f}")

        # Interpretation
        st.info(
            t("ti.interpretation").format(
                conf=int(confidence_level * 100),
                cov=int(coverage_level * 100),
            )
        )

        # Distribution plot with TI bounds
        fig = ReportGenerator.distribution_plot(
            data,
            ti.mean,
            ti.std,
            lower=lower,
            upper=upper,
            title=t("ti.title"),
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        bound = ti.unilateral_interval(side=side)

        col_a, col_b = st.columns(2)
        if side == "lower":
            col_a.metric(t("ti.lower_bound"), f"{bound:.4f}")
        else:
            col_a.metric(t("ti.upper_bound"), f"{bound:.4f}")
        col_b.metric(t("ti.k_factor"), f"{k_val:.4f}")

        # Interpretation
        st.info(
            t("ti.interpretation").format(
                conf=int(confidence_level * 100),
                cov=int(coverage_level * 100),
            )
        )

        # Distribution plot with single TI bound
        fig_kwargs = {"lower": bound} if side == "lower" else {"upper": bound}
        fig = ReportGenerator.distribution_plot(
            data,
            ti.mean,
            ti.std,
            title=t("ti.title"),
            **fig_kwargs,
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------
    # Calculation details
    # -------------------------------------------------------------------

    with st.expander(t("ti.details")):
        ti_stats = ti.get_statistics()
        details = {
            t("stats.n"): ti_stats["n"],
            t("stats.mean"): f"{ti_stats['mean']:.6f}",
            t("stats.std"): f"{ti_stats['std']:.6f}",
            t("stats.variance"): f"{ti_stats['variance']:.6f}",
            t("stats.min"): f"{ti_stats['min']:.6f}",
            t("stats.max"): f"{ti_stats['max']:.6f}",
            t("sidebar.confidence"): f"{int(confidence_level * 100)} %",
            t("sidebar.coverage"): f"{int(coverage_level * 100)} %",
            t("ti.k_factor"): f"{k_val:.4f}",
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
        "n": ti.n,
        "mean": ti.mean,
        "std": ti.std,
        "confidence": confidence_level,
        "coverage": coverage_level,
        "k_factor": k_val,
    }
    if is_bilateral:
        results_export["lower_bound"] = lower
        results_export["upper_bound"] = upper
    else:
        results_export["bound"] = bound
        results_export["side"] = side

    excel_buf = DataHandler.export_to_excel(results_export, data)
    st.download_button(
        t("ti.export"),
        data=excel_buf,
        file_name="ti_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
