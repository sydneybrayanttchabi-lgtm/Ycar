## 2026-08-20 - Singleton Caching for Intl.NumberFormat in React Components
**Learning:** Instantiating `new Intl.NumberFormat()` on every format call inside React renders creates heavy CPU overhead and GC pressure (instantiation is ~50-70x slower than `.format()`). In files like `app.py`, which is a TSX React component with CRLF line endings, formatting utilities must reuse singleton formatters while preserving CRLF to prevent git churn.
**Action:** Always hoist `Intl.NumberFormat` instances to module-level singletons or memoize them when locale/options are static.
