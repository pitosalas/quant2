#!/usr/bin/env python3
# asymmetric_grid.py — Grid showing asymmetric entangled state (biased 00/11)
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import math
import time

import streamlit as st

from sim.runner import run_trials_asymmetric
from viz import registry
from viz.two_qubit_grid import build_two_qubit_grid_html

# θ = π/3 gives cos²(π/6) = 75% chance of |00⟩, sin²(π/6) = 25% chance of |11⟩
THETA = math.pi / 3


def render(args: list[str], placeholder=None) -> None:
    """Animate n asymmetric entangled experiments. Outcomes are 00 (~75%) or 11 (~25%)."""
    n = int(args[0]) if args else 16
    results: list[str | None] = [None] * n
    if placeholder is None:
        placeholder = st.empty()

    for i in range(n):
        single = run_trials_asymmetric(THETA, 1)
        outcome = next(k for k, v in single.items() if v > 0)
        results[i] = outcome
        placeholder.markdown(build_two_qubit_grid_html(results, n), unsafe_allow_html=True)
        time.sleep(0.3)


registry.register("asymmetric-grid", render)
