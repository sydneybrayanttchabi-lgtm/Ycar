# Palette's Journal - Critical UX Learnings

## 2025-05-18 - Missing Dealership Data & Dead Action Links
**Learning:** In catalog and dataset-driven vehicle interfaces with incomplete or sparse vendor metadata, hardcoded external CTA action links (`<a>`) become dead links when target URLs are blank (`href=""`), confusing users and triggering unwanted page reloads or empty new tabs.
**Action:** Always conditionally guard external dealer/vendor CTA links: when URLs are absent, render an explicitly disabled, styled button with explanatory text rather than an active link, and provide fallback labels in corresponding detail metrics cards.
