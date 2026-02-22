"""
Normality testing and outlier removal utilities.

Functions extracted from the legacy ``biostats/utils.py`` module.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy import stats


def check_normality(
    data: Sequence[float] | np.ndarray,
    alpha: float = 0.05,
) -> dict:
    """Run multiple normality tests on *data*.

    Parameters
    ----------
    data : array-like
        Observations to test.
    alpha : float
        Significance level for the decision.

    Returns
    -------
    dict
        Keys: ``shapiro`` (if n <= 5000), ``anderson``, ``ks``,
        ``jarque_bera``.  Each value is a dict with ``statistic``,
        ``p_value`` (when available), and ``is_normal``.
    """
    arr = np.asarray(data, dtype=float)
    results: dict = {}

    # Shapiro-Wilk (limited to n <= 5000)
    if len(arr) <= 5000:
        stat, p = stats.shapiro(arr)
        results["shapiro"] = {
            "statistic": float(stat),
            "p_value": float(p),
            "is_normal": p > alpha,
        }

    # Anderson-Darling
    ad = stats.anderson(arr, dist="norm")
    results["anderson"] = {
        "statistic": float(ad.statistic),
        "critical_values": dict(
            zip(["15%", "10%", "5%", "2.5%", "1%"], [float(v) for v in ad.critical_values])
        ),
        "is_normal": ad.statistic < ad.critical_values[2],  # 5 % level
    }

    # Kolmogorov-Smirnov
    ks_stat, ks_p = stats.kstest(
        arr, "norm", args=(float(np.mean(arr)), float(np.std(arr, ddof=1)))
    )
    results["ks"] = {
        "statistic": float(ks_stat),
        "p_value": float(ks_p),
        "is_normal": ks_p > alpha,
    }

    # Jarque-Bera
    jb_stat, jb_p = stats.jarque_bera(arr)
    results["jarque_bera"] = {
        "statistic": float(jb_stat),
        "p_value": float(jb_p),
        "is_normal": jb_p > alpha,
    }

    return results


def remove_outliers(
    data: Sequence[float] | np.ndarray,
    method: str = "iqr",
    threshold: float = 1.5,
) -> tuple[np.ndarray, np.ndarray]:
    """Remove outliers from *data*.

    Parameters
    ----------
    data : array-like
        Input observations.
    method : str
        Detection method: ``'iqr'``, ``'zscore'``, or ``'mad'``.
    threshold : float
        Sensitivity parameter.  For IQR this is the multiplier (default
        1.5); for z-score and MAD it is the cut-off value.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        ``(cleaned_data, outlier_indices)``
    """
    arr = np.asarray(data, dtype=float)

    if method == "iqr":
        q1 = float(np.percentile(arr, 25))
        q3 = float(np.percentile(arr, 75))
        iqr = q3 - q1
        mask = (arr >= q1 - threshold * iqr) & (arr <= q3 + threshold * iqr)

    elif method == "zscore":
        z = np.abs((arr - np.mean(arr)) / np.std(arr, ddof=0))
        mask = z < threshold

    elif method == "mad":
        median = float(np.median(arr))
        mad = float(np.median(np.abs(arr - median)))
        if mad == 0:
            mask = np.ones(len(arr), dtype=bool)
        else:
            modified_z = 0.6745 * (arr - median) / mad
            mask = np.abs(modified_z) < threshold

    else:
        raise ValueError(f"Unknown method '{method}'. Use 'iqr', 'zscore', or 'mad'.")

    outlier_indices = np.where(~mask)[0]
    return arr[mask], outlier_indices
