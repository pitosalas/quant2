# TF10 — More Entanglement

## T01 — Add Ry gate to gates.py
**Status**: done
**Description**: Add `Ry(theta: float) -> np.ndarray` function returning 2x2 rotation matrix. Add `I_X = np.kron(I2, X)` constant. Add `Ry_I(theta)` returning `np.kron(Ry(theta), I2)`.
**Test**: Ry(π) ≈ iX (bit flip); Ry(π/2) is unitary.

## T02 — Add runners for anticorrelated and asymmetric
**Status**: done
**Description**: Add `run_trials_anticorrelated(n)` and `run_trials_asymmetric(theta, n)` to runner.py. Gate sequences: anticorrelated = [H_I, CNOT, I_X]; asymmetric = [Ry_I(theta), CNOT].
**Test**: anticorrelated: only "01" and "10"; asymmetric at θ=π/3: only "00" and "11", ~75/25.

## T03 — anticorrelated-grid viz
**Status**: done
**Description**: `src/viz/anticorrelated_grid.py`. Thin wrapper around build_two_qubit_grid_html. Uses run_trials_anticorrelated. Register as "anticorrelated-grid".
**Test**: 100 trials produce only "01" and "10".

## T04 — asymmetric-grid viz
**Status**: done
**Description**: `src/viz/asymmetric_grid.py`. Uses run_trials_asymmetric(π/3, ...). Register as "asymmetric-grid".
**Test**: 200 trials produce only "00" and "11"; "00" count > "11" count.

## T05 — Add chapter 4 text to book.md
**Status**: done
**Description**: Add entanglement chapter: four Bell states, anti-correlated example, asymmetric Ry(θ) example. Intuitive, non-mathematical.
**Test**: Manual.

## T06 — All tests pass
**Status**: done
**Test**: `uv run pytest` exits 0.
