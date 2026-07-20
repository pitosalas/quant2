---
version: "1.0"
generated: "2026-06-21"
---

# grover_start.py — Equal Superposition Starting State for Grover's Algorithm

## Introduction

Before Grover's search algorithm can do anything interesting, it needs a starting point: a quantum state where every possible answer is equally plausible. This module renders that starting state as a bar chart — a simple visualization that anchors the viewer's intuition before the algorithm's oracle and diffusion steps reshape the probability landscape.

The program draws a 4-qubit system with 16 computational basis states (|0⟩ through |15⟩), each assigned an identical amplitude of 1/√16 = 0.25. This uniform distribution is what the Hadamard transform produces when applied to each qubit initialized to |0⟩. It is the canonical "blank slate" from which Grover's algorithm begins its amplification work.

---

## Imports and Constants

The module has a minimal dependency footprint: NumPy for the amplitude calculation, Matplotlib for rendering, and Streamlit for embedding the chart in the app. The `registry` import connects this visualization to the broader quant2 dispatch system.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure
import streamlit as st

from viz import registry
```

Two module-level constants define the problem size. `N = 16` is the number of basis states in a 4-qubit system (2^4). The amplitude is derived directly from the normalization constraint: all amplitudes must square-sum to 1, so each is 1/√N.

```python
N = 16
AMPLITUDE = 1 / np.sqrt(N)
```

Computing `AMPLITUDE` at module load time is a deliberate choice. It is a mathematical constant for this visualization — not a configuration value — so deriving it once and reusing it is both efficient and semantically clear. It also avoids recomputing `np.sqrt(N)` inside a potentially repeated render path.

---

## Building the Figure

The `draw_superposition` function owns the entire chart construction. It is deliberately separated from the Streamlit rendering logic so that the Matplotlib figure can be created, inspected, or tested independently of any web framework.

```python
def draw_superposition() -> matplotlib.figure.Figure:
    labels = [str(i) for i in range(N)]
    amplitudes = [AMPLITUDE] * N
```

The labels are the decimal integers 0 through 15, representing each computational basis state. Using decimal labels rather than binary strings (like "0000", "0001", ...) is a readability tradeoff: decimal is more compact and conventional in introductory quantum computing material, even though binary would be more faithful to the underlying qubit structure.

The amplitudes list is a flat repetition of the single constant value — there is no variation to encode at this stage. The uniform height of every bar is the entire visual message.

```python
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(labels, amplitudes, color="#2266cc", edgecolor="white", linewidth=1, width=0.7)
```

The figure size `(8, 3.5)` keeps the chart wide enough to show all 16 bars without crowding while remaining compact enough to fit naturally in a Streamlit column. The blue color `#2266cc` and white edge lines give the bars a clean, separated appearance. A bar width of 0.7 (leaving 0.3 units of gap per bar) prevents the chart from looking like a solid block.

```python
    ax.set_ylim(0, 0.5)
    ax.set_ylabel("Amplitude", fontsize=11)
    ax.set_xlabel("State (0–15)", fontsize=11)
    ax.set_title("After Hadamard: all 16 states in equal superposition", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)
    fig.tight_layout()
    return fig
```

Setting `ylim` to `(0, 0.5)` rather than letting Matplotlib auto-scale is intentional. Later visualizations in the Grover sequence will show amplitudes rising toward 1.0 for the marked state and falling toward 0 for others. Fixing the y-axis upper bound to 0.5 gives subsequent charts a natural comparison baseline. It also makes clear that 0.25 is a small value relative to what a "found" state looks like.

The title names the Hadamard gate explicitly, connecting the visual to the underlying operation. The spine removal (`top`, `right`) follows a minimalist style: fewer chart borders reduce visual noise without losing the reference lines that matter for reading bar heights.

---

## Streamlit Render Entry Point

The `render` function is the interface between this module and the quant2 visualization registry. Its signature — `args: list[str], placeholder=None` — is the standard contract expected by the registry dispatcher.

```python
def render(args: list[str], placeholder=None) -> None:
    """Draw bar chart of 16-state equal superposition for 4-qubit Grover's."""
    if placeholder is None:
        placeholder = st.empty()
    fig = draw_superposition()
    placeholder.pyplot(fig)
    plt.close(fig)
```

The `args` parameter is accepted but ignored here; this visualization has no configurable parameters. The `placeholder` fallback to `st.empty()` allows the function to be called with or without a pre-allocated Streamlit container, making it composable in both direct invocation and registry-dispatched contexts.

The explicit `plt.close(fig)` call after rendering is a resource hygiene requirement. Matplotlib accumulates figures in memory unless they are explicitly closed, and in a long-running Streamlit process that call could otherwise produce a memory leak.

---

## Registry Registration

The final line connects this module to the quant2 dispatcher under the key `"grover-start"`.

```python
registry.register("grover-start", render)
```

Registration happens at module import time as a side effect. This is a deliberate architectural choice in quant2: visualizations declare themselves rather than being listed in a central manifest. The tradeoff is that the registry's contents depend on which modules have been imported, which means the module must be imported before "grover-start" is a valid key. In a Streamlit app where all viz modules are imported at startup, this works reliably.

---

## Observations for Improvement

**1. Hardcoded qubit count.** `N = 16` is fixed at the module level. A more flexible design would accept the qubit count as a parameter (via `args` or a config object) and compute `N = 2 ** num_qubits`. This would allow the same visualization to serve 3-qubit, 5-qubit, or arbitrary systems without code changes.

**2. Unused `args` parameter.** The `render` signature accepts `args` but silently ignores it. A guard that raises or logs a warning when unexpected args are passed would surface integration mistakes early rather than hiding them.

**3. Binary state labels as an option.** Decimal labels are compact but lose the qubit-level structure. An `args`-driven flag to switch between decimal and binary string labels (e.g., `"0000"` through `"1111"`) would make the chart more instructive for audiences already familiar with binary representations.

**4. Y-axis upper bound assumption.** The fixed `ylim` of 0.5 is implicitly coordinated with later Grover step visualizations. If those charts change their scale, this chart would silently become inconsistent. Defining the shared y-limit as a named constant (or importing it from a shared config) would make the coupling explicit and easier to maintain.

**5. No test coverage.** The module has no associated tests. A minimal test could assert that `draw_superposition()` returns a `Figure`, that the figure contains exactly one `Axes`, that the axes has 16 bars, and that every bar height equals `1 / np.sqrt(16)`. This would encode the core invariants and catch regressions from future refactoring.
