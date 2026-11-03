# Palette's Journal

## 2026-11-03 - Accessible Tab Navigation Semantics in React SPAs
**Learning:** In single-page React dashboards where tab switching toggles major content views, plain `<button>` elements inside generic `<div>` containers lack accessibility affordances. Screen readers cannot identify them as mutually exclusive tabs or associate them with their respective panels. Furthermore, removing default button outlines without explicit `:focus-visible` styling makes keyboard navigation invisible.
**Action:** Always wrap tabs in `role="tablist"` with descriptive `aria-label`, assign each tab `role="tab"`, `aria-selected`, and `aria-controls`, link content views with `role="tabpanel"` and `aria-labelledby`, and supply visible focus rings via `focus-visible:ring-2`.
