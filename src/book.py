#!/usr/bin/env python3
# book.py — Streamlit app rendering all chapters as one continuous book
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

CSS = (Path(__file__).parent / "styles" / "main.css").read_text()
SCROLL_TOP_JS = (Path(__file__).parent / "styles" / "scroll_top.js").read_text()

import viz.single_qubit_anim  # noqa: F401
import viz.qubit_grid  # noqa: F401
import viz.zero_qubit_grid  # noqa: F401
import viz.x_gate_grid  # noqa: F401
import viz.two_qubit_grid  # noqa: F401
import viz.entangled_grid  # noqa: F401
import viz.anticorrelated_grid  # noqa: F401
import viz.asymmetric_grid  # noqa: F401
import viz.two_qubit_bar  # noqa: F401
import viz.grover_anim  # noqa: F401
import viz.grover_start  # noqa: F401
import viz.grover_oracle  # noqa: F401
from chapter_renderer import render_chapter_text

BOOK_FILE = Path(__file__).parent.parent / "content" / "book_dialog.md"
BOOK_VERSION = "V1.5"
BOOK_DATE = "July 19 2026"
CHAPTER_SELECT_KEY = "chapter_select"
PENDING_CHAPTER_KEY = "pending_chapter"


def extract_introduction(text: str) -> str | None:
    """Return the Introduction section's content, if present.

    The Introduction is shown in a popup dialog rather than as a chapter,
    so it is not part of parse_dialogs.
    """
    sections = re.split(r"\n---\n", text)
    for section in sections:
        section = section.strip()
        if section.startswith("## Introduction"):
            return section
    return None


def parse_dialogs(text: str) -> list[tuple[str, str]]:
    """Split book text on --- into (chapter_label, content) pairs.

    Filters out non-section content (end-of-dialogue marker, etc.) and the
    Introduction section, which is shown separately in a popup dialog. Each
    remaining section's label is its own "## " heading text verbatim (e.g.
    "Dialog 1: Qubits") — the heading is the single source of truth for
    numbering, shared by the dropdown and the in-page chapter title.
    """
    sections = re.split(r"\n---\n", text)
    dialogs = []
    for section in sections:
        section = section.strip()
        if not section.startswith("## ") or section.startswith("## Introduction"):
            continue
        title = section.splitlines()[0][3:].strip()
        dialogs.append((title, section))
    return dialogs


def render_continue_button(target_label: str, key: str) -> None:
    """Render a button that advances the chapter dropdown to target_label.

    The dropdown's own session-state key can't be written after the widget
    is instantiated in this run, so the click just records the target and
    reruns; main() applies it before creating the widget on the next run.
    """
    if st.button("Continue to next Dialog →", key=key):
        st.session_state[PENDING_CHAPTER_KEY] = target_label
        st.rerun()


@st.dialog("Introduction")
def show_introduction(content: str) -> None:
    render_chapter_text(content, [0])


def render_byline(introduction: str | None) -> None:
    """Byline under the title: opens the Introduction popup when clicked.

    The GitHub link lives inside the Introduction popup content itself.
    """
    label = f"Pito Salas - {BOOK_VERSION} - {BOOK_DATE}"
    with st.container(key="byline"):
        if introduction:
            if st.button(label, key="byline_button"):
                show_introduction(introduction)
        else:
            st.markdown(label)


def main():
    st.set_page_config(page_title="The Quantum Computing Dialogs", layout="centered")
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
    st.title("The Quantum Computing Dialogs")

    text = BOOK_FILE.read_text()
    introduction = extract_introduction(text)
    render_byline(introduction)

    dialogs = parse_dialogs(text)
    chapter_labels = [label for label, _ in dialogs]
    content_by_label = dict(dialogs)

    pending = st.session_state.pop(PENDING_CHAPTER_KEY, None)
    if pending is not None:
        st.session_state[CHAPTER_SELECT_KEY] = pending
        st.iframe(f"<script>{SCROLL_TOP_JS}</script>", height=1)

    selected_label = st.selectbox(
        "Chapter",
        chapter_labels,
        key=CHAPTER_SELECT_KEY,
        label_visibility="collapsed",
    )
    i = chapter_labels.index(selected_label)

    viz_counter = [0]
    render_chapter_text(content_by_label[selected_label], viz_counter)
    if i < len(dialogs) - 1:
        render_continue_button(chapter_labels[i + 1], key=f"continue_{i}")


main()
