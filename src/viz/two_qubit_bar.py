#!/usr/bin/env python3
# two_qubit_bar.py — Animated bar chart for two-qubit outcome distributions
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time

import matplotlib.pyplot as plt
import matplotlib.figure
import streamlit as st

from quant2.gates import H, H_I, CNOT
from sim.runner import run_trials_2qubit, run_trials_entangled
from viz import registry


OUTCOMES = ["00", "01", "10", "11"]
COLORS = ["#888888", "#4488ee", "#ee4444", "#9944cc"]


def draw_two_qubit_histogram(counts: dict[str, int], title: str) -> matplotlib.figure.Figure:
    total = sum(counts.values())
    values = [counts[k] / total if total > 0 else 0.0 for k in OUTCOMES]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(OUTCOMES, values, color=COLORS, edgecolor="white", linewidth=1.5, width=0.5)

    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.02,
                f"{val:.1%}",
                ha="center", va="bottom", fontsize=12, fontweight="bold",
            )

    ax.axhline(0.25, color="gray", linestyle="--", linewidth=1, alpha=0.5)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability", fontsize=11)
    ax.set_title(title, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=12)
    fig.tight_layout()
    return fig


def animate_bar(run_one, title: str, n: int, placeholder=None) -> None:
    counts: dict[str, int] = {"00": 0, "01": 0, "10": 0, "11": 0}
    if placeholder is None:
        placeholder = st.empty()
    for _ in range(n):
        single = run_one()
        outcome = next(k for k, v in single.items() if v > 0)
        counts[outcome] += 1
        fig = draw_two_qubit_histogram(counts, f"{title} — {sum(counts.values())} trials")
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.1)


def render_unentangled(args: list[str], placeholder=None) -> None:
    n = int(args[0]) if args else 50
    if placeholder is None:
        col, _ = st.columns([1, 1])
        placeholder = col.empty()
    animate_bar(lambda: run_trials_2qubit([H], [H], 1), "H|0⟩ ⊗ H|0⟩ (unentangled)", n, placeholder)


def render_entangled(args: list[str], placeholder=None) -> None:
    n = int(args[0]) if args else 50
    if placeholder is None:
        col, _ = st.columns([1, 1])
        placeholder = col.empty()
    animate_bar(lambda: run_trials_entangled([H_I, CNOT], 1), "Bell state |Φ+⟩ (entangled)", n, placeholder)


registry.register("two-qubit-bar", render_unentangled)
registry.register("entangled-bar", render_entangled)
