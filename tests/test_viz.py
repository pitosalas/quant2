#!/usr/bin/env python3
# test_viz.py — Tests for viz.histogram.draw_histogram
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
import matplotlib
matplotlib.use("Agg")
import matplotlib.figure
from viz.histogram import draw_histogram


def test_draw_histogram_returns_figure():
    """draw_histogram must return a matplotlib Figure."""
    fig = draw_histogram({0: 50, 1: 50}, "test")
    assert isinstance(fig, matplotlib.figure.Figure)


def test_draw_histogram_empty_counts_raises():
    """All-zero counts must raise ValueError."""
    with pytest.raises(ValueError):
        draw_histogram({0: 0, 1: 0}, "bad")


def test_draw_histogram_single_outcome():
    """Single non-zero outcome is a valid histogram."""
    fig = draw_histogram({0: 100}, "only zero")
    assert isinstance(fig, matplotlib.figure.Figure)


def test_draw_histogram_no_label():
    """Calling without label arg must not error."""
    fig = draw_histogram({0: 40, 1: 60})
    assert isinstance(fig, matplotlib.figure.Figure)
