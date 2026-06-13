# TF13 — Plato/Aristotle Dialog Book

For Feature F13. Each task step includes a test where feasible.

## T01 — Create content/book_dialog.md
**Status**: done
**Description**: Write `content/book_dialog.md` as Plato/Aristotle Socratic dialogue covering all chapters from `book.md`. Use substance from `content/dialog.md`. Insert all `:visualize` directives at correct locations. Do not modify `content/book.md`.
**Test**: File exists; contains all six chapter headings; contains all `:visualize` directives present in `book.md`.

## T02 — Verify visualize directives match book.md
**Status**: done
**Description**: Check that every `:visualize` directive in `book.md` also appears in `book_dialog.md` at a semantically correct location.
**Test**: `grep ":visualize" content/book_dialog.md` output matches expected list from `book.md`.

## T03 — Wire book_dialog.md into Streamlit renderer (optional)
**Status**: deferred
**Description**: Add a toggle or selector in `src/book.py` to switch between `book.md` and `book_dialog.md`. Keep default as `book.md`.
**Note**: Dialog version adopted as the default; toggle not needed. `src/book.py` now points directly to `book_dialog.md`.
**Test**: Streamlit app loads dialog version without errors; all visualizations render.
