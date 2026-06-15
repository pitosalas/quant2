# TF15 — Zero Qubit Grid Visualization

## T01 — Create zero_qubit_grid.py viz
**Status**: done
**Description**: Create `src/viz/zero_qubit_grid.py`. Import `build_cell_html` and `build_grid_html` from `qubit_grid`. render() creates `Qubit.zero()` and measures without H gate — always 0. Register as `zero-qubit-grid`.
**Test**: Verify all N results are 0; verify HTML contains no red cells.

## T02 — Insert visualization in book_dialog.md
**Status**: done
**Description**: After line 21 (Plato's "Always. No randomness..." speech), add short framing text and `:visualize zero-qubit-grid 20` before the Hadamard section.
**Test**: Run chapter_renderer test suite; confirm `zero-qubit-grid` tag is parsed and dispatched.

## T03 — Write tests
**Status**: done
**Description**: Add tests in `tests/test_viz.py` or new file covering: (a) all outcomes are 0, (b) HTML renders correct cell count, (c) registry lookup returns the render function.
**Test**: `pytest tests/` passes with new tests included.
