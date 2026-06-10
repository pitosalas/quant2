# F03 — Chapter CLI: Rich Text + Interactive Illustration

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: Per-chapter scripts that display chapter markdown and interactive illustrations. Pattern: `src/chapterNN-slug.py`. Chapter text lives in `chapters/chapterNN.md`. No tests for the CLI scripts themselves (UI/display code); quantum model layer is tested separately in F01.

## How to Demo
**Setup**: `uv sync`

**Steps**:
1. `uv run python src/chapter01-qbits.py`
2. Read chapter text rendered in terminal
3. Interactive matplotlib window opens
4. Drag θ slider — watch α, β and measurement distribution update live

**Expected output**: Rich panel with chapter text in terminal. Matplotlib histogram updating reactively as slider moves.
