# Palette UX Journal

## 2025-05-18 - Unlinked Form Controls and Unaccessible Tab Navigation in TSX Components
**Learning:** In React components styled with utility classes, section headers are sometimes rendered as `<p>` or `<label>` tags without `htmlFor` or `id` linkage to their associated `<select>` or `<input>` controls. Additionally, custom tab buttons often lack `role="tablist"` and `role="tab"` semantic markup, rendering them opaque to screen readers.
**Action:** Always link form inputs with explicit `htmlFor` and `id` attributes and provide proper ARIA tab navigation attributes (`role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`) when working on single-page tabbed interfaces.
