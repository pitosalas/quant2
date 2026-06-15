# TF18 — Prev/Next Dialog Navigation Buttons

## T01 — Add render_nav_button helper to book.py
**Status**: done
**Description**: Add `render_nav_button(target_label, button_text, key)` that on click sets session state and reruns; on rerun injects JS via `st.components.v1.html` to click the target tab.
**Test**: Button renders; clicking sets session state key.

## T02 — Wire prev/next into tab loop
**Status**: done
**Description**: In `main()`, wrap `render_chapter_text` with conditional prev (top, skip for i==0) and next (bottom, skip for last) nav buttons.
**Test**: Dialog 1 has no prev; dialog 6 has no next; middle dialogs have both.

## T03 — Tests
**Status**: done
**Description**: Unit test `parse_dialogs` still passes; integration: verify button keys are unique across tabs.
**Test**: pytest passes — 114 tests pass.
