---
name: feedback-run-tests
description: Always run all tests after any code or file change
metadata:
  type: feedback
---

Always run `uv run pytest --tb=short -q` after every code change before reporting done.

**Why:** User explicitly requires it. Missing this breaks the session workflow.
**How to apply:** After any edit to Python source files, run tests immediately. Surface failures before moving on.
