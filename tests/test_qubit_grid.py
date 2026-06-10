#!/usr/bin/env python3
# test_qubit_grid.py — Tests for viz.qubit_grid.build_grid_figure
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import matplotlib
matplotlib.use("Agg")
import matplotlib.figure
import pytest

from viz.qubit_grid import build_grid_figure


def test_build_grid_figure_returns_figure():
    """build_grid_figure must return a matplotlib Figure."""
    fig = build_grid_figure([None, 0, 1, None], 4)
    assert isinstance(fig, matplotlib.figure.Figure)
    matplotlib.pyplot.close(fig)


def test_build_grid_figure_axis_count():
    """Grid for n=4 must produce exactly 4 axes (1 row x 4 cols)."""
    import matplotlib.pyplot as plt
    fig = build_grid_figure([None, 0, 1, None], 4)
    visible_axes = [ax for ax in fig.get_axes() if ax.get_visible()]
    assert len(visible_axes) == 4
    plt.close(fig)
