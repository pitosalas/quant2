#!/usr/bin/env python3
# two_qubit_entangled.py — Entangled two-qubit system with 4-element state vector
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np

OUTCOMES = ["00", "01", "10", "11"]


class EntangledPair:
    """Two-qubit system with full 4-element complex state vector.

    Basis order: |00⟩=0, |01⟩=1, |10⟩=2, |11⟩=3.
    Initialized to |00⟩.
    """

    def __init__(self):
        self.state = np.array([1.0, 0.0, 0.0, 0.0], dtype=complex)

    def apply(self, gate: np.ndarray) -> None:
        if gate.shape != (4, 4):
            raise ValueError(f"Gate must be 4x4, got {gate.shape}")
        self.state = gate @ self.state

    def measure(self) -> str:
        probs = np.abs(self.state) ** 2
        probs = probs / probs.sum()
        idx = int(np.random.choice(4, p=probs))
        collapsed = np.zeros(4, dtype=complex)
        collapsed[idx] = 1.0
        self.state = collapsed
        return OUTCOMES[idx]
