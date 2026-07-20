# F21 — Chapter dropdown navigation

**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Replace Streamlit's native tab bar (`st.tabs`) with a
dropdown (`st.selectbox`) for choosing which chapter to view. Streamlit's
tab bar wraps to a horizontal scroll strip once labels overflow the width,
and its overflow-scroll affordances (arrow buttons, edge fade gradient)
could not be made to look right against this app's fixed background color
— the fade gradient in particular is designed to blend into Streamlit's own
theme background and rendered as a hard black-to-white bar, and CSS
overrides aimed at the arrow buttons made things worse (overlap, then
invisible controls). A dropdown sidesteps the whole problem. Labels keep
the original "Dialog N: Title" format. The dropdown is capped to 320px wide
(was stretching full-width), its background/text/border are hardcoded to
match the app's gold accent buttons (`#ffd700` bg, black text, `#ccaa00`
border, both closed and in the open option list, including a dark-gray
hover state) rather than following light/dark theme, and forced via
`!important` on every nested element since the closed control and the
open-menu portal both re-apply theme-based styling at multiple nesting
levels. The prev/next buttons that briefly existed alongside the dropdown
were removed — the dropdown alone is now the only navigation control.

## How to Demo
**Setup**: `./run.bash` (or `uv run streamlit run src/book.py`).

**Steps**:
1. Open the app — a "Chapter" dropdown appears instead of a tab bar,
   about a third of the page wide, styled gold/black like the "▶ Run
   Experiment" buttons, defaulting to "Dialog 1: Qubits".
2. Pick a different chapter from the dropdown — its content renders below.
   No separate prev/next buttons.
3. Open the dropdown and hover an option — background goes dark gray with
   white text; closed and open states both stay gold/black regardless of
   system light/dark mode.

**Expected output**: No tab bar, no scroll arrows/gradient artifacts, no
prev/next buttons; a narrow gold-styled dropdown navigates between all six
chapters.
