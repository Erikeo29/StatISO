"""
StatISO core calculation engine.

Pure Python statistical library implementing ISO 2602:1980 (confidence intervals)
and ISO 16269-6:2014 (tolerance intervals).
"""

__version__ = "2.0.0"

from .constants import (
    get_k_factor,
    get_t_value,
    UNILATERAL_K_FACTORS,
    BILATERAL_K_FACTORS,
    T_VALUES_BILATERAL,
    T_VALUES_UNILATERAL,
)
from .iso2602 import ConfidenceInterval
from .iso16269 import ToleranceInterval
from .capability import ProcessCapability
from .normality import check_normality, remove_outliers
from .stats_utils import calculate_sample_size, compare_means

__all__ = [
    "get_k_factor",
    "get_t_value",
    "UNILATERAL_K_FACTORS",
    "BILATERAL_K_FACTORS",
    "T_VALUES_BILATERAL",
    "T_VALUES_UNILATERAL",
    "ConfidenceInterval",
    "ToleranceInterval",
    "ProcessCapability",
    "check_normality",
    "remove_outliers",
    "calculate_sample_size",
    "compare_means",
]
