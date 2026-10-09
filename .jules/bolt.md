## 2026-10-09 - Prevent WebGL ModelViewer Re-instantiation via React.memo

**Learning:** `app.py` renders interactive 3D model custom elements (`<model-viewer>`) alongside dynamic simulation controls (exchange rates, freight costs, car filters). Without memoization on `ModelViewerComponent` and metric cards, every input change in the customs calculator triggers parent re-renders that force DOM updates and unnecessary WebGL re-initializations for the 3D model.

**Action:** Wrap sub-components that render heavy custom elements or static views (`ModelViewerComponent`, `MetricCard`, `CustomsReceipt`) in `React.memo` to isolate parent state changes.
