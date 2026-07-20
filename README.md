# quant2

A simulator and teacher of quantum computing. quant2 renders an interactive
"book" of dialogs that explains core quantum computing concepts — qubits,
gates, superposition, measurement, entanglement, and Grover's search
algorithm — with inline, runnable visualizations next to the text that
explains them.

## What it is

The app is a single continuous-scroll Streamlit page (`src/book.py`) built
from `content/book_dialog.md`, a markdown file written as a teaching dialog
and split into six chapters, chosen via a dropdown selector:

- Qubits
- Quantum Gates
- Two-Qubit Registers
- Entangled Qubits
- Grover's Search Algorithm
- Limits and Realities

Each chapter is plain markdown text interleaved with `:visualize` and
`:static-viz` directives. The renderer (`src/chapter_renderer.py`) reads the
markdown block by block, and dispatches those directives to a registry of
visualization functions (`src/viz/registry.py`) instead of hardcoding which
chart goes where. `:visualize` directives get a "▶ Run Experiment" button
and, for the ones registered as step animations, animate frame-by-frame
(`registry.render_step`, throttled with `time.sleep(0.33)` between frames)
before landing on a final static render. `:static-viz` directives render
immediately, no button.

Registered visualizations (name → source file), all under `src/viz/`:

| Directive name | Module | What it shows |
|---|---|---|
| `single-qubit` | `single_qubit_anim.py` | Single qubit state, animated |
| `qubit-grid` | `qubit_grid.py` | Grid of qubits collapsing on measurement |
| `zero-qubit-grid` / `zero-qubit-legend` | `zero_qubit_grid.py` | All-zero qubit grid + legend |
| `x-gate-grid` | `x_gate_grid.py` | Effect of the X gate across a grid |
| `two-qubit-grid` | `two_qubit_grid.py` | Two-qubit register grid |
| `entangled-grid` | `entangled_grid.py` | Entangled pair collapsing together |
| `anticorrelated-grid` | `anticorrelated_grid.py` | Anti-correlated entangled pairs |
| `asymmetric-grid` | `asymmetric_grid.py` | Asymmetric-probability qubit grid |
| `two-qubit-bar` / `entangled-bar` | `two_qubit_bar.py` | Bar chart of two-qubit outcome counts |
| `grover-start` | `grover_start.py` | Grover's algorithm setup |
| `grover-oracle` | `grover_oracle.py` | Grover's oracle step |
| `grover-anim` | `grover_anim.py` | Full Grover's search animation |

Styling (`src/styles/main.css`) is loaded from a file rather than inlined in
Python, and injected via `st.markdown`. Chapter navigation is a dropdown
(`st.selectbox`) plus prev/next buttons that switch its selection.

## Simulation core

Under the visualizations is a small, dependency-light quantum simulator in
`src/quant2/`:

- `qubit.py` — `Qubit` class: a 2-element complex state vector
  `[alpha, beta]`, normalized on construction. Supports `apply(gate)` (2x2
  unitary), `measure()` (probabilistic collapse to `|0⟩`/`|1⟩`), and
  `bloch_angles()` for Bloch-sphere plotting. Raises `ValueError` if a state
  or gate ever produces a non-normalized vector — no silent correction.
- `gates.py` — standard single-qubit gates `X`, `Y`, `Z`, `H`, `I2`; the
  2-qubit `CNOT`; tensor-product helpers `H_I` and `I_X`; and a
  parameterized `Ry(theta)` rotation gate plus its 2-qubit lift `Ry_I`.
- `two_qubit.py` / `two_qubit_entangled.py` — two-qubit register state and
  entanglement operations.
- `measurement.py` — measurement helpers shared across the simulator.
- `sim/runner.py` — `run_trials(gates, n)` applies a sequence of gates to a
  fresh qubit and repeats measurement `n` times to produce outcome counts,
  used to drive histograms in the UI.

`src/quant2/__main__.py` is a small non-Streamlit demo entry point: it runs
a few canned experiments (H, X, Z, and HZH gate sequences) against 1000
trials each and opens a matplotlib dashboard (`viz/bloch.py`) instead of the
Streamlit book.

## Installation

Requires Python >= 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo url>
cd quant2
uv sync
```

## Usage

Run the interactive book (Streamlit UI):

```bash
./run.bash
# or directly:
uv run streamlit run src/book.py
```

This starts a local Streamlit server (default `http://localhost:8501`) with
the full dialog book and inline visualizations.

Run the non-UI matplotlib demo instead:

```bash
uv run python -m quant2
```

## Development

Run the test suite (pytest, configured via `pyproject.toml` with
`pythonpath = ["src"]`):

```bash
uv run pytest
```

Tests live in `tests/` and cover the qubit/gate math, single- and two-qubit
simulation, entanglement, Grover's algorithm, the visualization registry,
and the chapter renderer's markdown/directive parsing.

## Project structure

This repo follows a literate/spec-driven process — see `CLAUDE.md` and
`.claude/process.md` for the full workflow. Briefly:

- `01-literate/` — generated literate docs, one per changed Python module
- `02-doc/` — `spec.md` (app spec), `current.md` (session handoff), `notes.md`
- `03-features/` — feature specs (`done/`, `notdone/`, `deferred/`)
- `04-tasks/` — implementation task lists, one per feature
- `05-issues/` — tracked issues (`open/`, `closed/`, `deferred/`)

## License

MIT — see [LICENSE](LICENSE)
