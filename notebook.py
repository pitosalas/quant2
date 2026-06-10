#!/usr/bin/env python3
# notebook.py — Interactive Marimo textbook: Introduction to Quantum Computing
# Author: Pito Salas and Claude Code
# Open Source Under MIT license

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium", css_file="notebook_styles.css")


@app.cell
def imports():
    import marimo as mo
    import numpy as np
    return mo, np


# ---------------------------------------------------------------------------
# Lesson 1: What is a Qubit?
# ---------------------------------------------------------------------------

@app.cell
def lesson1_intro(mo):
    mo.md("""
    # Quantum Computing: An Interactive Introduction

    ## Lesson 1 — What is a Qubit?

    A classical bit is always **0** or **1**. A qubit is different: before you
    measure it, it can exist in a *superposition* — a blend of both states at once.

    A qubit is described by two numbers, called **a** and **b**:

    **state = a * |0> + b * |1>**

    The chance of measuring 0 is `a squared`, and of measuring 1 is `b squared`.
    They must always add up to 1 — certainty is conserved.

    Use the slider to set amplitude **a**. The value of **b** is computed automatically
    so the probabilities still add to 100%.
    """)


@app.cell
def lesson1_controls(mo):
    a_slider = mo.ui.slider(0.0, 1.0, step=0.05, value=1.0, label="a (amplitude of |0>)")
    return (a_slider,)


@app.cell
def lesson1_output(mo, np, a_slider):
    a = a_slider.value
    b = np.sqrt(max(0.0, 1.0 - a**2))

    prob0 = a**2
    prob1 = b**2

    bar0 = "█" * int(prob0 * 20)
    bar1 = "█" * int(prob1 * 20)

    mo.vstack([
        a_slider,
        mo.md(f"""
| Outcome | Amplitude | Probability | Bar |
|---------|-----------|-------------|-----|
| 0       | a = {a:.2f} | {prob0:.1%}  | {bar0} |
| 1       | b = {b:.2f} | {prob1:.1%}  | {bar1} |

**State:** {a:.2f} * |0> + {b:.2f} * |1>

> **Try it:** Drag **a** to 0.71 — both outcomes become equally likely (50/50).
> That is superposition. Drag to 1.0 and measuring always gives 0.
        """),
    ])


# ---------------------------------------------------------------------------
# Lesson 2–5 stubs
# ---------------------------------------------------------------------------

@app.cell
def lesson2_stub(mo):
    mo.md("""
    ---
    ## Lesson 2 — The Hadamard Gate: Creating Superposition
    *Coming soon.*
    """)


@app.cell
def lesson3_stub(mo):
    mo.md("""
    ---
    ## Lesson 3 — X, Y, Z Gates: Flipping and Rotating
    *Coming soon.*
    """)


@app.cell
def lesson4_stub(mo):
    mo.md("""
    ---
    ## Lesson 4 — Measurement and Randomness
    *Coming soon.*
    """)


@app.cell
def lesson5_stub(mo):
    mo.md("""
    ---
    ## Lesson 5 — Gate Sequences: Building Circuits
    *Coming soon.*
    """)


if __name__ == "__main__":
    app.run()
