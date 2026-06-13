## Qubits

A qubit is a Quantum Bit. Unlike a classical bit — which is always 0 or 1 — a qubit has no definite value until it is **measured**. Before measurement, it exists in a **superposition**: genuinely both 0 and 1 at the same time, not merely unknown.

When measured, the qubit **collapses** to either 0 or 1. The probability of each outcome is determined by two numbers called **amplitudes**: α (alpha) and β (beta). The rules are:

- P(measuring 0) = |α|²
- P(measuring 1) = |β|²
- |α|² + |β|² = 1 (probabilities must sum to 1)

The **Hadamard gate** (H) sets α = β = 1/√2, giving exactly 50% probability for each outcome. This is the most common way to put a qubit into superposition.

A freshly created qubit starts in state |0⟩: α = 1, β = 0. Without any gate applied, it measures 0 every single time — no randomness, no superposition. Just a deterministic classical bit. The Hadamard is what creates the quantum behavior.

#### Here we run 20 experiments: each creates a qubit, applies H, then measures it.

Each cell starts as "?" (superposition) and collapses to 0 or 1 when measured.

:visualize qubit-grid 20

#### Over many experiments, the 50/50 split becomes clear.

:visualize single-qubit 100

The histogram converges on 50% for each outcome — exactly what |α|² = |β|² = 0.5 predicts.

---

## Quantum Gates

A **quantum gate** is an operation that changes a qubit's amplitudes without measuring it. Gates are the quantum equivalent of logic gates in classical computing, with one key difference: every quantum gate is **reversible**. You can always undo a quantum gate by applying it again (or its inverse). Classical gates like AND are not reversible — you can't recover the inputs from the output.

### The X Gate — Quantum NOT

The simplest gate is the **Pauli-X gate**, also called the quantum NOT. It flips |0⟩ to |1⟩ and |1⟩ to |0⟩. No superposition, no randomness — purely deterministic.

*Before running this experiment, predict: what will every cell show?*

:visualize x-gate-grid 20

Every cell shows 1. The X gate is the quantum equivalent of a classical NOT. Notice: no randomness at all. The qubit starts in |0⟩ (α=1, β=0), X gate swaps the amplitudes to α=0, β=1, so measurement always gives 1.

Contrast this with the Hadamard grid above — the H gate set α = β = 1/√2, making the outcome genuinely random. The gate is what determines the behavior; the qubit itself is just a state vector.

### Gates Are Not Measurements

An important point that often causes confusion: **applying a gate does not collapse the qubit**. Gates manipulate amplitudes while the qubit remains in superposition. Only measurement collapses it. This means you can chain many gates together — H, then X, then H again — and the qubit stays quantum throughout, only collapsing when you finally measure.

This is the basis of quantum algorithms: run many gates to sculpt the amplitudes, then measure at the end.

---

## Two-Qubit Registers

A quantum register holds more than one qubit. The simplest case is two **independent** (unentangled) qubits — each has its own state, each collapses separately when measured.

We apply H to both qubits. Each has a 50/50 chance of measuring 0 or 1, independently. When we measure both together, we get a 2-bit string: 00, 01, 10, or 11. Since the qubits are independent, all four combinations are equally likely — about 25% each.

### Experiment: two independent qubits

Each cell shows the 2-bit result. White = 00, blue = 01, red = 10, purple = 11. The colors scatter randomly — no pattern between the two bits.

:visualize two-qubit-grid 20

:visualize two-qubit-bar 100

All four outcomes appear roughly equally. Knowing that q0 measured 0 tells you nothing about q1 — the bits are uncorrelated.

That changes completely when the qubits are *entangled*.

---

## Entangled Qubits

**Entanglement** is a quantum correlation between two qubits. Once entangled, the qubits no longer have independent states — they share a single joint state. Measuring one instantly fixes the outcome of the other, regardless of distance.

### The Bell State

The most famous entangled state is the **Bell state** |Φ+⟩. We create it with two gates:

1. **Hadamard (H)** on qubit 0 — puts q0 into superposition
2. **CNOT** (Controlled-NOT) — flips q1 if and only if q0 is 1

After H, q0 is in superposition. The CNOT then links q1 to q0: wherever q0 goes, q1 follows. The two qubits are now entangled — 50% chance of measuring 00, 50% chance of 11. The outcomes 01 and 10 are **impossible** — the two qubits always agree.

### Experiment: Bell state (entangled qubits)

Watch the grid. Only white (00) and purple (11) cells appear. Blue (01) and red (10) never occur.

:visualize entangled-grid 20

:visualize entangled-bar 100

Compare this to the unentangled grid above. The color distribution looks similar — roughly half 00, half 11. But the *structure* is completely different. In the unentangled case, each bit decided independently. Here, they are locked together: q0 = 0 guarantees q1 = 0, always.

### Can entanglement produce opposites?

