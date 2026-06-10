# TF01 — Single Qubit Implementation

Task file for F01-single-qubit.

## T01 — Define Qubit class with state vector
**Status**: done
**Description**: `Qubit` class holds a 2-element complex numpy array (alpha, beta) where |alpha|²+|beta|²=1. Init to |0⟩ by default. Include `__repr__` showing amplitudes and probabilities.

## T02 — Implement single-qubit gates
**Status**: done
**Description**: Apply standard 2x2 unitary matrices: X (NOT/flip), H (Hadamard/superposition), Z (phase flip), Y. Method `apply(gate)` multiplies state vector by gate matrix.

## T03 — Implement measurement
**Status**: done
**Description**: `measure()` collapses state to |0⟩ or |1⟩ based on |alpha|² probability. Returns 0 or 1. State vector updates to collapsed state.

## T04 — Bloch sphere representation
**Status**: done
**Description**: Compute θ and φ angles from state vector. `bloch_angles()` returns (theta, phi). Optional: ASCII Bloch sphere sketch.

## T05 — Simulation runner
**Status**: done
**Description**: Run N trials: init qubit, apply gate sequence, measure, tally results. Print distribution. Demonstrates superposition and gate behavior statistically.

## T06 — Tests
**Status**: done
**Description**: pytest tests for: |0⟩ init, X gate flips to |1⟩, H gate produces 50/50 over 1000 trials (within tolerance), Z gate preserves measurement probability, measure collapses correctly.
