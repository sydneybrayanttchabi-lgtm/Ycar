## 2026-10-17 - React.memo on interactive simulator subcomponents
**Learning:** In interactive React dashboards with frequent state updates (e.g., range sliders and tab switches), wrapping subcomponents like metric cards, receipts, and 3D viewers in `React.memo` eliminates redundant re-renders and re-evaluations on cold render paths.
**Action:** Always memoize leaf presentational components that receive simple primitive/memoized props when parent components contain frequent input handlers.
