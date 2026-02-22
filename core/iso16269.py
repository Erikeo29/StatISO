"""
ISO 16269-6:2014 -- Statistical tolerance intervals.

Provides bilateral / unilateral tolerance intervals for normally distributed
populations using tabulated k-factors.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .constants import get_k_factor


class ToleranceInterval:
    """Tolerance interval calculator per ISO 16269-6:2014.

    Parameters
    ----------
    data : array-like
        Sample observations (at least 2 values).
    confidence : float
        Confidence level -- 0.90, 0.95, or 0.99.
    coverage : float
        Population coverage proportion -- 0.90, 0.95, or 0.99.
    """

    _VALID_LEVELS = {0.90, 0.95, 0.99}

    def __init__(
        self,
        data: Sequence[float] | np.ndarray,
        confidence: float = 0.95,
        coverage: float = 0.95,
    ):
        self.data = np.asarray(data, dtype=float)
        self.n: int = len(self.data)
        self.confidence = confidence
        self.coverage = coverage

        if self.n < 2:
            raise ValueError("Sample size must be at least 2")
        if confidence not in self._VALID_LEVELS:
            raise ValueError(f"Confidence must be one of {sorted(self._VALID_LEVELS)}")
        if coverage not in self._VALID_LEVELS:
            raise ValueError(f"Coverage must be one of {sorted(self._VALID_LEVELS)}")

        self.mean: float = float(np.mean(self.data))
        self.std: float = float(np.std(self.data, ddof=1))

    # ------------------------------------------------------------------
    # Private helper
    # ------------------------------------------------------------------

    def _k(self, bilateral: bool) -> float:
        k = get_k_factor(self.n, self.confidence, self.coverage, bilateral=bilateral)
        if k is None:
            raise ValueError(
                f"k-factor not available for n={self.n}, "
                f"confidence={self.confidence}, coverage={self.coverage}"
            )
        return k

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def bilateral_interval(self) -> tuple[float, float]:
        """Two-sided tolerance interval.

        Returns
        -------
        tuple[float, float]
            (lower_limit, upper_limit) such that the interval is expected
            to contain at least *coverage* proportion of the population
            with probability *confidence*.
        """
        k = self._k(bilateral=True)
        return self.mean - k * self.std, self.mean + k * self.std

    def unilateral_interval(self, side: str = "lower") -> float:
        """One-sided tolerance bound.

        Parameters
        ----------
        side : str
            ``'lower'`` for a lower bound, ``'upper'`` for an upper bound.

        Returns
        -------
        float
            The tolerance limit.
        """
        if side not in ("lower", "upper"):
            raise ValueError("side must be 'lower' or 'upper'")

        k = self._k(bilateral=False)
        return self.mean - k * self.std if side == "lower" else self.mean + k * self.std

    def get_statistics(self) -> dict:
        """Descriptive statistics of the sample.

        Returns
        -------
        dict
            Keys: ``n``, ``mean``, ``std``, ``variance``, ``min``, ``max``,
            ``confidence``, ``coverage``.
        """
        return {
            "n": self.n,
            "mean": self.mean,
            "std": self.std,
            "variance": self.std ** 2,
            "min": float(np.min(self.data)),
            "max": float(np.max(self.data)),
            "confidence": self.confidence,
            "coverage": self.coverage,
        }
