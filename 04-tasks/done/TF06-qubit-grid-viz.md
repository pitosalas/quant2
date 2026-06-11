# TF06 — Qubit Grid Visualization

Task file for F06.

## T01 — src/viz/qubit_grid.py
**Status**: done
**Description**: Create `src/viz/qubit_grid.py`. `render(args: list[str]) -> None`. `n = int(args[0]) if args else 16`. Grid layout: 4 columns, ceil(n/4) rows. Use matplotlib to draw all cells each frame — unmeasured="?" gray, measured 0=blue tint, measured 1=red tint. Large centered text per cell, "Exp #N" label above. Animate with `st.empty()`, measure one qubit per step, `time.sleep(0.15)`. Register as `"qubit-grid"`.
**Test**: `tests/test_qubit_grid.py` — `build_grid_figure(results, n)` returns a Figure (unit-testable helper, no Streamlit).

## T02 — Import in chapter01.py
**Status**: done
**Description**: Add `import viz.qubit_grid` to `src/chapter01.py` to trigger registration.
**Test**: registry contains `"qubit-grid"` after import.

## T03 — Add directive to chapter01.md
**Status**: done
**Description**: Add `:visualize qubit-grid 20` at a good point in `chapters/chapter01.md`.
**Test**: Manual — grid animation appears inline.

## T04 — All tests pass
**Status**: done
**Description**: `uv run pytest` exits 0.
**Test**: `uv run pytest` — all tests pass.
