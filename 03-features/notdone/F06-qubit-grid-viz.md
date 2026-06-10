# F06 — Qubit Grid Visualization

**Priority**: High
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: New `:visualize` named visualization — `qubit-grid` — shows N qubit experiments as a grid of boxes, animating left-to-right top-to-bottom. Each cell starts with "?" and flips to "0" or "1" when that experiment is measured.

## Directive

```
:visualize qubit-grid 20
```

Arg: number of experiments (default 16).

## Visual design

- Grid of equal-sized boxes, ~4 columns wide
- Each box: label "Exp #N" above, large centered character inside — "?" before measured, "0" or "1" after
- Boxes for 0 outcomes: blue tint. Boxes for 1 outcomes: red tint. Unmeasured: light gray.
- Animation: one experiment per step, brief pause, redraws full grid each step
- Final frame stays visible (no loop)

## Implementation

- `src/viz/qubit_grid.py` — `render(args)`, registers as `"qubit-grid"`
- Uses `st.empty()` + matplotlib figure redrawn each step
- Imported in `chapter01.py` to trigger registration

## How to Demo
**Setup**: `uv sync`

**Steps**:
1. Add `:visualize qubit-grid 20` to a chapter markdown file
2. `uv run streamlit run src/chapter01.py`
3. Watch grid fill left-to-right, each cell flipping from ? to 0/1

**Expected output**: Animated grid, final state shows all results with color coding.
