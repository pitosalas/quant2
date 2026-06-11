# TF08 — Two-Qubit Entangled System

Task file for F08.

## T01 — src/quant2/gates.py — add 4×4 gates
**Status**: done
**Description**: Add to `src/quant2/gates.py`: `H_I = np.kron(H, I2)` (H on qubit 0, identity on qubit 1) and ensure `CNOT` is defined as the standard 4×4 matrix. `I2 = np.eye(2)`. Export both.
**Test**: `tests/test_gates.py` — `H_I` is 4×4, unitary; `CNOT @ CNOT == I4`.

## T02 — src/quant2/two_qubit_entangled.py
**Status**: done
**Description**: Create `EntangledPair` class. State: `np.ndarray` shape (4,) complex, initialized to `[1,0,0,0]` (|00⟩). `apply(gate)` multiplies in place. `measure() -> str` collapses by `abs(state)**2` probabilities, returns one of {"00","01","10","11"}, updates state to collapsed basis vector.
**Test**: `tests/test_two_qubit_entangled.py` — Bell state (H_I then CNOT): 200 trials produce only "00" and "11"; never "01" or "10". Product state (H_I only, no CNOT): all four outcomes appear.

## T03 — src/sim/runner.py — add run_trials_entangled
**Status**: done
**Description**: Add `run_trials_entangled(gate_sequence: list, n: int) -> dict[str, int]` to `src/sim/runner.py`. Each trial: fresh `EntangledPair()`, apply gates in order, measure. Return counts dict with all 4 keys.
**Test**: `tests/test_runner.py` — `run_trials_entangled([H_I, CNOT], 100)` keys == {"00","01","10","11"}, counts["01"]==0, counts["10"]==0.

## T04 — src/viz/entangled_grid.py
**Status**: done
**Description**: Create `src/viz/entangled_grid.py`. Same structure as `two_qubit_grid.py`. `render(args)`, `build_entangled_grid_figure(results, n) -> Figure`. Register as `"entangled-grid"`. Reuse same color scheme.
**Test**: `tests/test_entangled_grid.py` — `build_entangled_grid_figure({"00":2,"11":2,"01":0,"10":0}, 4)` returns Figure.

## T05 — chapters/chapter02.md — add entanglement section
**Status**: done
**Description**: Append entanglement section to `chapters/chapter02.md`. Explain: superposition vs entanglement, Bell state creation (H then CNOT), why only 00/11 appear. Add `:visualize entangled-grid 20` after explanation. Keep prose concise; no HTML.
**Test**: Manual — renders cleanly.

## T06 — src/chapter02.py — import entangled_grid
**Status**: done
**Description**: Add `import viz.entangled_grid  # noqa: F401` to `src/chapter02.py`.
**Test**: `uv run streamlit run src/chapter02.py` runs without error (manual).

## T07 — All tests pass
**Status**: done
**Description**: `uv run pytest` exits 0.
**Test**: `uv run pytest` — all tests pass.
