# Palette's Journal - Critical UX & Accessibility Learnings

## 2026-11-10 - Accessible Tab Navigation with Roving Tabindex in Dark Mode
**Learning:** In single-page React apps with custom tab interfaces styled via Tailwind, tabs often lack semantic ARIA roles (`tablist`, `tab`, `tabpanel`), keyboard arrow key navigation, and visible focus rings. On dark backgrounds (`#0e1117`), standard browser outlines are nearly invisible; pairing `focus-visible:ring-2 focus-visible:ring-red-500` with `rounded-t-lg` provides crisp keyboard indicators that blend seamlessly with active tab underline highlights.
**Action:** When implementing tab switchers, ensure `role="tablist"` on container, `role="tab"` + `aria-selected` + `aria-controls` + roving `tabIndex` on buttons, and `role="tabpanel"` + `aria-labelledby` on content panels, with Left/Right arrow key handling.
