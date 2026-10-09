## 2026-03-30 - DOM-based XSS in Custom Web Component Rendering
**Vulnerability:** Unsafe string interpolation of component props (`src`, `alt`, `className`) into `containerRef.current.innerHTML` in `ModelViewerComponent` allowed potential DOM XSS when parsing external model URLs or vehicle names.
**Learning:** Custom Web Components (`<model-viewer>`) wrapped in React components via `useRef` should be created using standard DOM APIs (`document.createElement` and `setAttribute`) rather than setting `innerHTML` via template literals.
**Prevention:** Avoid `innerHTML` template string interpolation when rendering Web Components or custom elements inside React ref containers; use standard DOM methods or direct JSX custom element bindings instead.
