---
version: "1.0"
generated: "2026-06-15"
---

# zero_qubit_grid.py — Fresh Qubit Always Collapses to Zero

## What It Demonstrates

A freshly created qubit (no gates applied) has amplitude alpha=1, beta=0.
It always collapses to 0 on measurement — no randomness, no superposition.
This viz makes that concrete: 20 cells fill in one by one, each going
yellow→blue, never red.

## Step-Based Animation Protocol

Each cell runs two frames:

1. **Frame 0 (even step)**: render pending cell (yellow ?)
2. **Frame 1 (odd step)**: measure, render result (blue 0)

```python
def render_step_zero(args, step, key, placeholder) -> bool:
    return animate_single_qubit_grid(lambda: Qubit.zero().measure(), args, step, key, placeholder)
```

The shared `animate_single_qubit_grid` from `qubit_grid.py` handles the
step/frame arithmetic. `render_step_zero` only supplies the measurement
function — `Qubit.zero().measure()` always returns 0.

## The Legend

A companion static viz (`zero-qubit-legend`) renders a bordered box
showing all three qubit states as they appear in the animations:

```python
def build_legend_html() -> str:
    cells = (
        build_legend_cell_html(PENDING_COLOR, "?", "unmeasured")
        + build_legend_cell_html(COLORS[0], "0", "measured: 0")
        + build_legend_cell_html(COLORS[1], "1", "measured: 1")
    )
    return _LEGEND_TEMPLATE.format(css=_CSS, cells=cells)
```

The legend uses `zero_qubit_legend.html` — a separate template that
wraps the 3 cells in a `<div class="qg-legend-box">` with a "LEGEND"
title and a visible border. CSS braces in that template must be doubled
(`{{`, `}}`) to survive Python's `.format()`.

## Registrations

```python
registry.register("zero-qubit-grid", render)          # blocking fallback
registry.register_step("zero-qubit-grid", render_step_zero)  # step-based
registry.register_static("zero-qubit-legend", render_legend) # always-visible
```

In the chapter file:
```
:visualize zero-qubit-grid 20
:static-viz zero-qubit-legend
```

## Color Scheme

| State | Color | Meaning |
|-------|-------|---------|
| Yellow `#ccaa00` | `?` | not yet measured |
| Blue `#2266cc` | `0` | collapsed to zero |
| Red `#cc2222` | `1` | collapsed to one |

## Observations

- `render()` (blocking fallback) and `render_step_zero()` have duplicated
  logic for displaying pending cells. If the fallback is never called in
  production, it could be removed.
- The legend could be parameterized to show only the colors relevant to
  the current viz, but three states are always worth showing — the viewer
  needs to know what red means even if it never appears here.
