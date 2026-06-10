#!/usr/bin/env python3
# test_qubit_grid.py — Tests for viz.qubit_grid.build_grid_html
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from viz.qubit_grid import build_grid_html


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
    """Measured cells show outcome digit; unmeasured cells show '?'."""
    html = build_grid_html([0, 1, None], 3)
    assert ">0<" in html
    assert ">1<" in html
    assert ">?<" in html


def test_build_grid_html_colors():
    """Each outcome maps to its expected color."""
    html = build_grid_html([0, 1, None], 3)
    assert "#2266cc" in html  # outcome 0 — blue
    assert "#cc2222" in html  # outcome 1 — red
    assert "#aaaaaa" in html  # unmeasured — gray
    assert "#000" in html  # experiment label — full black
