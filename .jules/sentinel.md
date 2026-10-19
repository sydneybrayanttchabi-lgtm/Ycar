## 2026-03-30 - DOM XSS in Custom Web Components (model-viewer)
**Vulnerability:** Insecure string interpolation of dynamic model URLs and attributes directly into `containerRef.current.innerHTML`.
**Learning:** When encapsulating custom HTML Web Components (like `<model-viewer>`) inside React components via `useRef`, developers often resort to setting raw `innerHTML` string templates, which introduces DOM-based XSS risks if attributes contain unescaped dynamic input.
**Prevention:** Construct custom web components safely using `document.createElement('model-viewer')` and `setAttribute()`, avoiding raw `innerHTML` string interpolation completely.
