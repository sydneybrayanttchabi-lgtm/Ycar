## 2026-03-30 - Form Label & ARIA Tab Accessibility
**Learning:** React custom UI components in this app used paragraph tags `<p>` instead of `<label htmlFor="...">` for inputs, and plain `<button>`/`<div>` elements for tabbed navigation without WAI-ARIA roles.
**Action:** When working on UI controls in this project, ensure inputs have corresponding `<label htmlFor="...">` attributes and tabbed interfaces follow standard WAI-ARIA tab list (`role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, `role="tabpanel"`) patterns.
