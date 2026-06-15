# TF17 — Multi-dialog navigation with fixed nav bar

## T01 — Add brief greeting to each dialog section in book_dialog.md
**Status**: done
**Description**: Add one short Plato/Aristotle opening line before first exchange in sections 2–6 (Quantum Gates, Two-Qubit Registers, Entangled Qubits, Grover's, Limits). Section 1 already has a full greeting.
**Test**: Each section starts with a Plato or Aristotle line when read cold.

## T02 — Refactor chapter_renderer: extract render_chapter_text(text, viz_counter)
**Status**: done
**Description**: Extract the block-rendering loop from render_chapter() into render_chapter_text(text, viz_counter). render_chapter() delegates to it. Keeps backward compat.
**Test**: Existing test_chapter_renderer.py passes unchanged.

## T03 — Add parse_dialogs() and tab navigation to book.py
**Status**: done
**Description**: Add parse_dialogs(text) -> list[(label, content)] splitting on \n---\n, filtering non-## sections, labeling "N. Title". Replace render_chapter() call in main() with st.tabs() loop using render_chapter_text(). Shared viz_counter across tabs prevents key collisions.
**Test**: App loads with 6 tabs; each tab renders its content with working animations.

## T04 — Tests
**Status**: done
**Description**: Add test for parse_dialogs: correct count, correct titles, no end-of-dialogue section included.
**Test**: pytest passes.
