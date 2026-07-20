#!/usr/bin/env python3
# test_qubit_grid.py — Tests for viz.qubit_grid.build_grid_html
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from viz.qubit_grid import animate_single_qubit_grid, build_grid_html


class RecordingPlaceholder:
    """Fake Streamlit placeholder that records each markdown() call."""

    def __init__(self):
        self.calls: list[str] = []

    def markdown(self, html: str, unsafe_allow_html: bool = False) -> None:
        self.calls.append(html)


def test_build_grid_html_returns_str():
    """build_grid_html must return an HTML string."""
    html = build_grid_html([None, 0, 1, None], 4)
    assert isinstance(html, str)
    assert "<div" in html


def test_build_grid_html_contains_all_cell_labels():
    """Grid must include a label for each cell index."""
    html = build_grid_html([0, 1, None], 3)
    assert "experiment #1" in html
    assert "experiment #2" in html
    assert "experiment #3" in html


def test_build_grid_html_outcome_labels():
    """Measured cells show outcome digit; unmeasured cells show no label."""
    html = build_grid_html([0, 1, None], 3)
    assert ">0<" in html
    assert ">1<" in html
    assert ">?<" not in html


def test_build_grid_html_colors():
    """Measured outcomes map to their expected colors; unmeasured cells have no color."""
    html = build_grid_html([0, 1, None], 3)
    assert "#2266cc" in html  # outcome 0 — blue
    assert "#cc2222" in html  # outcome 1 — red
    assert "#aaaaaa" not in html  # unmeasured cells are empty, no gray
    assert "qg-label" in html  # experiment label present, theme-inherited color


def test_animate_single_qubit_grid_draws_final_frame_when_done():
    """Regression: the step reporting done=True must also draw that frame.

    Previously, completion was signaled one step later by a call that drew
    nothing, which erased the last rendered frame from the placeholder.
    """
    placeholder = RecordingPlaceholder()
    step = 0
    done = False
    while not done:
        calls_before = len(placeholder.calls)
        done = animate_single_qubit_grid(lambda: 0, ["2"], step, "test", placeholder)
        if done:
            assert len(placeholder.calls) == calls_before + 1
            assert "experiment #2" in placeholder.calls[-1]
        step += 1
