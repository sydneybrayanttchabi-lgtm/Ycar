## 2026-10-26 - Prevent DOM XSS in Custom Web Components
**Vulnerability:** Unsanitized string interpolation into `innerHTML` for custom elements (`<model-viewer>`).
**Learning:** React components wrapping custom elements via `innerHTML` can inadvertently open DOM XSS vectors if element attributes or URLs are derived from dynamic or parsed data.
**Prevention:** Construct custom elements programmatically with `document.createElement()` and `setAttribute()`, then insert them into container refs with `replaceChildren()`.
