# Sentinel's Journal

## 2026-11-06 - DOM-based XSS via innerHTML wrapper for Custom Elements
**Vulnerability:** React components wrapping Web Components (such as `<model-viewer>`) often fall back to `containerRef.current.innerHTML = '<model-viewer ...>'` when integrating custom elements. When attribute values like `src` or `alt` are interpolated directly into the HTML string from parsed data (e.g., CSV imports or user input), unescaped quotes or HTML tags result in DOM-based XSS.
**Learning:** React JSX handles HTML escaping automatically for standard elements, but custom Web Components without full React bindings are sometimes rendered via imperative `innerHTML` string templates, completely bypassing React's built-in XSS protections.
**Prevention:** Always use safe DOM manipulation methods (`document.createElement`, `setAttribute`, and `replaceChildren` / `appendChild`) or properly typed custom element JSX declarations rather than template string interpolation into `innerHTML`.
