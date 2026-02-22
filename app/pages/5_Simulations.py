"""Page 5 -- Interactive pedagogical simulations."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import streamlit as st

from core.iso2602 import ConfidenceInterval
from core.iso16269 import ToleranceInterval
from core.capability import ProcessCapability
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

st.title(t("sim.title"))

# ---------------------------------------------------------------------------
# Simulation selector
# ---------------------------------------------------------------------------

simulation = st.selectbox(
    t("sim.select"),
    options=[
        t("sim.ic_vs_it"),
        t("sim.sample_size"),
        t("sim.capability"),
        t("sim.coverage"),
    ],
    key="sim_selector",
)

# ===================================================================
# Simulation 1: CI vs TI comparison
# ===================================================================

if simulation == t("sim.ic_vs_it"):
    st.markdown("---")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        n_sim = st.slider(
            t("sim.n"),
            min_value=10,
            max_value=200,
            value=50,
            step=5,
            key="sim1_n",
        )

    with col_b:
        confidence_sim = st.select_slider(
            t("sim.confidence"),
            options=[0.90, 0.95, 0.99],
            value=0.95,
            key="sim1_conf",
        )

    with col_c:
        coverage_sim = st.select_slider(
            t("sim.coverage_prop"),
            options=[0.90, 0.95, 0.99],
            value=0.95,
            key="sim1_cov",
        )

    if st.button(t("sim.run"), key="sim1_run", type="primary"):
        rng = np.random.default_rng()
        sim_data = rng.normal(loc=100, scale=5, size=n_sim)

        ci = ConfidenceInterval(sim_data, confidence=confidence_sim)
        ci_lo, ci_hi = ci.bilateral_interval()

        ti = ToleranceInterval(
            sim_data, confidence=confidence_sim, coverage=coverage_sim
        )
        ti_lo, ti_hi = ti.bilateral_interval()

        mean_val = float(np.mean(sim_data))
        std_val = float(np.std(sim_data, ddof=1))

        # Distribution plot with both sets of bounds
        fig = ReportGenerator.distribution_plot(
            sim_data,
            mean_val,
            std_val,
            lower=ci_lo,
            upper=ci_hi,
            title=t("sim.ic_vs_it"),
        )
        # Add TI bounds as additional vertical lines
        fig.add_vline(
            x=ti_lo,
            line_dash="dot",
            line_color="orange",
            annotation_text=f"TI Low={ti_lo:.2f}",
        )
        fig.add_vline(
            x=ti_hi,
            line_dash="dot",
            line_color="orange",
            annotation_text=f"TI High={ti_hi:.2f}",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(t("comp.ci_label"), f"[{ci_lo:.3f}, {ci_hi:.3f}]")
        with col2:
            st.metric(t("comp.ti_label"), f"[{ti_lo:.3f}, {ti_hi:.3f}]")

        st.info(t("sim.obs_ic_it"))

# ===================================================================
# Simulation 2: Sample size impact
# ===================================================================

elif simulation == t("sim.sample_size"):
    st.markdown("---")

    if st.button(t("sim.run"), key="sim2_run", type="primary"):
        n_values = [5, 10, 15, 20, 30, 50, 100, 200]
        ci_widths: list[float] = []
        ti_widths: list[float] = []

        rng = np.random.default_rng(42)

        for n in n_values:
            sim_data = rng.normal(loc=100, scale=5, size=n)

            ci = ConfidenceInterval(sim_data, confidence=0.95)
            ci_lo, ci_hi = ci.bilateral_interval()
            ci_widths.append(ci_hi - ci_lo)

            try:
                ti = ToleranceInterval(
                    sim_data, confidence=0.95, coverage=0.95
                )
                ti_lo, ti_hi = ti.bilateral_interval()
                ti_widths.append(ti_hi - ti_lo)
            except ValueError:
                # k-factor not available for this n -- use last valid width
                ti_widths.append(float("nan"))

        fig = ReportGenerator.sample_size_effect_plot(
            n_values=n_values,
            ci_widths=ci_widths,
            ti_widths=ti_widths,
            ci_label=t("comp.ci_label"),
            ti_label=t("comp.ti_label"),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(t("sim.obs_sample"))

# ===================================================================
# Simulation 3: Capability analysis
# ===================================================================

elif simulation == t("sim.capability"):
    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        process_mean = st.number_input(
            t("sim.process_mean"),
            value=100.0,
            step=1.0,
            key="sim3_mean",
        )
        process_std = st.number_input(
            t("sim.process_std"),
            value=5.0,
            min_value=0.1,
            step=0.5,
            key="sim3_std",
        )

    with col_b:
        lsl = st.number_input(
            t("sim.lsl"),
            value=85.0,
            step=1.0,
            key="sim3_lsl",
        )
        usl = st.number_input(
            t("sim.usl"),
            value=115.0,
            step=1.0,
            key="sim3_usl",
        )

    if st.button(t("sim.run"), key="sim3_run", type="primary"):
        if lsl >= usl:
            st.error(f"{t('common.error')}: LSL >= USL")
        else:
            rng = np.random.default_rng()
            sim_data = rng.normal(loc=process_mean, scale=process_std, size=200)

            pc = ProcessCapability(sim_data, lsl=lsl, usl=usl)
            results = pc.compute()
            interp = pc.get_interpretation()

            mean_val = float(np.mean(sim_data))
            std_val = float(np.std(sim_data, ddof=1))

            # Capability plot
            fig = ReportGenerator.capability_plot(
                sim_data,
                mean_val,
                std_val,
                lsl=lsl,
                usl=usl,
                title=t("sim.capability"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Metrics
            cols = st.columns(4)
            if "Cp" in results:
                cols[0].metric(t("cap.cp"), f"{results['Cp']:.3f}")
            if "Cpk" in results:
                cols[1].metric(t("cap.cpk"), f"{results['Cpk']:.3f}")
            if "Cpl" in results:
                cols[2].metric(t("cap.cpl"), f"{results['Cpl']:.3f}")
            if "Cpu" in results:
                cols[3].metric(t("cap.cpu"), f"{results['Cpu']:.3f}")

            # Interpretation
            level = interp["level"]
            if level == "excellent":
                st.success(t("cap.excellent"))
            elif level == "capable":
                st.success(t("cap.capable"))
            elif level == "marginal":
                st.warning(t("cap.marginal"))
            else:
                st.error(t("cap.incapable"))

            if results.get("pct_out_of_spec") is not None:
                st.metric(
                    t("cap.pct_out"),
                    f"{results['pct_out_of_spec']:.4f}%",
                )

# ===================================================================
# Simulation 4: CI coverage
# ===================================================================

elif simulation == t("sim.coverage"):
    st.markdown("---")

    if st.button(t("sim.launch_coverage"), key="sim4_run", type="primary"):
        true_mean = 100.0
        n_sample = 30
        n_simulations = 100
        confidence_cov = 0.95

        rng = np.random.default_rng()
        intervals: list[tuple[float, float]] = []
        count_contains = 0

        for _ in range(n_simulations):
            sim_data = rng.normal(loc=true_mean, scale=5, size=n_sample)
            ci = ConfidenceInterval(sim_data, confidence=confidence_cov)
            lo, hi = ci.bilateral_interval()
            intervals.append((lo, hi))
            if lo <= true_mean <= hi:
                count_contains += 1

        # Show first 50 intervals
        fig = ReportGenerator.coverage_simulation_plot(
            intervals[:50],
            true_mean=true_mean,
            title=t("sim.coverage"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Coverage count
        st.metric(
            t("sim.coverage"),
            t("sim.coverage_result").format(n=count_contains),
        )

        st.info(t("sim.obs_coverage"))
