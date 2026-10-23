## 2026-10-23 - React memoization in hybrid Python/TSX repositories
**Learning:** `app.py` in this project contains React TSX UI code rather than Python code. Frequent slider/input state updates in `App` cause unnecessary re-renders of presentational components and DOM manipulation in custom elements like `<model-viewer>`.
**Action:** Wrap presentational subcomponents (`MetricCard`, `CustomsReceipt`, `ModelViewerComponent`) in `React.memo` and hoist static array allocations outside the main render loop.
