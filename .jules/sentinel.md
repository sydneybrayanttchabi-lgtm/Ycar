## 2025-05-18 - Prevent DOM-based XSS in custom web component mounting
**Vulnerability:** Unsanitized interpolation of `src` and `alt` properties directly into `containerRef.current.innerHTML` template strings allowed DOM-based XSS or HTML attribute injection.
**Learning:** Custom elements like `<model-viewer>` mounted in React wrappers should use DOM manipulation APIs (`document.createElement` and `setAttribute`) rather than raw string templating in `innerHTML`.
**Prevention:** Avoid `innerHTML` for mounting custom DOM elements; build elements programmatically using `document.createElement`, set attributes safely, and attach them using `replaceChildren()`.
