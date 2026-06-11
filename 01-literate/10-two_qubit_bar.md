---
version: "1.0"
generated: "2026-06-10"
---

# two_qubit_bar.py — Animated Two-Qubit Bar Chart

## Purpose

Where the grid shows individual experiments evolving over time, the bar chart
shows the *accumulating distribution* of outcomes. After N trials the bars
converge toward the true quantum probabilities. This is a powerful pedagogical
contrast: the same quantum system looks random trial-by-trial but predictably
converges in aggregate.

## Histogram Drawing

```python
def draw_two_qubit_histogram(counts: dict[str, int], title: str) -> Figure:
    total = sum(counts.values())
    values = [counts[k] / total if total > 0 else 0.0 for k in OUTCOMES]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(OUTCOMES, values, color=COLORS, ...)
    ax.axhline(0.25, color="gray", linestyle="--", ...)  # 25% reference line
    ...
```

The dashed reference line at 25% is significant: for an unentangled H⊗H system,
all four outcomes are equally likely at exactly 25%. The chart makes it
visually obvious when the empirical distribution converges to this uniform
baseline.

## The Animation Core

```python
def animate_bar(run_one, title: str, n: int, placeholder=None) -> None:
    counts: dict[str, int] = {"00": 0, "01": 0, "10": 0, "11": 0}
    if placeholder is None:
        placeholder = st.empty()
    for _ in range(n):
        single = run_one()
        outcome = next(k for k, v in single.items() if v > 0)
        counts[outcome] += 1
        fig = draw_two_qubit_histogram(counts, f"{title} — {sum(counts.values())} trials")
        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.1)
```

`run_one` is a callable that returns a single-trial `dict[str,int]`. This
parameterisation lets `animate_bar` serve both entangled and unentangled
systems without modification.

The `plt.close(fig)` after each frame is essential — without it, Matplotlib
accumulates open figure handles and memory leaks across frames.

## Two Render Functions

```python
def render_unentangled(args: list[str], placeholder=None) -> None:
    n = int(args[0]) if args else 50
    animate_bar(lambda: run_trials_2qubit([H], [H], 1),
                "H|0⟩ ⊗ H|0⟩ (unentangled)", n, placeholder)

def render_entangled(args: list[str], placeholder=None) -> None:
    n = int(args[0]) if args else 50
    animate_bar(lambda: run_trials_entangled([H_I, CNOT], 1),
                "Bell state |Φ+⟩ (entangled)", n, placeholder)
```

The two functions are registered under different names:

```python
registry.register("two-qubit-bar", render_unentangled)
registry.register("entangled-bar", render_entangled)
```

Both converge to only `"00"` and `"11"` at 50% each — but through different
physics. The unentangled version produces those outcomes independently; the
Bell state produces them with perfect correlation.

## Possible Improvements

- **Convergence indicator**: a "distance from expected" metric shown below the
  chart would make the convergence more concrete.
- **Trial count in args**: currently `n` defaults to 50; the chapter could
  pass `:visualize two-qubit-bar 100` to show slower, more dramatic convergence.
- **Anticorrelated and asymmetric bar charts**: only the Bell state has a bar
  variant. Adding `anticorrelated-bar` and `asymmetric-bar` would complete the
  parallel between the grid and bar visualizations.
