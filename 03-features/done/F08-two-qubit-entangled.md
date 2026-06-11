# F08 — Two-Qubit Entangled System (Bell State)

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Extend the simulator to represent an entangled 2-qubit system using a 4-element state vector. Demonstrate the Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2 — created by H on q0 then CNOT. Show N experiments in the same grid format; reader observes only "00" and "11" ever appear (never "01" or "10"), which is the signature of entanglement.

## Model layer

`src/quant2/two_qubit_entangled.py` — `EntangledPair` class with a 4-element complex state vector (basis order: |00⟩, |01⟩, |10⟩, |11⟩). Methods:

- `apply(gate4x4)` — multiply state vector by 4×4 matrix
- `measure() -> str` — collapse to one of {"00","01","10","11"} by probability, update state vector

`src/quant2/gates.py` — add 4×4 matrices: `H_I = H ⊗ I` (Hadamard on first qubit, identity on second), `CNOT` (already 4×4 if not present).

## Simulation layer

`run_trials_entangled(gate_sequence: list[np.ndarray], n: int) -> dict[str, int]` in `src/sim/runner.py`. Each trial starts fresh `EntangledPair`, applies gates, measures. Default gate sequence for Bell state: `[H_I, CNOT]`.

## Visualization

New `:visualize` viz — `entangled-grid`:

- Same grid layout as `two-qubit-grid`
- Same color scheme: 00=white, 11=`#e0ccff`, 01=`#cce5ff`, 10=`#ffcccc`
- Visually: 01 and 10 cells never appear for Bell state — reader sees only 00 and 11
- Optional: after animation completes, display outcome counts as small text below grid

## Chapter content

Extends `chapters/chapter02.md` with a second section explaining entanglement — why measuring q0 instantly determines q1's outcome, what "correlation" means physically. Uses `:visualize entangled-grid 20`.

## How to Demo
**Setup**: `uv sync`

**Steps**:
1. `uv run streamlit run src/chapter02.py`
2. Read entanglement section
3. Watch `entangled-grid` — only "00" and "11" appear
4. Compare with `two-qubit-grid` above where all four outcomes appear

**Expected output**: Grid fills only with "00" and "11" outcomes (~50/50). "01" and "10" never appear.
