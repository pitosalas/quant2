#!/usr/bin/env python3
# __main__.py — Demo entry point for quant2
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import numpy as np
from quant2.qubit import Qubit
from quant2.gates import X, H, Z
from quant2.simulate import run_simulation
from quant2.viz import demo_dashboard


def main():
    print("=== quant2: Single Qubit Demo ===\n")

    experiments = [
        ("H gate\n|0⟩ → superposition", [H]),
        ("X gate\n|0⟩ → |1⟩", [X]),
        ("Z gate\n|0⟩ → |0⟩ (phase flip)", [Z]),
        ("HZH = X\n|0⟩ → |1⟩", [H, Z, H]),
    ]

    results = []
    for label, gates in experiments:
        counts = run_simulation(gates, n_trials=1000, label=label.replace("\n", " — "))
        q = Qubit.zero()
        for g in gates:
            q = q.apply(g)
        results.append((label, counts, q))

    print("\nLaunching visualizations...")
    demo_dashboard(results)


if __name__ == "__main__":
    main()
