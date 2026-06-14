# Current Session Handoff

**Date**: 2026-06-13
**Status**: F01–F13 complete. No open features. Grover's example being built interactively.

## In Progress
- Building a concrete 4-qubit Grover's example in book_dialog.md (interactive, step by step)
  - grover-start viz: done (equal superposition of 16 states)
  - grover-oracle viz: done (state 11 amplitude flipped negative)
  - Next: diffusion/amplification step visualization
- Corrected explanation of joint amplitudes: unentangled qubits keep per-qubit alpha/beta; entanglement is when joint state can no longer be factored

## Blocked
- Streamlit Cloud: main file path needs updating to `src/book.py` in Streamlit dashboard settings (manual step)

## Completed This Session
- Added grover-start visualization: 16-bar chart showing equal superposition after Hadamard
- Added grover-oracle visualization: same chart with state 11 bar flipped negative (orange)
- Added Aristotle/Plato dialog explaining the oracle step
- Added explanation of how multi-qubit registers have joint amplitudes (not per-qubit)
- Added truth table for asymmetric entangled state
- Fixed all Qbit/qbit spellings to qubit throughout
- Renamed content/images/qbit.svg → qubit.svg
- Grid animations now reveal cells one at a time (all 6 grid vizs)
- x_gate_grid: ? → 0 → 1 animation per cell
- Unmeasured cells render empty (no grey qubit)
- "Run Experiment" button replaces auto-run on page load
- Closed F13: book_dialog.md adopted as default book
- Removed unused dependencies: rich, watchdog (watchdog re-added by user)
- Added run.bash for easy app launch
- 99 tests passing

## Completed Previous Sessions
- F07–F12: all quantum chapters complete
- Unified book: single content/book_dialog.md as active book
- Per-viz replay: @st.fragment for isolated animation replay
- CSS: Telex headers, Helvetica body at 1.3rem
- Literate docs: 01-gates.md through 13-grover_oracle.md

## Defined, Not Started
- Diffusion step visualization for 4-qubit Grover's example

## Next
1. Build grover-diffusion visualization showing amplitude amplification after one iteration
2. Fix Streamlit Cloud main file path (manual dashboard setting)
3. Define new features as needed
