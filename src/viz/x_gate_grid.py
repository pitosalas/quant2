#!/usr/bin/env python3
# x_gate_grid.py — Grid visualization showing X gate always produces |1⟩
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time

import streamlit as st

from quant2.qubit import Qubit
from quant2.gates import X
from viz import registry
from viz.qubit_grid import build_grid_html, build_pending_grid_html


def render_step_x_gate(args: list[str], step: int, key: str, placeholder) -> bool:
    """3 frames per cell: ? (pending) → 0 (initial state) → 1 (after X gate)."""
    n = int(args[0]) if args else 16
    results_key = f"{key}_results"

    if step == 0:
        st.session_state[results_key] = [None] * n
    results = st.session_state.get(results_key, [None] * n)

    cell = step // 3
    if cell >= n:
        st.session_state.pop(results_key, None)
        return True

    frame = step % 3
    if frame == 0:
        html = build_pending_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
    elif frame == 1:
        results[cell] = 0
        st.session_state[results_key] = results
        html = build_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
    else:
        results[cell] = Qubit.zero().apply(X).measure()
        st.session_state[results_key] = results
        html = build_grid_html(results[:cell + 1], cell + 1)
        placeholder.markdown(html, unsafe_allow_html=True)

    return False


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
        results[i] = 0
        html = build_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)
        results[i] = Qubit.zero().apply(X).measure()
        html = build_grid_html(results[:i + 1], i + 1)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.33)


registry.register("x-gate-grid", render)
registry.register_step("x-gate-grid", render_step_x_gate)
