"""
Process capability analysis (Cp, Cpk, Cpl, Cpu).

Extracted from the former ``ToleranceInterval.process_capability()`` method
to keep the ISO 16269 module focused on tolerance intervals.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy import stats


class ProcessCapability:
    """Compute process capability indices against specification limits.

    Parameters
    ----------
    data : array-like
        Process measurements.
    lsl : float | None
        Lower specification limit.
    usl : float | None
        Upper specification limit.

    Raises
    ------
    ValueError
        If neither *lsl* nor *usl* is provided, or if the sample has
        fewer than 2 observations.
    """

    def __init__(
        self,
        data: Sequence[float] | np.ndarray,
        lsl: float | None = None,
        usl: float | None = None,
    ):
        if lsl is None and usl is None:
            raise ValueError("At least one specification limit (lsl or usl) must be provided")

        self.data = np.asarray(data, dtype=float)
        if len(self.data) < 2:
            raise ValueError("Sample size must be at least 2")

        self.lsl = lsl
        self.usl = usl
        self.mean: float = float(np.mean(self.data))
        self.std: float = float(np.std(self.data, ddof=1))

    def compute(self) -> dict:
        """Calculate capability indices and out-of-spec percentages.

        Returns
        -------
        dict
            Always present: ``pct_out_of_spec``.
            Conditionally present depending on which limits are set:
            ``Cp``, ``Cpk``, ``Cpu``, ``Cpl``,
            ``pct_below_lsl``, ``pct_above_usl``.
        """
        results: dict = {}

        if self.lsl is not None and self.usl is not None:
            results["Cp"] = (self.usl - self.lsl) / (6 * self.std)
            cpu = (self.usl - self.mean) / (3 * self.std)
            cpl = (self.mean - self.lsl) / (3 * self.std)
            results["Cpk"] = min(cpu, cpl)
            results["Cpu"] = cpu
            results["Cpl"] = cpl
            results["pct_below_lsl"] = float(
                stats.norm.cdf(self.lsl, self.mean, self.std) * 100
            )
            results["pct_above_usl"] = float(
                (1 - stats.norm.cdf(self.usl, self.mean, self.std)) * 100
            )
            results["pct_out_of_spec"] = results["pct_below_lsl"] + results["pct_above_usl"]

        elif self.lsl is not None:
            cpl = (self.mean - self.lsl) / (3 * self.std)
            results["Cpl"] = cpl
            results["Cpk"] = cpl
            results["pct_below_lsl"] = float(
                stats.norm.cdf(self.lsl, self.mean, self.std) * 100
            )
            results["pct_out_of_spec"] = results["pct_below_lsl"]

        else:  # usl only
            cpu = (self.usl - self.mean) / (3 * self.std)
            results["Cpu"] = cpu
            results["Cpk"] = cpu
            results["pct_above_usl"] = float(
                (1 - stats.norm.cdf(self.usl, self.mean, self.std)) * 100
            )
            results["pct_out_of_spec"] = results["pct_above_usl"]

        return results

    def get_interpretation(self) -> dict:
        """Qualitative interpretation of the process capability.

        Returns
        -------
        dict
            Keys: ``Cpk``, ``level``, ``description``.
            Level is one of ``'excellent'``, ``'capable'``,
            ``'marginal'``, ``'incapable'``.
        """
        indices = self.compute()
        cpk = indices.get("Cpk", 0.0)

        if cpk >= 1.67:
            level, desc = "excellent", "Cpk >= 1.67 -- six-sigma capable"
        elif cpk >= 1.33:
            level, desc = "capable", "1.33 <= Cpk < 1.67 -- process is capable"
        elif cpk >= 1.0:
            level, desc = "marginal", "1.00 <= Cpk < 1.33 -- barely capable, improvement recommended"
        else:
            level, desc = "incapable", "Cpk < 1.00 -- process is not capable"

        return {"Cpk": cpk, "level": level, "description": desc}
