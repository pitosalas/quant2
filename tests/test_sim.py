#!/usr/bin/env python3
# test_sim.py — Tests for sim.runner.run_trials
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import pytest
from quant2.gates import H, X
from sim.runner import run_trials


def test_run_trials_x_all_ones():
    """X gate on |0⟩ always gives |1⟩."""
    counts = run_trials([X], 100)
    assert counts[1] == 100
    assert counts[0] == 0


def test_run_trials_sums_to_n():
    """Total counts must equal n."""
    np.random.seed(42)
    counts = run_trials([H], 1000)
    assert sum(counts.values()) == 1000


def test_run_trials_h_roughly_half():
    """H gate produces ~50% split over many trials."""
    np.random.seed(0)
    counts = run_trials([H], 2000)
    frac = counts[1] / 2000
    assert 0.46 < frac < 0.54, f"Expected ~0.5 but got {frac}"


def test_run_trials_empty_gate_sequence_stays_zero():
    """No gates applied: |0⟩ always measures 0."""
    counts = run_trials([], 50)
    assert counts[0] == 50
    assert counts[1] == 0


def test_run_trials_zero_n_raises():
    """n=0 must raise ValueError."""
    with pytest.raises(ValueError):
        run_trials([H], 0)


def test_run_trials_negative_n_raises():
    """Negative n must raise ValueError."""
    with pytest.raises(ValueError):
        run_trials([H], -5)
