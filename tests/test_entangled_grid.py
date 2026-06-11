#!/usr/bin/env python3
# test_entangled_grid.py — Tests for entangled_grid (reuses two_qubit_grid HTML builder)
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from viz.two_qubit_grid import build_two_qubit_grid_html


def test_bell_state_results_render():
    """Only 00/11 outcomes plus None must produce valid HTML."""
    results = ["00", "11", "00", None, "11", None, "00", "11"]
    html = build_two_qubit_grid_html(results, 8)
    assert isinstance(html, str) and len(html) > 0


def test_all_unmeasured():
    """All-None grid must not raise."""
    html = build_two_qubit_grid_html([None] * 8, 8)
    assert isinstance(html, str)


def test_non_multiple_of_cols():
    """n not a multiple of 4 must not raise."""
    html = build_two_qubit_grid_html(["00", "11", "00"], 3)
    assert isinstance(html, str)
