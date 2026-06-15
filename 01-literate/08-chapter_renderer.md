---
version: "2.0"
generated: "2026-06-15"
---

# chapter_renderer.py — Markdown Chapter Renderer with Visualization Directives

## The Problem It Solves

A chapter file mixes explanatory prose and live simulations. Pure `st.markdown`
handles prose. Viz directives (`:visualize name args`, `:static-viz name`) need
Python dispatch. `chapter_renderer` splits blocks on blank lines and routes each.

## Parsing Directives

```python
blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
for block in blocks:
    first_line = block.splitlines()[0]
    if first_line.startswith(":static-viz"):
        ...
    elif first_line.startswith(":visualize"):
        ...
    else:
        st.markdown(block)
```

Three cases: static viz (always visible), animated viz (button-gated), plain markdown.

## Non-Blocking Animated Vizs

Each `:visualize` directive gets its own `@st.fragment` closure. Fragments are
Streamlit's mechanism for re-running a UI subtree independently of the rest of
the page. Without them, all animations would serialize.

```python
def make_viz_fragment(name, args, key):
    @st.fragment
    def viz_fragment():
        step_key = f"{key}_step"
        if st.button("▶ Run Experiment", key=key):
            st.session_state[step_key] = 0
            st.rerun(scope="fragment")
        step = st.session_state.get(step_key, -1)
        if step < 0:
            return
        placeholder = st.empty()
        if registry.has_step_render(name):
            done = registry.render_step(name, args, step, key, placeholder)
            if done:
                st.session_state[step_key] = -1
            else:
                time.sleep(0.33)
                st.session_state[step_key] = step + 1
                st.rerun(scope="fragment")
        else:
            registry.render(name, args, placeholder)
            st.session_state[step_key] = -1
    return viz_fragment
```

The step counter lives in `st.session_state` under `{key}_step`. Each
`st.rerun(scope="fragment")` re-enters only that fragment — all other
animations on the page continue unaffected.

## Key Uniqueness

The `viz_counter` list (passed by reference) ensures unique keys across
all tabs and all chapter sections:

```python
key = f"replay_{name}_{viz_counter[0]}"
viz_counter[0] += 1
```

A shared counter across all dialogs prevents key collisions when the same
viz name appears in multiple tabs.

## Static Vizs

`:static-viz` bypasses the button and fragment entirely:

```python
registry.render_static(name, args)
```

Used for the legend, which must always be visible below the zero-qubit-grid.

## Entry Points

- `render_chapter_text(text, viz_counter)` — renders a string
- `render_chapter(path, viz_counter)` — reads a file, delegates to above
- `render_book(paths)` — renders multiple files in sequence

## Observations

- The `time.sleep(0.33)` inside `viz_fragment` blocks that fragment's thread.
  In Streamlit's threading model this is acceptable per-fragment, but under
  heavy concurrent use it could saturate worker threads.
- Step-based rendering and legacy blocking render coexist via `has_step_render`.
  Migrating all vizes to step-based would let the fallback branch be removed.
