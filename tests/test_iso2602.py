"""Tests for core.iso2602 — Confidence intervals (ISO 2602:1980)."""

import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.iso2602 import ConfidenceInterval


class TestConfidenceInterval:
    def test_bilateral_95(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        lo, hi = ci.bilateral_interval()
        assert lo < ci.mean < hi
        assert hi - lo > 0

    def test_bilateral_99(self, normal_data_30):
        ci95 = ConfidenceInterval(normal_data_30, confidence=0.95)
        ci99 = ConfidenceInterval(normal_data_30, confidence=0.99)
        w95 = ci95.bilateral_interval()[1] - ci95.bilateral_interval()[0]
        w99 = ci99.bilateral_interval()[1] - ci99.bilateral_interval()[0]
        assert w99 > w95, "99% CI should be wider than 95%"

    def test_bilateral_90(self, normal_data_30):
        ci90 = ConfidenceInterval(normal_data_30, confidence=0.90)
        ci95 = ConfidenceInterval(normal_data_30, confidence=0.95)
        w90 = ci90.bilateral_interval()[1] - ci90.bilateral_interval()[0]
        w95 = ci95.bilateral_interval()[1] - ci95.bilateral_interval()[0]
        assert w90 < w95, "90% CI should be narrower than 95%"

    def test_unilateral_lower(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        lower = ci.unilateral_interval(side="lower")
        assert lower < ci.mean

    def test_unilateral_upper(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        upper = ci.unilateral_interval(side="upper")
        assert upper > ci.mean

    def test_invalid_side(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30)
        with pytest.raises(ValueError):
            ci.unilateral_interval(side="middle")

    def test_small_sample(self, small_data):
        ci = ConfidenceInterval(small_data, confidence=0.95)
        lo, hi = ci.bilateral_interval()
        assert lo < hi

    def test_min_sample_size(self):
        with pytest.raises(ValueError):
            ConfidenceInterval(np.array([1.0]))

    def test_invalid_confidence(self, normal_data_30):
        with pytest.raises(ValueError):
            ConfidenceInterval(normal_data_30, confidence=0.80)

    def test_get_statistics(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        s = ci.get_statistics()
        assert s["n"] == 30
        assert "mean" in s
        assert "std" in s
        assert "se" in s
        assert s["df"] == 29

    def test_prediction_interval(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        lo, hi = ci.prediction_interval()
        # Prediction interval should be wider than confidence interval
        ci_lo, ci_hi = ci.bilateral_interval()
        assert (hi - lo) > (ci_hi - ci_lo)

    def test_hypothesis_test_not_rejected(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        result = ci.hypothesis_test(ci.mean)
        assert not result["reject_null"]

    def test_hypothesis_test_rejected(self, normal_data_30):
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        result = ci.hypothesis_test(ci.mean + 10 * ci.std)
        assert result["reject_null"]

    def test_difference_of_means(self, normal_data_30):
        rng = np.random.default_rng(99)
        other = rng.normal(100, 1.5, 30)
        ci = ConfidenceInterval(normal_data_30, confidence=0.95)
        lo, hi = ci.difference_of_means(other)
        assert lo < hi
