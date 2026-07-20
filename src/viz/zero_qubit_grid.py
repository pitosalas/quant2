#!/usr/bin/env python3
# zero_qubit_grid.py — Animated grid of fresh qubits, always measuring 0
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from pathlib import Path

import streamlit as st

from quant2.qubit import Qubit
from viz import registry
from viz.qubit_grid import (
    CSS, TEMPLATE, SVG_ICON, COLORS, COLS,
    PENDING_COLOR, build_pending_cell_html,
    animate_single_qubit_grid,
)

LEGEND_TEMPLATE = (Path(__file__).parent / "zero_qubit_legend.html").read_text()


def build_zero_cell_html(idx: int, outcome: int | None) -> str:
    if outcome is None:
        return build_pending_cell_html(idx)
    color = COLORS[outcome]
    svg = SVG_ICON.replace('width="1em" height="1em"', 'width="2em" height="2em"')
    return (
        f'<div class="qg-cell">'
        f'<div class="qg-label">experiment #{idx + 1}</div>'
        f'<span class="qg-icon" style="color:{color};">{svg}</span>'
        f'<div class="qg-outcome" style="color:{color};">{outcome}</div>'
        f'</div>'
    )


def build_zero_grid_html(results: list[int | None], n: int) -> str:
    cells = "".join(build_zero_cell_html(i, results[i]) for i in range(n))
    return TEMPLATE.format(css=CSS, cols=COLS, cells=cells)


def build_legend_cell_html(color: str, symbol: str, label: str) -> str:
    svg = SVG_ICON.replace('width="1em" height="1em"', 'width="2em" height="2em"')
    return (
        f'<div class="qg-cell">'
        f'<div class="qg-label">{label}</div>'
        f'<span class="qg-icon" style="color:{color};">{svg}</span>'
        f'<div class="qg-outcome" style="color:{color};">{symbol}</div>'
        f'</div>'
    )


def build_legend_html(text: str = "") -> str:
    cells = (
        build_legend_cell_html(PENDING_COLOR, "?", "unmeasured")
        + build_legend_cell_html(COLORS[0], "0", "measured: 0")
        + build_legend_cell_html(COLORS[1], "1", "measured: 1")
    )
    text_section = f'<div class="qg-legend-text">{text}</div>' if text else ""
    return LEGEND_TEMPLATE.format(css=CSS, cells=cells, text_section=text_section)


def render_step_zero(args: list[str], step: int, key: str, placeholder) -> bool:
    return animate_single_qubit_grid(
        lambda: Qubit.zero().measure(), args, step, key, placeholder
    )


def render_legend(args: list[str], placeholder=None) -> None:
    text = " ".join(args)
    st.markdown(build_legend_html(text), unsafe_allow_html=True)


def render(args: list[str], placeholder=None) -> None:
    """Blocking render — used as fallback and in tests."""
    n = int(args[0]) if args else 20
    results: list[int | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        html = build_zero_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)
        results[i] = Qubit.zero().measure()
        html = build_zero_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)


registry.register("zero-qubit-grid", render)
registry.register_step("zero-qubit-grid", render_step_zero)
registry.register_static("zero-qubit-legend", render_legend)
