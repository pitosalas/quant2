# F17 — Multi-dialog navigation with fixed nav bar

**Priority**: High
**Done:** no
**Tasks File Created:** yes
**Tests Written:** no
**Test Passing:** no
**Description**: Split book_dialog.md into numbered dialog files (Dialog 1, Dialog 2, etc.), each with a descriptive title and an opening greeting between Aristotle and Plato. Add a fixed navigation bar at the top of the page showing all dialog titles as anchor links so the reader can jump directly to any dialog without scrolling.

## Dialogs (proposed split)
- Dialog 1 — Qubits (current ## Qubits section)
- Dialog 2 — Quantum Gates (current ## Quantum Gates section)
- Dialog 3 — Two-Qubit Registers (current ## Two-Qubit Registers section)
- Dialog 4 — Entangled Qubits (current ## Entangled Qubits section)
- Dialog 5 — Grover's Search (current ## Grover's Search Algorithm section)
- Dialog 6 — Limits and Realities (current ## Limits and Realities section)

## How to Demo
**Setup**: Run `./run.bash`

**Steps**:
1. Observe fixed nav bar at top with 6 dialog titles
2. Click any title — page scrolls to that dialog
3. Reload — nav bar persists, each dialog has greeting

**Expected output**: Fixed sticky nav bar; each dialog opens with Aristotle/Plato greeting; all existing content and visualizations preserved.

## Open Questions
- Keep as one file with anchors, or split into separate markdown files?
- Nav bar: Streamlit sidebar vs sticky CSS header vs st.tabs?
- Greeting: reuse existing opening lines or add fresh exchange per dialog?
