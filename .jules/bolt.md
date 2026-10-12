## 2025-05-18 - React Component Memoization in Single-File App
**Learning:** In single-file React TSX apps like app.py with interactive state (range sliders, select inputs), unmemoized sub-components cause total component tree re-renders on high-frequency events like slider dragging.
**Action:** Wrap pure sub-components (`MetricCard`, `CustomsReceipt`, `ModelViewerComponent`) in `React.memo` and move static array allocations outside the render loop.
