#!/usr/bin/env python3
# runner.py — Run multi-trial qubit simulations and return outcome distributions
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from quant2.qubit import Qubit


def run_trials(gate_sequence: list, n: int) -> dict[int, int]:
    """Apply gate_sequence to |0⟩ n times, measure each time. Returns {0: count, 1: count}."""
    if n <= 0:
        raise ValueError(f"n must be > 0, got {n}")

    counts = {0: 0, 1: 0}
    for _ in range(n):
        q = Qubit.zero()
        for gate in gate_sequence:
            q = q.apply(gate)
        counts[q.measure()] += 1
    return counts
