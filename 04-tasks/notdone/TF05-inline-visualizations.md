# TF05 — Named Inline Visualizations

Task file for F05.

## T01 — src/viz/registry.py
**Status**: done
**Description**: Create `src/viz/registry.py`. Dict `REGISTRY: dict[str, callable]` mapping viz name → render function. Provide `register(name, fn)` and `render(name, args)` helpers. `render` raises `KeyError` with clear message if name not found.
**Test**: `tests/test_registry.py` — register a stub fn, call render, verify it's called with correct args.

## T02 — src/chapter_renderer.py
**Status**: done
**Description**: Create `src/chapter_renderer.py` with `render_chapter(path: Path) -> None`. Reads markdown file, splits into blocks on blank lines. For each block: if starts with `:visualize`, parse words → `name=words[1]`, `args=words[2:]`, call `registry.render(name, args)`. Otherwise call `st.markdown(block)`.
**Test**: `tests/test_chapter_renderer.py` — mock registry, verify `:visualize foo 10` calls render("foo", ["10"]) and plain text calls st.markdown.

## T03 — src/viz/single_qubit_anim.py
**Status**: done
**Description**: Create `src/viz/single_qubit_anim.py`. Implements `render(args: list[str]) -> None`. Reads `n = int(args[0]) if args else 20`. Uses `st.empty()` to animate: loop N times, measure H|0⟩, update running counts bar chart in the placeholder, `time.sleep(0.15)`. Register as `"single-qubit"` in registry.
**Test**: Not feasible to unit test Streamlit rendering. Manual: run chapter01 and observe animation.

## T04 — Update chapter01.py to use chapter_renderer
**Status**: done
**Description**: Replace manual markdown parsing in `src/chapter01.py` with `render_chapter(CHAPTER_FILE)`. Remove the inline paragraph-splitting logic.
**Test**: `uv run streamlit run src/chapter01.py` renders correctly (manual).

## T05 — Add :visualize directive to chapter01.md
**Status**: done
**Description**: Add `:visualize single-qubit 30` at the appropriate point in `chapters/chapter01.md` where the animation should appear inline.
**Test**: Manual — animation appears in correct position between text blocks.

## T06 — All tests pass
**Status**: done
**Description**: `uv run pytest` exits 0.
**Test**: `uv run pytest` — all tests pass.
