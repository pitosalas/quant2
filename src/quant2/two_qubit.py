#!/usr/bin/env python3
# two_qubit.py — Two independent (unentangled) qubits and joint measurement
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

from dataclasses import dataclass

from quant2.qubit import Qubit


@dataclass
class TwoQubitState:
    q0: Qubit
    q1: Qubit

    @classmethod
    def zero(cls) -> "TwoQubitState":
        return cls(q0=Qubit.zero(), q1=Qubit.zero())


def measure_pair(q0: Qubit, q1: Qubit) -> str:
    """Measure two independent qubits and return 2-bit outcome string."""
    return f"{q0.measure()}{q1.measure()}"
