#!/usr/bin/env python3
# grover_start.py — Bar chart showing 4-qubit equal superposition starting state
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure
import streamlit as st

from viz import registry

N = 16
AMPLITUDE = 1 / np.sqrt(N)


def draw_superposition() -> matplotlib.figure.Figure:
    labels = [str(i) for i in range(N)]
    amplitudes = [AMPLITUDE] * N

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(
        labels, amplitudes, color="#2266cc", edgecolor="white", linewidth=1, width=0.7
    )

    ax.set_ylim(0, 0.5)
    ax.set_ylabel("Amplitude", fontsize=11)
    ax.set_xlabel("State (0–15)", fontsize=11)
    ax.set_title("After Hadamard: all 16 states in equal superposition", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)
    fig.tight_layout()
    return fig


def render(args: list[str], placeholder=None) -> None:
    """Draw bar chart of 16-state equal superposition for 4-qubit Grover's."""
    if placeholder is None:
        placeholder = st.empty()
    fig = draw_superposition()
    placeholder.pyplot(fig)
    plt.close(fig)


registry.register("grover-start", render)
