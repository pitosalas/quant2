# F05 — Named Inline Visualizations

**Priority**: High
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: Chapter markdown can embed named interactive visualizations inline using a `:visualize` directive. The Streamlit chapter renderer detects these lines and replaces them with live widgets.

## Directive syntax

```
:visualize <name> [arg1] [arg2] ...
```

- Line must start with `:visualize`
- Words after `:visualize` are split on whitespace: first word = name, rest = positional args (strings)
- Each viz function decides how to interpret its args
- Other `:` directives may be added in future using the same parsing pattern

## Architecture

- `src/viz/registry.py` — dict mapping name → render function. Each render fn signature: `render(args: list[str]) -> None` (calls Streamlit directly).
- `src/chapter_renderer.py` — reads a markdown file, splits on `\n\n`, renders each block: plain blocks via `st.markdown`, `:visualize` lines via registry lookup.
- Viz functions live in `src/viz/` and register themselves in `registry.py`.

## First visualization: `single-qubit`

Name: `single-qubit`  
Args: `[n_experiments]` (default 20)

Shows N qubit measurement experiments one at a time using `st.empty()` + loop. Each step: create H|0⟩ qubit, measure it, display running tally as a bar chart. Pause briefly between steps so reader can watch results accumulate. Final state shows full histogram.

## How to Demo
**Setup**: `uv sync`

**Steps**:
1. Add `:visualize single-qubit 30` to `chapters/chapter01.md`
2. `uv run streamlit run src/chapter01.py`
3. Observe chapter text renders, then visualization runs in place

**Expected output**: Text above, animated bar chart accumulating 30 measurements, text below.
