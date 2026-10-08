# Palette's Journal

## 2025-05-18 - Form Labels & WAI-ARIA Tab Navigation Accessibility
**Learning:** React TSX components serving single-page dashboards often omit explicit `id`/`htmlFor` associations on select controls and range inputs, breaking screen reader navigation. Furthermore, custom button-based tab bars lack `role="tablist"` and `role="tabpanel"` semantics.
**Action:** When working on React TSX dashboard interfaces, always audit `<select>`, `<input type="range">`, and tab navigation controls to ensure full `htmlFor`/`id` linking and standard ARIA tab attributes (`aria-selected`, `aria-controls`, `role="tabpanel"`).
