## Qubits

**Aristotle:** Plato, I have been studying this doctrine of *quantum computing*, and *quantum bits* in particular. They call it a qubit. I confess I cannot reconcile it with anything in our natural philosophy.

**Plato:** Then let us examine it together, as we would any question about the nature of things. Tell me what troubles you.

**Aristotle:** A classical bit, they say, is always either one thing or another — zero or one. But a qubit, before we look at it, is *both at once*. Not merely unknown to us, but genuinely indeterminate in nature. Is this not a contradiction?

**Plato:** And yet, is it so different from what we said of the Forms? The thing in the world is not fully one thing or another until it is instantiated in matter. The qubit exists in **superposition** — genuinely both zero and one at the same time — until the act of measurement forces it to declare itself.

**Aristotle:** So measurement is not discovery but *creation*?

**Plato:** Precisely. When we measure, the qubit **collapses** to either zero or one. The probability of each outcome is governed by two numbers — the ancients of this theory call them **amplitudes**: alpha and beta.

**Aristotle:** And what do these amplitudes determine?

**Plato:** The probability of measuring zero equals the square of the absolute value of alpha, and of measuring one equals the square of the absolute value of beta. And they must sum to one — the qubit must land somewhere.

**Aristotle:** A freshly made qubit begins in the zero state, I read — alpha is one, beta is zero. So it always measures zero?

**Plato:** Always. No randomness, no superposition. A deterministic thing, indistinguishable from a classical bit. The quantum character must be *created* by an operation. That operation is called the **Hadamard gate**.

**Aristotle:** What then is the **Hadamard gate**, in its nature? Where does it fit in the account?

**Plato:** **Hadamard gate** sets alpha and beta each equal to one over the square root of two, yielding exactly fifty percent probability for each outcome. Without it, no quantum behavior. The gate is what makes a qubit truly quantum.

#### Here we run 20 experiments: each creates a qubit, applies H, then measures it.

Each cell starts as "?" (superposition) and collapses to 0 or 1 when measured.

:visualize qubit-grid 20

#### Over many experiments, the 50/50 split becomes clear.

:visualize single-qubit 100

The histogram converges on 50% for each outcome — showing the effect of the **Hadamard gate**. The qubit is put into a state where it has equal probability of *collapsing* into a zero or 1. This is exactly what squaring each amplitude of one over the square root of two gives: probability 0.5.

---

## Quantum Gates

**Aristotle:** You spoke of gates. What are they, in their essence?

**Plato:** A **quantum gate** is an operation that changes a qubit's amplitudes without measuring it. They are the quantum equivalent of logic gates in classical reckoning, with one crucial difference: every quantum gate is **reversible**. You can always undo it. Classical gates like AND are not reversible — you cannot recover the inputs from the output.

**Aristotle:** What are these gates in the physical world?

**Plato:** That depends on how the qubit is made. With superconducting qubits — as IBM and Google build — they are pulses of microwave radiation manipulating energy levels in tiny circuits. With trapped ions, laser pulses nudge the internal states of individual atoms. The physics differs, but the mathematical abstraction is the same: precise controls that change amplitudes in predictable ways.

**Aristotle:** But how then can you apply more than one? Do you apply one, then another?

**Plato:** Sequentially in time. Send the first pulse, wait for it to settle, then the second. The key is precision — timing, frequency, intensity, all carefully calibrated. Unlike measurement, applying a gate is **deterministic** — it always produces a predictable outcome.

### The X Gate — Quantum NOT

**Aristotle:** Then let us proceed, as always, from the simple to the complex. Show me the simplest gate.

**Plato:** The **Pauli-X gate** — the quantum NOT. It flips the zero state to the one state, and the one state back to zero. No superposition, no randomness — purely deterministic.


**Aristotle:** Can the *Pauli-X gate* be applied to any qubit, or does it need to be in a *collapsed* state?

**Plato:** It can be applied to any qubit in any state — collapsed or in superposition. The X gate simply swaps the two amplitudes: whatever alpha was becomes beta, and vice versa. 

