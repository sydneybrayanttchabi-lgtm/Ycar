# Sentinel's Journal - Security Learnings

## 2025-05-18 - DOM XSS in Custom Web Component Rendering
**Vulnerability:** ModelViewerComponent in `app.py` directly interpolated untrusted dynamic values (`src`, `alt`, and `className`) into template strings assigned to `containerRef.current.innerHTML`. If data from external or user-controlled sources contains unescaped markup or quotes, this could lead to Cross-Site Scripting (DOM XSS).
**Learning:** Wrapping custom HTML elements or web components (`<model-viewer>`) in React components via `innerHTML` template strings bypasses React's built-in JSX sanitization, exposing the DOM to XSS injection.
**Prevention:** Avoid `innerHTML` template interpolation when wrapping custom elements in React. Instead, safely instantiate elements using `document.createElement` and assign attributes using `setAttribute` or direct element properties.
