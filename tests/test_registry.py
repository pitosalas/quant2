#!/usr/bin/env python3
# test_registry.py — Tests for viz.registry
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from viz import registry


def test_register_and_render_calls_fn():
    """register then render must call the fn with the correct args."""
    called_with = []

    def stub(args):
        called_with.append(args)

    registry.register("test-stub", stub)
    registry.render("test-stub", ["a", "b"])
    assert called_with == [["a", "b"]]


def test_render_unknown_name_raises_value_error():
    """render with an unregistered name must raise ValueError."""
    with pytest.raises(ValueError, match="Unknown visualization"):
        registry.render("no-such-viz", [])


def test_register_overwrites_existing():
    """Registering the same name twice replaces the earlier fn."""
    results = []

    def fn_first(args):
        results.append("first")

    def fn_second(args):
        results.append("second")

    registry.register("overwrite-test", fn_first)
    registry.register("overwrite-test", fn_second)
    registry.render("overwrite-test", [])
    assert results == ["second"]
