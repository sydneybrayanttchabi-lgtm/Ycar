# Bolt's Journal

## 2025-05-18 - Module-level Intl.NumberFormat and Memoization
**Learning:** `app.py` is a React TSX component file disguised as `.py` using CRLF line endings. In interactive React applications with sliders or frequent re-renders, instantiating `Intl.NumberFormat` inside format functions adds unnecessary garbage collection overhead.
**Action:** Always hoist `Intl.NumberFormat` instances to module scope and wrap pure presentational sub-components with `React.memo` to prevent redundant re-renders during state updates.
