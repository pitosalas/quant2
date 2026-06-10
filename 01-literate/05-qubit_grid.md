---
version: "1.0"
generated: "2026-06-10"
---

# qubit_grid — Animated Qubit Grid Visualization

## What It Does

`qubit_grid.py` implements the `qubit-grid` visualization directive for the chapter renderer. It runs N independent qubit experiments — each starting in |0⟩, passing through a Hadamard gate, then collapsing on measurement — and shows the results as an animated grid. The viewer watches the grid fill cell by cell, each box flipping from "?" to "0" or "1" and changing color.

This module sits at the visualization layer: it knows about Streamlit and matplotlib but nothing about chapter structure or simulation orchestration.

## Grid Layout

The grid uses a fixed column count (`COLS = 8`) so rows scale with N. Each cell occupies one matplotlib `Axes` subplot. Two lookup tables drive the rendering:

```python
COLORS = {
    "unmeasured": "#f0f0f0",
    0: "#cce0ff",
    1: "#ffcccc",
}
LABELS = {
    None: "?",
    0: "0",
    1: "1",
}
```

Using `None` as the unmeasured sentinel keeps the `results` list naturally typed as `list[int | None]` without a separate "pending" enum.

## The Figure Builder

`build_grid_figure` is a pure matplotlib function — no Streamlit dependency. This makes it unit-testable:

```python
def build_grid_figure(results: list[int | None], n: int) -> matplotlib.figure.Figure:
    rows = math.ceil(n / COLS)
    fig, axes = plt.subplots(rows, COLS, figsize=(10, 1.2 * rows))
```

The `figsize` is calibrated so rows stay compact (1.2 height units per row vs. the 8-wide figure). The caller must close the returned figure to avoid memory leaks.

Axes normalization handles the edge cases matplotlib creates:

```python
if rows == 1 and COLS == 1:
    axes_flat = [axes]
elif rows == 1:
    axes_flat = list(axes)
elif COLS == 1:
    axes_flat = list(axes)
else:
    axes_flat = [ax for row in axes for ax in row]
```

`plt.subplots` returns a 2D array, a 1D array, or a single Axes depending on shape — this block normalizes all cases to a flat list.

Each cell draws a rounded box via `FancyBboxPatch` in axes-coordinate space, then overlays two text elements: a small gray experiment number at the top and a bold outcome character centered in the box. Cells beyond `n` are hidden with `ax.set_visible(False)`.

## Animation Loop

`render` drives the Streamlit animation using a single `st.empty()` placeholder:

```python
def render(args: list[str]) -> None:
    n = int(args[0]) if args else 16
    results: list[int | None] = [None] * n
    placeholder = st.empty()

    for i in range(n):
        q = Qubit.zero().apply(H)
        results[i] = q.measure()
        fig = build_grid_figure(results, n)
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.07)
```

Each step: create a fresh H|0⟩ qubit, measure it, update the results list, redraw the full figure into the same placeholder (replacing the previous frame), then close the figure. The 70 ms sleep keeps the animation visually smooth without being sluggish.

`plt.close(fig)` after each `placeholder.pyplot` is essential — without it, matplotlib accumulates figures in memory for the full duration of the animation.

## Registration

The module self-registers at import time:

```python
registry.register("qubit-grid", render)
```

`chapter01.py` imports this module to trigger registration; the chapter renderer then calls `registry.render("qubit-grid", args)` when it encounters a `:visualize qubit-grid N` directive.

## Observations for Improvement

- **8 columns is hardcoded**: for small N (e.g. 4) the grid looks sparse. A `max(4, min(8, n))` column heuristic would scale better.
- **Full redraw per frame**: rebuilding the entire figure every step is O(N) per step, making total work O(N²). For large N (>100), pre-allocating patches and updating only the new cell's color/text would be significantly faster.
- **No pause after completion**: the final frame disappears if the page reruns. Calling `placeholder.pyplot(fig)` after the loop (without closing) would pin the final state.
- **`build_grid_figure` docstring is multi-line**: per the style guide, this method is complex enough to warrant explanation — but the current docstring describes *what*, not *why*. The non-obvious choice (caller must close the figure) is worth keeping; the obvious part ("returns a Figure") can go.
