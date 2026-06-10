#!/usr/bin/env python3
# simulate.py — Run multi-trial qubit simulations and report outcome distributions
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
from quant2.qubit import Qubit


def run_simulation(gate_sequence: list, n_trials: int = 1000, label: str = "") -> dict:
    """
    Apply gate_sequence to |0⟩ n_trials times, measure each time.
    Returns counts {0: n, 1: n} and prints distribution.
    """
    if n_trials <= 0:
        raise ValueError(f"n_trials must be > 0, got {n_trials}")

    counts = {0: 0, 1: 0}
    for _ in range(n_trials):
        q = Qubit.zero()
        for gate in gate_sequence:
            q = q.apply(gate)
        counts[q.measure()] += 1

    print(f"\nSimulation: {n_trials} trials{' — ' + label if label else ''}")
    for outcome, count in sorted(counts.items()):
        bar = "#" * int(40 * count / n_trials)
        print(f"  |{outcome}⟩  {bar:<40}  {count:5d}  ({100*count/n_trials:5.1f}%)")
    return counts
