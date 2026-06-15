#!/usr/bin/env python3
# test_registry.py — Tests for viz.registry
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import pytest
from viz import registry


def test_register_and_render_calls_fn():
    """register then render must call the fn with the correct args."""
    called_with = []

    def stub(args, placeholder=None):
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

    def fn_first(args, placeholder=None):
        results.append("first")

    def fn_second(args, placeholder=None):
        results.append("second")

    registry.register("overwrite-test", fn_first)
    registry.register("overwrite-test", fn_second)
    registry.render("overwrite-test", [])
    assert results == ["second"]


def test_register_step_and_render_step():
    """register_step then render_step must call fn with correct args and return its value."""
    calls = []

    def step_stub(args, step, key, placeholder=None):
        calls.append((args, step, key))
        return step >= 2

    registry.register_step("test-step-stub", step_stub)
    done = registry.render_step("test-step-stub", ["x"], 1, "mykey")
    assert not done
    assert calls == [(["x"], 1, "mykey")]

    done = registry.render_step("test-step-stub", ["x"], 2, "mykey")
    assert done


def test_render_step_unknown_raises():
    """render_step with unregistered name must raise ValueError."""
    with pytest.raises(ValueError, match="No step renderer"):
        registry.render_step("no-step-viz", [], 0, "k")


def test_has_step_render_true_and_false():
    """has_step_render returns True only for names in STEP_REGISTRY."""
    registry.register_step("has-step-test", lambda a, s, k, p=None: True)
    assert registry.has_step_render("has-step-test") is True
    assert registry.has_step_render("definitely-not-registered-xyz") is False


def test_register_static_and_render_static():
    """register_static then render_static must call fn."""
    calls = []

    def static_stub(args, placeholder=None):
        calls.append(args)

    registry.register_static("test-static-stub", static_stub)
    registry.render_static("test-static-stub", ["z"])
    assert calls == [["z"]]


def test_render_static_unknown_raises():
    """render_static with unregistered name must raise ValueError."""
    with pytest.raises(ValueError, match="Unknown static visualization"):
        registry.render_static("no-static-viz", [])
