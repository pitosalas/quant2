#!/usr/bin/env python3
# two_qubit_grid.py — Animated two-qubit unentangled grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from pathlib import Path

import streamlit as st

from sim.runner import run_trials_2qubit
from quant2.gates import H
from viz import registry


COLORS = {
    "0": "#2266cc",
    "1": "#cc2222",
    None: "#aaaaaa",
}
COLS = 4

_HERE = Path(__file__).parent
_CSS = (_HERE / "two_qubit_grid.css").read_text()
_TEMPLATE = (_HERE / "two_qubit_grid.html").read_text()
_SVG_ICON = (_HERE / "../../content/images/qbit.svg").resolve().read_text()


def bit_svg(bit: str | None) -> str:
    sized = _SVG_ICON.replace('width="1em" height="1em"', 'width="1.5em" height="1.5em"')
    color = COLORS[bit]
    return f'<span class="tqg-icon" style="color:{color};">{sized}</span>'


def build_two_qubit_cell_html(idx: int, outcome: str | None) -> str:
    """Build HTML for one two-qubit cell. outcome is '00'/'01'/'10'/'11' or None."""
    if outcome is None:
        b0, b1 = None, None
    else:
        b0, b1 = outcome[0], outcome[1]

    label0 = b0 if b0 is not None else "?"
    label1 = b1 if b1 is not None else "?"

    bit0_html = (
        f'<div class="tqg-bit" style="color:{COLORS[b0]};">'
        f'{bit_svg(b0)}'
        f'<span class="tqg-bitval">{label0}</span>'
        f'</div>'
    )
    bit1_html = (
        f'<div class="tqg-bit" style="color:{COLORS[b1]};">'
        f'{bit_svg(b1)}'
        f'<span class="tqg-bitval">{label1}</span>'
        f'</div>'
    )
    return (
        f'<div class="tqg-cell">'
        f'<div class="tqg-label">experiment #{idx + 1}</div>'
        f'<div class="tqg-word">{bit0_html}{bit1_html}</div>'
        f'</div>'
    )


def build_two_qubit_grid_html(results: list[str | None], n: int) -> str:
    """Build HTML for an n-cell two-qubit measurement grid."""
    cells = "".join(build_two_qubit_cell_html(i, results[i]) for i in range(n))
    return _TEMPLATE.format(css=_CSS, cols=COLS, cells=cells)


def render(args: list[str], placeholder=None) -> None:
    """Animate n two-qubit experiments one at a time in the grid."""
    n = int(args[0]) if args else 16
    results: list[str | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        single = run_trials_2qubit([H], [H], 1)
        outcome = next(k for k, v in single.items() if v > 0)
        results[i] = outcome
        placeholder.markdown(build_two_qubit_grid_html(results, n), unsafe_allow_html=True)
        time.sleep(0.3)


registry.register("two-qubit-grid", render)
