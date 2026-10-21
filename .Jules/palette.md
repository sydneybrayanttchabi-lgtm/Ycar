## 2026-10-21 - Semantic ARIA Tabs & Form Control Associations in TSX Components
**Learning:** Custom tab interfaces and form controls in dark UI dashboards often lack keyboard focus states, explicit label-input `htmlFor` associations, and `role="tablist"`/`role="tab"` semantic markup, rendering them inaccessible to screen readers and keyboard users.
**Action:** Always wrap tabs with `role="tablist"`, assign `role="tab"`, `aria-selected`, `aria-controls`, and `focus-visible:ring-2` to tab buttons, and explicitly link form `<label htmlFor="...">` with `<input id="...">` / `<select id="...">`.
