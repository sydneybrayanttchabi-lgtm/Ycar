# Bolt's Journal - Critical Performance Learnings

## 2026-10-08 - Preventing full component re-renders and innerHTML re-injections in React-wrapped custom web components
**Learning:** Wrapping complex UI components (`CustomsReceipt`, `MetricCard`) and custom web element wrappers (`ModelViewerComponent`) with `React.memo` prevents unnecessary re-renders when parent state updates (such as sliding range inputs or changing tabs in `App`). For components like `ModelViewerComponent` that touch imperative APIs or DOM `innerHTML`, `React.memo` avoids unnecessary DOM updates.
**Action:** Always wrap heavy display components or DOM-manipulating React wrappers in `React.memo` when parent state updates frequently.
