## 2026-03-30 - DOM XSS via Web Component innerHTML Injection
**Vulnerability:** Constructing web custom elements (like `<model-viewer>`) using `innerHTML` string interpolation with component props (`src`, `alt`, `className`) allows raw HTML and script injection if properties contain untrusted or unescaped data.
**Learning:** React components wrapping Web Components or third-party custom elements often resort to `innerHTML` or `dangerouslySetInnerHTML`. Interpolating strings directly into HTML markup bypasses React's automatic JSX escaping mechanism.
**Prevention:** Always construct Web Component nodes using standard DOM APIs (`document.createElement`) and pass dynamic attributes safely via `setAttribute` or element property assignments rather than string interpolation into `innerHTML`.