A collapsed qubit is merely a special case: alpha one, beta zero, or alpha zero, beta one. The gate does not know how the qubit arrived at those amplitudes. 

- Apply X to a collapsed zero and you get a definite one. 

- Apply it to a collapsed one and you get a definite zero. 

- Apply it mid-superposition and the amplitudes swap just the same. 

The gate operates on whatever amplitudes are present — it does not ask their history.

*Our first experiment creates a qubit and then applies that X gate. We do this same thing, over and over again, in a series of experiments. As a new qubit starts in a zero state, what do you expect to see?*

:visualize x-gate-grid 20

Every cell shows 1. The X gate is the quantum equivalent of a classical NOT. The qubit starts in the zero state; the X gate swaps the amplitudes to alpha equals zero, beta equals one, so measurement always gives 1.

Contrast this with the Hadamard grid above — the H gate set alpha and beta each to one over the square root of two, making the outcome genuinely random. The gate determines the behavior; the qubit itself is merely a state vector.

### Gates Are Not Measurements

**Aristotle:** Does applying a gate collapse the qubit?

**Plato:** It does not. This is a point that causes much confusion. Gates manipulate amplitudes while the qubit remains in superposition. Only measurement collapses it. This means you can chain many gates together — H, then X, then H again — and the qubit stays quantum throughout, collapsing only when you finally measure.

**Aristotle:** And this is the basis of quantum algorithms?

**Plato:** Exactly. Run many gates to sculpt the amplitudes, then measure at the end.

---

## Two-Qubit Registers

**Aristotle:** What of two qubits together — is the register merely doubled, or does something new emerge in kind?

**Plato:** A quantum register holds more than one qubit. The simplest case is two **independent** — unentangled — qubits. Each has its own state, each collapses separately when measured.

**Aristotle:** But wait — you said a qubit has two amplitudes, alpha and beta. When you put two qubits together, which qubit owns the amplitudes?

**Plato:** That is exactly the right question. When two qubits are unentangled, each qubit still has its own alpha and beta. The joint state is simply their product — the four joint amplitudes are alpha-one times alpha-two, alpha-one times beta-two, beta-one times alpha-two, and beta-one times beta-two. You can still think of each qubit owning its own pair of amplitudes independently.

We can apply the Hadamard gate to both qubits. Each qubit has a 50/50 chance of measuring zero or one, independently. When we measure both together, we get a two-bit string: 00, 01, 10, or 11. Since the qubits are independent, all four combinations are equally likely — about 25% each.

**Aristotle:** And knowing what one measured tells us nothing about the other?

**Plato:** Nothing at all. That changes completely when the qubits are *entangled*.

### Experiment: register with two independent qubits

We create a quantum register with two qubits. Each cell shows the 2-bit result. White = 00, blue = 01, red = 10, purple = 11. We do this multiple times to see different results.

:visualize two-qubit-grid 20

If we ran this same experiment, creating a quantum register with two qubits, many many times, lets see how often we see each possible outcome.

:visualize two-qubit-bar 50

---

## Entangled Qubits

**Aristotle:** I have heard this very important idea called *entanglement*. Explain it to me. You said it was a correlation without classical equivalent.

**Plato:** When the qubits are unentangled, each retains its own separate amplitudes — they are, if you will, independent substances. The joint state is simply their product. You may speak of each qubit's nature separately, as you would of any two distinct things in the world.

**Aristotle:** So entanglement is when that breaks down?

**Plato:** Precisely. Entanglement is exactly the condition where the joint state can no longer be factored back into separate per-qubit amplitudes. At that point, the amplitudes belong irreducibly to the **joint states** of the pair — zero-zero, zero-one, one-zero, one-one — each with its own amplitude that cannot be recovered from any individual qubit alone. Four amplitudes in total, all summing to one when squared.

**Aristotle:** So once entangled, register as a whole is the thing with amplitudes when entangled, not the individual qubits?

**Plato:** Correct. And that pattern generalises: three qubits give eight joint states, four qubits give sixteen. The number doubles with every qubit added. This exponential growth in the amplitude space is precisely where quantum computers get their power.

