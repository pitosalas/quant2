#!/usr/bin/env python3
# registry.py — Named visualization registry for inline chapter directives
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

REGISTRY: dict[str, callable] = {}
STEP_REGISTRY: dict[str, callable] = {}
STATIC_REGISTRY: dict[str, callable] = {}


def register(name: str, fn: callable) -> None:
    REGISTRY[name] = fn


def register_step(name: str, fn: callable) -> None:
    """Register a step render function: fn(args, step, key, placeholder) -> bool (True = done)."""
    STEP_REGISTRY[name] = fn


def register_static(name: str, fn: callable) -> None:
    """Register a static viz that renders inline without a button."""
    STATIC_REGISTRY[name] = fn


def has_step_render(name: str) -> bool:
    return name in STEP_REGISTRY


def render(name: str, args: list[str], placeholder=None) -> None:
    if name not in REGISTRY:
        registered = list(REGISTRY.keys())
        raise ValueError(f"Unknown visualization {name!r}. Registered: {registered}")
    REGISTRY[name](args, placeholder)


def render_step(name: str, args: list[str], step: int, key: str, placeholder=None) -> bool:
    """Call the step render function. Returns True when animation is complete."""
    if name not in STEP_REGISTRY:
        raise ValueError(f"No step renderer for {name!r}")
    return STEP_REGISTRY[name](args, step, key, placeholder)


def render_static(name: str, args: list[str], placeholder=None) -> None:
    if name not in STATIC_REGISTRY:
        raise ValueError(f"Unknown static visualization {name!r}")
    STATIC_REGISTRY[name](args, placeholder)
