## 2026-03-06 - DOM XSS via innerHTML String Interpolation in Web Components
**Vulnerability:** Direct string interpolation of untrusted props (`src`, `alt`, `className`) into `innerHTML` within `ModelViewerComponent`.
**Learning:** When encapsulating Web Components or custom elements (`<model-viewer>`) in React, using `innerHTML` template strings bypasses React's JSX auto-escaping, opening DOM-based XSS attack vectors.
**Prevention:** Always construct custom elements using `document.createElement()` and `setAttribute()` or React custom element props instead of `innerHTML` string interpolation.