**Plato:** With two unentangled qubits, each has its own pair of amplitudes — independent. When you entangle them, you end up with a single shared state that cannot be factored into separate amplitudes. 

**Entanglement** is a quantum correlation. Once entangled, the qubits no longer have independent states — they share one joint state. Measuring one instantly fixes the outcome of the other, regardless of distance. Einstein called it spooky action at a distance.

### The Bell State

**Aristotle:** How is it made?

**Plato:** The most famous entangled state is the **Bell state** known as Phi-plus. We create it with two gates:

1. **Hadamard (H)** on qubit 0 — puts q0 into superposition
2. **CNOT** (Controlled-NOT) — flips q1 if and only if q0 is 1

After H, q0 is in superposition. The CNOT links q1 to q0: wherever q0 goes, q1 follows. The result:

> **psi equals one over the square root of two times the zero-zero state, plus one over the square root of two times the one-one state**

Fifty percent chance of measuring 00, fifty percent chance of 11. The outcomes 01 and 10 are **impossible** — the two qubits always agree.

### Experiment: Bell state (entangled qubits)

Watch the grid. Only white (00) and purple (11) cells appear. Blue (01) and red (10) never occur.

:visualize entangled-grid 20

:visualize entangled-bar 100

**Aristotle:** Compare it to the unentangled grid. The distribution looks similar — roughly half 00, half 11. And yet appearances deceive. One cannot, from the mere count of outcomes, discern the deeper order that binds them.

**Plato:** The distribution looks similar, yes. But the *structure* is completely different. In the unentangled case, each bit decided independently. Here, they are locked together: q0 = 0 guarantees q1 = 0, always.

### Can entanglement produce opposites?

**Aristotle:** Are both qubits always going to be in the same state after measuring, or are there other kinds of entanglement?

**Plato:** Not all entanglement results in identical states. There are actually **four Bell states**, each with a different correlation pattern. You can create an entangled state where the qubits always *disagree* — if one measures 0, the other is guaranteed to measure 1. We add one extra gate — X on q1 — after the CNOT.

*Before running: predict what colors you'll see.*

:visualize anticorrelated-grid 20

Only blue (01) and red (10) appear — never white or purple. The qubits are still entangled, still correlated, but now perfectly *anti*-correlated. Measuring q0 = 0 guarantees q1 = 1. Entanglement is really about **correlation**, not necessarily sameness.

### Asymmetric Entanglement

**Aristotle:** Is it possible that the second qubit's state is determined probabilistically rather than simply equal or opposite?

**Plato:** Absolutely. You can create entangled states with more complex correlations — measuring qubit 1 as 0 might leave qubit 2 with a 70% chance of being 0 and 30% of being 1. Entanglement doesn't require a 50/50 split either. Replace the Hadamard with a rotation gate at a different angle, and one outcome becomes more likely than the other — while preserving the entanglement.

**Aristotle:** Can you show me what outcomes are possible?

**Plato:** Here is the full truth table for this state. We use a rotation gate at angle pi over three, followed by a CNOT. The joint outcomes are:

| q0 | q1 | Probability |
|----|----|-------------|
| 0  | 0  | 75%         |
| 0  | 1  | 0%          |
| 1  | 0  | 0%          |
| 1  | 1  | 25%         |

The qubits always agree — 01 and 10 are impossible, just as before. But now 00 is three times more likely than 11. The entanglement is intact; only the balance has shifted.

*Predict: will 00 or 11 be more common in the grid below?*

:visualize asymmetric-grid 20

About 75% of cells show 00 (white), only 25% show 11 (purple). Yet 01 and 10 never appear — the qubits are still entangled. The entanglement is about the *correlation structure*, not the probabilities.

**Aristotle:** Can more than two qubits be entangled?

**Plato:** Absolutely. Three, four, many qubits in increasingly complex ways. The more qubits entangled, the more complex the correlations — and that is where quantum computers get their real power. Information encoded across many entangled qubits simultaneously, in ways that have no classical equivalent.

---

## Grover's Search Algorithm

