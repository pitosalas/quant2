#!/usr/bin/env python3
# chapter01.py — Streamlit app for Chapter 1: Qubits
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

import viz.single_qubit_anim  # noqa: F401 — registers "single-qubit" on import
import viz.qubit_grid  # noqa: F401 — registers "qubit-grid" on import
from chapter_renderer import render_chapter

CHAPTER_FILE = Path(__file__).parent.parent / "chapters" / "chapter01.md"


def main():
    st.set_page_config(page_title="quant2 — Chapter 1", layout="centered")
    render_chapter(CHAPTER_FILE)


main()
