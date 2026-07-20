# Current Session Handoff

**Date**: 2026-07-20
**Status**: F01–F21 complete. 120 tests passing.

## In Progress
- None

## Blocked
- None

## Completed This Session
- F20: Introduction popup
  - Short first-person "how this was made" note, byline ("Pito Salas - V1.5
    - July 19 2026") under the title opens it in an `st.dialog` popup
  - GitHub link lives inside the popup content
- F21: Chapter dropdown navigation
  - Replaced `st.tabs` with a `st.selectbox` dropdown — Streamlit's tab
    overflow-scroll affordances (arrow buttons, edge fade gradient) couldn't
    be made to look right against a fixed background color
  - "Dialog N: Title" labels live in the `## ` headings in
    `content/book_dialog.md` (single source of truth for dropdown + in-page
    title)
  - "Continue to next Dialog →" button at the bottom of each chapter, with
    scroll-to-top (`st.iframe` + injected JS targeting `[data-testid="stMain"]`,
    since `window.scrollTo` alone didn't hit Streamlit's actual scroll
    container)
- Fixed color scheme: background/text/tab/dropdown colors are now hardcoded
  (`#eeebe5` bg, `#2a2a2a` text, gold/black dropdown matching the buttons)
  instead of following system light/dark theme — several iterations to get
  legible in both modes and to kill Streamlit's theme-reactive nested
  styling on the dropdown control and popover menu
- Fixed a real bug: step-animations (`qubit-grid`, `x-gate-grid`,
  `two-qubit-grid`, and everything built on their shared helpers) reported
  "done" one step after drawing the final frame, via a call that drew
  nothing — erasing the last frame right after the animation finished.
  Regression tests added in `test_qubit_grid.py`, `test_two_qubit_grid.py`,
  new `test_x_gate_grid.py`
- Subtle divider line between dialogue turns (`.stMarkdown p` border-top)
- Fixed `src/book.py` syntax error (`sections 2= re.split(...)`) that was
  crashing the app on load
- Replaced deprecated `st.components.v1.html` with `st.iframe`
- Deployment: confirmed working on Streamlit Community Cloud — earlier "no
  github repo" error was a GitHub App authorization gap (fixed by
  reconnecting GitHub on share.streamlit.io); "app has gone to sleep" is
  normal free-tier idle behavior, not an error

## Completed Previous Sessions
- F19: Style guide compliance pass
- F15–F18: zero-qubit-grid, non-blocking animations, dialog navigation, prev/next nav buttons
- F07–F14: all quantum chapters, Grover’s oracle/start vizs, dialog style
- grover-start viz: equal superposition of 16 states
- grover-oracle viz: state 11 amplitude flipped negative (orange bar)

## Defined, Not Started
- Diffusion step visualization for 4-qubit Grover’s example (grover-diffusion)

## Next
1. Build grover-diffusion visualization showing amplitude amplification after one iteration
