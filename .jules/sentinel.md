# Sentinel Security Journal

## 2026-03-29 - DOM XSS via Unsafe innerHTML Interpolation in ModelViewerComponent
**Vulnerability:** Constructing `<model-viewer>` custom HTML strings via template literal interpolation with dynamic data (`src`, `alt`, `className`) and assigning directly to `innerHTML` introduced a DOM-based Cross-Site Scripting (XSS) risk.
**Learning:** React component wrappers for web components or custom elements sometimes rely on `innerHTML` to set initial attributes when props cannot be easily passed via JSX.
**Prevention:** Always construct custom elements using DOM API methods like `document.createElement()` and set attributes safely using `setAttribute()`, avoiding string interpolation in `innerHTML`.
