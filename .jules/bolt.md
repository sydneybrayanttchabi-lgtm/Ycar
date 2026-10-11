# Bolt's Journal - Critical Learnings

## 2025-05-18 - Avoid instantiating Intl.NumberFormat inside frequent utility functions
**Learning:** Instantiating `new Intl.NumberFormat(...)` on every call to number formatting helper functions (`formatFCFA`, `formatUSD`) creates massive overhead (~70x slowdown) and garbage collection pressure, especially when values are re-formatted rapidly on slider inputs or list items.
**Action:** Always cache `Intl.NumberFormat` instances at module scope when the locale and options remain constant.
