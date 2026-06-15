#!/usr/bin/env python3
# test_chapter_renderer.py — Tests for chapter_renderer.render_chapter
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch, call
import pytest


def _make_tmp_chapter(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "test_chapter.md"
    p.write_text(content)
    return p


def test_plain_text_calls_st_markdown(tmp_path):
    """Plain text blocks must be forwarded to st.markdown."""
    chapter_file = _make_tmp_chapter(tmp_path, "Hello world\n\nSecond paragraph")

    with patch("streamlit.markdown") as mock_md, \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    mock_render.assert_not_called()
    assert call("Hello world") in mock_md.call_args_list
    assert call("Second paragraph") in mock_md.call_args_list


def _noop_fragment(fn):
    """Stand-in for st.fragment that executes the function directly (no Streamlit runtime needed)."""
    return fn


def test_visualize_directive_calls_registry_render(tmp_path):
    """:visualize foo 10 must call registry.render('foo', ['10'], ...)."""
    chapter_file = _make_tmp_chapter(tmp_path, ":visualize foo 10")

    with patch("streamlit.markdown") as mock_md, \
         patch("streamlit.button"), \
         patch("streamlit.fragment", _noop_fragment), \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    assert mock_render.call_count == 1
    assert mock_render.call_args[0][0] == "foo"
    assert mock_render.call_args[0][1] == ["10"]
    mock_md.assert_not_called()


def test_mixed_blocks(tmp_path):
    """Mixed blocks: text before and after a :visualize directive."""
    content = "Intro text\n\n:visualize bar 5\n\nTrailing text"
    chapter_file = _make_tmp_chapter(tmp_path, content)

    with patch("streamlit.markdown") as mock_md, \
         patch("streamlit.button"), \
         patch("streamlit.fragment", _noop_fragment), \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    assert mock_render.call_count == 1
    assert mock_render.call_args[0][0] == "bar"
    assert mock_render.call_args[0][1] == ["5"]
    assert call("Intro text") in mock_md.call_args_list
    assert call("Trailing text") in mock_md.call_args_list


def test_visualize_with_no_args(tmp_path):
    """:visualize name with no extra args passes empty list to render."""
    chapter_file = _make_tmp_chapter(tmp_path, ":visualize myvis")

    with patch("streamlit.markdown"), \
         patch("streamlit.button"), \
         patch("streamlit.fragment", _noop_fragment), \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    assert mock_render.call_args[0][0] == "myvis"
    assert mock_render.call_args[0][1] == []


def test_parse_dialogs_count_and_titles():
    """parse_dialogs must return one entry per ## section, excluding end markers."""
    import sys
    sys.path.insert(0, "src")
    from book import parse_dialogs

    text = "## Alpha\n\ncontent\n\n---\n\n## Beta\n\ncontent\n\n---\n\n*End of dialogue*"
    dialogs = parse_dialogs(text)
    assert len(dialogs) == 2
    assert dialogs[0][0] == "Dialog 1: Alpha"
    assert dialogs[1][0] == "Dialog 2: Beta"


def test_parse_dialogs_filters_non_sections():
    """parse_dialogs must skip sections not starting with ##."""
    import sys
    sys.path.insert(0, "src")
    from book import parse_dialogs

    text = "## Real\n\ncontent\n\n---\n\n*End of dialogue*"
    dialogs = parse_dialogs(text)
    assert len(dialogs) == 1
    assert "Real" in dialogs[0][0]


def test_parse_dialogs_real_book():
    """parse_dialogs on the actual book_dialog.md must return 6 dialogs."""
    import sys
    from pathlib import Path
    sys.path.insert(0, "src")
    from book import parse_dialogs

    book_file = Path("content/book_dialog.md")
    if not book_file.exists():
        return  # skip if not in project root
    dialogs = parse_dialogs(book_file.read_text())
    assert len(dialogs) == 6
