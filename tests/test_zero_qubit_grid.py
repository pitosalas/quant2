#!/usr/bin/env python3
# test_zero_qubit_grid.py — Tests for viz.zero_qubit_grid
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import viz.zero_qubit_grid  # noqa: F401 — triggers registry.register side effect
from viz import registry
from viz.zero_qubit_grid import build_zero_cell_html, build_zero_grid_html, build_legend_html
from quant2.qubit import Qubit


def test_zero_qubit_grid_registered():
    """zero-qubit-grid must be registered in the viz registry."""
    assert "zero-qubit-grid" in registry.REGISTRY
    assert callable(registry.REGISTRY["zero-qubit-grid"])


def test_fresh_qubit_always_measures_zero():
    """Qubit.zero().measure() must return 0 every time — no gate applied."""
    results = [Qubit.zero().measure() for _ in range(100)]
    assert all(r == 0 for r in results)


def test_pending_cell_shows_question_mark():
    """Unmeasured cell must show ? in yellow, not empty."""
    html = build_zero_cell_html(0, None)
    assert ">?<" in html
    assert "#ccaa00" in html


def test_measured_cell_shows_zero():
    """Measured cell with outcome 0 must show 0 in blue."""
    html = build_zero_cell_html(0, 0)
    assert ">0<" in html
    assert "#2266cc" in html


def test_legend_contains_all_three_states():
    """Legend must include yellow ?, blue 0, and red 1 cells."""
    html = build_legend_html()
    assert ">?<" in html
    assert ">0<" in html
    assert ">1<" in html
    assert "#ccaa00" in html
    assert "#2266cc" in html
    assert "#cc2222" in html


def test_legend_text_arg_appears_in_html():
    """Text passed to build_legend_html must appear in the output."""
    html = build_legend_html("Yellow means uncommitted.")
    assert "Yellow means uncommitted." in html
    assert "qg-legend-text" in html


def test_legend_no_text_omits_text_div():
    """With no text arg, the text div element must not appear in the output."""
    html = build_legend_html()
    assert '<div class="qg-legend-text">' not in html
