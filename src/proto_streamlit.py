#!/usr/bin/env python3
# proto_streamlit.py — Streamlit prototype: chapter text inline with interactive viz
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from quant2.qubit import Qubit

CHAPTER_FILE = Path(__file__).parent.parent / "chapters" / "chapter01.md"
N_TRIALS = 500


def amplitudes(theta_deg: float) -> tuple[float, float]:
    theta = np.radians(theta_deg)
    return float(np.cos(theta / 2)), float(np.sin(theta / 2))


def run_trials(theta_deg: float, n: int) -> dict[int, int]:
    alpha, beta = amplitudes(theta_deg)
    counts = {0: 0, 1: 0}
    for _ in range(n):
        q = Qubit(complex(alpha), complex(beta))
        counts[q.measure()] += 1
    return counts


def draw_histogram(counts: dict[int, int], theta_deg: float):
    alpha, beta = amplitudes(theta_deg)
    total = sum(counts.values())
    fig, ax = plt.subplots(figsize=(5, 3.5))
    labels = ["|0⟩", "|1⟩"]
    values = [counts[0] / total, counts[1] / total]
    colors = ["#4477cc", "#cc4444"]
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.5, width=0.4)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.1%}", ha="center", va="bottom", fontsize=13, fontweight="bold")
    ax.set_title(f"α = {alpha:.3f}   β = {beta:.3f}   ({N_TRIALS} measurements)", fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Probability")
    ax.axhline(0.5, color="gray", linestyle="--", linewidth=1, alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


# ── Page ──────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="quant2 — Chapter 1", layout="centered")

chapter_text = CHAPTER_FILE.read_text()

# First half of chapter text
paragraphs = [p.strip() for p in chapter_text.strip().split("\n\n") if p.strip()]
for para in paragraphs[:2]:
    st.markdown(para)

# Inline interactive illustration
st.markdown("---")
st.markdown("**Try it:** drag the slider to change α and β, watch the measurement distribution update.")

col1, col2 = st.columns([1, 2])
with col1:
    theta = st.slider("θ (degrees)", 0, 180, 90, step=1,
                      help="θ=0 → always |0⟩, θ=90 → 50/50, θ=180 → always |1⟩")
    alpha, beta = amplitudes(theta)
    st.metric("α", f"{alpha:.3f}")
    st.metric("β", f"{beta:.3f}")

with col2:
    counts = run_trials(theta, N_TRIALS)
    st.pyplot(draw_histogram(counts, theta))

st.markdown("---")

# Remaining text
for para in paragraphs[2:]:
    st.markdown(para)
