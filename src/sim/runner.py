#!/usr/bin/env python3
# runner.py — Run multi-trial qubit simulations and return outcome distributions
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from quant2.qubit import Qubit
from quant2.two_qubit import measure_pair
from quant2.two_qubit_entangled import EntangledPair
from quant2.gates import H_I, CNOT, I_X, Ry_I


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


def run_trials_2qubit(gates0: list, gates1: list, n: int) -> dict[str, int]:
    """Apply gate sequences to two independent |0⟩ qubits n times. Returns {\"00\":c,...}."""
    if n <= 0:
        raise ValueError(f"n must be > 0, got {n}")

    counts: dict[str, int] = {"00": 0, "01": 0, "10": 0, "11": 0}
    for _ in range(n):
        q0 = Qubit.zero()
        for gate in gates0:
            q0 = q0.apply(gate)
        q1 = Qubit.zero()
        for gate in gates1:
            q1 = q1.apply(gate)
        counts[measure_pair(q0, q1)] += 1
    return counts


def run_trials_entangled(gate_sequence: list, n: int) -> dict[str, int]:
    """Apply gate_sequence to fresh EntangledPair n times. Returns {\"00\":c,...}."""
    if n <= 0:
        raise ValueError(f"n must be > 0, got {n}")

    counts: dict[str, int] = {"00": 0, "01": 0, "10": 0, "11": 0}
    for _ in range(n):
        pair = EntangledPair()
        for gate in gate_sequence:
            pair.apply(gate)
        counts[pair.measure()] += 1
    return counts


def run_trials_anticorrelated(n: int) -> dict[str, int]:
    """Run n trials of anti-correlated Bell state |Ψ+⟩ = (|01⟩+|10⟩)/√2."""
    return run_trials_entangled([H_I, CNOT, I_X], n)


def run_trials_asymmetric(theta: float, n: int) -> dict[str, int]:
    """Run n trials of asymmetric entangled state cos(θ/2)|00⟩ + sin(θ/2)|11⟩."""
    return run_trials_entangled([Ry_I(theta), CNOT], n)
