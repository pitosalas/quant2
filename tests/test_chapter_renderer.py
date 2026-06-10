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


def test_visualize_directive_calls_registry_render(tmp_path):
    """:visualize foo 10 must call registry.render('foo', ['10'])."""
    chapter_file = _make_tmp_chapter(tmp_path, ":visualize foo 10")

    with patch("streamlit.markdown") as mock_md, \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    mock_render.assert_called_once_with("foo", ["10"])
    mock_md.assert_not_called()


def test_mixed_blocks(tmp_path):
    """Mixed blocks: text before and after a :visualize directive."""
    content = "Intro text\n\n:visualize bar 5\n\nTrailing text"
    chapter_file = _make_tmp_chapter(tmp_path, content)

    with patch("streamlit.markdown") as mock_md, \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    mock_render.assert_called_once_with("bar", ["5"])
    assert call("Intro text") in mock_md.call_args_list
    assert call("Trailing text") in mock_md.call_args_list


def test_visualize_with_no_args(tmp_path):
    """:visualize name with no extra args passes empty list to render."""
    chapter_file = _make_tmp_chapter(tmp_path, ":visualize myvis")

    with patch("streamlit.markdown"), \
         patch("viz.registry.render") as mock_render:
        import chapter_renderer
        chapter_renderer.render_chapter(chapter_file)

    mock_render.assert_called_once_with("myvis", [])
