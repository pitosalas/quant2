#!/usr/bin/env python3
# x_gate_grid.py — Grid visualization showing X gate always produces |1⟩
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time
from pathlib import Path

import streamlit as st

from quant2.qubit import Qubit
from quant2.gates import X
from viz import registry
from viz.qubit_grid import build_grid_html


def render(args: list[str], placeholder=None) -> None:
    """Animate n X-gate measurements — always 1, no randomness."""
    n = int(args[0]) if args else 16
    results: list[int | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        placeholder.markdown(build_grid_html(results[:i+1], i+1), unsafe_allow_html=True)
        time.sleep(0.18)
        results[i] = 0
        placeholder.markdown(build_grid_html(results[:i+1], i+1), unsafe_allow_html=True)
        time.sleep(0.4)
        results[i] = Qubit.zero().apply(X).measure()
        placeholder.markdown(build_grid_html(results[:i+1], i+1), unsafe_allow_html=True)
        time.sleep(0.07)


registry.register("x-gate-grid", render)