**Aristotle:** I have followed the account of gates and entanglement well enough. But a philosopher who stops at principles and never reaches their application has not finished his work. Give me an example of how you build these ideas into something useful. A search, perhaps.

**Plato:** **Grover's algorithm** is one famous example. Here is how it works:  You have a list of N items and one is marked — it is the answer. You do not know which one. Classically, finding it takes N divided by two steps on average — you check items one by one. Grover's algorithm finds it in roughly the square root of N steps. The trick is exploiting superposition and a technique called **amplitude amplification**.

**Aristotle:** Can you make this concrete? Walk me through an actual search.

**Plato:** Let us take a register of four qubits. Four qubits can represent sixteen values — zero through fifteen. Imagine a list of sixteen items, exactly one of which is the answer. Classically you would check them one by one — eight checks on average before finding it. Grover's algorithm finds it in roughly four steps: the square root of sixteen.

### Step 1 — Put everything in superposition

**Plato:** Apply Hadamard to all four qubits. Now the single register holds all sixteen states simultaneously — zero through fifteen — each with equal amplitude of one quarter. This is not sixteen experiments. It is one register, one moment, sixteen possibilities coexisting. Like a die with sixteen sides.

**Aristotle:** And all sixteen are present at once, in the same register? As a Form contains all its instances, yet is itself one thing?

**Plato:** Precisely. That is the whole point. A classical computer would have to check them one by one. This register already contains all of them.

:visualize grover-start

### Step 2 — The Oracle

**Aristotle:** How does it know which answer is correct without examining each?

**Plato:** The oracle is a quantum circuit built for your specific problem. It assumes you have some way to *recognize* the answer once you see it. It does not classically search; instead, it marks the correct answer by **flipping its amplitude from positive to negative** — multiplying that state's amplitude by −1 — while leaving all others unchanged. It does not tell you the answer. It merely tags it.

**Aristotle:** So after the oracle, the target is singled out — but invisibly?

**Plato:** Exactly. In our example the target is state eleven. After the oracle, fifteen states still have amplitude positive one quarter, and state eleven has amplitude negative one quarter. The probabilities are unchanged — squaring removes the sign. You could not find the answer by measuring now. But the tag is there, waiting to be exploited.

:visualize grover-oracle

**Aristotle:** The bar for eleven dips below zero while all others remain the same. The chart looks almost identical to before — and yet something fundamental has changed.

**Plato:** That is the oracle's power and its subtlety. Nothing visible to an outside observer. But the sign is now different, and the diffusion step will use that difference to amplify the target.

### Step 3 — Amplitude Amplification

**Plato:** Now apply the **diffusion operator**: it reflects all amplitudes around their average. The diffusion operator reflects all amplitudes around their mean:

1. Apply Hadamard gates to all qubits
2. Apply a phase flip to every state except the all-zeros state
3. Apply Hadamard gates again

Since the marked state has a negative amplitude and everything else is positive, the average is slightly below 0.5. After reflection:
- The marked state (negative) gets boosted to nearly 1
- All other states (positive) get pushed toward 0

**Aristotle:** The wrong answers cancel out?

**Plato:** Precisely. This is interference — quantum interference, not classical. The amplitudes of wrong answers subtract away; the right answer accumulates. After just one iteration with 4 states, the target amplitude reaches exactly 1. Measure, and you get the answer with certainty.

Repeat the oracle and diffusion operator approximately **the square root of N times**. Each iteration amplifies the correct answer further.

### Watch it happen

The chart below shows the amplitudes — not just probabilities, for amplitudes can be negative — evolving through the algorithm. The target state is one-one, shown in orange.

:visualize grover-anim 11

Notice: after the oracle, the orange bar flips below zero. After diffusion, it jumps to 1 while everything else collapses to 0. One iteration — done.

**Aristotle:** What happens if you run too many iterations?

**Plato:** The animation shows a second iteration. Watch: the oracle flips the target negative again, and diffusion pushes it back down. The algorithm *overshoots*. For 4 states, you must measure after exactly 1 iteration. For larger searches, the optimal number is approximately the square root of N.

