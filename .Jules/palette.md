## 2026-03-30 - Accessible Form Controls and Tab Navigation
**Learning:** In custom React tab structures and form fields without explicit `<label htmlFor="...">` links, screen readers cannot properly associate input purposes or describe active tab panels.
**Action:** Always associate form control `id`s with `<label htmlFor="...">` and pair tab buttons with panels using `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, `role="tabpanel"`, and `aria-labelledby`.
