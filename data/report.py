"""Plotly-based chart generator for StatISO pages.

This module is pure Plotly -- it does NOT import Streamlit,
so charts can be tested and rendered outside the Streamlit runtime.
"""

import numpy as np
import plotly.graph_objects as go
from scipy import stats
from typing import Optional


class ReportGenerator:
    """Interactive Plotly chart factory for StatISO."""

    # ------------------------------------------------------------------
    # Distribution analysis
    # ------------------------------------------------------------------

    @staticmethod
    def distribution_plot(
        data: np.ndarray,
        mean: float,
        std: float,
        lower: Optional[float] = None,
        upper: Optional[float] = None,
        title: str = "Distribution",
    ) -> go.Figure:
        """Histogram + fitted normal curve + optional limit lines.

        Parameters
        ----------
        data : np.ndarray
            1-D array of sample values.
        mean, std : float
            Distribution parameters for the normal overlay.
        lower, upper : float, optional
            Vertical reference lines (e.g. spec limits).
        title : str
            Chart title.
        """
        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=data,
            name="Data",
            nbinsx=20,
            marker_color="lightblue",
            opacity=0.7,
            histnorm="probability density",
        ))

        x_range = np.linspace(data.min() - 2 * std, data.max() + 2 * std, 200)
        y_norm = stats.norm.pdf(x_range, mean, std)
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_norm,
            mode="lines",
            name="Normal",
            line=dict(color="red", width=2),
        ))

        fig.add_vline(
            x=mean, line_dash="solid", line_color="blue",
            annotation_text=f"Mean={mean:.3f}",
        )

        if lower is not None:
            fig.add_vline(
                x=lower, line_dash="dash", line_color="green",
                annotation_text=f"Lower={lower:.3f}",
            )
        if upper is not None:
            fig.add_vline(
                x=upper, line_dash="dash", line_color="green",
                annotation_text=f"Upper={upper:.3f}",
            )

        fig.update_layout(
            title=title,
            xaxis_title="Value",
            yaxis_title="Density",
            template="plotly_white",
            showlegend=True,
        )
        return fig

    # ------------------------------------------------------------------
    # Q-Q plot
    # ------------------------------------------------------------------

    @staticmethod
    def qq_plot(data: np.ndarray, title: str = "Q-Q Plot") -> go.Figure:
        """Normal Q-Q plot.

        Parameters
        ----------
        data : np.ndarray
            1-D sample array.
        title : str
            Chart title.
        """
        sorted_data = np.sort(data)
        n = len(data)
        theoretical = stats.norm.ppf(np.linspace(0.5 / n, 1 - 0.5 / n, n))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=theoretical,
            y=sorted_data,
            mode="markers",
            name="Data",
            marker=dict(color="blue", size=8),
        ))

        # Reference line: y = mean + std * x
        slope = np.std(data, ddof=1)
        intercept = np.mean(data)
        fig.add_trace(go.Scatter(
            x=theoretical,
            y=intercept + slope * theoretical,
            mode="lines",
            name="Reference",
            line=dict(color="red", dash="dash"),
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Theoretical quantiles",
            yaxis_title="Sample quantiles",
            template="plotly_white",
        )
        return fig

    # ------------------------------------------------------------------
    # Box plot
    # ------------------------------------------------------------------

    @staticmethod
    def box_plot(data: np.ndarray, title: str = "Box Plot") -> go.Figure:
        """Box plot with outlier markers.

        Parameters
        ----------
        data : np.ndarray
            1-D sample array.
        title : str
            Chart title.
        """
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=data,
            name="Data",
            boxpoints="outliers",
            marker_color="lightseagreen",
        ))
        fig.update_layout(
            title=title,
            yaxis_title="Value",
            template="plotly_white",
        )
        return fig

    # ------------------------------------------------------------------
    # Process capability
    # ------------------------------------------------------------------

    @staticmethod
    def capability_plot(
        data: np.ndarray,
        mean: float,
        std: float,
        lsl: Optional[float] = None,
        usl: Optional[float] = None,
        title: str = "Process Capability",
    ) -> go.Figure:
        """Distribution with specification limits for capability analysis.

        Parameters
        ----------
        data : np.ndarray
            1-D sample array.
        mean, std : float
            Distribution parameters.
        lsl, usl : float, optional
            Lower / upper specification limits.
        title : str
            Chart title.
        """
        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=data,
            name="Data",
            nbinsx=25,
            marker_color="lightblue",
            opacity=0.7,
            histnorm="probability density",
        ))

        x_min = min(data.min(), lsl or data.min()) - 3 * std
        x_max = max(data.max(), usl or data.max()) + 3 * std
        x_range = np.linspace(x_min, x_max, 300)
        y_norm = stats.norm.pdf(x_range, mean, std)
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_norm,
            mode="lines",
            name="Normal",
            line=dict(color="blue", width=2),
        ))

        if lsl is not None:
            fig.add_vline(
                x=lsl, line_dash="dash", line_color="red",
                annotation_text=f"LSL={lsl:.3f}",
            )
        if usl is not None:
            fig.add_vline(
                x=usl, line_dash="dash", line_color="red",
                annotation_text=f"USL={usl:.3f}",
            )
        fig.add_vline(
            x=mean, line_dash="solid", line_color="green",
            annotation_text=f"Mean={mean:.3f}",
        )

        fig.update_layout(
            title=title,
            xaxis_title="Value",
            yaxis_title="Density",
            template="plotly_white",
            showlegend=True,
        )
        return fig

    # ------------------------------------------------------------------
    # CI vs TI comparison
    # ------------------------------------------------------------------

    @staticmethod
    def comparison_plot(
        ci_lower: float,
        ci_upper: float,
        ti_lower: float,
        ti_upper: float,
        mean: float,
        data: np.ndarray,
        ci_label: str = "CI",
        ti_label: str = "TI",
    ) -> go.Figure:
        """Side-by-side confidence interval vs tolerance interval comparison.

        Parameters
        ----------
        ci_lower, ci_upper : float
            Confidence interval bounds.
        ti_lower, ti_upper : float
            Tolerance interval bounds.
        mean : float
            Sample mean.
        data : np.ndarray
            Raw data for scatter overlay.
        ci_label, ti_label : str
            Display labels for each interval.
        """
        fig = go.Figure()

        # CI range bar
        fig.add_trace(go.Scatter(
            x=[ci_lower, ci_upper],
            y=[ci_label, ci_label],
            mode="lines+markers",
            name=ci_label,
            line=dict(color="steelblue", width=6),
            marker=dict(size=12),
        ))

        # TI range bar
        fig.add_trace(go.Scatter(
            x=[ti_lower, ti_upper],
            y=[ti_label, ti_label],
            mode="lines+markers",
            name=ti_label,
            line=dict(color="forestgreen", width=6),
            marker=dict(size=12),
        ))

        # Mean marker
        fig.add_trace(go.Scatter(
            x=[mean, mean],
            y=[ci_label, ti_label],
            mode="markers",
            name="Mean",
            marker=dict(color="red", size=14, symbol="diamond"),
        ))

        # Data scatter
        fig.add_trace(go.Scatter(
            x=data,
            y=["Data"] * len(data),
            mode="markers",
            name="Data",
            marker=dict(color="grey", size=5, opacity=0.5),
        ))

        fig.update_layout(
            title=f"{ci_label} vs {ti_label}",
            xaxis_title="Value",
            template="plotly_white",
            height=350,
        )
        return fig

    # ------------------------------------------------------------------
    # CI coverage simulation
    # ------------------------------------------------------------------

    @staticmethod
    def coverage_simulation_plot(
        intervals: list[tuple[float, float]],
        true_mean: float,
        title: str = "CI Coverage Simulation",
    ) -> go.Figure:
        """Visualize CI coverage: green if contains true_mean, red otherwise.

        Parameters
        ----------
        intervals : list[tuple[float, float]]
            List of (lower, upper) interval bounds.
        true_mean : float
            True population mean for coverage assessment.
        title : str
            Chart title.
        """
        fig = go.Figure()

        for i, (lo, hi) in enumerate(intervals):
            contains = lo <= true_mean <= hi
            color = "green" if contains else "red"
            fig.add_trace(go.Scatter(
                x=[lo, hi],
                y=[i, i],
                mode="lines",
                line=dict(color=color, width=2),
                showlegend=False,
            ))

        fig.add_vline(
            x=true_mean, line_dash="dash", line_color="blue",
            annotation_text=f"\u03bc={true_mean}",
        )

        fig.update_layout(
            title=title,
            xaxis_title="Value",
            yaxis_title="Sample",
            template="plotly_white",
            height=max(400, len(intervals) * 8),
        )
        return fig

    # ------------------------------------------------------------------
    # Sample size effect
    # ------------------------------------------------------------------

    @staticmethod
    def sample_size_effect_plot(
        n_values: list[int],
        ci_widths: list[float],
        ti_widths: list[float],
        ci_label: str = "CI width",
        ti_label: str = "TI width",
    ) -> go.Figure:
        """Plot CI and TI width as a function of sample size.

        Parameters
        ----------
        n_values : list[int]
            Sample sizes evaluated.
        ci_widths, ti_widths : list[float]
            Corresponding interval widths.
        ci_label, ti_label : str
            Legend labels.
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=n_values,
            y=ci_widths,
            mode="lines+markers",
            name=ci_label,
            line=dict(color="steelblue"),
        ))
        fig.add_trace(go.Scatter(
            x=n_values,
            y=ti_widths,
            mode="lines+markers",
            name=ti_label,
            line=dict(color="forestgreen"),
        ))

        fig.update_layout(
            title="Interval width vs sample size",
            xaxis_title="n",
            yaxis_title="Width",
            template="plotly_white",
        )
        return fig
