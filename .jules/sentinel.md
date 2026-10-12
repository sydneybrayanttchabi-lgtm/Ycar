## 2026-03-29 - Safe Custom Web Component Rendering in React Ref Containers
**Vulnerability:** DOM XSS via raw `innerHTML` string interpolation inside React `useRef` side-effects when loading custom Web Components like `<model-viewer>`.
**Learning:** React JSX sanitizes expressions in standard JSX, but direct `innerHTML` string interpolation inside `useEffect` / `useRef` DOM hooks bypasses React's security controls and allows unescaped property/attribute injection.
**Prevention:** Always use `document.createElement()` and explicit `setAttribute()` / property assignments when imperatively constructing custom elements in React ref containers rather than setting raw `innerHTML`.
