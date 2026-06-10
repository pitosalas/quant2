#!/usr/bin/env python3
# measurement.py — Deterministic probability extraction from quantum state vectors
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
from quant2.qubit import Qubit


def probabilities(qubit: Qubit) -> dict[str, float]:
    """Return basis state label -> probability without collapsing state."""
    return {"0": qubit.prob_zero, "1": qubit.prob_one}


def probabilities_vec(state_vec: np.ndarray) -> dict[str, float]:
    """Return all basis state probabilities for an n-qubit state vector."""
    n_states = len(state_vec)
    n_qubits = int(np.log2(n_states))
    if 2**n_qubits != n_states:
        raise ValueError(f"State vector length {n_states} is not a power of 2")
    probs = (np.abs(state_vec) ** 2).real
    return {format(i, f"0{n_qubits}b"): float(probs[i]) for i in range(n_states)}
