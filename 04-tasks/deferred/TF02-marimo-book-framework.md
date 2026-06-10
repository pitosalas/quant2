# TF02 — Marimo Book Framework for Browser Display

Task file for Feature F02. Each step includes a test where feasible.

## T01 — Project dependencies and pyproject.toml
**Status**: done
**Description**: Add `marimo` and `numpy` to `pyproject.toml` dependencies. Confirm `uv sync` succeeds and `marimo` CLI is available.
**Test**: `uv run python -c "import marimo, numpy"` exits 0.

## T02 — Quantum model layer: qubit and state vector
**Status**: done
**Description**: `src/quant2/qubit.py` — `Qubit` class with normalized state vector, `zero()`, `one()`, `apply(gate)`, `measure()`, `bloch_angles()`, `prob_zero`, `prob_one`. No Marimo imports. Tests in `tests/test_qubit.py`.

## T03 — Quantum model layer: gates
**Status**: done
**Description**: `src/quant2/gates.py` — X, Y, Z, H (single-qubit) and CNOT (2-qubit 4×4). Tests in `tests/test_gates_cnot.py`.

## T04 — Quantum model layer: measurement
**Status**: done
**Description**: `src/quant2/measurement.py` — `probabilities(qubit)` and `probabilities_vec(state_vec)`. Deterministic, no random sampling. Tests in `tests/test_gates_cnot.py`.

## T05 — Render layer: chapter definitions
**Status**: done
**Description**: `src/render/chapters.py` — `CHAPTERS` list with `{id, title, render, reactive, reactive_keys}`. Three chapters: Qubit, Gates, Measurement. All quantum logic delegated to `quant2.*`. No inline math.

## T06 — Main Marimo notebook
**Status**: done
**Description**: `src/main.py` — Marimo app with chapter dropdown, static layout cell, reactive output cell. Each chapter wires UI controls to qmodel layer via chapters.py.
**Test**: `uv run marimo run src/main.py` — manual verification required.

## T07 — WASM single-file export
**Status**: done
**Description**: Create `src/main_wasm.py` with all `src/quant2/` and `src/render/` modules inlined. Run `marimo export html-wasm src/main_wasm.py -o docs/index.html --mode run`. Commit `docs/` output.
**Test**: Open `docs/index.html` in browser — all three chapters load and controls respond (manual; note in work log).

## T08 — Tests suite runnable with plain pytest
**Status**: done
**Description**: 32 tests pass with `uv run pytest`. pythonpath = ["src"] added to pyproject.toml.
