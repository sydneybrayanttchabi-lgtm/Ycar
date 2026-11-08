# Bolt's Journal - Critical Performance Learnings

## 2025-05-18 - Module-level Intl.NumberFormat Caching
**Learning:** Instantiating `new Intl.NumberFormat()` within utility formatting functions called repeatedly during React renders (especially when scrubbing input sliders like freight cost or typing exchange rates) is very expensive (~2.3s vs ~33ms for 50k calls, a ~70x speedup). In V8/Node/browser runtimes, `Intl.NumberFormat` construction involves complex locale resolution and internal data structure setup, incurring heavy CPU and GC allocation overhead.
**Action:** Always hoist fixed-locale `Intl.NumberFormat` formatters to module scope or memoize them when formatting values rendered in high-frequency React component updates.
