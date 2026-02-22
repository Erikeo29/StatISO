"""Shared fixtures for StatISO tests."""

import numpy as np
import pytest


@pytest.fixture
def normal_data_30():
    """30 normally-distributed samples (seed=42, mean=100, std=1.5)."""
    rng = np.random.default_rng(42)
    return rng.normal(100, 1.5, 30)


@pytest.fixture
def normal_data_50():
    """50 normally-distributed samples (seed=42, mean=100, std=1.5)."""
    rng = np.random.default_rng(42)
    return rng.normal(100, 1.5, 50)


@pytest.fixture
def small_data():
    """Small dataset (n=5) for edge-case testing."""
    return np.array([98.5, 100.1, 101.3, 99.7, 100.4])


@pytest.fixture
def data_with_outliers():
    """Dataset with obvious outliers."""
    rng = np.random.default_rng(42)
    data = rng.normal(100, 1.5, 30)
    data = np.append(data, [120.0, 80.0])  # two outliers
    return data
