## 2026-10-29 - DOM XSS in Custom Web Component Wrapper
**Vulnerability:** Unsafe template string interpolation inside `innerHTML` in `ModelViewerComponent` (`app.py`).
**Learning:** In React components wrapping Web Components (like `<model-viewer>`), setting `innerHTML` directly with interpolated strings bypasses React's JSX auto-escaping and exposes the app to DOM XSS if model URLs or labels contain untrusted input.
**Prevention:** Construct Web Component instances using `document.createElement` and set attributes safely via `setAttribute` or React elements.
