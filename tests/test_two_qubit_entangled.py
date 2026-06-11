#!/usr/bin/env python3
# test_two_qubit_entangled.py — Tests for EntangledPair and Bell state behavior
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import pytest
from quant2.gates import H_I, CNOT, I2
from quant2.two_qubit_entangled import EntangledPair


def test_initial_state_is_00():
    """Fresh EntangledPair starts in |00⟩."""
    pair = EntangledPair()
    assert pair.measure() == "00"


def test_bell_state_only_00_and_11():
    """Bell state (H_I then CNOT): only 00 and 11 ever appear."""
    np.random.seed(42)
    seen = set()
    for _ in range(200):
        pair = EntangledPair()
        pair.apply(H_I)
        pair.apply(CNOT)
        seen.add(pair.measure())
    assert seen == {"00", "11"}, f"Unexpected outcomes: {seen - {'00', '11'}}"


def test_bell_state_never_01_or_10():
    """Bell state: 01 and 10 must not appear."""
    np.random.seed(0)
    for _ in range(200):
        pair = EntangledPair()
        pair.apply(H_I)
        pair.apply(CNOT)
        outcome = pair.measure()
        assert outcome not in {"01", "10"}, f"Got forbidden outcome {outcome}"


def test_product_state_all_four_outcomes():
    """H⊗H (both qubits in superposition): all four outcomes appear — no entanglement."""
    from quant2.gates import H
    H_H = np.kron(H, H)
    np.random.seed(5)
    seen = set()
    for _ in range(300):
        pair = EntangledPair()
        pair.apply(H_H)
        seen.add(pair.measure())
    assert seen == {"00", "01", "10", "11"}


def test_apply_wrong_shape_raises():
    """apply must raise ValueError for non-4x4 gate."""
    pair = EntangledPair()
    with pytest.raises(ValueError):
        pair.apply(np.eye(2))


def test_h_i_is_4x4():
    """H_I must be a 4x4 matrix."""
    assert H_I.shape == (4, 4)


def test_h_i_unitary():
    """H_I must be unitary: H_I @ H_I† == I4."""
    assert np.allclose(H_I @ H_I.conj().T, np.eye(4))


def test_cnot_self_inverse():
    """CNOT applied twice == identity."""
    assert np.allclose(CNOT @ CNOT, np.eye(4))
