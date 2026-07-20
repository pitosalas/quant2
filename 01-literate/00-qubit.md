---
version: "1.0"
generated: "2026-06-21"
---

# qubit.py — The Quantum State Vector

## Introduction

`qubit.py` is the foundational module of `quant2`. Everything else — gates,
measurement, simulation, visualization — depends on the type it defines.
A `Qubit` is a wrapper around a two-element complex NumPy array, the state
vector `[α, β]` where `|α|² + |β|² = 1`. That constraint — normalization —
is the physical meaning: probabilities must sum to one.

The module is deliberately small. It defines exactly one class with exactly
the operations needed: construction, gate application, measurement, and Bloch
sphere angles. No UI, no simulation loops, no registry calls.

---

## Design: Immutable-ish State with Explicit Collapse

The class has an interesting hybrid identity. Gate application is immutable —
`apply()` returns a new `Qubit`, leaving the original unchanged:

```python
def apply(self, gate: np.ndarray) -> "Qubit":
    if gate.shape != (2, 2):
        raise ValueError(f"Gate must be 2x2, got shape {gate.shape}")
    new_vec = gate @ self.vec
    norm = np.linalg.norm(new_vec)
    if not np.isclose(norm, 1.0):
        raise ValueError(f"Gate produced non-normalized state (norm={norm:.4f})")
    return Qubit(new_vec[0], new_vec[1])
```

But measurement is deliberately mutating — `measure()` collapses the state
in place, mirroring quantum mechanics:

```python
def measure(self) -> int:
    ...
    self.vec = np.array([1.0, 0.0] if outcome == 0 else [0.0, 1.0], dtype=complex)
    return outcome
```

This asymmetry is intentional. In quantum mechanics, unitary evolution (gate
application) is reversible; measurement is not. The API encodes that physics.

---

## Construction and Normalization

The constructor validates normalization at the boundary — any deviation from
`‖[α,β]‖ = 1` raises immediately:

```python
def __init__(self, alpha: complex = 1.0, beta: complex = 0.0):
    vec = np.array([alpha, beta], dtype=complex)
    norm = np.linalg.norm(vec)
    if not np.isclose(norm, 1.0):
        raise ValueError(f"State vector must be normalized (norm={norm:.4f})")
    self.vec = vec
```

The two factory methods provide the most common starting states:

```python
@classmethod
def zero(cls) -> "Qubit":
    return cls(1.0, 0.0)   # |0⟩

@classmethod
def one(cls) -> "Qubit":
    return cls(0.0, 1.0)   # |1⟩
```

---

## Measurement: Validate, Then Trust

The `measure()` method is the most nuanced part of the module. After multiple
gate applications, floating-point arithmetic can introduce tiny drift in the
norm. `numpy.random.choice` requires probabilities that sum to exactly 1.0.
The method validates that the state is still well-formed (within a generous
tolerance), then normalizes to machine precision for numpy's strict needs:

```python
def measure(self) -> int:
    probs = np.array([self.prob_zero, self.prob_one])
    total = float(probs.sum())
    if not np.isclose(total, 1.0, atol=1e-6):
        raise ValueError(
            f"State probabilities sum to {total:.8f}; possible state corruption"
        )
    probs = probs / total
    outcome = int(np.random.choice([0, 1], p=probs))
    self.vec = np.array([1.0, 0.0] if outcome == 0 else [0.0, 1.0], dtype=complex)
    return outcome
```

The key design decision: **validate at the boundary, raise on corruption,
then trust the normalized value for numpy's call.** The renormalization step
is not compensating for a logic error — it is correcting sub-ULP floating
point drift that is inherent in sequential matrix multiplication. A tolerance
of `1e-6` is deliberately wide enough to catch genuine corruption (e.g., a
non-unitary gate that slipped through) while allowing normal float drift.

```
            ┌─────────────────────────────────────┐
            │           measure()                  │
            │                                     │
            │  build probs from |α|², |β|²        │
            │       ↓                             │
            │  validate total ≈ 1.0 (1e-6)        │
            │       ↓ (raise if bad)              │
            │  normalize for numpy                │
            │       ↓                             │
            │  np.random.choice → outcome         │
            │       ↓                             │
            │  collapse self.vec to |0⟩ or |1⟩   │
            └─────────────────────────────────────┘
```

---

## Bloch Sphere Angles

The Bloch sphere is a geometric representation of a single qubit's state.
Any normalized state `α|0⟩ + β|1⟩` maps to a point on the unit sphere:

```python
def bloch_angles(self) -> tuple[float, float]:
    alpha, beta = self.vec
    theta = 2.0 * np.arccos(np.clip(abs(alpha), 0.0, 1.0))
    phi = float(np.angle(beta) - np.angle(alpha))
    return float(theta), phi
```

`theta` is the polar angle (0 = north pole = |0⟩, π = south pole = |1⟩).
`phi` is the azimuthal angle encoding the relative phase between α and β.
`np.clip` guards against floating-point values slightly outside [0, 1] that
would make `arccos` return `nan`.

---

## Observations on Improvement

**No phase tracking after measurement.** After `measure()`, the state is
collapsed to a pure basis state with real amplitudes. The global phase is
lost. For the pedagogical purposes of this app this is fine, but a more
complete simulation would preserve it.

**`apply()` re-validates normalization.** This is defensive and correct, but
means every gate application pays a `np.linalg.norm` cost. For bulk
simulations (`run_trials` with large `n`), a fast path that skips
re-validation for known-unitary gates could be worth adding.

**`state` property returns a copy.** This prevents external mutation of the
internal state vector, which is correct. The cost is a heap allocation per
call. Callers that just want probabilities should use `prob_zero`/`prob_one`
directly.
