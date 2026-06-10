# TF03 — Chapter CLI: Rich Text + Interactive Illustration

Task file for F03.

## T01 — Add rich dependency
**Status**: done
**Description**: `uv add rich` — added to pyproject.toml.

## T02 — chapter01-qbits.py
**Status**: done
**Description**: `src/chapter01-qbits.py` — loads `chapters/chapter01.md`, renders via `rich.Panel(Markdown(...))`, opens matplotlib figure with θ slider driving live qubit measurement histogram. `amplitudes(theta_deg)` helper eliminates duplicated α/β computation.
**Test**: No automated test — display/UI code. Manual: run and verify slider updates histogram.
