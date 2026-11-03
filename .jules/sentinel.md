# Sentinel's Security Journal

## 2025-05-18 - DOM XSS via Web Component innerHTML Injection
**Vulnerability:** `ModelViewerComponent` in `app.py` previously injected raw HTML strings containing external model URLs (`src`) and car names (`alt`) via `containerRef.current.innerHTML` to mount the `<model-viewer>` custom element. An attacker who controls CSV or data inputs could execute arbitrary JavaScript via payload injection in the unescaped template string.
**Learning:** Developers often resort to `innerHTML` when integrating third-party custom elements (Web Components like `@google/model-viewer`) into React due to TypeScript JSX intrinsic element typing gaps.
**Prevention:** Extend JSX `IntrinsicElements` in a global type declaration to enable native, declarative JSX rendering of custom elements (`<model-viewer ... />`), allowing React to handle attribute binding and property escaping natively and avoiding raw HTML string interpolation.
