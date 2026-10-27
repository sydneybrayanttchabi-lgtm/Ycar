## 2026-03-30 - Custom Tab Controls and Unlabeled Selects
**Learning:** Custom tab buttons without `role="tablist"`, `role="tab"`, and `aria-selected` attributes are inaccessible to screen reader users and lack keyboard focus indicators. Additionally, form select inputs with text elements instead of associated `<label>` tags hinder assistive technology navigation.
**Action:** Always include proper ARIA tab roles, `aria-selected`, `aria-controls`, and `focus-visible` styles on custom tab navigation, and pair select inputs with standard `<label htmlFor="...">` elements.
