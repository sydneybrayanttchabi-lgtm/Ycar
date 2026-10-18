# Bolt's Journal - Critical Learnings

## 2026-10-18 - `Intl.NumberFormat` Instantiation & React Component Memoization Overhead
**Learning:** Re-instantiating `Intl.NumberFormat` inside repeatedly called formatting functions (`formatFCFA`, `formatUSD`) creates significant CPU and garbage collection overhead during frequent re-renders or list formatting. Caching module-level `Intl.NumberFormat` instances makes formatting orders of magnitude faster. Additionally, wrapping leaf subcomponents (`CustomsReceipt`, `MetricCard`) in `React.memo` avoids unnecessary re-renders when parent simulator inputs change.
**Action:** Always instantiate `Intl.NumberFormat` once at module scope or memoize formatting instances, and wrap stateless presenter components in `React.memo`.
