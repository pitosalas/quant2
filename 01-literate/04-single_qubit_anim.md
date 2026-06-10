---
version: "1.0"
generated: "2026-06-10"
---

# single_qubit_anim — Single-Qubit Measurement Histogram

## What It Does

`single_qubit_anim.py` implements the `single-qubit` visualization directive. It runs N independent H|0⟩ measurements, counts how many collapsed to 0 vs. 1, and renders the final histogram via matplotlib. There is no animation — the chapter reader sees the finished result immediately.

The design choice to show only the final state (not animate step-by-step) makes this viz compact and fast to load. It pairs with `qubit-grid`, which does animate, so readers see both a summary and a live unfolding of the same experiment.

## Measurement and Counting

```python
def render(args: list[str]) -> None:
    n = int(args[0]) if args else 20
    counts = {0: 0, 1: 0}
    for _ in range(n):
        counts[Qubit.zero().apply(H).measure()] += 1
    st.pyplot(draw_histogram(counts, f"H|0⟩ — {n} measurements"))
```

Each iteration: initialize |0⟩, apply H (equal superposition), measure (collapses to 0 or 1 with probability 0.5 each). The result indexes directly into `counts` — no conditional needed.

`draw_histogram` lives in `viz.histogram` and is shared across visualizations that display outcome distributions.

## Registration

```python
registry.register("single-qubit", render)
```

Imported by `chapter01.py` to trigger self-registration. The chapter renderer calls `registry.render("single-qubit", args)` when it encounters `:visualize single-qubit N`.

## Possible Improvements

- **Theoretical overlay**: draw a horizontal line at 0.5 probability so readers can see how close the empirical result lands.
- **Configurable trials**: `n` already comes from `args`, but a minimum guard (e.g. `max(n, 5)`) would prevent misleading 1- or 2-shot histograms.
- **Shared histogram**: if multiple chapters run the same measurement series, the histogram logic could accept pre-computed counts rather than re-running experiments.
