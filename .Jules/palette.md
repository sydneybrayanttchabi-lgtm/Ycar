# Palette's Journal

## 2026-03-29 - Form Labels and Tab Accessibility in Single-File React Component
**Learning:** React interfaces rendered in single-file components (like `app.py`) often omit `id`/`htmlFor` associations and `role="tab"`/`role="tabpanel"` ARIA attributes on custom tab systems, degrading keyboard and screen-reader accessibility.
**Action:** Always add explicit `id` and `htmlFor` pairings to inputs/labels, `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, `role="tabpanel"`, and `focus-visible` ring indicators when enhancing UI elements.
