#!/usr/bin/env python3
# gates.py — Standard single-qubit gate matrices
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

# 2-qubit gate: basis order |00⟩, |01⟩, |10⟩, |11⟩
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
], dtype=complex)
