#!/usr/bin/env python3
# registry.py — Named visualization registry for inline chapter directives
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

REGISTRY: dict[str, callable] = {}


def register(name: str, fn: callable) -> None:
    """Register a render function under the given name."""
    REGISTRY[name] = fn


def render(name: str, args: list[str]) -> None:
    """Call the registered render function for name, passing args.

    Raises ValueError if name is not registered.
    """
    if name not in REGISTRY:
        registered = list(REGISTRY.keys())
        raise ValueError(f"Unknown visualization {name!r}. Registered: {registered}")
    REGISTRY[name](args)
