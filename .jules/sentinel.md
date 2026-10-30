## 2026-10-30 - DOM-Based XSS in Custom Web Component Rendering
**Vulnerability:** String template interpolation in `innerHTML` when rendering custom Web Components (`<model-viewer>`). Unsanitized props (`src`, `alt`) from dynamic CSV inputs could inject arbitrary HTML/attribute values and execute XSS payloads.
**Learning:** React wrappers around custom web components often resort to `innerHTML` string interpolation, bypassing React's automatic string escaping and introducing DOM XSS risks.
**Prevention:** Construct custom web components imperatively using `document.createElement()` and `setAttribute()` (or direct property assignment) instead of `innerHTML` template strings.
