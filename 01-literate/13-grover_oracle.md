---
version: "1.0"
generated: "2026-06-21"
---

# Grover's Oracle: Marking a Target State by Phase Flip

## Introduction

Grover's algorithm is one of quantum computing's canonical results: it searches an unsorted database of N items in O(sqrt(N)) steps, a quadratic speedup over classical brute-force search. The algorithm works in two repeating phases — an oracle step and a diffusion step — applied iteratively until the target state is amplified to near-certainty.

This module visualizes the first of those two phases: the **oracle**. Specifically, it shows what happens to the quantum amplitudes of a 4-qubit register (16 states) immediately after the oracle acts. The oracle's job is deceptively simple: it marks one state (the "target") by flipping its amplitude from positive to negative, leaving all other amplitudes unchanged. This phase flip is invisible to any direct measurement, but it sets up the subsequent diffusion step to constructively interfere in favor of the target.

The visualization is registered in the quant2 viz registry so it can be embedded in any Streamlit narrative using the `:visualize grover-oracle` directive.

---

## The State Space: 4 Qubits, 16 Amplitudes

A 4-qubit register can represent any superposition of 2^4 = 16 computational basis states, labeled |0> through |15>. Before the oracle acts, Grover's algorithm initializes the system in a uniform superposition — every state gets exactly the same amplitude.

The equal-superposition amplitude is 1/sqrt(N). This is not an arbitrary normalization; it follows directly from the requirement that probabilities (amplitude squared, summed over all states) must equal 1.

```python
N = 16
AMPLITUDE = 1 / np.sqrt(N)
TARGET = 11
```

Choosing state 11 as the target is a pedagogical convenience. Any state from 0 to 15 would work identically. Eleven is visually distinctive in the middle of the register — not the first state, not the last, not a power of two — which makes it easy to spot in the chart without the eye jumping to a boundary.

---

## Building the Oracle Picture

The oracle's effect is purely a sign change on the target state. In quantum circuit terms this is implemented with a multi-controlled Z gate, but for visualization purposes we simply construct the amplitude array directly: every element is `+AMPLITUDE`, except for the target element which is `-AMPLITUDE`.

Color reinforces the sign distinction. Blue bars (#2266cc) represent the untouched states. The single orange bar (#ff9900) at position 11 draws the eye immediately to the marked state, signaling that something structurally different has happened there.

```python
def draw_oracle() -> matplotlib.figure.Figure:
    labels = [str(i) for i in range(N)]
    amplitudes = [AMPLITUDE if i != TARGET else -AMPLITUDE for i in range(N)]
    colors = ["#ff9900" if i == TARGET else "#2266cc" for i in range(N)]
```

Both lists are built with list comprehensions rather than numpy operations. This is intentional: the lists are short (16 elements), and the conditional logic reads more clearly as a Python expression than as a masked array assignment. Numpy would add no performance benefit at this scale.

---

## Chart Construction and Axis Choices

The bar chart is sized to fit comfortably inside a Streamlit sidebar or content column (8 inches wide, 3.5 inches tall). The bars are given a slight gap via `width=0.7` — a full-width bar chart at this state count would look dense and hard to count.

```python
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(labels, amplitudes, color=colors, edgecolor="white", linewidth=1, width=0.7)
```

A horizontal line at y=0 is essential. Without it, the negative bar at position 11 reads only as "shorter", not as "flipped below zero". The zero line makes the sign inversion immediately legible.

```python
    ax.axhline(0, color="black", linewidth=1)
    ax.set_ylim(-0.5, 0.5)
```

The y-axis range is set to [-0.5, 0.5] rather than being derived from the data. The actual amplitudes are approximately +/-0.25, so an auto-scaled axis would zoom in tightly and make the uniform bars look tall. The fixed range communicates that these amplitudes are small fractions — a visual reminder that no single state is dominant yet.

The top and right spines are suppressed. This is a cosmetic choice from the Tufte tradition: chartjunk removal. The remaining two spines (left and bottom) are sufficient for reading values from a simple bar chart.

```python
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)
```

---

## Highlighting the Target Tick Label

After drawing the bars, the x-axis tick label for the target state gets separate treatment: it is colored orange and bolded to match the bar above it. This creates a visual correspondence between the axis annotation and the marked bar.

```python
    ax.get_xticklabels()[TARGET].set_color("#ff9900")
    ax.get_xticklabels()[TARGET].set_fontweight("bold")
```

One subtlety: `get_xticklabels()` only returns labels after the figure has been laid out. Calling this before `ax.bar(...)` or on an unflushed canvas would return an empty list or default labels. The call order here — after all data is plotted — ensures the labels are present and correctly indexed.

---

## The Render Entry Point

The `render` function is the interface the viz registry calls. It accepts a list of string arguments (unused here — there are no configurable parameters for this visualization) and an optional Streamlit placeholder for in-place updates.

```python
def render(args: list[str], placeholder=None) -> None:
    """Draw bar chart showing oracle phase-flip on state 11 in 4-qubit register."""
    if placeholder is None:
        placeholder = st.empty()
    fig = draw_oracle()
    placeholder.pyplot(fig)
    plt.close(fig)
```

`plt.close(fig)` is important. Matplotlib figures accumulate in memory if not explicitly closed, and Streamlit reruns the entire script on each interaction. Without this call, repeated renders would leak figures and eventually raise a `RuntimeWarning` about too many open figures.

The placeholder pattern (passing an `st.empty()` container rather than calling `st.pyplot()` directly) is a quant2 convention that allows the calling narrative to control where in the layout the figure appears and to replace it cleanly on rerun.

---

## Registry Wiring

The final line registers this visualization under the key `"grover-oracle"`, making it available to any `:visualize grover-oracle` directive in a literate document.

```python
registry.register("grover-oracle", render)
```

This side-effect at module level is a deliberate exception to the "no side effects at import time" guideline. The registry pattern in quant2 works by importing viz modules, which triggers registration. This is consistent with every other visualization in the codebase and is the agreed-upon architecture for discoverable, pluggable renders.

---

## Observations on Potential Improvements

**1. TARGET and N are module-level constants, not parameters.**
If a user wanted to explore how the oracle looks with a different target state or a different qubit count, they cannot do so through the `:visualize` directive. The `args` list is accepted but ignored. A natural improvement would be parsing `args[0]` as a target state and `args[1]` as a qubit count, defaulting to 11 and 4 respectively, and computing N from the qubit count.

**2. The amplitude computation is repeated in two list comprehensions.**
`amplitudes` and `colors` both iterate over `range(N)` and both branch on `i != TARGET`. A single pass building both lists together would be slightly more readable and avoids the risk of the two lists drifting out of sync if TARGET changes.

**3. No test for the oracle logic itself.**
The module has no corresponding unit test that verifies the amplitude at TARGET is negative and all others are positive. Given the simplicity of the logic this is low risk, but adding a test for `draw_oracle()` that checks the bar heights would encode the intent and catch accidental changes to the amplitude formula.

**4. Figure size is hardcoded.**
The `(8, 3.5)` figsize works well in a wide Streamlit content column but may not suit sidebar or mobile layouts. Passing figsize as an optional argument or reading it from a shared quant2 theme configuration would make the visualization more composable.

**5. The title string is long.**
At 10pt font the title fits, but it is near the limit for narrow displays. Splitting the conceptual content across a title and a subtitle (using `ax.set_title` plus `fig.text`) would be more robust.
