## 2026-10-25 - DOM XSS in ModelViewerComponent String Interpolation
**Vulnerability:** Unsafe string interpolation of `src` and `alt` props inside `innerHTML` template string in React component `ModelViewerComponent`.
**Learning:** React components using `innerHTML` with unsanitized CSV data bypass React's standard JSX auto-escaping, introducing DOM XSS risks.
**Prevention:** Construct elements via `document.createElement()` and set untrusted inputs using `setAttribute()` or use standard JSX elements.
