#!/usr/bin/env python3
# __main__.py — Demo entry point for quant2
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import logging

from quant2.qubit import Qubit
from quant2.gates import X, H, Z
from sim.runner import run_trials
from viz.bloch import demo_dashboard

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("=== quant2: Single Qubit Demo ===")

    experiments = [
        ("H gate\n|0⟩ → superposition", [H]),
        ("X gate\n|0⟩ → |1⟩", [X]),
        ("Z gate\n|0⟩ → |0⟩ (phase flip)", [Z]),
        ("HZH = X\n|0⟩ → |1⟩", [H, Z, H]),
    ]

    results = []
    for label, gates in experiments:
        counts = run_trials(gates, 1000)
        q = Qubit.zero()
        for g in gates:
            q = q.apply(g)
        results.append((label, counts, q))

    logger.info("Launching visualizations...")
    demo_dashboard(results)


if __name__ == "__main__":
    main()
