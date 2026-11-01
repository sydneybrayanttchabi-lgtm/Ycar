# Sentinel Security Journal

This journal tracks critical security learnings, vulnerability patterns, and architectural constraints specific to this codebase.

## 2026-11-01 - DOM XSS via innerHTML in Custom Web Component Wrapper
**Vulnerability:** In `ModelViewerComponent`, 3D model URL and car title/alt properties (sourced from external CSV) were directly interpolated into a template string assigned to `containerRef.current.innerHTML`. Unsanitized strings in CSV fields allow breaking out of HTML attributes and executing arbitrary scripts (DOM XSS).
**Learning:** Wrapping third-party custom web components in React often leads developers to resort to `innerHTML` when custom elements have special attribute or mounting requirements.
**Prevention:** Construct DOM elements programmatically via `document.createElement(...)` and configure properties/attributes using `setAttribute(...)` or element properties, avoiding string interpolation into raw HTML entirely.
