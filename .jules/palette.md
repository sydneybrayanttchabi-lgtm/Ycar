# Palette's Journal - Critical Learnings

## 2025-05-18 - Form controls and inputs in app.py lack explicit labeling and ARIA range semantics
**Learning:** In `app.py`, controls such as dropdown selects and number/range inputs were styled with adjacent paragraph/label text elements that lacked `htmlFor` / `id` bindings, preventing screen readers from announcing field names on focus and breaking click-to-focus behavior. Range sliders also lacked `aria-valuetext` for formatted currency values.
**Action:** When working on forms in this repository, always link `<label htmlFor="...">` directly to control `id`s and supply `aria-valuemin`, `aria-valuemax`, `aria-valuenow`, and `aria-valuetext` for range inputs to ensure full assistive tech accessibility.
