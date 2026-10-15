## 2025-10-15 - DOM-based XSS via innerHTML in Custom Component
**Vulnerability:** Unescaped string interpolation inside `innerHTML` in `ModelViewerComponent` when building `<model-viewer>` HTML string using external CSV data (`src` and `alt`).
**Learning:** React wrapper for Web Components (`<model-viewer>`) used string template concatenation in `innerHTML`, which allowed potential attribute injection / XSS if CSV or model URLs contain raw quote characters or tags.
**Prevention:** Use `document.createElement` and safe `setAttribute` calls instead of raw `innerHTML` string interpolation when rendering web components or dynamic elements.
