# Current Session Handoff

**Date**: 2026-06-10
**Status**: F04–F06 complete. F07/F08 defined. Housekeeping: templates/ cleaned, codereview.md v3.2.

## In Progress
Nothing.

## Blocked
- Streamlit Cloud: main file path needs updating to `src/chapter01.py` in Streamlit dashboard settings.

## Completed This Session
- F01: quant2 package — Qubit, gates (X/Y/Z/H/CNOT), measurement. Tests passing.
- F02: Marimo book framework — deferred.
- F03: Chapter CLI — `src/chapter01-qbits.py` renders chapter markdown via rich.
- F04: 3-layer restructure (quant2/sim/viz) + Streamlit chapter renderer.
- F05: Inline `:visualize` directive system — registry, chapter_renderer, single-qubit animation.
- F06: `qubit-grid` visualization — 8-column grid, animated H|0⟩ measurements, 0.07s/step.
- SVG icon (images/qbit.svg) used instead of rectangles; CSS/HTML extracted to separate files.
- codereview.md updated to v3.2: new "Web Assets" section — no inline CSS/JS/HTML in Python.
- `.claude/templates/` cleaned: now contains only 5 bootstrapping templates (was duplicating live files).
- CLAUDE.md fixed: references `.claude/process.md` and `.claude/codereview.md` (not templates/).
- `notebook.py` and `notebook_styles.css` deleted (dead code, F02 deferred).

## Defined, Not Started
- F07: Two-qubit unentangled system — `TwoQubitState`, `run_trials_2qubit`, `two-qubit-grid` viz, chapter02.
- F08: Two-qubit entangled system (Bell state) — `EntangledPair` 4-vec, `run_trials_entangled`, `entangled-grid` viz.

## Next
1. Move F04/F05/F06 feature and task files from notdone/ to done/
2. Implement TF07 (two-qubit unentangled): `two_qubit.py`, `runner.py` extension, `two_qubit_grid.py`, `chapter02.md`, `chapter02.py`
3. Then TF08 (entangled Bell state)
4. Fix Streamlit Cloud main file path
