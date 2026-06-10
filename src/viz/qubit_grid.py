#!/usr/bin/env python3
# qubit_grid.py — Animated qubit grid visualization for Streamlit
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import math
import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st

from quant2.qubit import Qubit
from quant2.gates import H
from viz import registry


COLORS = {
    "unmeasured": "#f0f0f0",
    0: "#cce0ff",
    1: "#ffcccc",
}
LABELS = {
    None: "?",
    0: "0",
    1: "1",
}
COLS = 8


def build_grid_figure(results: list[int | None], n: int) -> matplotlib.figure.Figure:
    """Build a matplotlib Figure showing an n-cell qubit measurement grid.

    results is a list of length n; each element is None (not yet measured), 0, or 1.
    Returns a new Figure — caller is responsible for closing it.
    """
    rows = math.ceil(n / COLS)
    fig, axes = plt.subplots(rows, COLS, figsize=(10, 1.2 * rows))

    # Normalize axes to a flat list of length rows*COLS
    if rows == 1 and COLS == 1:
        axes_flat = [axes]
    elif rows == 1:
        axes_flat = list(axes)
    elif COLS == 1:
        axes_flat = list(axes)
    else:
        axes_flat = [ax for row in axes for ax in row]

    for idx, ax in enumerate(axes_flat):
        if idx < n:
            outcome = results[idx]
            fill_color = COLORS[outcome] if outcome is not None else COLORS["unmeasured"]
            label_text = LABELS[outcome]

            # Draw white box with gray border
            rect = mpatches.FancyBboxPatch(
                (0.05, 0.15), 0.90, 0.70,
                boxstyle="square,pad=0",
                linewidth=1.5,
                edgecolor="#aaaaaa",
                facecolor=fill_color,
                transform=ax.transAxes,
                clip_on=False,
            )
            ax.add_patch(rect)

            ax.text(
                0.5, 0.90,
                f"#{idx + 1}",
                transform=ax.transAxes,
                ha="center", va="center",
                fontsize=6, color="gray",
            )

            ax.text(
                0.5, 0.50,
                label_text,
                transform=ax.transAxes,
                ha="center", va="center",
                fontsize=14, fontweight="bold",
            )
        else:
            ax.set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.tight_layout()
    return fig


def render(args: list[str]) -> None:
    """Animate n qubit measurements as a growing grid."""
    n = int(args[0]) if args else 16
    results: list[int | None] = [None] * n
    placeholder = st.empty()

    for i in range(n):
        q = Qubit.zero().apply(H)
        results[i] = q.measure()
        fig = build_grid_figure(results, n)
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.07)


registry.register("qubit-grid", render)
