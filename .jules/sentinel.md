## 2026-10-23 - DOM-based XSS via Dynamic innerHTML Construction
**Vulnerability:** Constructing web components using raw template literal string interpolation into `element.innerHTML` (`<model-viewer src="${src}">`).
**Learning:** React ref-driven DOM manipulation bypassing React's JSX auto-escaping directly executes raw HTML string evaluation in `innerHTML`, enabling DOM XSS when props contain untrusted input.
**Prevention:** Construct elements safely via `document.createElement()` and set individual attributes using `setAttribute()` or standard DOM properties instead of string interpolation into `innerHTML`.
