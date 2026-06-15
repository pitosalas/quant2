# TF16 — Non-blocking animations with abstracted grid runners

## T01 — Extend registry with step and static support
**Status**: done
**Description**: Add STEP_REGISTRY, STATIC_REGISTRY dicts. Add register_step(name, fn), register_static(name, fn), has_step_render(name), render_step(name, args, step, key, placeholder), render_static(name, args, placeholder) to registry.py.
**Test**: test_registry.py: register_step + render_step roundtrip; render_step unknown name raises; render_static calls fn.

## T02 — Update chapter_renderer for step-based and static rendering
**Status**: done
**Description**: Add `import time`. Handle :static-viz directive (inline render, no button). For :visualize with step renderer: use step state + st.rerun(scope="fragment") pattern, 0.33s between frames. For :visualize without step renderer: keep current blocking render fallback.
**Test**: test_chapter_renderer.py: static-viz renders inline; step-based viz advances state on each call.

## T03 — Add animate_single_qubit_grid helper to qubit_grid.py
**Status**: done
**Description**: Add animate_single_qubit_grid(measure_fn, args, step, key, placeholder) -> bool. 2 frames/cell: frame 0 = pending ?, frame 1 = measure + show. Handles results in session_state[key_results]. Register step render for qubit-grid.
**Test**: Verify step 0 shows pending, step 1 shows result, step 2*n returns True.

## T04 — Add step render to zero_qubit_grid; extract legend as static viz
**Status**: done
**Description**: Add render_step_zero using animate_single_qubit_grid with Qubit.zero().measure. Add render_legend registered under zero-qubit-legend as static viz. Remove legend from end of render(). Add :static-viz zero-qubit-legend to book_dialog.md after Plato's color explanation.
**Test**: render_step returns True at step 2*n; legend HTML contains all three states.

## T05 — Add step render to x_gate_grid
**Status**: done
**Description**: 3 frames/cell: 0=pending, 1=show 0 (initial), 2=measure+show 1 (after X). Register step render. Import build_pending_grid_html.
**Test**: step 0 shows pending, step 1 shows 0, step 2 shows 1, step 3*n returns True.

## T06 — Add animate_two_qubit_grid helper + step renders for all 4 two-qubit grids
**Status**: done
**Description**: Add animate_two_qubit_grid(run_fn, args, step, key, placeholder) -> bool to two_qubit_grid.py. 2 frames/cell: 0=pending, 1=run+show. Each of entangled_grid, anticorrelated_grid, asymmetric_grid registers a step render via this helper. two_qubit_grid registers its own step render via same helper.
**Test**: Each grid step render: step 0 pending, step 1 measured, step 2*n done.

## T07 — Tests
**Status**: done
**Description**: Add tests covering: registry step/static APIs; chapter_renderer :static-viz; each step renderer's frame logic. Ensure 104 existing tests still pass.
**Test**: pytest passes including new tests.
