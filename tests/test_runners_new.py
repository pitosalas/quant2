#!/usr/bin/env python3
# test_runners_new.py — Tests for anticorrelated and asymmetric runners
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import math
import numpy as np
from sim.runner import run_trials_anticorrelated, run_trials_asymmetric


def test_anticorrelated_only_01_and_10():
    """Anti-correlated Bell state: only 01 and 10 outcomes."""
    np.random.seed(42)
    counts = run_trials_anticorrelated(200)
    assert counts["00"] == 0
    assert counts["11"] == 0
    assert counts["01"] + counts["10"] == 200


def test_asymmetric_only_00_and_11():
    """Asymmetric entanglement: only 00 and 11 outcomes."""
    np.random.seed(7)
    counts = run_trials_asymmetric(math.pi / 3, 200)
    assert counts["01"] == 0
    assert counts["10"] == 0
    assert counts["00"] + counts["11"] == 200


def test_asymmetric_biased_toward_00():
    """Asymmetric at θ=π/3: 00 appears ~75%, 11 ~25%."""
    np.random.seed(0)
    counts = run_trials_asymmetric(math.pi / 3, 1000)
    frac_00 = counts["00"] / 1000
    assert 0.68 < frac_00 < 0.82, f"Expected ~0.75 but got {frac_00}"
