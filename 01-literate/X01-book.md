---
version: "1.0"
generated: "2026-06-10"
---

# book.py — Streamlit App Entry Point

## What It Does

`book.py` is the top-level Streamlit script. It loads the CSS, imports all
visualization modules (triggering their self-registration), then renders the
single book file.

```python
import viz.single_qubit_anim   # noqa: F401  → registers "single-qubit"
import viz.qubit_grid           # noqa: F401  → registers "qubit-grid"
import viz.x_gate_grid          # noqa: F401  → registers "x-gate-grid"
import viz.two_qubit_grid       # noqa: F401  → registers "two-qubit-grid"
import viz.entangled_grid       # noqa: F401  → registers "entangled-grid"
import viz.anticorrelated_grid  # noqa: F401  → registers "anticorrelated-grid"
import viz.asymmetric_grid      # noqa: F401  → registers "asymmetric-grid"
import viz.two_qubit_bar        # noqa: F401  → registers "two-qubit-bar", "entangled-bar"
import viz.grover_anim          # noqa: F401  → registers "grover-anim"
```

The `# noqa: F401` comments suppress unused-import lint warnings — the imports
are purely for their side-effects (registration).

```python
BOOK_FILE = Path(__file__).parent.parent / "chapters" / "book.md"

def main():
    st.set_page_config(page_title="quant2", layout="centered")
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
    render_chapter(BOOK_FILE)

main()
```

## Notes

- `sys.path.insert(0, str(Path(__file__).parent))` at the top ensures
  `src/` is on the path when Streamlit runs the file directly.
- CSS is injected as a `<style>` block — Streamlit has no native way to load
  external stylesheets.
- The `main()` call at module level is required by Streamlit's execution model.
