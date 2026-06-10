#!/usr/bin/env python3
# chapter_renderer.py — Render a markdown chapter file with inline viz directives
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path

import streamlit as st

from viz import registry


def render_chapter(path: Path) -> None:
    """Read a markdown file and render each block, dispatching :visualize directives."""
    text = path.read_text()
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    for block in blocks:
        first_line = block.splitlines()[0]
        if first_line.startswith(":visualize"):
            words = first_line.split()
            name = words[1]
            args = words[2:]
            registry.render(name, args)
        else:
            st.markdown(block)
