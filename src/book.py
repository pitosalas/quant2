#!/usr/bin/env python3
# book.py — Streamlit app rendering all chapters as one continuous book
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

_CSS = (Path(__file__).parent / "styles" / "main.css").read_text()

import viz.single_qubit_anim  # noqa: F401
import viz.qubit_grid  # noqa: F401
import viz.x_gate_grid  # noqa: F401
import viz.two_qubit_grid  # noqa: F401
import viz.entangled_grid  # noqa: F401
import viz.anticorrelated_grid  # noqa: F401
import viz.asymmetric_grid  # noqa: F401
import viz.two_qubit_bar  # noqa: F401
import viz.grover_anim  # noqa: F401
from chapter_renderer import render_chapter

BOOK_FILE = Path(__file__).parent.parent / "content" / "book_dialog.md"


def main():
    st.set_page_config(page_title="quant2", layout="centered")
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
    render_chapter(BOOK_FILE)


main()
