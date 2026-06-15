# F15 — Zero Qubit Grid Visualization

**Priority**: Medium
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: Add a `zero-qubit-grid` visualization showing N fresh qubits created and measured immediately (no Hadamard), always collapsing to 0. Insert after line 21 of book_dialog.md to demonstrate the baseline deterministic behavior before introducing the H gate.

## How to Demo
**Setup**: Run `./run.bash`

**Steps**:
1. Navigate to the Qubits section
2. Observe the zero-qubit-grid: all cells show ? then collapse to 0
3. Compare with the qubit-grid below it (H gate applied) — random 0/1

**Expected output**: All N cells show 0. No randomness.
