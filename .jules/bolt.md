# Bolt's Journal

## 2026-03-06 - DOM Node Re-creation vs Attribute Updates in WebGL Custom Elements
**Learning:** In React components wrapping custom WebGL elements (like `<model-viewer>`), setting `innerHTML` on every prop change destroys and re-creates the web component instance, forcing costly WebGL context re-initialization and shadow DOM teardowns. Reusing the DOM element and updating attributes directly avoids WebGL context recreation and frame drops during state updates.
**Action:** Always check if custom elements or heavy DOM containers already exist before replacing `innerHTML`. Re-use existing DOM nodes and update attributes selectively.
