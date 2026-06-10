#!/usr/bin/env python3
# single_qubit_anim.py — Animated single-qubit measurement histogram for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time

import matplotlib.pyplot as plt
import streamlit as st

from quant2.qubit import Qubit
from quant2.gates import H
from viz.histogram import draw_histogram
from viz import registry


def render(args: list[str]) -> None:
    """Animate N measurements of H|0⟩ and then show the final histogram."""
    n = int(args[0]) if args else 20
    counts = {0: 0, 1: 0}
    placeholder = st.empty()

    for _ in range(n):
        q = Qubit.zero().apply(H)
        outcome = q.measure()
        counts[outcome] += 1

        labels = ["|0⟩", "|1⟩"]
        values = [counts[0], counts[1]]
        total = sum(values)
        probs = [v / total for v in values]

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(labels, probs, color=["#4477cc", "#cc4444"], width=0.5)
        ax.set_ylim(0, 1.15)
        ax.set_ylabel("Probability")
        ax.set_title(f"Running counts after {total} measurements")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.15)

    placeholder.empty()
    label = f"H|0⟩ — {n} measurements"
    st.pyplot(draw_histogram(counts, label))


registry.register("single-qubit", render)
