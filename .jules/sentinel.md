## 2026-10-11 - DOM XSS in Custom Web Component Injection
**Vulnerability:** Dynamic string interpolation inside `innerHTML` within `useRef` hook in `ModelViewerComponent` (`app.py`).
**Learning:** Rendering custom web components like `<model-viewer>` via React `useRef` and `innerHTML` bypasses React's automatic JSX XSS escaping mechanisms when passing attributes (`src`, `alt`, `class`).
**Prevention:** Construct elements using `document.createElement('model-viewer')` and assign attributes securely using `.setAttribute()` or property assignment instead of direct `innerHTML` string templates.
