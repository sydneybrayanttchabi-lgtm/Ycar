## 2026-03-06 - Web Component & WebGL Context Preservation
**Learning:** Re-rendering custom web components like `<model-viewer>` via `innerHTML` string updates destroys and recreates the underlying DOM node and WebGL context, causing heavy GPU/CPU overhead and visually disruptive flickering.
**Action:** Preserve web component DOM elements across renders using React refs and update element attributes/properties directly.
