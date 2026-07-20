---
id: F19
title: Style Guide Compliance Pass
status: done
done: yes
tests_written: yes
tests_passing: yes
tasks_file_created: yes
---

## Summary

Fix all MUST and SHOULD violations found in the June 2026 style guide check.

## Acceptance Criteria

- No inline JS strings in Python source files
- All imports at top of file
- No leading underscore on custom identifiers
- All lines <= 88 chars
- `Callable` used instead of `callable` in annotations
- Float renormalization in qubit.py replaced with validate-then-trust pattern
- `print()` in __main__.py replaced with logging
- All existing tests pass
