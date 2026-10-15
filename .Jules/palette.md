# Palette's UX Journal

## 2026-03-06 - Accessible Tab Interfaces and Form Inputs in React
**Learning:** Custom tab buttons and unlabelled select/range inputs degrade accessibility for screen reader and keyboard users when standard ARIA roles and label associations are absent.
**Action:** Always ensure tab containers use `role="tablist"`, buttons have `role="tab"`, `aria-selected`, and `aria-controls`, and form controls have explicit `id` and `<label htmlFor="...">` associations.
