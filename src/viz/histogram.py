#!/usr/bin/env python3
# histogram.py — Bar chart for qubit measurement outcome distributions
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import matplotlib.pyplot as plt
import matplotlib.figure


def draw_histogram(counts: dict[int, int], label: str = "") -> matplotlib.figure.Figure:
    """Return a Figure showing measurement outcome probabilities."""
    total = sum(counts.values())
    if total == 0:
        raise ValueError("counts must have at least one non-zero entry")

    sorted_keys = sorted(counts)
    labels = [f"|{k}⟩" for k in sorted_keys]
    values = [counts[k] / total for k in sorted_keys]
    palette = ["#4477cc", "#cc4444", "#44aa44", "#cc8800"]
    colors = [palette[i % len(palette)] for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.5, width=0.5)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{val:.1%}",
            ha="center",
            va="bottom",
            fontsize=13,
            fontweight="bold",
        )

    ax.axhline(0.5, color="gray", linestyle="--", linewidth=1, alpha=0.6)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability", fontsize=11)
    if label:
        ax.set_title(label, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=12)
    fig.tight_layout()
    return fig
