#!/usr/bin/env python3
# grover_anim.py — Animated Grover's algorithm amplitude visualization
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure
import streamlit as st

from quant2.gates import H
from viz import registry


STATES = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]
STATE_INDEX = {"00": 0, "01": 1, "10": 2, "11": 3}

# Diffusion operator: 2/N * ones - I  (inversion about average)
GROVER_N = 4
DIFFUSION = (2 / GROVER_N) * np.ones((GROVER_N, GROVER_N)) - np.eye(GROVER_N)


def make_oracle(target_idx: int) -> np.ndarray:
    """Phase-flip oracle for target state: flip sign of target amplitude."""
    op = np.eye(GROVER_N)
    op[target_idx, target_idx] = -1
    return op


def build_grover_frames(target: str) -> list[tuple[np.ndarray, str]]:
    """Compute amplitude snapshots through 2 Grover iterations.

    Returns list of (amplitudes, label) pairs for animation frames.
    """
    target_idx = STATE_INDEX[target]
    oracle = make_oracle(target_idx)
    state = np.zeros(GROVER_N)
    frames = []

    # Initialization: H⊗H puts all states in equal superposition
    state = np.full(GROVER_N, 0.5)
    frames.append((state.copy(), "Step 1: Equal superposition\n(H gate on both qubits)"))

    for iteration in range(1, 3):
        # Oracle: flip target amplitude
        state = oracle @ state
        frames.append((state.copy(), f"Step {(iteration-1)*2+2}: Oracle marks |{target}⟩\n(target amplitude flips negative)"))

        # Diffusion: inversion about average
        state = DIFFUSION @ state
        frames.append((state.copy(), f"Step {(iteration-1)*2+3}: Diffusion amplifies target\n(iteration {iteration})"))

    return frames


def draw_amplitude_frame(amplitudes: np.ndarray, label: str, target: str) -> matplotlib.figure.Figure:
    """Draw signed amplitude bar chart for one Grover frame."""
    target_idx = STATE_INDEX[target]
    colors = []
    for i, amp in enumerate(amplitudes):
        if i == target_idx:
            colors.append("#ff9900" if amp >= 0 else "#cc4400")
        else:
            colors.append("#2266cc" if amp >= 0 else "#cc2222")

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(STATES, amplitudes, color=colors, edgecolor="white", linewidth=1.5, width=0.5)

    for bar, amp in zip(bars, amplitudes):
        if abs(amp) > 0.05:
            y = bar.get_height() + (0.04 if amp >= 0 else -0.08)
            ax.text(bar.get_x() + bar.get_width() / 2, y,
                    f"{amp:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.axhline(0, color="black", linewidth=1)
    ax.axhline(0.5, color="gray", linestyle="--", linewidth=0.8, alpha=0.5, label="initial")
    ax.set_ylim(-1.2, 1.2)
    ax.set_ylabel("Amplitude", fontsize=11)
    ax.set_title(label, fontsize=10, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Highlight target state label
    ax.get_xticklabels()[target_idx].set_color("#ff9900")
    ax.get_xticklabels()[target_idx].set_fontweight("bold")

    fig.tight_layout()
    return fig


def render(args: list[str], placeholder=None) -> None:
    """Animate Grover's algorithm amplitude evolution for 2-qubit system."""
    target = args[0] if args else "11"
    if placeholder is None:
        col, _ = st.columns([1, 1])
        placeholder = col.empty()

    frames = build_grover_frames(target)
    for amplitudes, label in frames:
        fig = draw_amplitude_frame(amplitudes, label, target)
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(1.2)


registry.register("grover-anim", render)
