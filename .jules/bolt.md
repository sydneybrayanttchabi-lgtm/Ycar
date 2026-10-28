## 2026-10-28 - Avoid `innerHTML` web component re-creation for WebGL components

**Learning:** Imperatively creating or updating custom web components (like `<model-viewer>`) via `containerRef.current.innerHTML` in React `useEffect` hooks destroys the underlying DOM element and WebGL canvas context whenever component props update or re-render triggers. Rendering custom elements declaratively (e.g., via `React.createElement('model-viewer', props)`) allows VDOM reconciliation to update attributes in-place without tearing down the WebGL context, avoiding GPU texture re-allocation and expensive DOM re-parsing.

**Action:** Prefer direct JSX / `React.createElement` custom element attribute binding over imperative `innerHTML` assignments when wrapping WebGL custom elements in React components.
