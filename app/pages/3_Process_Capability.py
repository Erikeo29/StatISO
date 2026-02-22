"""Page 3 -- Process capability analysis (Cp, Cpk, Cpl, Cpu)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
import streamlit as st

from core.capability import ProcessCapability
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

st.set_page_config(
    page_title=t("nav.capability"), page_icon="\U0001F4CA", layout="wide"
)
st.title(t("cap.title"))

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
# Specification limits input
# ---------------------------------------------------------------------------

mean_val = float(np.mean(data))
std_val = float(np.std(data, ddof=1))

col_lsl, col_usl = st.columns(2)

with col_lsl:
    use_lsl = st.checkbox(t("cap.lsl"), value=True, key="cap_use_lsl")
    lsl_value = None
    if use_lsl:
        lsl_value = st.number_input(
            t("cap.lsl"),
            value=round(mean_val - 3 * std_val, 4),
            format="%.4f",
            key="cap_lsl_input",
            label_visibility="collapsed",
        )

with col_usl:
    use_usl = st.checkbox(t("cap.usl"), value=True, key="cap_use_usl")
    usl_value = None
    if use_usl:
        usl_value = st.number_input(
            t("cap.usl"),
            value=round(mean_val + 3 * std_val, 4),
            format="%.4f",
            key="cap_usl_input",
            label_visibility="collapsed",
        )

# ---------------------------------------------------------------------------
# Calculate button
# ---------------------------------------------------------------------------

if st.button(t("cap.calculate"), type="primary"):
    if lsl_value is None and usl_value is None:
        st.error(t("common.error"))
        st.stop()

    try:
        pc = ProcessCapability(data, lsl=lsl_value, usl=usl_value)
    except ValueError as exc:
        st.error(f"{t('common.error')}: {exc}")
        st.stop()

    indices = pc.compute()
    interpretation = pc.get_interpretation()

    # -------------------------------------------------------------------
    # Results -- capability indices
    # -------------------------------------------------------------------

    st.subheader(t("cap.results"))

    # Main metrics row
    metric_cols = st.columns(4)

    if "Cp" in indices:
        metric_cols[0].metric(t("cap.cp"), f"{indices['Cp']:.4f}")
    if "Cpk" in indices:
        metric_cols[1].metric(t("cap.cpk"), f"{indices['Cpk']:.4f}")
    if "Cpl" in indices:
        metric_cols[2].metric(t("cap.cpl"), f"{indices['Cpl']:.4f}")
    if "Cpu" in indices:
        metric_cols[3].metric(t("cap.cpu"), f"{indices['Cpu']:.4f}")

    # Out-of-spec percentage
    st.metric(
        t("cap.pct_out"),
        f"{indices.get('pct_out_of_spec', 0):.4f} %",
    )

    # -------------------------------------------------------------------
    # Interpretation with colour-coded feedback
    # -------------------------------------------------------------------

    st.subheader(t("common.interpretation"))

    level = interpretation["level"]

    if level == "excellent":
        st.success(t("cap.excellent"))
        st.success(t("cap.interpretation_capable"))
    elif level == "capable":
        st.success(t("cap.capable"))
        st.success(t("cap.interpretation_capable"))
    elif level == "marginal":
        st.warning(t("cap.marginal"))
        st.warning(t("cap.interpretation_incapable"))
    else:
        st.error(t("cap.incapable"))
        st.error(t("cap.interpretation_incapable"))

    # -------------------------------------------------------------------
    # Capability plot
    # -------------------------------------------------------------------

    fig = ReportGenerator.capability_plot(
        data,
        mean_val,
        std_val,
        lsl=lsl_value,
        usl=usl_value,
        title=t("cap.title"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------
    # Details expander
    # -------------------------------------------------------------------

    with st.expander(t("ci.details")):
        detail_rows = {
            t("stats.n"): len(data),
            t("stats.mean"): f"{mean_val:.6f}",
            t("stats.std"): f"{std_val:.6f}",
        }
        if lsl_value is not None:
            detail_rows[t("cap.lsl")] = f"{lsl_value:.4f}"
        if usl_value is not None:
            detail_rows[t("cap.usl")] = f"{usl_value:.4f}"
        for key in ("Cp", "Cpk", "Cpl", "Cpu"):
            if key in indices:
                detail_rows[key] = f"{indices[key]:.4f}"
        if "pct_below_lsl" in indices:
            detail_rows["% < LSL"] = f"{indices['pct_below_lsl']:.4f} %"
        if "pct_above_usl" in indices:
            detail_rows["% > USL"] = f"{indices['pct_above_usl']:.4f} %"
        detail_rows[t("cap.pct_out")] = (
            f"{indices.get('pct_out_of_spec', 0):.4f} %"
        )

        df_details = pd.DataFrame(
            list(detail_rows.items()),
            columns=["Parameter", "Value"],
        )
        st.dataframe(df_details, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------
    # Export
    # -------------------------------------------------------------------

    results_export = {
        "n": len(data),
        "mean": mean_val,
        "std": std_val,
    }
    if lsl_value is not None:
        results_export["LSL"] = lsl_value
    if usl_value is not None:
        results_export["USL"] = usl_value
    results_export.update(indices)

    excel_buf = DataHandler.export_to_excel(results_export, data)
    st.download_button(
        t("ci.export"),
        data=excel_buf,
        file_name="capability_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
