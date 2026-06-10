#!/usr/bin/env python3
# single_qubit_anim.py — Animated single-qubit measurement histogram for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import streamlit as st

from quant2.qubit import Qubit
from quant2.gates import H
from viz.histogram import draw_histogram
from viz import registry


def render(args: list[str]) -> None:
    """Run N measurements of H|0⟩ and show the final histogram."""
    n = int(args[0]) if args else 20
    counts = {0: 0, 1: 0}
    for _ in range(n):
        counts[Qubit.zero().apply(H).measure()] += 1
    st.pyplot(draw_histogram(counts, f"H|0⟩ — {n} measurements"))


registry.register("single-qubit", render)
