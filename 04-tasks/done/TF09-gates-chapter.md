# TF09 — Gates Chapter

## T01 — x-gate-grid viz
**Status**: done
**Description**: Create `src/viz/x_gate_grid.py`. Grid showing X gate applied to |0⟩ — every cell measures 1. Reuses qubit_grid HTML infrastructure. Register as "x-gate-grid".
**Test**: HTML contains all "1" outcomes, no "0".

## T02 — Add chapter 3 text to book.md
**Status**: done
**Description**: Add gates chapter prose: X gate as quantum NOT, H revisited, gates as reversible, can re-apply H to collapse/restore superposition. Include x-gate-grid viz.
**Test**: Manual — renders in book.py.

## T03 — All tests pass
**Status**: done
**Test**: `uv run pytest` exits 0.
