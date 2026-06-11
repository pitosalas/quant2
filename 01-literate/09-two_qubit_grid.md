---
version: "1.1"
generated: "2026-06-11"
---

# two_qubit_grid.py — Animated Two-Qubit Measurement Grid

## Concept

The two-qubit grid visualizes quantum measurements as a familiar metaphor:
binary words. Each experiment shows two qubits side-by-side in a rectangular
cell with a divider, like a 2-bit register. The left cell is qubit 0, the
right is qubit 1. Blue means 0; red means 1.

This makes joint outcomes like `"01"` visually unambiguous — you see two
separate coloured icons and digits, one per qubit position.

## HTML Architecture

Rather than using Matplotlib, the grid is rendered as HTML injected via
`st.markdown(unsafe_allow_html=True)`. This gives fine-grained CSS control
and efficient incremental updates — only the grid HTML changes as each
experiment result arrives.

Assets are loaded at module import time:

```python
_HERE = Path(__file__).parent
_CSS = (_HERE / "two_qubit_grid.css").read_text()
_TEMPLATE = (_HERE / "two_qubit_grid.html").read_text()
_SVG_ICON = (_HERE / "../../content/images/qbit.svg").resolve().read_text()
```

The SVG icon is loaded from `content/images/qbit.svg` relative to the repo
root — the same shared asset used by `qubit_grid.py`. The `resolve()` call
normalises the traversal path at import time.

Per `codereview.md`: no inline CSS or HTML strings in Python — they live in
separate asset files.

## Cell Construction

Each cell is a two-qubit "word" with a label, two icons, and two digit labels:

```python
def build_two_qubit_cell_html(idx: int, outcome: str | None) -> str:
    if outcome is None:
        b0, b1 = None, None
    else:
        b0, b1 = outcome[0], outcome[1]

    bit0_html = (
        f'<div class="tqg-bit" style="color:{COLORS[b0]};">'
        f'{bit_svg(b0)}'
        f'<span class="tqg-bitval">{label0}</span>'
        f'</div>'
    )
    # similar for bit1_html ...
    return f'<div class="tqg-cell"> ... </div>'
```

When `outcome is None` (not yet measured), both bits show grey `?`. This lets
the grid render all N slots immediately, with unmeasured slots visually
distinct.

## SVG Qubit Icon

The shared qubit icon from `content/images/qbit.svg` is inlined into each bit
cell, resized to `1.5em`:

```python
def bit_svg(bit: str | None) -> str:
    sized = _SVG_ICON.replace('width="1em" height="1em"', 'width="1.5em" height="1.5em"')
    color = COLORS[bit]
    return f'<span class="tqg-icon" style="color:{color};">{sized}</span>'
```

Colour is applied via CSS `color:` on the wrapping span. The SVG uses
`currentColor` internally so a single SVG file serves all colour variants.

## Animation Loop

```python
def render(args: list[str], placeholder=None) -> None:
    n = int(args[0]) if args else 16
    results: list[str | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        single = run_trials_2qubit([H], [H], 1)
        outcome = next(k for k, v in single.items() if v > 0)
        results[i] = outcome
        placeholder.markdown(build_two_qubit_grid_html(results, n), unsafe_allow_html=True)
        time.sleep(0.3)
```

One trial at a time, the full grid HTML is rebuilt and pushed to the same
Streamlit placeholder. The 300ms delay makes the evolution visible.

## Shared Grid Builder

`build_two_qubit_grid_html` is also imported by `entangled_grid.py`,
`anticorrelated_grid.py`, and `asymmetric_grid.py`. All four visualizations
share the same visual layout; only the trial runner differs.

## Possible Improvements

- **Colour constants**: `COLORS` duplicates the same hex codes as `qubit_grid.py`.
  A shared `viz/colors.py` module would eliminate the duplication.
- **SVG resize string replacement**: the width/height swap is fragile — if the
  SVG template changes its attribute format, the replacement silently produces
  the wrong size. A proper SVG parser or template variable in the SVG file
  would be more robust.
