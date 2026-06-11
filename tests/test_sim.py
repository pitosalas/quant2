#!/usr/bin/env python3
# test_sim.py — Tests for sim.runner.run_trials
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import pytest
from quant2.gates import H, X, H_I, CNOT
from sim.runner import run_trials, run_trials_2qubit, run_trials_entangled


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


def test_run_trials_2qubit_has_all_four_keys():
    """run_trials_2qubit always returns dict with all four 2-bit keys."""
    counts = run_trials_2qubit([X], [X], 100)
    assert set(counts.keys()) == {"00", "01", "10", "11"}


def test_run_trials_2qubit_sums_to_n():
    """Total counts must equal n."""
    np.random.seed(42)
    counts = run_trials_2qubit([H], [H], 100)
    assert sum(counts.values()) == 100


def test_run_trials_2qubit_x_x_all_11():
    """X on both qubits: all outcomes must be 11."""
    counts = run_trials_2qubit([X], [X], 50)
    assert counts["11"] == 50
    assert counts["00"] == counts["01"] == counts["10"] == 0


def test_run_trials_2qubit_h_h_all_four_outcomes():
    """H on both: all four outcomes appear over enough trials."""
    np.random.seed(3)
    counts = run_trials_2qubit([H], [H], 200)
    assert all(counts[k] > 0 for k in ("00", "01", "10", "11"))


def test_run_trials_2qubit_zero_n_raises():
    """n=0 must raise ValueError."""
    with pytest.raises(ValueError):
        run_trials_2qubit([H], [H], 0)


def test_run_trials_entangled_bell_no_01_or_10():
    """Bell state: 01 and 10 must never appear."""
    np.random.seed(99)
    counts = run_trials_entangled([H_I, CNOT], 100)
    assert counts["01"] == 0
    assert counts["10"] == 0


def test_run_trials_entangled_sums_to_n():
    """Total counts must equal n."""
    np.random.seed(1)
    counts = run_trials_entangled([H_I, CNOT], 100)
    assert sum(counts.values()) == 100


def test_run_trials_entangled_has_all_four_keys():
    """run_trials_entangled always returns dict with all four keys."""
    counts = run_trials_entangled([H_I, CNOT], 10)
    assert set(counts.keys()) == {"00", "01", "10", "11"}


def test_run_trials_entangled_zero_n_raises():
    """n=0 must raise ValueError."""
    with pytest.raises(ValueError):
        run_trials_entangled([H_I, CNOT], 0)
