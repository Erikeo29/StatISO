"""Tests for core.iso16269 — Tolerance intervals (ISO 16269-6:2014)."""

import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.iso16269 import ToleranceInterval


class TestToleranceInterval:
    def test_bilateral_95_95(self, normal_data_30):
        ti = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.95)
        lo, hi = ti.bilateral_interval()
        assert lo < ti.mean < hi
        assert hi - lo > 0

    def test_bilateral_wider_than_ci(self, normal_data_30):
        """TI should always be wider than CI for same confidence."""
        from core.iso2602 import ConfidenceInterval

        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        ti = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.95)
        ci_width = ci.bilateral_interval()[1] - ci.bilateral_interval()[0]
        ti_width = ti.bilateral_interval()[1] - ti.bilateral_interval()[0]
        assert ti_width > ci_width

    def test_higher_coverage_wider(self, normal_data_30):
        ti90 = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.90)
        ti99 = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.99)
        w90 = ti90.bilateral_interval()[1] - ti90.bilateral_interval()[0]
        w99 = ti99.bilateral_interval()[1] - ti99.bilateral_interval()[0]
        assert w99 > w90

    def test_higher_confidence_wider(self, normal_data_30):
        ti90 = ToleranceInterval(normal_data_30, confidence=0.90, coverage=0.95)
        ti99 = ToleranceInterval(normal_data_30, confidence=0.99, coverage=0.95)
        w90 = ti90.bilateral_interval()[1] - ti90.bilateral_interval()[0]
        w99 = ti99.bilateral_interval()[1] - ti99.bilateral_interval()[0]
        assert w99 > w90

    def test_unilateral_lower(self, normal_data_30):
        ti = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.95)
        lower = ti.unilateral_interval(side="lower")
        assert lower < ti.mean

    def test_unilateral_upper(self, normal_data_30):
        ti = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.95)
        upper = ti.unilateral_interval(side="upper")
        assert upper > ti.mean

    def test_invalid_side(self, normal_data_30):
        ti = ToleranceInterval(normal_data_30)
        with pytest.raises(ValueError):
            ti.unilateral_interval(side="middle")

    def test_invalid_confidence(self, normal_data_30):
        with pytest.raises(ValueError):
            ToleranceInterval(normal_data_30, confidence=0.80)

    def test_invalid_coverage(self, normal_data_30):
        with pytest.raises(ValueError):
            ToleranceInterval(normal_data_30, coverage=0.80)

    def test_min_sample_size(self):
        with pytest.raises(ValueError):
            ToleranceInterval(np.array([1.0]))

    def test_get_statistics(self, normal_data_30):
        ti = ToleranceInterval(normal_data_30, confidence=0.95, coverage=0.95)
        s = ti.get_statistics()
        assert s["n"] == 30
        assert s["confidence"] == 0.95
        assert s["coverage"] == 0.95

    def test_small_sample(self, small_data):
        ti = ToleranceInterval(small_data, confidence=0.95, coverage=0.95)
        lo, hi = ti.bilateral_interval()
        assert lo < hi
