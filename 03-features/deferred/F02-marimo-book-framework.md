# F02 — Marimo Book Framework for Browser Display

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Build skeletal interactive "book" in Marimo that runs locally and deploys to browser via GitHub Pages / Marimo cloud. Follows the pattern from `back/`: `src/main.py` for local dev, `src/main_wasm.py` (all modules inlined) for static export, `docs/` for WASM HTML output. Book covers quantum computing basics chapter by chapter with reactive UI cells.

Structure:
- Chapter 1: What is a Qubit? (Bloch sphere concept, superposition)
- Chapter 2: Quantum Gates (X, H, CNOT — visual matrix representation)
- Chapter 3: Measurement and Probability
- Navigation: chapter selector dropdown, each chapter self-contained as `mo.md` + interactive cells

**Architecture constraint**: Strict separation between quantum model layer and rendering layer.
- `src/qmodel/` — pure quantum logic (qubits, gates, state vectors, measurement). No Marimo, no display.
- `src/render/` — all Marimo/visualization code. Calls qmodel API only, never raw math.
- Rationale: rendering approach will change (WASM, cloud, different viz libs). Model must be swappable independently.

Deploy target: GitHub Pages via `marimo export html-wasm src/main_wasm.py -o docs/index.html --mode run`

## How to Demo
**Setup**: `uv sync && uv run marimo run src/main.py`

**Steps**:
1. Open browser at localhost URL shown
2. Select chapter from dropdown
3. Interact with sliders/controls in each chapter
4. Verify reactivity (output updates on input change)

**Expected output**: Multi-chapter interactive notebook renders in browser. Chapters selectable. Reactive cells respond to user input.
