#!/usr/bin/env python3
# chapter02.py — Streamlit app for Chapter 2: Two-Qubit Systems
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

import viz.two_qubit_grid  # noqa: F401 — registers "two-qubit-grid" on import
import viz.entangled_grid  # noqa: F401 — registers "entangled-grid" on import
from chapter_renderer import render_chapter

CHAPTER_FILE = Path(__file__).parent.parent / "chapters" / "chapter02.md"


def main():
    st.set_page_config(page_title="quant2 — Chapter 2", layout="centered")
    render_chapter(CHAPTER_FILE)


main()