So far our Bell state makes the qubits always *agree*. But you can also create an entangled state where the qubits always *disagree* — if one measures 0, the other is guaranteed to measure 1. We get this by adding one extra gate (X on q1) after the CNOT.

*Before running: predict what colors you'll see.*

:visualize anticorrelated-grid 20

Only blue (01) and red (10) appear — never white or purple. The qubits are still entangled, still correlated, but now perfectly *anti*-correlated. Measuring q0 = 0 guarantees q1 = 1.

This shows there are multiple kinds of entanglement. Physicists call these the **four Bell states** — the two we've seen plus two more that are related by phase.

### Asymmetric Entanglement

Entanglement doesn't require a 50/50 split either. By replacing the Hadamard with a rotation gate at a different angle, we can make one outcome more likely than the other — while preserving the entanglement (no 01 or 10 outcomes).

*Predict: will 00 or 11 be more common in the grid below?*

:visualize asymmetric-grid 20

About 75% of cells show 00 (white), only 25% show 11 (purple). Yet 01 and 10 never appear — the qubits are still entangled, still correlated. The entanglement is about the *correlation structure*, not the probabilities.

---

## Grover's Search Algorithm

One of the most elegant quantum algorithms is **Grover's search**. Here's the problem it solves: you have a list of N items and one of them is "marked" (it's the answer you're looking for). You don't know which one. Classically, finding it takes N/2 steps on average — you check items one by one. Grover's algorithm finds it in roughly √N steps.

The trick is exploiting superposition and a technique called **amplitude amplification**.

### Step 1 — Put everything in superposition

Apply Hadamard to all qubits. Now the quantum system is in a superposition of all possible answers simultaneously — each with equal amplitude. With 2 qubits, that's 4 states: |00⟩, |01⟩, |10⟩, |11⟩, each with amplitude 0.5.

### Step 2 — The Oracle

The oracle is a special circuit that "marks" the correct answer by **flipping its amplitude from positive to negative**. It doesn't tell you the answer — it just tags it. All other amplitudes remain positive and unchanged.

After the oracle, three states have amplitude +0.5 and one (the target) has amplitude −0.5. The probabilities are all still equal (since probability = amplitude²) — you can't measure the answer yet.

### Step 3 — Amplitude Amplification

Now apply the **diffusion operator**: it reflects all amplitudes around their average. Since the marked state has a negative amplitude and everything else is positive, the average is slightly below 0.5. After reflection:
- The marked state (negative) gets boosted to nearly 1
- All other states (positive) get pushed toward 0

After just one iteration with 4 states (2 qubits), the target amplitude reaches exactly 1. Measure, and you get the answer with certainty.

### Watch it happen

The chart below shows the amplitudes (not just probabilities — amplitudes can be negative) evolving through the algorithm. The target state is |11⟩, shown in orange.

:visualize grover-anim 11

Notice: after the oracle, the orange bar flips below zero. After diffusion, it jumps to 1 while everything else collapses to 0. One iteration — done.

### What happens if you run too many iterations?

The animation shows a second iteration. Watch what happens: the oracle flips the target negative again, and diffusion pushes it back down. The algorithm "overshoots." For 4 states, you must measure after exactly 1 iteration. For larger searches, the optimal number of iterations is approximately √N.

---

## Limits and Realities

Quantum computers are powerful but face real constraints. Understanding these isn't pessimism — it's necessary for knowing when to use them.

### Decoherence

A qubit in superposition is fragile. Any interaction with the environment — heat, vibration, stray electromagnetic fields — can cause the qubit to collapse prematurely. This is called **decoherence**. It's the fundamental challenge of building quantum hardware.

Current superconducting qubits (used by IBM, Google) maintain coherence for roughly 100 microseconds to 1 millisecond. That sounds short, but a single gate operation takes nanoseconds — so you can chain hundreds to thousands of gates before coherence is lost.

### Repeating the computation

Quantum algorithms are probabilistic. Even when the algorithm is designed to make the right answer highly likely, you usually run it many times and take the most common result. This repetition overhead is real — it can eat into the quantum speedup for some problems.

For Grover's on 4 items, one iteration gives probability 1. For 16 items, two iterations give ~97% probability. For 1 million items, about 785 iterations give ~99%. Still much faster than checking all million items classically.

### Which problems actually benefit?

Not all problems get a quantum speedup. Quantum computers excel at:

- **Search problems** (Grover's) — quadratic speedup over brute-force search
- **Factoring large numbers** (Shor's algorithm) — exponential speedup, threatens current encryption
- **Simulating quantum systems** — chemistry, materials science, drug discovery
- **Optimization problems** — finding good solutions in large spaces

For everyday tasks — sorting a list, running a website, sending email — quantum computers offer no advantage. A classical computer will always be faster for those.

The honest picture: quantum computers are a specialized tool for a specific class of hard problems. That class includes some very important problems. That's why they matter.
