"""
ISO 2602:1980 -- Confidence intervals for the mean.

Provides bilateral / unilateral confidence intervals, prediction intervals,
difference-of-means intervals, and one-sample hypothesis tests.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from scipy import stats

from .constants import get_t_value


class ConfidenceInterval:
    """Confidence interval calculator per ISO 2602:1980.

    Parameters
    ----------
    data : array-like
        Sample observations (at least 2 values).
    confidence : float
        Confidence level -- 0.90, 0.95, or 0.99.
    """

    _VALID_CONFIDENCE = {0.90, 0.95, 0.99}

    def __init__(self, data: Sequence[float] | np.ndarray, confidence: float = 0.95):
        self.data = np.asarray(data, dtype=float)
        self.n: int = len(self.data)
        self.confidence = confidence
        self.df: int = self.n - 1

        if self.n < 2:
            raise ValueError("Sample size must be at least 2")
        if confidence not in self._VALID_CONFIDENCE:
            raise ValueError(f"Confidence must be one of {sorted(self._VALID_CONFIDENCE)}")

        self.mean: float = float(np.mean(self.data))
        self.std: float = float(np.std(self.data, ddof=1))
        self.se: float = self.std / math.sqrt(self.n)

    # ------------------------------------------------------------------
    # Private helper
    # ------------------------------------------------------------------

    def _t(self, df: int | float, bilateral: bool = True) -> float:
        """Resolve a t-value from ISO tables, falling back to scipy."""
        t = get_t_value(int(df), self.confidence, bilateral=bilateral)
        if t is not None:
            return t
        if bilateral:
            return float(stats.t.ppf((1 + self.confidence) / 2, df))
        return float(stats.t.ppf(self.confidence, df))

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def bilateral_interval(self) -> tuple[float, float]:
        """Two-sided confidence interval for the population mean.

        Returns
        -------
        tuple[float, float]
            (lower_limit, upper_limit)
        """
        margin = self._t(self.df) * self.se
        return self.mean - margin, self.mean + margin

    def unilateral_interval(self, side: str = "lower") -> float:
        """One-sided confidence bound for the population mean.

        Parameters
        ----------
        side : str
            ``'lower'`` or ``'upper'``.

        Returns
        -------
        float
            The confidence bound.
        """
        if side not in ("lower", "upper"):
            raise ValueError("side must be 'lower' or 'upper'")

        margin = self._t(self.df, bilateral=False) * self.se
        return self.mean - margin if side == "lower" else self.mean + margin

    def prediction_interval(self, future_samples: int = 1) -> tuple[float, float]:
        """Prediction interval for future observations.

        Parameters
        ----------
        future_samples : int
            Number of future observations to cover.

        Returns
        -------
        tuple[float, float]
            (lower_limit, upper_limit)
        """
        if future_samples < 1:
            raise ValueError("future_samples must be >= 1")

        se_pred = self.std * math.sqrt(1 / future_samples + 1 / self.n)
        margin = self._t(self.df) * se_pred
        return self.mean - margin, self.mean + margin

    def difference_of_means(
        self,
        other_data: Sequence[float] | np.ndarray,
        equal_variance: bool = True,
    ) -> tuple[float, float]:
        """Confidence interval for the difference of two independent means.

        Parameters
        ----------
        other_data : array-like
            Second sample.
        equal_variance : bool
            Assume equal population variances (pooled t-test). When ``False``
            the Welch-Satterthwaite approximation is used.

        Returns
        -------
        tuple[float, float]
            (lower_limit, upper_limit)
        """
        other = np.asarray(other_data, dtype=float)
        n2 = len(other)
        mean2 = float(np.mean(other))
        std2 = float(np.std(other, ddof=1))
        diff = self.mean - mean2

        if equal_variance:
            sp = math.sqrt(
                ((self.n - 1) * self.std ** 2 + (n2 - 1) * std2 ** 2)
                / (self.n + n2 - 2)
            )
            se_diff = sp * math.sqrt(1 / self.n + 1 / n2)
            df_comb = self.n + n2 - 2
        else:
            se_diff = math.sqrt(self.std ** 2 / self.n + std2 ** 2 / n2)
            df_comb = (
                (self.std ** 2 / self.n + std2 ** 2 / n2) ** 2
                / (
                    (self.std ** 2 / self.n) ** 2 / (self.n - 1)
                    + (std2 ** 2 / n2) ** 2 / (n2 - 1)
                )
            )

        margin = self._t(df_comb) * se_diff
        return diff - margin, diff + margin

    def hypothesis_test(
        self,
        null_value: float,
        alternative: str = "two-sided",
    ) -> dict:
        """One-sample t-test against *null_value*.

        Parameters
        ----------
        null_value : float
            Hypothesised population mean.
        alternative : str
            ``'two-sided'``, ``'less'``, or ``'greater'``.

        Returns
        -------
        dict
            Keys: ``t_statistic``, ``p_value``, ``null_value``,
            ``sample_mean``, ``alternative``, ``reject_null``,
            ``significance_level``.
        """
        if alternative not in ("two-sided", "less", "greater"):
            raise ValueError("alternative must be 'two-sided', 'less', or 'greater'")

        t_stat = (self.mean - null_value) / self.se

        if alternative == "two-sided":
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), self.df))
        elif alternative == "less":
            p_value = stats.t.cdf(t_stat, self.df)
        else:
            p_value = 1 - stats.t.cdf(t_stat, self.df)

        alpha = 1 - self.confidence
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "null_value": null_value,
            "sample_mean": self.mean,
            "alternative": alternative,
            "reject_null": p_value < alpha,
            "significance_level": alpha,
        }

    def get_statistics(self) -> dict:
        """Descriptive statistics of the sample.

        Returns
        -------
        dict
            Keys: ``n``, ``mean``, ``std``, ``se``, ``variance``, ``cv``,
            ``min``, ``max``, ``median``, ``q1``, ``q3``, ``confidence``,
            ``df``.
        """
        return {
            "n": self.n,
            "mean": self.mean,
            "std": self.std,
            "se": self.se,
            "variance": self.std ** 2,
            "cv": (self.std / self.mean * 100) if self.mean != 0 else float("inf"),
            "min": float(np.min(self.data)),
            "max": float(np.max(self.data)),
            "median": float(np.median(self.data)),
            "q1": float(np.percentile(self.data, 25)),
            "q3": float(np.percentile(self.data, 75)),
            "confidence": self.confidence,
            "df": self.df,
        }
