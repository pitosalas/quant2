# F04 — Code Restructure + Streamlit Chapter Framework

**Priority**: High
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: Three related changes:

## Part A — Layer Separation

Enforce strict three-layer architecture with no cross-layer imports downward:

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Model | `src/quant2/` | Pure quantum abstractions: Qubit, gates, measurement. No simulation, no display, no print. |
| Simulation | `src/sim/` | Run trials, collect statistics, return data structures. Calls model only. No display. |
| Visualization | `src/viz/` | All matplotlib/display code. Calls sim and model. Never imported by lower layers. |

Current violations to fix:
- `src/quant2/simulate.py` has `print()` calls — move to `src/sim/`
- `src/quant2/viz.py` mixed with display logic — move to `src/viz/`
- `src/chapter01-qbits.py` duplicates simulation and viz inline — refactor to use layers

## Part B — Content and Style Separation

No HTML or CSS strings inside Python files:
- Lesson text in `chapters/chapterNN.md` — never hardcoded in Python
- Custom CSS in `src/styles/main.css` — loaded from file, not inline strings
- No `style="..."` attributes constructed in Python (matplotlib `ax.*` calls excepted)
- Python files contain only logic, layout wiring, and Streamlit component calls

## Part C — Streamlit Chapter Framework

Replace the `chapter01-qbits.py` CLI pattern (rich + separate matplotlib window) with Streamlit. Each chapter becomes `src/chapterNN-slug.py` — a Streamlit app with text and interactive viz inline in the browser.

Pattern established by `src/proto_streamlit.py`:
- Chapter markdown rendered inline via `st.markdown`
- Interactive controls (`st.slider`, `st.radio`) interleaved with text
- Matplotlib figures embedded inline via `st.pyplot`
- Deploys to Streamlit Cloud from `pitosalas/quant2` repo

`proto_streamlit.py` becomes the canonical `chapter01.py` once restructure is done.

## How to Demo
**Setup**: `uv sync`

**Steps**:
1. `uv run streamlit run src/chapter01.py`
2. Browser opens — chapter text and histogram on same page
3. Drag slider — histogram updates in place
4. Verify imports: `from sim.runner import run_trials` (not from quant2)

**Expected output**: Clean layer separation confirmed by import structure. Streamlit app runs with no errors.
