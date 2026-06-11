#!/usr/bin/env python3
# gates.py — Standard single-qubit gate matrices
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

I2 = np.eye(2, dtype=complex)

# 2-qubit gates: basis order |00⟩, |01⟩, |10⟩, |11⟩
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
], dtype=complex)

# H ⊗ I: Hadamard on qubit 0, identity on qubit 1
H_I = np.kron(H, I2)

# I ⊗ X: identity on qubit 0, X (NOT) on qubit 1
I_X = np.kron(I2, X)


def Ry(theta: float) -> np.ndarray:
    """Rotation gate around Y-axis by angle theta."""
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def Ry_I(theta: float) -> np.ndarray:
    """Ry(theta) ⊗ I: rotation on qubit 0, identity on qubit 1."""
    return np.kron(Ry(theta), I2)
