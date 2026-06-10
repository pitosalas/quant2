#!/usr/bin/env python3
# chapter01.py — Streamlit app for Chapter 1: Qbits
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import streamlit as st

from quant2.qubit import Qubit
from sim.runner import run_trials
from viz.histogram import draw_histogram

CHAPTER_FILE = Path(__file__).parent.parent / "chapters" / "chapter01.md"
STYLES_FILE = Path(__file__).parent / "styles" / "main.css"
N_TRIALS = 500


def load_css() -> str:
    return STYLES_FILE.read_text()


def amplitudes(theta_deg: float) -> tuple[float, float]:
    theta = np.radians(theta_deg)
    return float(np.cos(theta / 2)), float(np.sin(theta / 2))


def run_angle_trials(theta_deg: float, n: int) -> dict[int, int]:
    alpha, beta = amplitudes(theta_deg)
    counts = {0: 0, 1: 0}
    for _ in range(n):
        q = Qubit(complex(alpha), complex(beta))
        counts[q.measure()] += 1
    return counts


def main():
    st.set_page_config(page_title="quant2 — Chapter 1", layout="centered")

    css = load_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    chapter_text = CHAPTER_FILE.read_text()
    paragraphs = [p.strip() for p in chapter_text.strip().split("\n\n") if p.strip()]

    for para in paragraphs[:2]:
        st.markdown(para)

    st.markdown("---")
    st.markdown("**Try it:** drag the slider to change α and β, watch the measurement distribution update.")

    col1, col2 = st.columns([1, 2])
    with col1:
        theta = st.slider(
            "θ (degrees)", 0, 180, 90, step=1,
            help="θ=0 → always |0⟩, θ=90 → 50/50, θ=180 → always |1⟩",
        )
        alpha, beta = amplitudes(theta)
        st.metric("α", f"{alpha:.3f}")
        st.metric("β", f"{beta:.3f}")

    with col2:
        counts = run_angle_trials(theta, N_TRIALS)
        label = f"α = {alpha:.3f}   β = {beta:.3f}   ({N_TRIALS} measurements)"
        st.pyplot(draw_histogram(counts, label))

    st.markdown("---")

    for para in paragraphs[2:]:
        st.markdown(para)


main()
