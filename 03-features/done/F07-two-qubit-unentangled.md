# F07 — Two-Qubit Unentangled System

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Extend the simulator and chapter framework to represent a pair of qubits that are independent (not entangled). Each qubit is measured separately; outcomes combine into a 2-bit result (00, 01, 10, 11). Introduces the concept of a multi-qubit register without entanglement.

## Model layer

Two independent `Qubit` objects — no tensor product needed for the unentangled case. Each qubit has its own gate sequence applied before measurement. A `TwoQubitState` dataclass holds `q0` and `q1`.

Measurement produces a 2-bit string: e.g. `"01"` means q0→0, q1→1.

## Simulation layer

`run_trials_2qubit(gates0, gates1, n) -> dict[str, int]` — keys are `"00"`, `"01"`, `"10"`, `"11"`. Both qubits start in |0⟩, each has its own gate sequence applied, then both are measured.

## Visualization

New `:visualize` named viz — `two-qubit-grid`:

- Same grid layout as `qubit-grid` (F06)
- Each cell shows the 2-bit outcome: `"00"`, `"01"`, `"10"`, `"11"` — or `"??"` before measured
- 4 outcome colors: 00=white, 01=light blue, 10=light red, 11=light purple
- Animates one experiment per step left-to-right top-to-bottom

## Chapter content

New file `chapters/chapter02.md` — introduces 2-qubit registers, explains why outcomes are still independent when not entangled, sets up the question of what changes when they *are* entangled (deferred to F08).

New Streamlit app `src/chapter02.py`.

## How to Demo
**Setup**: `uv sync`

**Steps**:
1. `uv run streamlit run src/chapter02.py`
2. Read chapter text about 2-qubit registers
3. Watch `two-qubit-grid` animation — each cell shows a 2-bit outcome
4. Observe that 00/01/10/11 appear roughly equally (both qubits in H|0⟩)

**Expected output**: Grid fills with 2-bit outcomes. Distribution ~25% each.
