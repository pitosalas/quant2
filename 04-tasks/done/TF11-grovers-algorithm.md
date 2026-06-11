# TF11 — Grover's Algorithm

## T01 — grover_anim viz
**Status**: done
**Description**: `src/viz/grover_anim.py`. Tracks 4-element state vector for 2-qubit Grover's. Animate signed amplitude bar chart through: init → after oracle → after diffusion, repeated for 2 iterations. Blue = positive, red = negative. Register as "grover-anim". Args: target state string e.g. "11".
**Test**: `build_grover_frames("11")` returns list of amplitude arrays with correct values.

## T02 — Add chapter 5 text to book.md
**Status**: done
**Description**: Grover's chapter: intuitive explanation of searching, superposition of all answers, oracle marks the target, diffusion amplifies it. Show 2 iterations to demonstrate over-rotation.
**Test**: Manual.

## T03 — All tests pass
**Status**: done
**Test**: `uv run pytest` exits 0.
