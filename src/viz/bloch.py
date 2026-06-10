#!/usr/bin/env python3
# bloch.py — Bloch sphere and measurement distribution chart visualizations
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
import matplotlib.pyplot as plt


def plot_bloch_sphere(qubit, title: str = "Bloch Sphere", ax=None, show: bool = True):
    """Draw a Bloch sphere for the given qubit state."""
    theta, phi = qubit.bloch_angles()
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    standalone = ax is None
    if standalone:
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection="3d")

    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.cos(v)[np.newaxis, :] * np.ones((len(u), 1))
    ax.plot_wireframe(sx, sy, sz, color="lightblue", alpha=0.15, linewidth=0.5)

    for vec, lbl in [
        ([1, 0, 0], "|+⟩"), ([-1, 0, 0], "|-⟩"),
        ([0, 1, 0], "|+i⟩"), ([0, -1, 0], "|-i⟩"),
        ([0, 0, 1], "|0⟩"), ([0, 0, -1], "|1⟩"),
    ]:
        ax.plot([0, vec[0] * 1.3], [0, vec[1] * 1.3], [0, vec[2] * 1.3],
                "k--", linewidth=0.6, alpha=0.4)
        ax.text(vec[0] * 1.4, vec[1] * 1.4, vec[2] * 1.4, lbl,
                fontsize=9, ha="center", va="center", color="gray")

    ax.quiver(0, 0, 0, x, y, z, color="#e03030", linewidth=2.5, arrow_length_ratio=0.15)
    ax.scatter([x], [y], [z], color="#e03030", s=40, zorder=5)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")
    ax.set_title(f"{title}\nθ={np.degrees(theta):.1f}°  φ={np.degrees(phi):.1f}°", fontsize=10)

    if standalone and show:
        plt.tight_layout()
        plt.show()


def plot_measurement_distribution(
    counts: dict, title: str = "Measurement Distribution", ax=None, show: bool = True
):
    """Draw a bar chart of measurement outcome probabilities."""
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(5, 4))

    total = sum(counts.values())
    if total == 0:
        raise ValueError("counts must have at least one non-zero entry")

    sorted_keys = sorted(counts)
    labels = [f"|{k}⟩" for k in sorted_keys]
    values = [counts[k] / total for k in sorted_keys]
    palette = ["#4477cc", "#cc4444", "#44aa44", "#cc8800"]
    colors = [palette[i % len(palette)] for i in range(len(labels))]

    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.5, width=0.5)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{val:.1%}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax.axhline(0.5, color="gray", linestyle="--", linewidth=1, alpha=0.6)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability", fontsize=11)
    ax.set_title(title, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=12)

    if standalone and show:
        plt.tight_layout()
        plt.show()


def demo_dashboard(gate_results: list[tuple[str, dict, object]]):
    """Show Bloch sphere + distribution side-by-side for each experiment."""
    if not gate_results:
        raise ValueError("gate_results must not be empty")

    n = len(gate_results)
    fig = plt.figure(figsize=(5 * n, 8))
    fig.suptitle("quant2 — Single Qubit Experiments", fontsize=14, fontweight="bold", y=1.01)

    for i, (label, counts, qubit) in enumerate(gate_results):
        ax_bloch = fig.add_subplot(2, n, i + 1, projection="3d")
        ax_dist = fig.add_subplot(2, n, n + i + 1)
        plot_bloch_sphere(qubit, title=label, ax=ax_bloch, show=False)
        plot_measurement_distribution(counts, title="", ax=ax_dist, show=False)

    plt.tight_layout()
    plt.show()
