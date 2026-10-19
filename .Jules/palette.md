## 2025-10-19 - Interactive Tab Controls and Form Labels Accessibility
**Learning:** React custom tab components and unlinked form text in single-page apps frequently lack ARIA tab attributes (`role="tablist"`, `role="tab"`, `aria-selected`, `role="tabpanel"`) and `htmlFor`/`id` bindings, preventing screen readers from identifying interactive controls and form input contexts.
**Action:** Always bind input labels with `htmlFor` and `id`, and ensure tab navigation elements use semantic ARIA roles and tabpanel bindings.
