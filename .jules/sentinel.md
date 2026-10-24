## 2025-05-10 - DOM XSS via Unsanitized URLs and innerHTML in React/Custom Elements
**Vulnerability:** External URLs (seller links, 3D model URLs) lacked protocol validation allowing potential `javascript:` URI scheme injection, and `ModelViewerComponent` rendered custom elements via `innerHTML` string interpolation without attribute escaping.
**Learning:** `innerHTML` string interpolation in React wrapper components for custom web elements bypasses JSX auto-escaping, leading to DOM XSS if attributes contain unescaped characters.
**Prevention:** Always validate external URL protocols (`http:`, `https:`) and construct custom DOM elements programmatically using `document.createElement()` and `setAttribute()` instead of setting `innerHTML` directly.
