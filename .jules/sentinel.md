## 2026-10-31 - DOM XSS in Custom Web Component Rendering
**Vulnerability:** `ModelViewerComponent` interpolated unvalidated external parameters (`src`, `alt`, and `className`) directly into an `innerHTML` template string inside a React `useEffect` hook to mount `<model-viewer>`. An attacker controlling the CSV data source or vehicle model attributes could inject arbitrary markup and execute JavaScript.
**Learning:** Wrapping custom web components via React container refs often tempts developers to use `innerHTML` string templates for quick setup, bypassing React's built-in JSX escaping.
**Prevention:** Construct DOM elements using `document.createElement`, set properties/attributes securely via `setAttribute`, and manipulate the DOM tree safely using `replaceChildren` and `appendChild`.
