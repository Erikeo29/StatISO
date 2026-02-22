"""Tests for core.capability — Process capability analysis."""

import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.capability import ProcessCapability


class TestProcessCapability:
    def test_bilateral_capable(self):
        """Centered process with wide specs should be capable."""
        rng = np.random.default_rng(42)
        data = rng.normal(100, 1.0, 50)
        pc = ProcessCapability(data, lsl=94.0, usl=106.0)
        result = pc.compute()
        assert result["Cp"] > 1.33
        assert result["Cpk"] > 1.0

    def test_bilateral_incapable(self):
        """Process with tight specs should be incapable."""
        rng = np.random.default_rng(42)
        data = rng.normal(100, 3.0, 50)
        pc = ProcessCapability(data, lsl=98.0, usl=102.0)
        result = pc.compute()
        assert result["Cp"] < 1.0

    def test_only_usl(self):
        rng = np.random.default_rng(42)
        data = rng.normal(100, 1.5, 30)
        pc = ProcessCapability(data, usl=106.0)
        result = pc.compute()
        assert "Cpu" in result
        assert "Cp" not in result

    def test_only_lsl(self):
        rng = np.random.default_rng(42)
        data = rng.normal(100, 1.5, 30)
        pc = ProcessCapability(data, lsl=94.0)
        result = pc.compute()
        assert "Cpl" in result
        assert "Cp" not in result

    def test_no_specs_raises(self):
        with pytest.raises(ValueError):
            ProcessCapability(np.array([1.0, 2.0, 3.0]))

    def test_interpretation_excellent(self):
        rng = np.random.default_rng(42)
        data = rng.normal(100, 0.5, 50)
        pc = ProcessCapability(data, lsl=94.0, usl=106.0)
        interp = pc.get_interpretation()
        assert interp["level"] == "excellent"

    def test_interpretation_incapable(self):
        rng = np.random.default_rng(42)
        data = rng.normal(100, 5.0, 50)
        pc = ProcessCapability(data, lsl=98.0, usl=102.0)
        interp = pc.get_interpretation()
        assert interp["level"] == "incapable"

    def test_pct_out_of_spec(self):
        rng = np.random.default_rng(42)
        data = rng.normal(100, 1.5, 50)
        pc = ProcessCapability(data, lsl=94.0, usl=106.0)
        result = pc.compute()
        assert result["pct_out_of_spec"] >= 0
        assert result["pct_out_of_spec"] < 100

    def test_off_center_process(self):
        """Off-center process: Cpk < Cp."""
        rng = np.random.default_rng(42)
        data = rng.normal(103, 1.0, 50)  # mean shifted toward USL
        pc = ProcessCapability(data, lsl=94.0, usl=106.0)
        result = pc.compute()
        assert result["Cpk"] < result["Cp"]
