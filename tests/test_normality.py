"""Tests for core.normality — Normality tests and outlier detection."""

import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.normality import check_normality, remove_outliers


class TestCheckNormality:
    def test_normal_data(self, normal_data_50):
        results = check_normality(normal_data_50)
        assert "shapiro" in results
        assert results["shapiro"]["is_normal"]

    def test_non_normal_data(self):
        rng = np.random.default_rng(42)
        data = rng.exponential(10, 100)
        results = check_normality(data)
        # At least one test should flag non-normality
        not_normal = sum(
            1 for v in results.values()
            if isinstance(v, dict) and not v.get("is_normal", True)
        )
        assert not_normal >= 1

    def test_all_four_tests(self, normal_data_50):
        results = check_normality(normal_data_50)
        assert "shapiro" in results
        assert "anderson" in results
        assert "ks" in results
        assert "jarque_bera" in results

    def test_custom_alpha(self, normal_data_50):
        results = check_normality(normal_data_50, alpha=0.01)
        assert "shapiro" in results


class TestRemoveOutliers:
    def test_iqr_method(self, data_with_outliers):
        cleaned, indices = remove_outliers(data_with_outliers, method="iqr")
        assert len(cleaned) < len(data_with_outliers)
        assert len(indices) > 0

    def test_zscore_method(self, data_with_outliers):
        cleaned, indices = remove_outliers(data_with_outliers, method="zscore", threshold=3.0)
        assert len(cleaned) <= len(data_with_outliers)

    def test_mad_method(self, data_with_outliers):
        cleaned, indices = remove_outliers(data_with_outliers, method="mad", threshold=3.5)
        assert len(cleaned) <= len(data_with_outliers)

    def test_no_outliers_in_clean_data(self, normal_data_30):
        cleaned, indices = remove_outliers(normal_data_30, method="iqr")
        # Most points should remain for normal data
        assert len(cleaned) >= len(normal_data_30) - 3

    def test_invalid_method(self, normal_data_30):
        with pytest.raises(ValueError):
            remove_outliers(normal_data_30, method="invalid")
