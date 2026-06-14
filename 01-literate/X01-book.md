---
version: "1.1"
generated: "2026-06-13"
---

# book.py — The Entry Point of a Living Quantum Textbook

## Introduction

`book.py` is the top-level Streamlit application for `quant2`, an interactive
quantum computing textbook. It does very little on its own — and that is by
design. Its job is to assemble the pieces: load the stylesheet, trigger
registration of all visualization modules, point at the book's content file,
and hand control to the chapter renderer. The entire file is fewer than thirty
lines, yet it orchestrates every component in the system.

The pedagogical premise of `quant2` is that explanatory prose and runnable
quantum simulations should live side by side, as in the best tradition of
literate programming. A Plato-and-Aristotle dialog inhabits the same markdown
file as `:visualize` directives that launch live experiments. `book.py` is the
shell that makes that possible.

---

## Path Setup and Imports

The file begins by inserting its own directory onto `sys.path`. This is a
deliberate concession to Streamlit's execution model, which does not always run
the script from a predictable working directory.

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
```

This single line makes all sibling modules — `chapter_renderer`, the `viz`
package, and `styles` — importable by name, regardless of how Streamlit
launched the process. It is a pragmatic workaround rather than a packaging
solution; the tradeoff is simplicity over cleanliness.

With the path prepared, Streamlit itself is imported:

```python
import streamlit as st
```

---

## Loading the Stylesheet at Import Time

The CSS file is read once, at module load, before any Streamlit rendering occurs:

```python
_CSS = (Path(__file__).parent / "styles" / "main.css").read_text()
```

Using `Path(__file__).parent` anchors the lookup to the source file's location,
making the path robust to working-directory variation. The leading underscore on
`_CSS` signals that this is a module-level constant not intended for external
use. Reading the CSS eagerly avoids repeated disk access during rendering and
keeps the `main()` function focused on Streamlit calls rather than file I/O.

The tradeoff: if `main.css` is missing, the app crashes at import time rather
than at render time. For a teaching app served in a controlled environment,
that fail-fast behavior is acceptable and even desirable.

---

## Registering Visualizations via Side-Effecting Imports

The most unusual section of the file is a sequence of imports that appear to do
nothing:

```python
import viz.single_qubit_anim  # noqa: F401
import viz.qubit_grid  # noqa: F401
import viz.x_gate_grid  # noqa: F401
import viz.two_qubit_grid  # noqa: F401
import viz.entangled_grid  # noqa: F401
import viz.anticorrelated_grid  # noqa: F401
import viz.asymmetric_grid  # noqa: F401
import viz.two_qubit_bar  # noqa: F401
import viz.grover_anim  # noqa: F401
import viz.grover_start  # noqa: F401
import viz.grover_oracle  # noqa: F401
```

Each `viz.*` module, when imported, calls `viz.registry.register(name, fn)` to
enroll its render function under a string name. That name is the same token
that appears in the book's `:visualize` directives. The `chapter_renderer`
later looks names up in this registry and dispatches to the corresponding
function.

This pattern — import-for-side-effect — is a deliberate architectural choice.
It keeps each visualization self-contained: the module owns its own name, its
own render logic, and its own registration call. `book.py` does not need to
know anything about any individual visualization; it just needs to ensure the
modules have been loaded. The `# noqa: F401` comments suppress linter warnings
about "imported but unused" symbols, which would otherwise fire because no
name from these imports is referenced directly.

The cost of this pattern is opacity. A reader scanning `book.py` cannot tell
from this file alone what visualizations exist or what their names are. They
must open each `viz/` module to find out. This is the standard tradeoff of
registry-based dispatch.

---

## Pointing at the Content File

The book's prose lives outside the `src/` tree:

```python
BOOK_FILE = Path(__file__).parent.parent / "content" / "book_dialog.md"
```

`Path(__file__).parent.parent` walks up one level from `src/` to the project
root, then descends into `content/`. This keeps source code and content
cleanly separated in the repository. It also means the content file can be
edited — even by non-programmers — without touching any Python.

---

## The main() Function

The application entry point is compact by design:

```python
def main():
    st.set_page_config(page_title="quant2", layout="centered")
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
    render_chapter(BOOK_FILE)
```

`st.set_page_config` must be the first Streamlit call in any session;
Streamlit enforces this. The `layout="centered"` choice constrains content
width, which is appropriate for a reading experience — wide layouts suit
dashboards, not text.

The CSS is injected via `st.markdown` with `unsafe_allow_html=True`. This is
the standard Streamlit idiom for applying global styles. There is no safer
alternative in the current Streamlit API for injecting a stylesheet; the risk
is low because the CSS content comes from a file in the project, not from user
input.

`render_chapter(BOOK_FILE)` hands control to `chapter_renderer.py`, which
reads the markdown file, splits it into paragraph-sized blocks, and dispatches
each block to either `st.markdown` (for prose) or the visualization registry
(for `:visualize` directives).

---

## The Invocation Pattern

The file ends with a bare call rather than the conventional guard:

```python
main()
```

This is intentional. Streamlit re-executes the entire script on each user
interaction. The `if __name__ == "__main__":` guard is meaningless in that
context — Streamlit always runs the script as a module, not as `__main__` in
the traditional sense. Calling `main()` unconditionally is clearer and
functionally equivalent.

---

## Observations on Improvement

**Registration brittleness.** The eleven explicit `import viz.*` lines must be
kept in sync with the set of modules in `viz/`. Adding a new visualization
requires editing `book.py` as well as creating the module. A more robust
approach would be to auto-discover all modules in `viz/` at startup — for
example, by iterating `Path(__file__).parent.glob("viz/*.py")` and importing
them programmatically. This would make adding a visualization a single-file
operation.

**Side-effecting imports are fragile.** The import-for-side-effect pattern
works, but it violates the principle that imports should not have behavioral
consequences. An alternative is to have each module expose a `register()`
function that `book.py` calls explicitly. This makes the registration
relationship visible in the calling code rather than hidden inside the imported
module.

**CSS fail-fast vs. graceful degradation.** Reading `_CSS` at import time
means a missing stylesheet crashes the app before any page renders. A
try/except around the read, falling back to an empty string with a logged
warning, would allow the app to function (albeit unstyled) even if the CSS
file is absent. Whether that is preferable depends on deployment discipline.

**Single book file.** `BOOK_FILE` is hardcoded to one path. The
`chapter_renderer` module already provides a `render_book(paths)` function that
accepts a list of chapter files. If the book grows, `book.py` will need to be
updated to pass multiple files. Externalizing the chapter list to a config file
or a directory scan would make that transition easier.

**No error handling around `render_chapter`.** If `BOOK_FILE` does not exist,
the app raises an unhandled `FileNotFoundError`. A brief try/except with a
`st.error(...)` message would produce a more informative failure for a user
encountering a misconfigured deployment.
