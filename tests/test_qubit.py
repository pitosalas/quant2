#!/usr/bin/env python3
# test_qubit.py — Tests for Qubit, gates, measurement, Bloch sphere, and simulation
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import pytest
from quant2 import Qubit, X, Y, Z, H


# T01 — Qubit class, state vector

def test_default_init_is_zero():
    q = Qubit.zero()
    assert np.isclose(q.prob_zero, 1.0)
    assert np.isclose(q.prob_one, 0.0)

def test_one_init():
    q = Qubit.one()
    assert np.isclose(q.prob_zero, 0.0)
    assert np.isclose(q.prob_one, 1.0)

def test_unnormalized_raises():
    with pytest.raises(ValueError, match="normalized"):
        Qubit(2.0, 0.0)

def test_state_is_copy():
    q = Qubit.zero()
    s = q.state
    s[0] = 99
    assert np.isclose(q.state[0], 1.0)  # mutation didn't affect internal state


# T02 — Gates

def test_x_flips_zero_to_one():
    q = Qubit.zero().apply(X)
    assert np.isclose(q.prob_one, 1.0)

def test_x_flips_one_to_zero():
    q = Qubit.one().apply(X)
    assert np.isclose(q.prob_zero, 1.0)

def test_x_twice_is_identity():
    q = Qubit.zero().apply(X).apply(X)
    assert np.isclose(q.prob_zero, 1.0)

def test_h_creates_superposition():
    q = Qubit.zero().apply(H)
    assert np.isclose(q.prob_zero, 0.5)
    assert np.isclose(q.prob_one, 0.5)

def test_h_twice_is_identity():
    q = Qubit.zero().apply(H).apply(H)
    assert np.isclose(q.prob_zero, 1.0)

def test_z_preserves_zero_probability():
    q = Qubit.zero().apply(Z)
    assert np.isclose(q.prob_zero, 1.0)

def test_z_preserves_one_probability():
    q = Qubit.one().apply(Z)
    assert np.isclose(q.prob_one, 1.0)

def test_hzh_equals_x():
    # HZH = X: should flip |0⟩ to |1⟩
    q = Qubit.zero().apply(H).apply(Z).apply(H)
    assert np.isclose(q.prob_one, 1.0)

def test_y_on_zero():
    q = Qubit.zero().apply(Y)
    assert np.isclose(q.prob_one, 1.0)


# T03 — Measurement

def test_measure_zero_state_always_zero():
    for _ in range(50):
        q = Qubit.zero()
        assert q.measure() == 0

def test_measure_one_state_always_one():
    for _ in range(50):
        q = Qubit.one()
        assert q.measure() == 1

def test_measure_collapses_state():
    q = Qubit.zero().apply(H)
    result = q.measure()
    if result == 0:
        assert np.isclose(q.prob_zero, 1.0)
    else:
        assert np.isclose(q.prob_one, 1.0)

def test_measure_superposition_distribution():
    np.random.seed(42)
    results = [Qubit.zero().apply(H).measure() for _ in range(1000)]
    frac = sum(results) / 1000
    assert 0.44 < frac < 0.56, f"Expected ~0.5 but got {frac}"


# T04 — Bloch sphere

def test_bloch_zero_state():
    q = Qubit.zero()
    theta, phi = q.bloch_angles()
    assert np.isclose(theta, 0.0)

def test_bloch_one_state():
    q = Qubit.one()
    theta, phi = q.bloch_angles()
    assert np.isclose(theta, np.pi)

def test_bloch_superposition():
    q = Qubit.zero().apply(H)
    theta, phi = q.bloch_angles()
    assert np.isclose(theta, np.pi / 2, atol=1e-6)


# T05 — Simulation runner

def test_simulation_x_gate_all_ones():
    from sim.runner import run_trials
    np.random.seed(0)
    counts = run_trials([X], 200)
    assert counts[1] == 200
    assert counts[0] == 0

def test_simulation_h_gate_roughly_half():
    from sim.runner import run_trials
    np.random.seed(0)
    counts = run_trials([H], 2000)
    frac = counts[1] / 2000
    assert 0.46 < frac < 0.54, f"Expected ~0.5 but got {frac}"
