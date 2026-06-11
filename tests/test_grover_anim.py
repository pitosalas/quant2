#!/usr/bin/env python3
# test_grover_anim.py — Tests for Grover's algorithm amplitude computation
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
from viz.grover_anim import build_grover_frames


def test_initial_frame_uniform():
    """First frame must have all amplitudes equal to 0.5."""
    frames = build_grover_frames("11")
    amps, _ = frames[0]
    assert np.allclose(amps, 0.5)


def test_oracle_flips_target():
    """Frame after first oracle: target amplitude is negative, others positive."""
    frames = build_grover_frames("11")
    amps, _ = frames[1]
    assert amps[3] < 0        # |11⟩ flipped
    assert all(amps[i] > 0 for i in range(3))


def test_diffusion_boosts_target_to_one():
    """Frame after first diffusion: target amplitude is ~1, others ~0."""
    frames = build_grover_frames("11")
    amps, _ = frames[2]
    assert abs(amps[3] - 1.0) < 1e-10
    assert all(abs(amps[i]) < 1e-10 for i in range(3))


def test_works_for_all_targets():
    """build_grover_frames works for all four target states."""
    for target in ("00", "01", "10", "11"):
        frames = build_grover_frames(target)
        amps, _ = frames[2]
        idx = {"00": 0, "01": 1, "10": 2, "11": 3}[target]
        assert abs(amps[idx] - 1.0) < 1e-10


def test_returns_five_frames():
    """Should return 5 frames: init + 2*(oracle+diffusion)."""
    frames = build_grover_frames("00")
    assert len(frames) == 5
