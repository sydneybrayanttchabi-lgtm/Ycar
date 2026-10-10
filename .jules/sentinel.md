# Sentinel Security Journal

## 2025-05-18 - Safe DOM Custom Element Mounting vs innerHTML
**Vulnerability:** DOM-based XSS vulnerability when inserting custom Web Components (`<model-viewer>`) via `innerHTML` string templates containing interpolated props (`src`, `alt`, `className`).
**Learning:** Using `innerHTML` string interpolation in React components to mount Web Components bypasses React's JSX auto-escaping and exposes the application to XSS if prop values contain raw HTML or quotes.
**Prevention:** Construct elements safely using standard DOM APIs (`document.createElement` and `element.setAttribute`) instead of assigning raw HTML strings to `innerHTML`.
