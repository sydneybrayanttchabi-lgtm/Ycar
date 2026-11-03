# Bolt's Journal - Critical Learnings

## 2026-11-03 - Hoisting Static Arrays in Monolithic React Components
**Learning:** In monolithic single-file React components like `app.py`, inline array generators like `Array.from({ length: ... }, ...)` inside JSX execute on every render (such as on slider input or state change), causing needless allocations and CPU cycles. Moving static sequences outside the component scope completely avoids re-allocation without altering behavior or styling.
**Action:** Identify static options or lookup structures generated inline in JSX and hoist them to top-level module constants.
