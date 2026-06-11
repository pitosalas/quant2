#!/usr/bin/env python3
# test_two_qubit_grid.py — Tests for two_qubit_grid HTML builder
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from viz.two_qubit_grid import build_two_qubit_cell_html, build_two_qubit_grid_html


def test_cell_html_returns_string():
    """build_two_qubit_cell_html returns a non-empty string."""
    html = build_two_qubit_cell_html(0, "01")
    assert isinstance(html, str) and len(html) > 0


def test_cell_html_contains_bits():
    """Cell HTML contains both bit values from outcome."""
    html = build_two_qubit_cell_html(0, "01")
    assert ">0<" in html and ">1<" in html


def test_cell_html_unmeasured_shows_question():
    """Unmeasured cell shows ? for both bits."""
    html = build_two_qubit_cell_html(0, None)
    assert html.count(">?<") == 2


def test_grid_html_returns_string():
    """build_two_qubit_grid_html returns a non-empty string."""
    results = ["00", "01", None, "11"]
    html = build_two_qubit_grid_html(results, 4)
    assert isinstance(html, str) and len(html) > 0


def test_grid_html_all_unmeasured():
    """All-None grid must not raise."""
    results = [None] * 8
    html = build_two_qubit_grid_html(results, 8)
    assert isinstance(html, str)


def test_grid_html_contains_exp_labels():
    """Grid HTML contains experiment labels for each cell."""
    results = ["00", "11"]
    html = build_two_qubit_grid_html(results, 2)
    assert "experiment #1" in html
    assert "experiment #2" in html
