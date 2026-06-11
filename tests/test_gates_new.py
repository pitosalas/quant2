#!/usr/bin/env python3
# test_gates_new.py — Tests for Ry, I_X, Ry_I gates
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import math
import numpy as np
import pytest
from quant2.gates import Ry, I_X, Ry_I, X, I2


def test_ry_pi_is_bit_flip():
    """Ry(π) applied to |0⟩ should give |1⟩ (up to global phase)."""
    state = np.array([1.0, 0.0])
    result = Ry(math.pi) @ state
    assert abs(result[0]) < 1e-10
    assert abs(abs(result[1]) - 1.0) < 1e-10


def test_ry_zero_is_identity():
    """Ry(0) is identity."""
    assert np.allclose(Ry(0), np.eye(2))


def test_ry_is_unitary():
    """Ry(θ) must be unitary for arbitrary θ."""
    gate = Ry(math.pi / 3)
    assert np.allclose(gate @ gate.conj().T, np.eye(2))


def test_i_x_shape():
    """I_X must be 4x4."""
    assert I_X.shape == (4, 4)


def test_i_x_flips_second_qubit():
    """|00⟩ under I_X → |01⟩."""
    state = np.array([1.0, 0.0, 0.0, 0.0])
    result = I_X @ state
    expected = np.array([0.0, 1.0, 0.0, 0.0])
    assert np.allclose(result, expected)


def test_ry_i_shape():
    """Ry_I must be 4x4."""
    assert Ry_I(math.pi / 3).shape == (4, 4)


def test_ry_i_unitary():
    """Ry_I must be unitary."""
    gate = Ry_I(math.pi / 4)
    assert np.allclose(gate @ gate.conj().T, np.eye(4))
