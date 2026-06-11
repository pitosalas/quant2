---
version: "1.0"
generated: "2026-06-10"
---

# registry.py — Named Visualization Registry

## What It Does

The registry is the glue between markdown chapter files and Python
visualisation code. A chapter file contains inline directives like:

```
:visualize qubit-grid 16
```

The renderer looks up `"qubit-grid"` in the registry and calls the associated
Python function. This decouples chapter content from implementation — a new
visualization is added in one place (its own module) and referenced by name
in markdown.

## Implementation

```python
REGISTRY: dict[str, callable] = {}

def register(name: str, fn: callable) -> None:
    REGISTRY[name] = fn

def render(name: str, args: list[str], placeholder=None) -> None:
    if name not in REGISTRY:
        registered = list(REGISTRY.keys())
        raise ValueError(f"Unknown visualization {name!r}. Registered: {registered}")
    REGISTRY[name](args, placeholder)
```

Three design choices worth noting:

1. **Module-level dict**: all viz modules are imported at startup in `book.py`,
   causing each module to call `register()` at import time. No explicit
   registration step is needed.

2. **Fail loud on unknown names**: rather than silently skipping an unknown
   directive, `render` raises `ValueError` with the list of registered names.
   Typos in markdown fail immediately.

3. **Optional placeholder**: the `placeholder` parameter is a Streamlit
   `st.empty()` container for animations. Passing it through here keeps
   render functions unaware of where they are placed on the page.

## Registration Pattern

Each viz module ends with:

```python
registry.register("qubit-grid", render)
```

This mirrors plugin patterns — each module self-registers when imported.
`book.py` drives all imports:

```python
import viz.qubit_grid        # registers "qubit-grid"
import viz.two_qubit_grid    # registers "two-qubit-grid"
import viz.grover_anim       # registers "grover-anim"
# ...
```

## Possible Improvements

- **Duplicate registration warning**: currently a second `register()` call
  silently overwrites the first. A warning would catch accidental duplicate
  names.
- **Typed callable signature**: `callable` is untyped. A `Protocol` for
  `(args: list[str], placeholder) -> None` would enable static type-checking
  of render functions.
