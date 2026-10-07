# Sentinel Journal - Security Learnings

## 2026-03-30 - Prevent DOM XSS in Custom Web Components
**Vulnerability:** Constructing `<model-viewer>` tags using string interpolation inside `innerHTML` with untrusted inputs (`src`, `alt`) allowed potential DOM-based Cross-Site Scripting (XSS).
**Learning:** Setting `innerHTML` using unescaped string variables is dangerous, even when rendering custom elements.
**Prevention:** Construct elements using `document.createElement()` and assign attributes/properties safely using DOM APIs or native JSX elements.
