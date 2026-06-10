#!/usr/bin/env python3
# test_gates_cnot.py — Tests for CNOT gate and measurement module
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import pytest
from quant2.gates import CNOT
from quant2.qubit import Qubit
from quant2.gates import H
from quant2.measurement import probabilities, probabilities_vec


# CNOT gate matrix correctness

def test_cnot_shape():
    assert CNOT.shape == (4, 4)

def test_cnot_is_unitary():
    assert np.allclose(CNOT @ CNOT.conj().T, np.eye(4))

def test_cnot_00_unchanged():
    state = np.array([1, 0, 0, 0], dtype=complex)
    result = CNOT @ state
    assert np.allclose(result, [1, 0, 0, 0])

def test_cnot_10_flips_target():
    # |10⟩ → |11⟩
    state = np.array([0, 0, 1, 0], dtype=complex)
    result = CNOT @ state
    assert np.allclose(result, [0, 0, 0, 1])

def test_cnot_11_flips_target():
    # |11⟩ → |10⟩
    state = np.array([0, 0, 0, 1], dtype=complex)
    result = CNOT @ state
    assert np.allclose(result, [0, 0, 1, 0])


# measurement.probabilities

def test_probabilities_zero_state():
    q = Qubit.zero()
    p = probabilities(q)
    assert np.isclose(p["0"], 1.0)
    assert np.isclose(p["1"], 0.0)

def test_probabilities_superposition():
    q = Qubit.zero().apply(H)
    p = probabilities(q)
    assert np.isclose(p["0"], 0.5)
    assert np.isclose(p["1"], 0.5)

def test_probabilities_sum_to_one():
    q = Qubit(complex(0.6), complex(0.8))
    p = probabilities(q)
    assert np.isclose(sum(p.values()), 1.0)

def test_probabilities_vec_two_qubit():
    # |00⟩ state vector
    state = np.array([1, 0, 0, 0], dtype=complex)
    p = probabilities_vec(state)
    assert np.isclose(p["00"], 1.0)
    assert np.isclose(p["01"], 0.0)

def test_probabilities_vec_invalid_length():
    with pytest.raises(ValueError, match="power of 2"):
        probabilities_vec(np.array([1, 0, 0], dtype=complex))
