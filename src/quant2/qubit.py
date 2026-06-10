#!/usr/bin/env python3
# qubit.py — Single qubit state vector with gate application, measurement, and Bloch sphere
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np


class Qubit:
    """Single qubit with state vector [alpha, beta] where |alpha|^2 + |beta|^2 = 1."""

    def __init__(self, alpha: complex = 1.0, beta: complex = 0.0):
        vec = np.array([alpha, beta], dtype=complex)
        norm = np.linalg.norm(vec)
        if not np.isclose(norm, 1.0):
            raise ValueError(f"State vector must be normalized (norm={norm:.4f})")
        self.vec = vec

    @classmethod
    def zero(cls) -> "Qubit":
        return cls(1.0, 0.0)

    @classmethod
    def one(cls) -> "Qubit":
        return cls(0.0, 1.0)

    @property
    def state(self) -> np.ndarray:
        return self.vec.copy()

    @property
    def prob_zero(self) -> float:
        return float(abs(self.vec[0]) ** 2)

    @property
    def prob_one(self) -> float:
        return float(abs(self.vec[1]) ** 2)

    def apply(self, gate: np.ndarray) -> "Qubit":
        if gate.shape != (2, 2):
            raise ValueError(f"Gate must be 2x2, got shape {gate.shape}")
        new_vec = gate @ self.vec
        norm = np.linalg.norm(new_vec)
        if not np.isclose(norm, 1.0):
            raise ValueError(f"Gate produced non-normalized state (norm={norm:.4f})")
        return Qubit(new_vec[0], new_vec[1])

    def measure(self) -> int:
        probs = np.array([self.prob_zero, self.prob_one])
        probs = probs / probs.sum()  # renormalize to prevent float drift crashing np.random.choice
        outcome = int(np.random.choice([0, 1], p=probs))
        self.vec = np.array([1.0, 0.0] if outcome == 0 else [0.0, 1.0], dtype=complex)
        return outcome

    def bloch_angles(self) -> tuple[float, float]:
        """Return (theta, phi) Bloch sphere angles in radians."""
        alpha, beta = self.vec
        theta = 2.0 * np.arccos(np.clip(abs(alpha), 0.0, 1.0))
        phi = float(np.angle(beta) - np.angle(alpha))
        return float(theta), phi

    def __repr__(self) -> str:
        a, b = self.vec
        return (
            f"Qubit(α={a:.4f}, β={b:.4f} | "
            f"P(0)={self.prob_zero:.4f}, P(1)={self.prob_one:.4f})"
        )
