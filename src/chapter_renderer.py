#!/usr/bin/env python3
# chapter_renderer.py — Render a markdown chapter file with inline viz directives
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from pathlib import Path

import streamlit as st

from viz import registry


def make_viz_fragment(name: str, args: list[str], key: str):
    @st.fragment
    def viz_fragment():
        step_key = f"{key}_step"

        if st.button("▶ Run Experiment", key=key):
            st.session_state[step_key] = 0
            st.rerun(scope="fragment")

        step = st.session_state.get(step_key, -1)
        if step < 0:
            return

        placeholder = st.empty()

        if registry.has_step_render(name):
            done = registry.render_step(name, args, step, key, placeholder)
            if done:
                st.session_state[step_key] = -1
            else:
                time.sleep(0.33)
                st.session_state[step_key] = step + 1
                st.rerun(scope="fragment")
        else:
            registry.render(name, args, placeholder)
            st.session_state[step_key] = -1

    return viz_fragment


def render_chapter_text(text: str, viz_counter: list[int] | None = None) -> None:
    """Render a markdown string, dispatching :visualize and :static-viz directives."""
    if viz_counter is None:
        viz_counter = [0]
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    for block in blocks:
        first_line = block.splitlines()[0]
        if first_line.startswith(":static-viz"):
            words = first_line.split()
            name, args = words[1], words[2:]
            registry.render_static(name, args)
        elif first_line.startswith(":visualize"):
            words = first_line.split()
            name = words[1]
            args = words[2:]
            key = f"replay_{name}_{viz_counter[0]}"
            viz_counter[0] += 1
            make_viz_fragment(name, args, key)()
        else:
            st.markdown(block)


def render_chapter(path: Path, viz_counter: list[int] | None = None) -> None:
    """Read a markdown file and render it."""
    if viz_counter is None:
        viz_counter = [0]
    render_chapter_text(path.read_text(), viz_counter)


def render_book(paths: list[Path]) -> None:
    """Render multiple chapter files in sequence as one continuous page."""
    viz_counter = [0]
    for path in paths:
        render_chapter(path, viz_counter)
