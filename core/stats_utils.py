"""
General-purpose statistical utilities.

Provides sample-size estimation and a lightweight two-sample mean comparison.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from scipy import stats

from .constants import get_t_value


def calculate_sample_size(
    confidence: float = 0.95,
    margin_error: float = 0.05,
    std_dev: float | None = None,
    proportion: float = 0.5,
) -> int:
    """Estimate required sample size for a given precision.

    When *std_dev* is provided the calculation targets estimation of a
    population mean; otherwise it targets a population proportion.

    Parameters
    ----------
    confidence : float
        Desired confidence level (e.g. 0.90, 0.95, 0.99).
    margin_error : float
        Acceptable margin of error (same unit as *std_dev* when estimating
        the mean, or absolute proportion when estimating a proportion).
    std_dev : float | None
        Known or estimated population standard deviation.  When ``None``
        the proportion formula is used instead.
    proportion : float
        Expected proportion (only used when *std_dev* is ``None``).

    Returns
    -------
    int
        Minimum sample size (rounded up).
    """
    if margin_error <= 0:
        raise ValueError("margin_error must be > 0")

    z = float(stats.norm.ppf((1 + confidence) / 2))

    if std_dev is not None:
        n = (z * std_dev / margin_error) ** 2
    else:
        n = (z ** 2 * proportion * (1 - proportion)) / (margin_error ** 2)

    return math.ceil(n)


def compare_means(
    data1: Sequence[float] | np.ndarray,
    data2: Sequence[float] | np.ndarray,
    confidence: float = 0.95,
    equal_variance: bool = True,
) -> dict:
    """Two-sample comparison of means with confidence interval.

    Parameters
    ----------
    data1, data2 : array-like
        Two independent samples.
    confidence : float
        Confidence level (0.90, 0.95, or 0.99).
    equal_variance : bool
        When ``True`` a pooled (Student) t-test is used; otherwise
        Welch's approximation is applied.

    Returns
    -------
    dict
        Keys: ``mean_diff``, ``ci_lower``, ``ci_upper``, ``t_statistic``,
        ``p_value``, ``df``, ``reject_null``, ``significance_level``.
    """
    a1 = np.asarray(data1, dtype=float)
    a2 = np.asarray(data2, dtype=float)
    n1, n2 = len(a1), len(a2)
    m1, m2 = float(np.mean(a1)), float(np.mean(a2))
    s1, s2 = float(np.std(a1, ddof=1)), float(np.std(a2, ddof=1))
    diff = m1 - m2

    if equal_variance:
        sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
        se = sp * math.sqrt(1 / n1 + 1 / n2)
        df = n1 + n2 - 2
    else:
        se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
        df = (
            (s1 ** 2 / n1 + s2 ** 2 / n2) ** 2
            / ((s1 ** 2 / n1) ** 2 / (n1 - 1) + (s2 ** 2 / n2) ** 2 / (n2 - 1))
        )

    t_stat = diff / se if se > 0 else 0.0
    p_value = float(2 * (1 - stats.t.cdf(abs(t_stat), df)))

    # Confidence interval for the difference
    t_crit = get_t_value(int(df), confidence, bilateral=True)
    if t_crit is None:
        t_crit = float(stats.t.ppf((1 + confidence) / 2, df))

    margin = t_crit * se
    alpha = 1 - confidence

    return {
        "mean_diff": diff,
        "ci_lower": diff - margin,
        "ci_upper": diff + margin,
        "t_statistic": t_stat,
        "p_value": p_value,
        "df": df,
        "reject_null": p_value < alpha,
        "significance_level": alpha,
    }
