# Sentinel's Journal - Critical Learnings Only

## 2025-02-18 - Safe DOM Creation for Web Components in TSX
**Vulnerability:** `ModelViewerComponent` in `app.py` previously interpolated `src` and `alt` directly into a template string passed to `innerHTML` when instantiating `<model-viewer>`, exposing the app to DOM-based XSS if car data attributes contain unsanitized or malicious input.
**Learning:** Even when custom elements (`model-viewer`) require imperative mounting because React does not natively map attributes to custom web components cleanly, setting attributes via standard DOM methods (`document.createElement`, `setAttribute`, `replaceChildren`) avoids DOM-based XSS without breaking custom element lifecycles.
**Prevention:** Avoid `innerHTML` template literal interpolation for custom elements or any dynamic data; use DOM manipulation methods (`document.createElement` / `setAttribute`) instead.
