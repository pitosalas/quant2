# TF07 — Two-Qubit Unentangled System

Task file for F07.

## T01 — src/quant2/two_qubit.py
**Status**: done
**Description**: Create `TwoQubitState` dataclass holding `q0: Qubit` and `q1: Qubit`. Add `measure_pair(q0: Qubit, q1: Qubit) -> str` that measures both independently and returns e.g. `"01"`. Both qubits start fresh in |0⟩ when constructed.
**Test**: `tests/test_two_qubit.py` — `measure_pair` returns one of {"00","01","10","11"}; H applied to both gives ~equal distribution over 200 trials.

## T02 — src/sim/runner.py — add run_trials_2qubit
**Status**: done
**Description**: Add `run_trials_2qubit(gates0: list, gates1: list, n: int) -> dict[str, int]` to `src/sim/runner.py`. Each trial: fresh Qubit for each, apply respective gate lists, call `measure_pair`. Accumulate counts. Keys always include all four outcomes (0 if never seen).
**Test**: `tests/test_runner.py` — `run_trials_2qubit([H], [H], 100)` returns dict with keys {"00","01","10","11"}, total = 100.

## T03 — src/viz/two_qubit_grid.py
**Status**: done
**Description**: Create `src/viz/two_qubit_grid.py`. `render(args: list[str]) -> None`. `n = int(args[0]) if args else 16`. Same 4-column grid layout as `qubit_grid.py`. Each cell: label "Exp #N", shows `"??"` until measured, then 2-bit string. Color: `"00"`=white, `"01"`=`#cce5ff`, `"10"`=`#ffcccc`, `"11"`=`#e0ccff`. Animate with `st.empty()`, one experiment per step, `time.sleep(0.15)`. Extract `build_two_qubit_grid_figure(results, n) -> Figure` as unit-testable helper. Register as `"two-qubit-grid"`.
**Test**: `tests/test_two_qubit_grid.py` — `build_two_qubit_grid_figure({"00":2,"01":1,"10":1,"11":0}, 4)` returns matplotlib Figure.

## T04 — chapters/chapter02.md
**Status**: done
**Description**: Write `chapters/chapter02.md`. Explain: a 2-qubit register, independent qubits, why 4 outcomes appear, probability of each (25% each for H|0⟩ ⊗ H|0⟩). Include `:visualize two-qubit-grid 20` at the right point. Keep prose concise; no HTML.
**Test**: Manual — markdown renders cleanly in Streamlit.

## T05 — src/chapter02.py
**Status**: done
**Description**: Create `src/chapter02.py`. Copy structure from `chapter01.py`: `sys.path.insert`, import viz modules including `viz.two_qubit_grid`, call `render_chapter(CHAPTER_FILE)` with `chapters/chapter02.md`.
**Test**: `uv run streamlit run src/chapter02.py` renders without error (manual).

## T06 — All tests pass
**Status**: done
**Description**: `uv run pytest` exits 0.
**Test**: `uv run pytest` — all tests pass.
