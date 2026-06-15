# F16 — Non-blocking animations with abstracted grid runners

**Priority**: High
**Done:** yes
**Tasks File Created:** yes
**Tests Written:** yes
**Test Passing:** yes
**Description**: Refactored all 7 animated grids to use st.rerun(scope="fragment") step-based rendering. Abstracted shared loop logic into animate_single_qubit_grid and animate_two_qubit_grid helpers. Added register_step/register_static to registry. Added :static-viz directive to chapter_renderer. 109 tests pass.
