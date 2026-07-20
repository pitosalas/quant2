# F20 — Introduction popup

**Priority**: Medium
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Add a short, first-person "how this was made" note (not the
Plato/Aristotle dialogue voice used by the other chapters) explaining why
and how this project was built — from a spoken conversation with Claude
about quantum computing basics, through a cleaned-up transcript, to a
Socratic dialogue, to this Streamlit app. It is not a book tab: a byline
under the page title — "Pito Salas - V1.5 - July 19 2026" — opens the note
in a popup dialog (`st.dialog`) when clicked; "github" alongside it is a
plain external link straight to the repo, independent of the popup. The six
dialogue chapters are unaffected and keep their original "Dialog N:"
numbering.

## How to Demo
**Setup**: `./run.bash` (or `uv run streamlit run src/book.py`).

**Steps**:
1. Open the app.
2. Confirm the byline "Pito Salas - V1.5 - July 19 2026 - github" appears
   as small text under the title.
3. Click the name/version/date part — a popup opens with the first-person
   note (a few short paragraphs, not the full original transcript essay).
4. Click "github" — opens the GitHub repo in a new tab, independent of the
   popup.
5. Confirm there is no separate "Introduction" tab, and the six dialogue
   tabs are labeled "Dialog 1: Qubits" through "Dialog 6: ...", unchanged.

**Expected output**: Popup opens with the note; "github" opens the repo
directly; tab bar shows only the six original dialogue chapters.
