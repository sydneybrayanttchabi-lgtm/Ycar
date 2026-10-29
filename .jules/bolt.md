## 2026-10-29 - Reusing Web Component DOM elements vs innerHTML in React

**Learning:** Replacing Web Component DOM nodes like `<model-viewer>` via `innerHTML` on every prop change forces full teardown and re-creation of WebGL contexts and 3D resources. Direct DOM element reference reuse and attribute updates eliminate WebGL context recreation overhead completely.

**Action:** When wrapping Web components in React components, maintain a reference to the custom DOM element and update its attributes directly rather than resetting `innerHTML`.
