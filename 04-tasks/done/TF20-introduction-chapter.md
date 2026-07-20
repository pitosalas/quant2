# TF20 — Introduction popup

Feature: F20-introduction-chapter

## Tasks

1. **Write the Introduction content** — done
   Turn the author's dictated notes into a first-person "## Introduction"
   section in `content/book_dialog.md` — three short paragraphs, a middle
   ground between the full original transcript-derived essay and an
   over-condensed two-sentence version.
   Test: manual read-through for accuracy (no mechanical test applies to
   prose content).

2. **Exclude Introduction from book tabs; extract it for a popup** — done
   Added `extract_introduction(text)` to `book.py`, returning the
   Introduction section's content if present. `parse_dialogs` skips any
   section titled "Introduction" entirely (no tab, no dialog number
   consumed) — the six dialogue chapters keep their original "Dialog N:"
   numbering.
   Test: `test_extract_introduction_present`, `test_extract_introduction_absent`,
   `test_parse_dialogs_excludes_introduction`, `test_parse_dialogs_real_book`
   (6 dialogs).

3. **Byline replaces the "what is this" link** — done
   Added `render_byline()` in `book.py`: a button labeled "Pito Salas - V1.5
   - July 19 2026" that opens the `show_introduction` popup when clicked,
   laid out inline (via `.st-key-byline` flex CSS) next to a plain `<a>` tag
   for "github" pointing at the repo — the GitHub link does not go through
   the popup/button at all.
   Test: manual click-through (`uv run streamlit run src/book.py`) — name
   opens the popup, "github" opens the repo in a new tab; no mechanical
   test for Streamlit dialog/CSS behavior.

4. **Run full suite** — done
   Test: `uv run pytest` — all 117 tests pass.
