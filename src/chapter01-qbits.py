#!/usr/bin/env python3
# chapter01-qbits.py — Interactive illustration of qbit measurement
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from quant2.qubit import Qubit

CHAPTER_FILE = Path(__file__).parent.parent / "chapters" / "chapter01.md"
N_TRIALS = 500


def load_chapter() -> str:
    return CHAPTER_FILE.read_text()


def run_trials(theta_deg: float, n: int) -> dict[int, int]:
    theta = np.radians(theta_deg)
    alpha = np.cos(theta / 2)
    beta = np.sin(theta / 2)
    counts = {0: 0, 1: 0}
    for _ in range(n):
        q = Qubit(complex(alpha), complex(beta))
        counts[q.measure()] += 1
    return counts


def draw_histogram(ax, counts: dict[int, int], theta_deg: float):
    ax.cla()
    total = sum(counts.values())
    labels = ["|0⟩", "|1⟩"]
    values = [counts[0] / total, counts[1] / total]
    colors = ["#4477cc", "#cc4444"]
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.5, width=0.4)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.1%}", ha="center", va="bottom", fontsize=13, fontweight="bold")
    theta = np.radians(theta_deg)
    alpha = np.cos(theta / 2)
    beta = np.sin(theta / 2)
    ax.set_title(
        f"α = {alpha:.3f}   β = {beta:.3f}   ({N_TRIALS} measurements)",
        fontsize=11, pad=10
    )
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Measurement probability", fontsize=11)
    ax.axhline(0.5, color="gray", linestyle="--", linewidth=1, alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=12)


def main():
    console = Console()
    text = load_chapter()

    console.print()
    console.print(Panel(Markdown(text), title="Chapter 1 — Qbits", border_style="blue", padding=(1, 2)))
    console.print()
    console.print("[dim]Opening interactive illustration...[/dim]")

    fig, ax_hist = plt.subplots(figsize=(7, 5))
    fig.subplots_adjust(bottom=0.2)
    fig.patch.set_facecolor("#fafafa")
    ax_hist.set_facecolor("white")

    initial_theta = 90.0
    counts = run_trials(initial_theta, N_TRIALS)
    draw_histogram(ax_hist, counts, initial_theta)

    ax_slider = fig.add_axes([0.15, 0.06, 0.7, 0.03])
    slider = Slider(ax_slider, "θ°", 0, 180, valinit=initial_theta, valstep=1, color="#4477cc")
    fig.text(0.5, 0.01, "Drag θ to change qubit angle — watch α, β and probabilities shift",
             ha="center", fontsize=9, color="#555555")

    def update(_val):
        c = run_trials(slider.val, N_TRIALS)
        draw_histogram(ax_hist, c, slider.val)
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.suptitle("Chapter 1 — Qbit Measurement", fontsize=13, fontweight="bold")
    plt.show()


if __name__ == "__main__":
    main()
