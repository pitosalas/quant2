#!/usr/bin/env python3
# qubit_grid.py — Animated qubit grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from pathlib import Path

import streamlit as st

from quant2.qubit import Qubit
from quant2.gates import H
from viz import registry


COLORS = {
    "unmeasured": "#aaaaaa",
    0: "#2266cc",
    1: "#cc2222",
}
LABELS = {
    None: "?",
    0: "0",
    1: "1",
}
COLS = 8

_HERE = Path(__file__).parent
_CSS = (_HERE / "qubit_grid.css").read_text()
_TEMPLATE = (_HERE / "qubit_grid.html").read_text()
_SVG_ICON = (_HERE / "../../images/qbit.svg").resolve().read_text()


def build_cell_html(idx: int, outcome: int | None) -> str:
    color = COLORS[outcome] if outcome is not None else COLORS["unmeasured"]
    label = LABELS[outcome]
    svg = _SVG_ICON.replace('width="1em" height="1em"', 'width="2em" height="2em"')
    return (
        f'<div class="qg-cell">'
        f'<div class="qg-label">experiment #{idx + 1}</div>'
        f'<span class="qg-icon" style="color:{color};">{svg}</span>'
        f'<div class="qg-outcome" style="color:{color};">{label}</div>'
        f'</div>'
    )


def build_grid_html(results: list[int | None], n: int) -> str:
    """Build HTML showing an n-cell qubit measurement grid.

    results is length n; each element is None (unmeasured), 0, or 1.
    Returns HTML string for st.markdown(unsafe_allow_html=True).
    """
    cells = "".join(build_cell_html(i, results[i]) for i in range(n))
    return _TEMPLATE.format(css=_CSS, cols=COLS, cells=cells)


def render(args: list[str], placeholder=None) -> None:
    """Animate n qubit measurements one at a time in the grid."""
    n = int(args[0]) if args else 16
    results: list[int | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        results[i] = Qubit.zero().apply(H).measure()
        placeholder.markdown(build_grid_html(results, n), unsafe_allow_html=True)
        time.sleep(0.07)


registry.register("qubit-grid", render)
