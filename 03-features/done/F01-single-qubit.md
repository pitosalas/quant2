# F01 — Single Qubit Abstraction

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Model a single qubit with its quantum states (|0⟩, |1⟩, superposition) and relevant single-qubit behaviors: state initialization, applying gates (X, H, Z, Y), measurement (collapse), and Bloch sphere representation. Superposition and measurement probability are core. Entanglement is deferred to F02 (requires 2+ qubits).

## How to Demo

**Setup**: `uv run python -m quant2` or equivalent entry point.

**Steps**:
1. Create qubit in |0⟩ state
2. Apply Hadamard gate → superposition
3. Measure repeatedly → show ~50/50 |0⟩/|1⟩ distribution
4. Apply X gate (NOT) → flip state
5. Print Bloch sphere angles (θ, φ) for each state

**Expected output**: Console output showing state vector, gate applications, measurement outcomes, and probability distribution across N trials.
