#!/usr/bin/env python3
# book.py — Streamlit app rendering all chapters as one continuous book
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import streamlit.components.v1 as components

_CSS = (Path(__file__).parent / "styles" / "main.css").read_text()

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


def parse_dialogs(text: str) -> list[tuple[str, str]]:
    """Split book text on --- into (tab_label, content) pairs.

    Filters out non-section content (end-of-dialogue marker, etc.).
    """
    sections = re.split(r"\n---\n", text)
    dialogs = []
    for i, section in enumerate(sections, start=1):
        section = section.strip()
        if not section.startswith("## "):
            continue
        title = section.splitlines()[0][3:].strip()
        dialogs.append((f"Dialog {i}: {title}", section))
    return dialogs


def render_nav_button(target_label: str, button_text: str, key: str) -> None:
    """Render a nav button that switches to the target tab when clicked."""
    nav_key = f"{key}_target"
    if st.session_state.get(nav_key):
        del st.session_state[nav_key]
        safe_label = target_label.replace('"', '\\"')
        components.html(
            f"""<script>
            const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
            for (const t of tabs) {{
                if (t.textContent.trim() === "{safe_label}") {{ t.click(); break; }}
            }}
            </script>""",
            height=0,
        )
    if st.button(button_text, key=key):
        st.session_state[nav_key] = True
        st.rerun()


def main():
    st.set_page_config(page_title="The Quantum Computing Dialogs", layout="centered")
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
    st.title("The Quantum Computing Dialogs")

    text = BOOK_FILE.read_text()
    dialogs = parse_dialogs(text)
    tab_labels = [label for label, _ in dialogs]
    tabs = st.tabs(tab_labels)

    viz_counter = [0]
    for i, (tab, (_, content)) in enumerate(zip(tabs, dialogs)):
        with tab:
            if i > 0:
                render_nav_button(tab_labels[i - 1], f"← {tab_labels[i - 1]}", key=f"nav_prev_{i}")
            render_chapter_text(content, viz_counter)
            if i < len(dialogs) - 1:
                render_nav_button(tab_labels[i + 1], f"{tab_labels[i + 1]} →", key=f"nav_next_{i}")


main()
