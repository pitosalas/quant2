#!/usr/bin/env python3
# entangled_grid.py — Animated entangled two-qubit grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import streamlit as st

from quant2.gates import H_I, CNOT
from sim.runner import run_trials_entangled
from viz import registry
from viz.two_qubit_grid import animate_two_qubit_grid, build_two_qubit_grid_html


def render_step_entangled(args: list[str], step: int, key: str, placeholder) -> bool:
    return animate_two_qubit_grid(
        lambda: run_trials_entangled([H_I, CNOT], 1), args, step, key, placeholder
    )


def render(args: list[str], placeholder=None) -> None:
    """Blocking render — used as fallback."""
    import time
    n = int(args[0]) if args else 16
    results: list[str | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        placeholder.markdown(build_two_qubit_grid_html(results[:i + 1], i + 1), unsafe_allow_html=True)
        time.sleep(0.33)
        single = run_trials_entangled([H_I, CNOT], 1)
        results[i] = next(k for k, v in single.items() if v > 0)
        placeholder.markdown(build_two_qubit_grid_html(results[:i + 1], i + 1), unsafe_allow_html=True)
        time.sleep(0.33)


registry.register("entangled-grid", render)
registry.register_step("entangled-grid", render_step_entangled)
