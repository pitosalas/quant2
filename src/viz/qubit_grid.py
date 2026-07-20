#!/usr/bin/env python3
# qubit_grid.py — Animated qubit grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from collections.abc import Callable
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
PENDING_COLOR = "#ccaa00"
COLS = 8

HERE = Path(__file__).parent
CSS = (HERE / "qubit_grid.css").read_text()
TEMPLATE = (HERE / "qubit_grid.html").read_text()
SVG_ICON = (HERE / "../../content/images/qubit.svg").resolve().read_text()


def build_cell_html(idx: int, outcome: int | None) -> str:
    if outcome is None:
        return (
            f'<div class="qg-cell">'
            f'<div class="qg-label">experiment #{idx + 1}</div>'
            f'<span class="qg-icon"></span>'
            f'<div class="qg-outcome"></div>'
            f'</div>'
        )
    color = COLORS[outcome]
    svg = SVG_ICON.replace('width="1em" height="1em"', 'width="2em" height="2em"')
    return (
        f'<div class="qg-cell">'
        f'<div class="qg-label">experiment #{idx + 1}</div>'
        f'<span class="qg-icon" style="color:{color};">{svg}</span>'
        f'<div class="qg-outcome" style="color:{color};">{LABELS[outcome]}</div>'
        f'</div>'
    )


def build_pending_cell_html(idx: int) -> str:
    svg = SVG_ICON.replace('width="1em" height="1em"', 'width="2em" height="2em"')
    return (
        f'<div class="qg-cell">'
        f'<div class="qg-label">experiment #{idx + 1}</div>'
        f'<span class="qg-icon" style="color:{PENDING_COLOR};">{svg}</span>'
        f'<div class="qg-outcome" style="color:{PENDING_COLOR};">?</div>'
        f'</div>'
    )


def build_grid_html(results: list[int | None], n: int) -> str:
    cells = "".join(build_cell_html(i, results[i]) for i in range(n))
    return TEMPLATE.format(css=CSS, cols=COLS, cells=cells)


def build_pending_grid_html(results: list[int | None], n: int) -> str:
    """Like build_grid_html but renders None cells as yellow '?' instead of empty."""
    cells = "".join(
        build_pending_cell_html(i)
        if results[i] is None
        else build_cell_html(i, results[i])
        for i in range(n)
    )
    return TEMPLATE.format(css=CSS, cols=COLS, cells=cells)


def animate_single_qubit_grid(
    measure_fn: Callable, args: list[str], step: int, key: str, placeholder
) -> bool:
    """Shared step renderer for single-qubit grids. 2 frames/cell: ? then result.

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
        html = build_pending_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
    else:
        results[cell] = measure_fn()
        st.session_state[results_key] = results
        html = build_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)

    return False


def render_step_qubit_grid(args: list[str], step: int, key: str, placeholder) -> bool:
    return animate_single_qubit_grid(
        lambda: Qubit.zero().apply(H).measure(), args, step, key, placeholder
    )


def render(args: list[str], placeholder=None) -> None:
    """Blocking render — used as fallback and in tests."""
    n = int(args[0]) if args else 16
    results: list[int | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        html = build_pending_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)
        results[i] = Qubit.zero().apply(H).measure()
        html = build_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)


registry.register("qubit-grid", render)
registry.register_step("qubit-grid", render_step_qubit_grid)
