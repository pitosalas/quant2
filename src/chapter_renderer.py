#!/usr/bin/env python3
# chapter_renderer.py — Render a markdown chapter file with inline viz directives
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path

import streamlit as st

from viz import registry


def make_viz_fragment(name: str, args: list[str], key: str):
    @st.fragment
    def viz_fragment():
        registry.render(name, args)
        st.button("▶ Replay", key=key)
    return viz_fragment


def render_chapter(path: Path, viz_counter: list[int] | None = None) -> None:
    """Read a markdown file and render each block, dispatching :visualize directives."""
    if viz_counter is None:
        viz_counter = [0]
    text = path.read_text()
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    for block in blocks:
        first_line = block.splitlines()[0]
        if first_line.startswith(":visualize"):
            words = first_line.split()
            name = words[1]
            args = words[2:]
            key = f"replay_{name}_{viz_counter[0]}"
            viz_counter[0] += 1
            make_viz_fragment(name, args, key)()
        else:
            st.markdown(block)


def render_book(paths: list[Path]) -> None:
    """Render multiple chapter files in sequence as one continuous page."""
    viz_counter = [0]
    for path in paths:
        render_chapter(path, viz_counter)
