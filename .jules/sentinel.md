# Sentinel Security Journal

## 2026-10-11 - DOM-Based XSS via Custom Web Components
**Vulnerability:** Constructing `<model-viewer>` web components using `innerHTML` with template string interpolation (`src`, `alt`, `className`) allows unescaped attributes or tags to trigger DOM XSS.
**Learning:** Even when custom web components like `<model-viewer>` are used in React apps via refs, `innerHTML` interpolation bypasses React's JSX auto-escaping protections.
**Prevention:** Construct elements dynamically via standard DOM methods (`document.createElement`, `setAttribute`) and clear/append with `replaceChildren()`.
