## 2026-10-07 - React memoization for interactive sliders and 3D model container
**Learning:** In interactive web dashboards containing range sliders (e.g. freight, currency rates) or heavy custom web elements (like `<model-viewer>`), frequent state updates trigger full sub-tree re-renders if subcomponents are not memoized with `React.memo`.
**Action:** Always wrap leaf display components (`MetricCard`, `CustomsReceipt`) and web component wrappers (`ModelViewerComponent`) in `React.memo` to prevent DOM re-evaluations during slider movements.
