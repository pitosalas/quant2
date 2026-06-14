#!/usr/bin/env python3
# entangled_grid.py — Animated entangled two-qubit grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time

import streamlit as st

from quant2.gates import H_I, CNOT
from sim.runner import run_trials_entangled
from viz import registry
from viz.two_qubit_grid import build_two_qubit_grid_html


def render(args: list[str], placeholder=None) -> None:
    """Animate n Bell-state experiments one at a time in the grid."""
    n = int(args[0]) if args else 16
    results: list[str | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        single = run_trials_entangled([H_I, CNOT], 1)
        outcome = next(k for k, v in single.items() if v > 0)
        results[i] = outcome
        placeholder.markdown(build_two_qubit_grid_html(results[:i+1], i+1), unsafe_allow_html=True)
        time.sleep(0.3)


registry.register("entangled-grid", render)
