# TF04 — Code Restructure + Streamlit Chapter Framework

Task file for F04. Parts A/B/C match F04.

## Part A — Layer Separation

## T01 — Create src/sim/ layer
**Status**: done
**Description**: Create `src/sim/__init__.py` and `src/sim/runner.py`. Move trial-running logic from `src/quant2/simulate.py` into `run_trials(gate_sequence, n) -> dict[int,int]`. No `print()` anywhere. Delete `src/quant2/simulate.py`.
**Test**: `tests/test_sim.py` — `run_trials([H], 1000)` returns counts summing to 1000; `run_trials([X], 100)[1] == 100`.

## T02 — Create src/viz/ layer
**Status**: done
**Description**: Create `src/viz/__init__.py` and `src/viz/histogram.py`. Move `draw_histogram(counts, label) -> Figure` out of all Python files into `src/viz/histogram.py`. Move Bloch sphere and distribution chart code from `src/quant2/viz.py` to `src/viz/bloch.py`. Delete `src/quant2/viz.py`.
**Test**: `tests/test_viz.py` — `draw_histogram({0:50,1:50}, "test")` returns a `matplotlib.figure.Figure`.

## T03 — Clean src/quant2/ (model only)
**Status**: done
**Description**: After T01/T02, `src/quant2/` contains only `qubit.py`, `gates.py`, `measurement.py`, `__init__.py`. Remove `simulate.py` and `viz.py`. Update `__init__.py` exports.
**Test**: `grep -r 'import matplotlib\|import sim\|print(' src/quant2/ --include="*.py"` returns no hits.

## Part B — Content and Style Separation

## T04 — Extract CSS to src/styles/main.css
**Status**: done
**Description**: Create `src/styles/main.css`. Audit all `.py` files for inline `style="..."` strings and CSS. Move to the CSS file. Load in Streamlit via `st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)` reading from file. Matplotlib `ax.*` style calls are exempt.
**Test**: `grep -rn 'style="' src/ --include="*.py"` returns no hits (matplotlib calls excluded).

## T05 — Verify chapter text not duplicated in Python
**Status**: done
**Description**: Confirm all lesson prose lives only in `chapters/`. No chapter text hardcoded in any `.py` file. Python loads and renders from file only.
**Test**: Manual review — no paragraph-length strings in any chapter `.py` file.

## Part C — Streamlit Chapter Framework

## T06 — Rewrite chapter01 as Streamlit app
**Status**: done
**Description**: Replace `src/proto_streamlit.py` → `src/chapter01.py`. Import from `sim.runner` and `viz.histogram`. Load text from `chapters/chapter01.md`. No inline HTML or CSS. Delete `src/chapter01-qbits.py` and `src/proto_streamlit.py`.
**Test**: `uv run streamlit run src/chapter01.py` starts without error (manual; note in work log).

## T07 — All tests pass
**Status**: done
**Description**: Full test suite green after all restructuring. Fix any broken imports.
**Test**: `uv run pytest` exits 0 with ≥32 tests collected.
