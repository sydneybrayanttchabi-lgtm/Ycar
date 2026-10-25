# Sentinel Security Journal

## 2026-10-25 - DOM XSS via raw innerHTML String Interpolation in React Custom Component
**Vulnerability:** `ModelViewerComponent` rendered custom HTML elements using `containerRef.current.innerHTML = ...` with unescaped variable interpolation (`src`, `alt`, `className`).
**Learning:** Inserting props or data loaded from external/dynamic sources (such as CSV fields or user inputs) into template strings assigned to `innerHTML` circumvents React's XSS protections and allows DOM-based XSS attacks.
**Prevention:** Avoid `innerHTML` when rendering custom Web Components or dynamic HTML elements. Instead, programmatically create elements with `document.createElement()` and assign attributes securely via `setAttribute()` or property assignment.
