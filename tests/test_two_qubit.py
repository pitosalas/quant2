#!/usr/bin/env python3
# test_two_qubit.py — Tests for TwoQubitState and measure_pair
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import pytest
from quant2.qubit import Qubit
from quant2.gates import H, X
from quant2.two_qubit import TwoQubitState, measure_pair


def test_measure_pair_returns_valid_outcome():
    """measure_pair must return one of the four 2-bit strings."""
    q0 = Qubit.zero().apply(H)
    q1 = Qubit.zero().apply(H)
    outcome = measure_pair(q0, q1)
    assert outcome in {"00", "01", "10", "11"}


def test_measure_pair_x_x_always_11():
    """X on both qubits: always measures 11."""
    for _ in range(20):
        q0 = Qubit.zero().apply(X)
        q1 = Qubit.zero().apply(X)
        assert measure_pair(q0, q1) == "11"


def test_measure_pair_no_gate_always_00():
    """No gates: both qubits stay |0⟩, always 00."""
    for _ in range(20):
        assert measure_pair(Qubit.zero(), Qubit.zero()) == "00"


def test_measure_pair_h_h_all_four_outcomes():
    """H on both qubits: all four outcomes appear over enough trials."""
    np.random.seed(7)
    seen = set()
    for _ in range(200):
        q0 = Qubit.zero().apply(H)
        q1 = Qubit.zero().apply(H)
        seen.add(measure_pair(q0, q1))
    assert seen == {"00", "01", "10", "11"}


def test_two_qubit_state_zero():
    """TwoQubitState.zero() constructs two |0⟩ qubits."""
    state = TwoQubitState.zero()
    assert state.q0.prob_zero == pytest.approx(1.0)
    assert state.q1.prob_zero == pytest.approx(1.0)
