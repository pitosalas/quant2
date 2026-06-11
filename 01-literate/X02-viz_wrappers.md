---
version: "1.0"
generated: "2026-06-10"
---

# Visualization Wrappers — entangled_grid, anticorrelated_grid, asymmetric_grid, x_gate_grid

These four modules follow the same structure: a thin `render()` function that
picks a runner variant, animates the grid, and registers under a name. They
are documented together because the pattern is identical.

## Shared Pattern

Each module:
1. Imports `build_two_qubit_grid_html` (or `build_grid_html`) from the grid module
2. Defines a `render(args, placeholder)` function that runs N single trials in a loop
3. Calls `registry.register(name, render)` at module level

```python
# entangled_grid.py
def render(args, placeholder=None):
    n = int(args[0]) if args else 16
    results = [None] * n
    placeholder = placeholder or st.empty()
    for i in range(n):
        single = run_trials_entangled([H_I, CNOT], 1)
        outcome = next(k for k, v in single.items() if v > 0)
        results[i] = outcome
        placeholder.markdown(build_two_qubit_grid_html(results, n), unsafe_allow_html=True)
        time.sleep(0.3)
registry.register("entangled-grid", render)
```

## Module Summary

| Module | Registry name | Runner | Physics |
|--------|--------------|--------|---------|
| `entangled_grid.py` | `"entangled-grid"` | `run_trials_entangled([H_I, CNOT], 1)` | Bell state Φ+: 00 or 11, 50/50 |
| `anticorrelated_grid.py` | `"anticorrelated-grid"` | `run_trials_anticorrelated(1)` | Bell state Ψ+: 01 or 10, anti-correlated |
| `asymmetric_grid.py` | `"asymmetric-grid"` | `run_trials_asymmetric(π/3, 1)` | Biased: 00 ~75%, 11 ~25% |
| `x_gate_grid.py` | `"x-gate-grid"` | `Qubit.zero().apply(X).measure()` | Deterministic: always 1 |

## Why These Are Separate Modules

Each module encodes specific physics: the gate sequence determines the
correlations shown. Keeping them separate makes the registry names meaningful
(the name matches the phenomenon) and allows different chapter sections to
reference each independently.

## Possible Improvements

The four grid modules share nearly identical `render` bodies. A factory
function in a shared module would eliminate the duplication:

```python
def make_grid_render(run_one, name):
    def render(args, placeholder=None):
        n = int(args[0]) if args else 16
        results = [None] * n
        placeholder = placeholder or st.empty()
        for i in range(n):
            single = run_one(1)
            outcome = next(k for k, v in single.items() if v > 0)
            results[i] = outcome
            placeholder.markdown(build_two_qubit_grid_html(results, n), unsafe_allow_html=True)
            time.sleep(0.3)
    registry.register(name, render)
```

This would reduce each module to a two-line registration call. The current
approach is easier to read individually but harder to update consistently.
