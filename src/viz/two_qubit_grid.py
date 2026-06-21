#!/usr/bin/env python3
# two_qubit_grid.py — Animated two-qubit unentangled grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from collections.abc import Callable
from pathlib import Path

import streamlit as st

from sim.runner import run_trials_2qubit
from quant2.gates import H
from viz import registry


COLORS = {
    "0": "#2266cc",
    "1": "#cc2222",
    None: "#ccaa00",
}
COLS = 4

HERE = Path(__file__).parent
CSS = (HERE / "two_qubit_grid.css").read_text()
TEMPLATE = (HERE / "two_qubit_grid.html").read_text()
SVG_ICON = (HERE / "../../content/images/qubit.svg").resolve().read_text()


def bit_svg(bit: str | None) -> str:
    sized = SVG_ICON.replace(
        'width="1em" height="1em"', 'width="1.5em" height="1.5em"'
    )
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
    return TEMPLATE.format(css=CSS, cols=COLS, cells=cells)


def animate_two_qubit_grid(
    run_fn: Callable, args: list[str], step: int, key: str, placeholder
) -> bool:
    """Shared step renderer for two-qubit grids. 2 frames/cell: ?? then result.

    Returns True when all n cells are complete.
    """
    n = int(args[0]) if args else 16
    results_key = f"{key}_results"

    if step == 0:
        st.session_state[results_key] = [None] * n
    results = st.session_state.get(results_key, [None] * n)

    cell = step // 2
    if cell >= n:
        st.session_state.pop(results_key, None)
        return True

    frame = step % 2
    if frame == 0:
        html = build_two_qubit_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
    else:
        single = run_fn()
        results[cell] = next(k for k, v in single.items() if v > 0)
        st.session_state[results_key] = results
        html = build_two_qubit_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)

    return False


def render_step_two_qubit(args: list[str], step: int, key: str, placeholder) -> bool:
    return animate_two_qubit_grid(
        lambda: run_trials_2qubit([H], [H], 1), args, step, key, placeholder
    )


def render(args: list[str], placeholder=None) -> None:
    """Blocking render — used as fallback and in tests."""
    n = int(args[0]) if args else 16
    results: list[str | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        html = build_two_qubit_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)
        single = run_trials_2qubit([H], [H], 1)
        outcome = next(k for k, v in single.items() if v > 0)
        results[i] = outcome
        html = build_two_qubit_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)


registry.register("two-qubit-grid", render)
registry.register_step("two-qubit-grid", render_step_two_qubit)
