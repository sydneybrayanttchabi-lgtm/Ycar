## 2025-05-18 - Unsafe innerHTML and Unvalidated Vendor URLs in React Car Viewer

**Vulnerability:**
The `ModelViewerComponent` rendered custom `<model-viewer>` elements using direct string interpolation into `containerRef.current.innerHTML` with untrusted properties (`src`, `alt`, `className`) parsed directly from CSV data. Concurrently, the dealership link (`selectedCar.Lien_Vendeur`) was rendered directly into an `<a href>` tag without validation, permitting execution of `javascript:` URI payloads.

**Learning:**
Wrapper components around Web Components in React often resort to raw `innerHTML` string interpolation when declarative custom element props are tricky. However, when attributes stem from external or semi-trusted data sources (like user-uploaded or external CSV data), raw `innerHTML` creates DOM-based XSS attack vectors. Similarly, external links from data files must not be trusted implicitly.

**Prevention:**
Always use standard DOM element creation (`document.createElement` and `setAttribute`) or sanitized React props instead of string templating into `innerHTML`. Validate external URLs with strict protocol whitelists (e.g. `^https?://`) before binding them to `href` attributes.
