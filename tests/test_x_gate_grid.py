#!/usr/bin/env python3
# test_x_gate_grid.py — Tests for viz.x_gate_grid step animation
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from viz.x_gate_grid import render_step_x_gate


class RecordingPlaceholder:
    """Fake Streamlit placeholder that records each markdown() call."""

    def __init__(self):
        self.calls: list[str] = []

    def markdown(self, html: str, unsafe_allow_html: bool = False) -> None:
        self.calls.append(html)


def test_render_step_x_gate_draws_final_frame_when_done():
    """Regression: the step reporting done=True must also draw that frame.

    Previously, completion was signaled one step later by a call that drew
    nothing, which erased the last rendered frame from the placeholder.
    """
    placeholder = RecordingPlaceholder()
    step = 0
    done = False
    while not done:
        calls_before = len(placeholder.calls)
        done = render_step_x_gate(["2"], step, "test", placeholder)
        if done:
            assert len(placeholder.calls) == calls_before + 1
            assert "experiment #2" in placeholder.calls[-1]
        step += 1
