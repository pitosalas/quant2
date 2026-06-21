#!/usr/bin/env python3
# grover_oracle.py — Bar chart showing 4-qubit state after oracle marks target
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure
import streamlit as st

from viz import registry

N = 16
AMPLITUDE = 1 / np.sqrt(N)
TARGET = 11


def draw_oracle() -> matplotlib.figure.Figure:
    labels = [str(i) for i in range(N)]
    amplitudes = [AMPLITUDE if i != TARGET else -AMPLITUDE for i in range(N)]
    colors = ["#ff9900" if i == TARGET else "#2266cc" for i in range(N)]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(labels, amplitudes, color=colors, edgecolor="white", linewidth=1, width=0.7)

    ax.axhline(0, color="black", linewidth=1)
    ax.set_ylim(-0.5, 0.5)
    ax.set_ylabel("Amplitude", fontsize=11)
    ax.set_xlabel("State (0–15)", fontsize=11)
    ax.set_title(
        "After Oracle: state 11 marked — amplitude flipped to negative", fontsize=10
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)

    ax.get_xticklabels()[TARGET].set_color("#ff9900")
    ax.get_xticklabels()[TARGET].set_fontweight("bold")

    fig.tight_layout()
    return fig


def render(args: list[str], placeholder=None) -> None:
    """Draw bar chart showing oracle phase-flip on state 11 in 4-qubit register."""
    if placeholder is None:
        placeholder = st.empty()
    fig = draw_oracle()
    placeholder.pyplot(fig)
    plt.close(fig)


registry.register("grover-oracle", render)