---

## Limits and Realities

**Aristotle:** Is there a way to directly examine the amplitudes?

**Plato:** Not directly. Measurement collapses the state and gives only a classical outcome. However, you can *infer* amplitudes through repeated experiments — prepare the same state many times, measure, count frequencies, and approximate the squared absolute values of alpha and beta.

**Aristotle:** So the computation must be repeated many times to detect the likely correct answer?

**Plato:** Exactly. That is a key limitation. You run the algorithm once and get a probabilistic answer. You repeat many times and take the most common result. This repetition overhead is real — it can eat into the quantum speedup for some problems.

**Aristotle:** It seems that the *oracle* is doing a lot of magic. What is it *actually* in reality?

**Plato:** A fair challenge. The oracle is a quantum circuit — a specific arrangement of gates — built to *recognize* the correct answer when presented with it. For our search of sixteen items, suppose item eleven is the answer. You construct a circuit that checks each state against the criterion for being the answer. When it encounters state eleven, it flips the amplitude to negative. For all other states, it does nothing. No measurement occurs; the superposition is preserved.

**Aristotle:** But you speak of state eleven. The register is still in a quantum superposition of all sixteen states. How can the oracle act on eleven specifically?

**Plato:** Because quantum gates act on the whole superposition at once. Think of the superposition as all sixteen possibilities present simultaneously. The oracle examines each one in parallel — not one after another, but all at the same moment. For fifteen of them it finds no match and passes through unchanged. For state eleven it finds the match and flips the sign. The register still holds all sixteen states after the oracle; only the mark on eleven has changed.

The oracle does not search. It recognizes. The burden of knowing what the answer looks like has been moved into the construction of the circuit itself. For simple cases — a database lookup, a pattern match — this circuit is straightforward to build. For harder problems, engineering the oracle requires its own ingenuity.

**Aristotle:** So the difficulty of the problem is not destroyed — it is relocated.

**Plato:** Precisely. The oracle assumes what is hardest: that you can recognize the correct answer when you see it. Grover's algorithm then exploits that recognition to find the answer faster than brute force. The speedup is real. But the oracle is not magic — it is the problem's own logic, encoded in gates.

### Decoherence

**Aristotle:** What other constraints?

**Plato:** A qubit in superposition is fragile. Any interaction with the environment — heat, vibration, stray electromagnetic fields — can cause the qubit to collapse prematurely. This is called **decoherence**. It is the fundamental challenge of building quantum hardware.

Current superconducting qubits maintain coherence for roughly 100 microseconds to 1 millisecond. Each gate operation takes nanoseconds to microseconds; a full algorithm run takes microseconds to milliseconds. A few hundred gate iterations may be feasible; thousands exceed coherence time and the computation falls apart. This is why current quantum computers are limited in **circuit depth**.

**Aristotle:** How many iterations are typical?

**Plato:** For Grover's on 4 items, one iteration gives probability 1. For 16 items, two iterations give roughly 97% probability. For 1 million items, about 785 iterations give 99%. Still much faster than checking all million items classically.

### Which problems actually benefit?

**Aristotle:** What kinds of problems do not need many iterations — where quantum interference strongly amplifies the right answer?

**Plato:** Several. **Shor's algorithm** — factoring large numbers — finds factors with high probability in a single run, and carries an exponential speedup that threatens current encryption. **Quantum simulation** — modeling molecular or chemical behavior, where the system naturally explores correct outcomes — this is chemistry, materials science, drug discovery. **Grover's search**, after the square root of N iterations, as we have seen. And various **optimization problems** — finding good solutions in large spaces.

**Aristotle:** And for the tasks of ordinary life — sorting a list, reckoning figures, carrying a message?

**Plato:** For sorting a list, running a calculation, sending a message — quantum computers offer no advantage. A classical machine will always be faster for those. Quantum computers are a specialized tool for a specific class of hard problems. That class includes some very important problems. That is why they matter.

**Aristotle:** Then let us not mistake the power of the instrument for a power over all things.

**Plato:** Well said.

---

*End of dialogue*
