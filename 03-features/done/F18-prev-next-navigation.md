---
id: F18
title: Prev/Next Dialog Navigation Buttons
status: done
done: yes
tests_written: yes
tests_passing: yes
tasks_file_created: yes
---

## Summary

Add prev/next navigation buttons to each dialog tab. "Go to previous dialog" appears at the top (except dialog 1). "Go to next dialog" appears at the bottom (except the last dialog). Clicking switches the active tab via JavaScript injection.

## Acceptance Criteria

- Dialog 1: no prev button at top; next button at bottom
- Dialogs 2–5: prev button at top, next button at bottom
- Dialog 6: prev button at top; no next button at bottom
- Clicking a button switches to the correct tab
- Buttons have unique Streamlit keys; no key collisions across tabs
