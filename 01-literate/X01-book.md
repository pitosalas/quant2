---
version: "2.0"
generated: "2026-06-21"
---

# book.py — The Entry Point of a Living Quantum Textbook

## Introduction

`book.py` is the top-level Streamlit application for `quant2`. It orchestrates
every other component: loads stylesheets and a JS helper, triggers registration
of all visualization modules, reads the book's content, splits it into six
tabbed dialogs, and wires up previous/next navigation buttons between them.

The pedagogical structure is a Socratic dialog between Aristotle and Plato,
split across six chapters ("dialogs"). `book.py` renders those as Streamlit
tabs, with each tab containing prose and live quantum experiments side by side.

---

## Path Setup and Static Asset Loading

The file begins with a path fix for Streamlit's execution model, followed by
loading two static assets — a CSS stylesheet and a JS navigation helper:

```python
CSS = (Path(__file__).parent / "styles" / "main.css").read_text()
NAV_JS = (Path(__file__).parent / "styles" / "nav_button.js").read_text()
```

Both assets follow the prescribed pattern: loaded via `Path(__file__).parent`,
stored as module-level constants without leading underscores (per style guide).
Reading them eagerly at import time avoids repeated disk I/O per Streamlit
rerun, and fails fast if a file is missing.

The JS file (`nav_button.js`) contains the logic for clicking a Streamlit tab
programmatically. It uses a `NAV_TARGET_LABEL` placeholder that Python replaces
at render time with the actual tab label string. This keeps all JavaScript in
`.js` files and out of Python source.

---

## Registering Visualizations via Side-Effecting Imports

A sequence of imports trigger visualization registration as a side effect:

```python
import viz.single_qubit_anim  # noqa: F401
import viz.qubit_grid          # noqa: F401
# ... (11 modules total)
```

Each `viz.*` module calls `registry.register(name, fn)` on import. The
`chapter_renderer` later resolves `:visualize name` directives against this
registry. This pattern keeps each visualization self-contained; `book.py`
only needs to ensure the modules are loaded.

---

## Parsing the Book into Dialogs

The book is one markdown file with `---` separating sections. `parse_dialogs`
splits it and filters for sections that begin with `## `:

```python
def parse_dialogs(text: str) -> list[tuple[str, str]]:
    sections = re.split(r"\n---\n", text)
    dialogs = []
    for i, section in enumerate(sections, start=1):
        section = section.strip()
        if not section.startswith("## "):
            continue
        title = section.splitlines()[0][3:].strip()
        dialogs.append((f"Dialog {i}: {title}", section))
    return dialogs
```

The `if not section.startswith("## ")` guard silently drops end-of-file
markers and blank separators, so the content author can use `---` freely
without breaking the parser.

---

## Prev/Next Navigation

Each dialog tab (except the first) has a "← Previous" button at the top, and
each (except the last) has a "Next →" button at the bottom. The button logic
uses Streamlit session state plus a JS injection to switch tabs:

```python
def render_nav_button(target_label: str, button_text: str, key: str) -> None:
    nav_key = f"{key}_target"
    if st.session_state.get(nav_key):
        del st.session_state[nav_key]
        safe_label = target_label.replace('"', '\\"')
        js = NAV_JS.replace("NAV_TARGET_LABEL", f'"{safe_label}"')
        components.html(f"<script>{js}</script>", height=0)
    if st.button(button_text, key=key):
        st.session_state[nav_key] = True
        st.rerun()
```

The two-phase pattern is necessary because `components.html` runs in the
browser but `st.button` triggers a Python rerun. On click: set a flag and
rerun. On the next rerun: detect the flag, inject the JS that clicks the
tab, clear the flag. The JS itself lives in `nav_button.js`:

```javascript
const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
for (const t of tabs) {
    if (t.textContent.trim() === NAV_TARGET_LABEL) { t.click(); break; }
}
```

`NAV_TARGET_LABEL` is replaced by Python with the actual label string before
injection, keeping all JavaScript out of Python source files.

---

## The main() Function

```python
def main():
    st.set_page_config(page_title="The Quantum Computing Dialogs", layout="centered")
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
    st.title("The Quantum Computing Dialogs")

    text = BOOK_FILE.read_text()
    dialogs = parse_dialogs(text)
    tab_labels = [label for label, _ in dialogs]
    tabs = st.tabs(tab_labels)

    viz_counter = [0]
    for i, (tab, (_, content)) in enumerate(zip(tabs, dialogs)):
        with tab:
            if i > 0:
                render_nav_button(
                    tab_labels[i - 1], f"← {tab_labels[i - 1]}", key=f"nav_prev_{i}"
                )
            render_chapter_text(content, viz_counter)
            if i < len(dialogs) - 1:
                render_nav_button(
                    tab_labels[i + 1], f"{tab_labels[i + 1]} →", key=f"nav_next_{i}"
                )
```

`viz_counter` is a single-element list — a mutable container passed by
reference so `render_chapter_text` can increment a shared counter across all
tabs without global state. Each `:visualize` directive gets a unique key
derived from this counter, preventing Streamlit widget key collisions.

---

## Observations on Improvement

**Auto-discovery of viz modules.** The eleven explicit `import viz.*` lines
must be kept in sync with the `viz/` directory by hand. Scanning
`Path(__file__).parent.glob("viz/*.py")` and importing programmatically would
make adding a new visualization a single-file operation.

**NAV_JS label injection is fragile.** Replacing `NAV_TARGET_LABEL` as a bare
string works, but would fail if the placeholder string appeared elsewhere in
the JS. A structured template (e.g., using `string.Template`) would be more
robust.

**Book file is hardcoded.** `BOOK_FILE` is a fixed path. If the project
grows to multiple books or configurable content paths, this will need to
become a parameter or config value.

**No error handling on missing content file.** If `BOOK_FILE` is absent the
app raises an unhandled `FileNotFoundError`. A `st.error()` with a clear
message would be more useful in a deployed environment.
